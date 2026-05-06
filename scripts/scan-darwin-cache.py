#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "httpx[http2]>=0.27",
#     "zstandard>=0.22",
# ]
# ///
"""
Scan the aarch64-darwin nixpkgs cache for Mach-O binaries whose
LC_CODE_SIGNATURE page hashes don't match the bytes they cover.

This is the empirical blast-radius check for NixOS/nixpkgs#507531 / NixOS/nix#15638:
the nix daemon's RewritingSink mutates bytes inside __TEXT,__cstring pages
that `ld -adhoc_codesign` has already hashed with the linker-signed flag
set, leaving stale page hashes in the CodeDirectory.

Pipeline per store path (all streaming, zero on-disk NAR persistence):
  1. Fetch <hash>.narinfo from the binary cache.
  2. Stream the NAR over HTTP, decompress (xz/zstd/bzip2/none) inline.
  3. Walk NAR entries; for each regular file, peek 4 bytes.
     - Non-Mach-O: skip the rest of the file inside the stream.
     - Mach-O: buffer the file and verify page hashes per slice.
  4. Emit one JSONL result line per scanned Mach-O slice.
  5. Record per-store-path completion in a SQLite state DB (WAL mode).

Concurrency: two modes, selected by --workers.
  --workers 0: single-process, async HTTP via one httpx client with
    --concurrency in-flight requests. Useful for debugging / sanity-checks
    because all work happens in one event loop on one interpreter thread.
  --workers N>0: multiprocess via mp.Pool.imap_unordered. Main process
    fetches the store-paths list, shards them into batches of --batch-size,
    and hands batches to N worker processes. Each worker runs its own
    asyncio event loop with its own httpx client doing
    --per-worker-concurrency in-flight requests. Results stream back to
    main; main writes the SQLite state DB and JSONL. This parallelizes
    HTTP + decompression + NAR parsing + SHA-256 across cores and is the
    recommended mode for full walks and daily-delta runs.

Resume: on re-run, paths already recorded in the state DB are skipped.
Safe to SIGINT; in-flight tasks finish and are persisted before exit.

Output JSONL is designed to be aggregated in post-processing — one row
per Mach-O slice, plus summary rows for errors / too-large files.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import logging
import lzma
import multiprocessing as mp
import os
import signal
import sqlite3
import struct
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import AsyncIterator, Iterable, Optional

import httpx


DEFAULT_CHANNEL = "https://channels.nixos.org/nixpkgs-25.11-darwin"
DEFAULT_CACHE = "https://cache.nixos.org"

log = logging.getLogger("scan")


# ---------------------------------------------------------------------------
# NAR format (streaming parser)
# ---------------------------------------------------------------------------
#
# All values are length-prefixed: u64le length, then bytes, padded to 8 bytes.
#
#   "nix-archive-1" ( <node> )
#   <node> ::= "(" "type" <string>
#              ( if "regular":   [ "executable" "" ] "contents" <string> )
#              ( if "directory": ( "entry" "(" "name" <name> "node" <node> ")" )* )
#              ( if "symlink":   "target" <string> )
#              ")"


PAD = 8


def _pad_bytes(n: int) -> int:
    return (PAD - (n % PAD)) % PAD


class AsyncByteStream:
    """
    Adapts an async iterator of bytes into a seekable-forward reader with
    .read / .skip / .read_u64 / .read_str primitives. Buffer is compacted
    periodically to keep memory bounded.
    """

    def __init__(self, source: AsyncIterator[bytes]):
        self._source = source
        self._buf = bytearray()
        self._off = 0
        self._eof = False

    async def _pull_one(self) -> None:
        try:
            chunk = await self._source.__anext__()
        except StopAsyncIteration:
            self._eof = True
            return
        if chunk:
            self._buf.extend(chunk)

    async def _fill(self, n: int) -> None:
        while len(self._buf) - self._off < n and not self._eof:
            await self._pull_one()
        if self._off > (1 << 20):
            del self._buf[: self._off]
            self._off = 0

    async def read(self, n: int) -> bytes:
        await self._fill(n)
        if len(self._buf) - self._off < n:
            raise EOFError(
                f"unexpected eof: need {n}, have {len(self._buf) - self._off}"
            )
        out = bytes(self._buf[self._off : self._off + n])
        self._off += n
        return out

    async def skip(self, n: int) -> None:
        while n > 0:
            await self._fill(min(n, 1 << 16))
            take = min(n, len(self._buf) - self._off)
            if take == 0:
                raise EOFError("unexpected eof during skip")
            self._off += take
            n -= take

    async def read_u64(self) -> int:
        return struct.unpack("<Q", await self.read(8))[0]

    async def read_str(self) -> bytes:
        n = await self.read_u64()
        if n > (1 << 32):
            raise ValueError(f"implausible NAR string length {n}")
        data = await self.read(n)
        pad = _pad_bytes(n)
        if pad:
            await self.skip(pad)
        return data


@dataclass
class NarRegularFile:
    path: str
    size: int
    executable: bool
    content: Optional[bytes]  # None if skipped (non-Mach-O or too large)
    truncated: bool = False  # True if skipped because > max_macho_bytes


async def iter_nar_regular_files(
    stream: AsyncByteStream,
    probe_bytes: int = 4,
    max_macho_bytes: int = 2 << 30,
) -> AsyncIterator[NarRegularFile]:
    """
    Walk a NAR; yield NarRegularFile for every regular file.

    Strategy to keep memory bounded:
      - For each file, read `probe_bytes` to test for Mach-O magic.
      - If not Mach-O: skip the rest of the file in the stream.
      - If Mach-O and size <= max_macho_bytes: buffer the full file.
      - If Mach-O and size >  max_macho_bytes: skip, mark truncated=True.
    """
    magic = await stream.read_str()
    if magic != b"nix-archive-1":
        raise ValueError(f"not a NAR (magic={magic!r})")

    async def expect(tok: bytes) -> None:
        got = await stream.read_str()
        if got != tok:
            raise ValueError(f"expected {tok!r}, got {got!r}")

    async def walk(prefix: str) -> AsyncIterator[NarRegularFile]:
        await expect(b"(")
        await expect(b"type")
        typ = await stream.read_str()

        if typ == b"regular":
            executable = False
            tok = await stream.read_str()
            if tok == b"executable":
                executable = True
                # empty-string value follows "executable"
                empty = await stream.read_str()
                if empty != b"":
                    raise ValueError(f"expected empty exec value, got {empty!r}")
                tok = await stream.read_str()
            if tok != b"contents":
                raise ValueError(f"expected 'contents', got {tok!r}")
            size = await stream.read_u64()
            pad = _pad_bytes(size)
            content: Optional[bytes] = None
            truncated = False
            if size == 0:
                content = b""
            else:
                probe_len = min(probe_bytes, size)
                head = await stream.read(probe_len)
                if _macho_magic(head):
                    if size <= max_macho_bytes:
                        rest = (
                            await stream.read(size - probe_len)
                            if size > probe_len
                            else b""
                        )
                        content = head + rest
                    else:
                        await stream.skip(size - probe_len)
                        truncated = True
                else:
                    await stream.skip(size - probe_len)
            if pad:
                await stream.skip(pad)
            yield NarRegularFile(prefix, size, executable, content, truncated)
            await expect(b")")

        elif typ == b"directory":
            while True:
                tok = await stream.read_str()
                if tok == b")":
                    return
                if tok != b"entry":
                    raise ValueError(f"expected 'entry' or ')', got {tok!r}")
                await expect(b"(")
                await expect(b"name")
                name = (await stream.read_str()).decode("utf-8", errors="replace")
                await expect(b"node")
                child_prefix = f"{prefix}/{name}" if prefix else name
                async for item in walk(child_prefix):
                    yield item
                await expect(b")")
            # unreachable (we 'return' on ')')

        elif typ == b"symlink":
            await expect(b"target")
            await stream.read_str()
            await expect(b")")
        else:
            raise ValueError(f"unknown NAR node type: {typ!r}")

    async for item in walk(""):
        yield item


# ---------------------------------------------------------------------------
# Mach-O analysis
# ---------------------------------------------------------------------------

LC_CODE_SIGNATURE = 0x1D
LC_REQ_DYLD = 0x80000000
LC_LOAD_DYLIB = 0x0C
LC_LOAD_WEAK_DYLIB = 0x18 | LC_REQ_DYLD
LC_REEXPORT_DYLIB = 0x1F | LC_REQ_DYLD
_DYLIB_CMDS = {LC_LOAD_DYLIB, LC_LOAD_WEAK_DYLIB, LC_REEXPORT_DYLIB}

CSMAGIC_EMBEDDED_SIGNATURE = 0xFADE0CC0
CSMAGIC_CODEDIRECTORY = 0xFADE0C02
CS_HASHTYPE_SHA1 = 1
CS_HASHTYPE_SHA256 = 2
CD_FLAG_LINKER_SIGNED = 0x20000

# Slot types inside a SuperBlob. Main CD is 0; alternate CDs live in
# [0x1000, 0x1010); both should be scanned (and the SHA-256 one preferred).
SLOT_CODEDIRECTORY = 0

_FAT_MAGICS = {b"\xca\xfe\xba\xbe", b"\xca\xfe\xba\xbf"}
_THIN_MAGICS = {
    b"\xcf\xfa\xed\xfe",  # MH_MAGIC_64 (LE)
    b"\xfe\xed\xfa\xcf",  # MH_CIGAM_64 (BE, rare on darwin)
    b"\xce\xfa\xed\xfe",  # MH_MAGIC    (LE, 32-bit)
    b"\xfe\xed\xfa\xce",  # MH_CIGAM    (BE, 32-bit)
}


def _macho_magic(data: bytes) -> bool:
    if len(data) < 4:
        return False
    head = bytes(data[:4])
    return head in _FAT_MAGICS or head in _THIN_MAGICS


def _cputype_name(ct: int, cs: int) -> str:
    # Just the common ones we care about on darwin.
    CPU_ARCH_ABI64 = 0x01000000
    CPU_TYPE_X86 = 7
    CPU_TYPE_ARM = 12
    ct_base = ct & ~CPU_ARCH_ABI64
    is_64 = bool(ct & CPU_ARCH_ABI64)
    if ct_base == CPU_TYPE_ARM and is_64:
        return "arm64e" if (cs & 0x00FFFFFF) == 2 else "arm64"
    if ct_base == CPU_TYPE_X86 and is_64:
        return "x86_64"
    if ct_base == CPU_TYPE_X86:
        return "i386"
    if ct_base == CPU_TYPE_ARM:
        return "arm"
    return f"cpu_0x{ct:08x}/0x{cs:08x}"


@dataclass
class SliceReport:
    is_fat: bool
    arch: str
    cpu_type: int
    cpu_subtype: int
    has_code_signature: bool = False
    cd_flags: int = 0
    linker_signed: bool = False
    hash_algo: int = 0
    page_size: int = 0
    n_code_slots: int = 0
    n_special_slots: int = 0
    code_limit: int = 0
    n_mismatches: int = 0
    first_bad_page: Optional[int] = None
    first_bad_offset: Optional[int] = None
    mismatches_sample: list[int] = field(default_factory=list)
    error: Optional[str] = None
    # Enriched fields (2026-04-18): capture the full SuperBlob shape so
    # downstream queries can classify binaries by signature class
    # (linker-signed, codesign-adhoc with empty CMS wrapper, Developer-ID
    # with non-empty CMS, etc.) without re-walking the binary.
    fat_variant: str = "thin"  # "thin" | "fat32" | "fat64"
    slots: list = field(default_factory=list)  # [{slot_type, blob_magic, blob_length}]
    alternate_cds: list = field(default_factory=list)  # non-primary CDs (SHA-1 + SHA-256 dual)
    cms_blob_length: int = 0  # CS_SIGNATURESLOT blob length: 0=absent, 8=empty wrapper, >8=payload
    has_entitlements: bool = False      # SuperBlob carries slot 0x5 (Entitlements XML)
    has_entitlements_der: bool = False  # SuperBlob carries slot 0x7 (Entitlements-DER)
    linked_dylibs: list[str] = field(default_factory=list)  # LC_LOAD_DYLIB / LC_LOAD_WEAK_DYLIB / LC_REEXPORT_DYLIB install names


def analyze_macho(data: bytes) -> list[SliceReport]:
    """Return one SliceReport per Mach-O slice (1 for thin, N for fat)."""
    if len(data) < 4:
        return [SliceReport(False, "unknown", 0, 0, error="file too small")]
    magic = bytes(data[:4])

    if magic in _FAT_MAGICS:
        return _analyze_fat(data, is_64=(magic == b"\xca\xfe\xba\xbf"))

    report = _analyze_thin(data)
    return [report]


def _analyze_fat(data: bytes, is_64: bool) -> list[SliceReport]:
    try:
        nfat = struct.unpack_from(">I", data, 4)[0]
    except struct.error:
        return [SliceReport(True, "unknown", 0, 0, error="bad fat header")]

    # Sanity: fat nfat > 16 is almost certainly a Java class file
    # (cafebabe + major.minor version).
    if nfat == 0 or nfat > 16:
        return [
            SliceReport(True, "unknown", 0, 0, error=f"implausible fat nfat={nfat}")
        ]

    arch_fmt = ">IIQQII" if is_64 else ">IIIIII"
    arch_sz = 32 if is_64 else 20
    base = 8

    results: list[SliceReport] = []
    for i in range(nfat):
        try:
            if is_64:
                cputype, cpusubtype, offset, size, _align, _res = struct.unpack_from(
                    arch_fmt, data, base + i * arch_sz
                )
            else:
                cputype, cpusubtype, offset, size, _align, _res = struct.unpack_from(
                    ">IIIIII", data, base + i * arch_sz
                )
        except struct.error:
            results.append(SliceReport(True, "unknown", 0, 0, error="bad fat_arch"))
            continue
        if offset + size > len(data):
            results.append(
                SliceReport(
                    True,
                    _cputype_name(cputype, cpusubtype),
                    cputype,
                    cpusubtype,
                    error="fat_arch out-of-bounds",
                )
            )
            continue
        sub = data[offset : offset + size]
        rep = _analyze_thin(sub)
        rep.is_fat = True
        rep.fat_variant = "fat64" if is_64 else "fat32"
        rep.arch = _cputype_name(cputype, cpusubtype)
        rep.cpu_type = cputype
        rep.cpu_subtype = cpusubtype
        results.append(rep)
    return results


def _analyze_thin(data: bytes) -> SliceReport:
    rep = SliceReport(is_fat=False, arch="unknown", cpu_type=0, cpu_subtype=0)
    if len(data) < 32:
        rep.error = "truncated mach_header"
        return rep
    magic = bytes(data[:4])
    is_64 = magic in (b"\xcf\xfa\xed\xfe", b"\xfe\xed\xfa\xcf")
    little = magic in (b"\xcf\xfa\xed\xfe", b"\xce\xfa\xed\xfe")
    if not little:
        rep.error = "big-endian Mach-O (scanner only handles little-endian)"
        return rep
    try:
        if is_64:
            _m, cputype, cpusubtype, _ft, ncmds, sizeofcmds, _flags, _res = (
                struct.unpack_from("<IIIIIIII", data, 0)
            )
            hdr_size = 32
        else:
            _m, cputype, cpusubtype, _ft, ncmds, sizeofcmds, _flags = (
                struct.unpack_from("<IIIIIII", data, 0)
            )
            hdr_size = 28
    except struct.error:
        rep.error = "bad mach_header"
        return rep

    rep.cpu_type = cputype
    rep.cpu_subtype = cpusubtype
    rep.arch = _cputype_name(cputype, cpusubtype)

    # Walk load commands, looking for LC_CODE_SIGNATURE.
    lc_off = hdr_size
    lc_end = hdr_size + sizeofcmds
    if lc_end > len(data):
        rep.error = "sizeofcmds exceeds slice"
        return rep

    sig_off = sig_size = None
    for _ in range(ncmds):
        if lc_off + 8 > lc_end:
            rep.error = "load cmds truncated"
            return rep
        cmd, cmdsize = struct.unpack_from("<II", data, lc_off)
        if cmdsize < 8 or lc_off + cmdsize > lc_end:
            rep.error = "malformed load cmd"
            return rep
        if cmd == LC_CODE_SIGNATURE:
            if cmdsize < 16:
                rep.error = "LC_CODE_SIGNATURE too small"
                return rep
            sig_off, sig_size = struct.unpack_from("<II", data, lc_off + 8)
        elif cmd in _DYLIB_CMDS:
            # dylib_command: cmd/cmdsize, then dylib { name_offset, ts, cur_ver, compat_ver }.
            # name is a null-terminated string starting at lc_off + name_offset
            # (relative to the command itself), with total length cmdsize.
            if cmdsize >= 24:
                name_off = struct.unpack_from("<I", data, lc_off + 8)[0]
                if 24 <= name_off < cmdsize:
                    raw = bytes(data[lc_off + name_off : lc_off + cmdsize])
                    raw = raw.split(b"\x00", 1)[0]
                    try:
                        rep.linked_dylibs.append(raw.decode("utf-8"))
                    except UnicodeDecodeError:
                        rep.linked_dylibs.append(raw.decode("latin-1"))
        lc_off += cmdsize

    if sig_off is None:
        return rep  # not signed; nothing to verify

    rep.has_code_signature = True
    if sig_off + sig_size > len(data):
        rep.error = "LC_CODE_SIGNATURE payload OOB"
        return rep
    blob = data[sig_off : sig_off + sig_size]

    # SuperBlob header: magic (u32be), length (u32be), count (u32be),
    # then count × (type u32be, offset u32be).
    if len(blob) < 12:
        rep.error = "signature blob too small"
        return rep
    sb_magic, _sb_len, sb_count = struct.unpack_from(">III", blob, 0)
    if sb_magic != CSMAGIC_EMBEDDED_SIGNATURE:
        rep.error = f"bad SuperBlob magic 0x{sb_magic:08x}"
        return rep

    # Enriched pass (2026-04-18): record the full SuperBlob directory so
    # downstream queries can categorize by signature shape without
    # re-fetching the binary. Also populates the convenience fields
    # has_entitlements / has_entitlements_der / cms_blob_length.
    for i in range(sb_count):
        idx_off = 12 + i * 8
        if idx_off + 8 > len(blob):
            break
        etype, eoff = struct.unpack_from(">II", blob, idx_off)
        if eoff + 8 > len(blob):
            continue
        bmagic, blength = struct.unpack_from(">II", blob, eoff)
        rep.slots.append(
            {"slot_type": etype, "blob_magic": bmagic, "blob_length": blength}
        )
        if etype == 0x5:
            rep.has_entitlements = True
        elif etype == 0x7:
            rep.has_entitlements_der = True
        elif etype == 0x10000:
            rep.cms_blob_length = blength

    # Find all CodeDirectory entries (main + alternates), pick best.
    best = None
    all_cds: list[dict] = []
    for i in range(sb_count):
        idx_off = 12 + i * 8
        if idx_off + 8 > len(blob):
            break
        etype, eoff = struct.unpack_from(">II", blob, idx_off)
        is_cd_slot = (etype == SLOT_CODEDIRECTORY) or (0x1000 <= etype < 0x1010)
        if not is_cd_slot:
            continue
        if eoff + 44 > len(blob):
            continue
        cd_magic = struct.unpack_from(">I", blob, eoff)[0]
        if cd_magic != CSMAGIC_CODEDIRECTORY:
            continue
        try:
            (
                _cd_magic,
                cd_len,
                _cd_ver,
                cd_flags,
                hash_off,
                _ident_off,
                n_special,
                n_code,
                code_limit,
                hash_size,
                hash_type,
                _platform,
                page_size_log2,
                _spare2,
            ) = struct.unpack_from(">IIIIIIIIIBBBBI", blob, eoff)
        except struct.error:
            continue
        cand = {
            "eoff": eoff,
            "cd_flags": cd_flags,
            "hash_off": hash_off,
            "n_special": n_special,
            "n_code": n_code,
            "code_limit": code_limit,
            "hash_size": hash_size,
            "hash_type": hash_type,
            "page_size": (1 << page_size_log2) if page_size_log2 else 0,
            "cd_len": cd_len,
        }
        all_cds.append(cand)
        if best is None or (
            best["hash_type"] != CS_HASHTYPE_SHA256 and hash_type == CS_HASHTYPE_SHA256
        ):
            best = cand

    if best is None:
        rep.error = "no CodeDirectory in signature"
        return rep

    # Record non-primary CDs for dual-CD analysis (SHA-1 + SHA-256 alternates).
    for cd in all_cds:
        if cd["eoff"] == best["eoff"]:
            continue
        rep.alternate_cds.append(
            {
                "hash_algo": cd["hash_type"],
                "n_code_slots": cd["n_code"],
                "n_special_slots": cd["n_special"],
                "code_limit": cd["code_limit"],
                "page_size": cd["page_size"],
                "cd_flags": cd["cd_flags"],
            }
        )

    rep.cd_flags = best["cd_flags"]
    rep.linker_signed = bool(best["cd_flags"] & CD_FLAG_LINKER_SIGNED)
    rep.hash_algo = best["hash_type"]
    rep.page_size = best["page_size"]
    rep.n_code_slots = best["n_code"]
    rep.n_special_slots = best["n_special"]
    rep.code_limit = best["code_limit"]

    hash_type = best["hash_type"]
    if hash_type == CS_HASHTYPE_SHA256:
        hasher = hashlib.sha256
    elif hash_type == CS_HASHTYPE_SHA1:
        hasher = hashlib.sha1
    else:
        rep.error = f"unsupported hash_type {hash_type} (expected SHA-1 or SHA-256)"
        return rep
    ps = best["page_size"]
    if ps == 0:
        rep.error = "page_size=0 (file-level hash, not page-level)"
        return rep

    hash_off_in_blob = best["eoff"] + best["hash_off"]
    hash_size = best["hash_size"]
    n = best["n_code"]
    limit = best["code_limit"]

    if hash_off_in_blob + n * hash_size > len(blob):
        rep.error = "hash slots OOB"
        return rep

    mismatches: list[int] = []
    for i in range(n):
        expected = blob[
            hash_off_in_blob + i * hash_size : hash_off_in_blob + (i + 1) * hash_size
        ]
        page_start = i * ps
        page_end = min((i + 1) * ps, limit)
        actual = hasher(data[page_start:page_end]).digest()
        if expected != actual:
            mismatches.append(i)

    rep.n_mismatches = len(mismatches)
    if mismatches:
        rep.first_bad_page = mismatches[0]
        rep.first_bad_offset = mismatches[0] * ps
        rep.mismatches_sample = mismatches[:8]
    return rep


# ---------------------------------------------------------------------------
# Binary-cache I/O
# ---------------------------------------------------------------------------


def _apply_shard_stripe(
    paths: list[str], shard: int, total_shards: int, source: str
) -> list[str]:
    """Deterministic stripe by line index: paths[i] belongs to shard
    (i % total_shards). Stripe beats chunk for load balance — a chunk
    split could assign one shard all the Swift toolchain or all the
    Electron apps while others finish early.
    """
    if total_shards <= 1:
        return paths
    before = len(paths)
    sliced = [p for i, p in enumerate(paths) if i % total_shards == shard]
    log.info(
        "sharding (%s): %d of %d paths assigned to shard %d/%d",
        source,
        len(sliced),
        before,
        shard,
        total_shards,
    )
    return sliced


async def fetch_store_paths(
    client: httpx.AsyncClient,
    channel_url: str,
    shard: int = 0,
    total_shards: int = 1,
) -> list[str]:
    """Fetch the channel's store-paths.xz and optionally return only this
    shard's slice."""
    url = f"{channel_url.rstrip('/')}/store-paths.xz"
    log.info("fetching %s", url)
    r = await client.get(url)
    r.raise_for_status()
    raw = lzma.decompress(r.content)
    paths = [ln for ln in raw.decode().splitlines() if ln.strip()]
    return _apply_shard_stripe(paths, shard, total_shards, "channel")


def load_paths_from_file(
    path_file: str, shard: int = 0, total_shards: int = 1
) -> list[str]:
    """Read a newline-separated list of /nix/store paths from disk.
    Mirrors fetch_store_paths' shard-stripe behaviour so the synthetic
    `release` channel (paths derived from `nix-eval-jobs` against
    `release-25.11`) drops in wherever fetch_store_paths is used.
    """
    log.info("loading paths from %s", path_file)
    with open(path_file) as f:
        paths = [
            ln.strip()
            for ln in f
            if ln.strip() and ln.lstrip().startswith("/nix/store/")
        ]
    return _apply_shard_stripe(paths, shard, total_shards, "file")


async def fetch_narinfo(
    client: httpx.AsyncClient, cache_url: str, store_path: str
) -> Optional[dict]:
    hash_part = os.path.basename(store_path).split("-", 1)[0]
    url = f"{cache_url.rstrip('/')}/{hash_part}.narinfo"
    r = await client.get(url)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    info: dict[str, str] = {}
    for line in r.text.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            info[k.strip()] = v.strip()
    return info


class _XzDec:
    def __init__(self) -> None:
        self._d = lzma.LZMADecompressor(format=lzma.FORMAT_AUTO)

    def feed(self, chunk: bytes) -> bytes:
        return self._d.decompress(chunk)


class _ZstdDec:
    def __init__(self) -> None:
        import zstandard  # lazy

        self._d = zstandard.ZstdDecompressor().decompressobj()

    def feed(self, chunk: bytes) -> bytes:
        return self._d.decompress(chunk)


class _Bz2Dec:
    def __init__(self) -> None:
        import bz2

        self._d = bz2.BZ2Decompressor()

    def feed(self, chunk: bytes) -> bytes:
        return self._d.decompress(chunk)


class _NoopDec:
    def feed(self, chunk: bytes) -> bytes:
        return chunk


def _make_decompressor(compression: str):
    c = compression.lower()
    if c in ("xz", "lzma"):
        return _XzDec()
    if c == "zstd":
        return _ZstdDec()
    if c in ("bzip2", "bz2"):
        return _Bz2Dec()
    if c in ("none", ""):
        return _NoopDec()
    raise ValueError(f"unsupported NAR compression: {compression!r}")


def _nar_url(cache_url: str, narinfo: dict) -> str:
    return f"{cache_url.rstrip('/')}/{narinfo['URL']}"


async def _decompressed_chunks(
    response: httpx.Response, compression: str
) -> AsyncIterator[bytes]:
    """
    Pure async generator: yields decompressed chunks from an already-opened
    streaming response. Lifecycle of the response must be managed by the
    caller via `async with client.stream(...)`. Putting `async with` inside
    an async generator causes GeneratorExit vs asyncio shutdown issues —
    don't.
    """
    dec = _make_decompressor(compression)
    async for chunk in response.aiter_bytes(chunk_size=1 << 18):
        out = dec.feed(chunk)
        if out:
            yield out


# ---------------------------------------------------------------------------
# SQLite state DB
# ---------------------------------------------------------------------------

_SCHEMA = """
CREATE TABLE IF NOT EXISTS scanned (
    store_path     TEXT PRIMARY KEY,
    status         TEXT NOT NULL,
    macho_slices   INTEGER NOT NULL DEFAULT 0,
    failing_slices INTEGER NOT NULL DEFAULT 0,
    error          TEXT,
    ts             INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS scanned_status ON scanned(status);
CREATE INDEX IF NOT EXISTS scanned_failing ON scanned(failing_slices) WHERE failing_slices > 0;
"""


def open_state(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(path), isolation_level=None, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.executescript(_SCHEMA)
    return conn


def load_done(conn: sqlite3.Connection) -> set[str]:
    """Return store paths considered already-handled.

    Skips paths whose last recorded status was a transient error
    (`fetch_error`, `parse_error`) so those get retried on subsequent
    runs. `ok` and `no_narinfo` are terminal and not retried.
    """
    return {
        r[0]
        for r in conn.execute(
            "SELECT store_path FROM scanned WHERE status IN ('ok', 'no_narinfo')"
        )
    }


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------


@dataclass
class Counters:
    total: int = 0
    done: int = 0
    fetch_errors: int = 0
    parse_errors: int = 0
    no_narinfo: int = 0
    macho_slices: int = 0
    failing_slices: int = 0


async def scan_store_path(
    client: httpx.AsyncClient,
    cache_url: str,
    store_path: str,
    max_macho_bytes: int,
) -> dict:
    narinfo = await fetch_narinfo(client, cache_url, store_path)
    if narinfo is None:
        return {"store_path": store_path, "status": "no_narinfo", "slices": []}
    try:
        compression = narinfo.get("Compression", "xz")
        url = _nar_url(cache_url, narinfo)
        slices_out: list[dict] = []
        async with client.stream("GET", url) as response:
            response.raise_for_status()
            chunks = _decompressed_chunks(response, compression)
            stream = AsyncByteStream(chunks)
            async for entry in iter_nar_regular_files(
                stream, max_macho_bytes=max_macho_bytes
            ):
                if entry.content is None:
                    if entry.truncated:
                        slices_out.append(
                            {
                                "store_path": store_path,
                                "path": entry.path,
                                "size": entry.size,
                                "status": "too_large",
                            }
                        )
                    continue
                if not _macho_magic(entry.content[:4]):
                    continue
                try:
                    reports = analyze_macho(entry.content)
                except (
                    Exception
                ) as e:  # defensive: don't let one bad file kill the scan
                    slices_out.append(
                        {
                            "store_path": store_path,
                            "path": entry.path,
                            "size": entry.size,
                            "status": "analyze_error",
                            "error": f"{type(e).__name__}: {e}",
                        }
                    )
                    continue
                for rep in reports:
                    slices_out.append(
                        {
                            "store_path": store_path,
                            "path": entry.path,
                            "size": entry.size,
                            "executable": entry.executable,
                            "is_fat": rep.is_fat,
                            "fat_variant": rep.fat_variant,
                            "arch": rep.arch,
                            "cpu_type": rep.cpu_type,
                            "cpu_subtype": rep.cpu_subtype,
                            "has_code_signature": rep.has_code_signature,
                            "cd_flags": rep.cd_flags,
                            "linker_signed": rep.linker_signed,
                            "hash_algo": rep.hash_algo,
                            "page_size": rep.page_size,
                            "n_code_slots": rep.n_code_slots,
                            "n_special_slots": rep.n_special_slots,
                            "code_limit": rep.code_limit,
                            "n_mismatches": rep.n_mismatches,
                            "first_bad_page": rep.first_bad_page,
                            "first_bad_offset": rep.first_bad_offset,
                            "mismatches_sample": rep.mismatches_sample,
                            "slots": rep.slots,
                            "alternate_cds": rep.alternate_cds,
                            "cms_blob_length": rep.cms_blob_length,
                            "has_entitlements": rep.has_entitlements,
                            "has_entitlements_der": rep.has_entitlements_der,
                            "linked_dylibs": rep.linked_dylibs,
                            "error": rep.error,
                            "status": "ok",
                        }
                    )
        return {"store_path": store_path, "status": "ok", "slices": slices_out}
    except Exception as e:
        return {
            "store_path": store_path,
            "status": "parse_error",
            "slices": [],
            "error": f"{type(e).__name__}: {e}",
        }


def _chunks(seq: list, n: int) -> Iterable[list]:
    for i in range(0, len(seq), n):
        yield seq[i : i + n]


def _persist_result(
    result: dict,
    state: sqlite3.Connection,
    out_f,
    counters: "Counters",
    start: float,
    log_every: int = 100,
) -> None:
    """Apply a single path result to DB, JSONL, and counters. Main process only."""
    sp = result["store_path"]
    macho = sum(1 for s in result["slices"] if s.get("status") == "ok")
    failing = sum(
        1
        for s in result["slices"]
        if s.get("status") == "ok" and (s.get("n_mismatches") or 0) > 0
    )

    out_f.write(json.dumps(result, separators=(",", ":")) + "\n")

    state.execute(
        "INSERT OR REPLACE INTO scanned "
        "(store_path, status, macho_slices, failing_slices, error, ts) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (sp, result["status"], macho, failing, result.get("error"), int(time.time())),
    )

    counters.done += 1
    counters.macho_slices += macho
    counters.failing_slices += failing
    if result["status"] == "fetch_error":
        counters.fetch_errors += 1
    elif result["status"] == "parse_error":
        counters.parse_errors += 1
    elif result["status"] == "no_narinfo":
        counters.no_narinfo += 1

    if counters.done % log_every == 0 or counters.done == counters.total:
        elapsed = time.time() - start
        rate = counters.done / elapsed if elapsed > 0 else 0.0
        eta_s = (counters.total - counters.done) / rate if rate > 0 else 0.0
        log.info(
            "progress %d/%d  rate=%.1f/s  eta=%.0fm  "
            "macho_slices=%d  failing=%d  no_narinfo=%d  fetch_err=%d  parse_err=%d",
            counters.done,
            counters.total,
            rate,
            eta_s / 60,
            counters.macho_slices,
            counters.failing_slices,
            counters.no_narinfo,
            counters.fetch_errors,
            counters.parse_errors,
        )


# ---------------------------------------------------------------------------
# Multiprocess mode: Pool.imap_unordered with batched async workers.
# ---------------------------------------------------------------------------
#
# Main process:
#   - fetches store-paths.xz once
#   - chunks todo list into batches of --batch-size
#   - hands batches to a pool of --workers processes via imap_unordered
#   - drains results and writes SQLite + JSONL (single writer)
#
# Each worker:
#   - runs asyncio.run(_batch_scan(batch)) which creates its own event loop
#     and its own httpx.AsyncClient with its own connection pool and
#     --per-worker-concurrency in-flight requests
#   - does HTTP + decompression + NAR parse + SHA-256 entirely inside the
#     worker process, so every core does real work
#
# Worker crash recovery falls out for free: if a worker dies mid-batch, the
# batch's results don't reach main, so those store paths are not recorded
# in the state DB and will be retried on the next run.


def _batch_worker(args: tuple) -> list[dict]:
    """mp.Pool entrypoint. Runs a full asyncio batch in its own event loop."""
    cache_url, paths, max_macho_bytes, concurrency = args
    try:
        return asyncio.run(_batch_scan(cache_url, paths, max_macho_bytes, concurrency))
    except Exception as e:  # defensive: never let a worker crash lose the whole pool
        return [
            {
                "store_path": p,
                "status": "fetch_error",
                "slices": [],
                "error": f"batch_worker_crash: {type(e).__name__}: {e}",
            }
            for p in paths
        ]


async def _batch_scan(
    cache_url: str, paths: list[str], max_macho_bytes: int, concurrency: int
) -> list[dict]:
    timeout = httpx.Timeout(connect=30.0, read=600.0, write=60.0, pool=None)
    limits = httpx.Limits(
        max_connections=concurrency * 2,
        max_keepalive_connections=concurrency,
    )
    async with httpx.AsyncClient(
        timeout=timeout,
        limits=limits,
        http2=True,
        follow_redirects=True,
        headers={"User-Agent": "nixpkgs-507531-cache-scanner/1"},
    ) as client:
        sem = asyncio.Semaphore(concurrency)

        async def one(p: str) -> dict:
            async with sem:
                try:
                    return await scan_store_path(client, cache_url, p, max_macho_bytes)
                except Exception as e:
                    return {
                        "store_path": p,
                        "status": "fetch_error",
                        "slices": [],
                        "error": f"{type(e).__name__}: {e}",
                    }

        return await asyncio.gather(*(one(p) for p in paths))


def _run_mp(args: argparse.Namespace) -> None:
    state = open_state(Path(args.state))
    done = load_done(state)
    log.info("resume: %d paths already scanned", len(done))

    out_f = open(args.out, "a", buffering=1)

    if args.paths_file:
        paths = load_paths_from_file(
            args.paths_file, shard=args.shard, total_shards=args.total_shards
        )
    else:
        # Fetch store-paths list once in main (short-lived async client).
        async def _fetch() -> list[str]:
            async with httpx.AsyncClient(
                timeout=httpx.Timeout(60.0),
                follow_redirects=True,
                headers={"User-Agent": "nixpkgs-507531-cache-scanner/1"},
            ) as client:
                return await fetch_store_paths(
                    client,
                    args.channel,
                    shard=args.shard,
                    total_shards=args.total_shards,
                )

        paths = asyncio.run(_fetch())
    log.info("path-list slice has %d paths", len(paths))
    todo = [p for p in paths if p not in done]
    if args.limit:
        todo = todo[: args.limit]
    log.info(
        "scanning %d paths: workers=%d batch_size=%d per_worker_concurrency=%d",
        len(todo),
        args.workers,
        args.batch_size,
        args.per_worker_concurrency,
    )

    batches = [
        (args.cache, chunk, args.max_macho_bytes, args.per_worker_concurrency)
        for chunk in _chunks(todo, args.batch_size)
    ]

    counters = Counters(total=len(todo))
    start = time.time()

    # Use spawn for clean worker state (no event loop inheritance).
    ctx = mp.get_context("spawn")
    with ctx.Pool(processes=args.workers) as pool:
        try:
            for batch_result in pool.imap_unordered(_batch_worker, batches):
                for r in batch_result:
                    _persist_result(r, state, out_f, counters, start)
        except KeyboardInterrupt:
            log.warning("interrupt received; terminating pool")
            pool.terminate()
            pool.join()
            raise

    out_f.close()
    log.info(
        "scan complete: %d paths, %d Mach-O slices, %d failing, "
        "%d no-narinfo, %d fetch-err, %d parse-err",
        counters.done,
        counters.macho_slices,
        counters.failing_slices,
        counters.no_narinfo,
        counters.fetch_errors,
        counters.parse_errors,
    )


# ---------------------------------------------------------------------------
# Single-process mode (--workers 0): the original async-only implementation.
# Kept as a debug / sanity-check path.
# ---------------------------------------------------------------------------


async def _run_single(args: argparse.Namespace) -> None:
    state = open_state(Path(args.state))
    done = load_done(state)
    log.info("resume: %d paths already scanned", len(done))

    out_f = open(args.out, "a", buffering=1)

    timeout = httpx.Timeout(connect=30.0, read=600.0, write=60.0, pool=None)
    limits = httpx.Limits(
        max_connections=args.concurrency * 2,
        max_keepalive_connections=args.concurrency,
    )
    stopping = False

    def _set_stop(*_) -> None:
        nonlocal stopping
        if not stopping:
            log.warning("interrupt received; finishing in-flight tasks, then exiting")
        stopping = True

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, _set_stop)
        except NotImplementedError:
            pass  # e.g. on Windows

    async with httpx.AsyncClient(
        timeout=timeout,
        limits=limits,
        http2=True,
        follow_redirects=True,
        headers={"User-Agent": "nixpkgs-507531-cache-scanner/1"},
    ) as client:
        if args.paths_file:
            paths = load_paths_from_file(
                args.paths_file,
                shard=args.shard,
                total_shards=args.total_shards,
            )
        else:
            paths = await fetch_store_paths(
                client,
                args.channel,
                shard=args.shard,
                total_shards=args.total_shards,
            )
        log.info("path-list slice has %d paths", len(paths))
        todo = [p for p in paths if p not in done]
        if args.limit:
            todo = todo[: args.limit]
        log.info("scanning %d paths (single-process)", len(todo))

        counters = Counters(total=len(todo))
        start = time.time()
        sem = asyncio.Semaphore(args.concurrency)

        async def worker(sp: str) -> None:
            if stopping:
                return
            async with sem:
                if stopping:
                    return
                try:
                    result = await scan_store_path(
                        client, args.cache, sp, args.max_macho_bytes
                    )
                except Exception as e:
                    result = {
                        "store_path": sp,
                        "status": "fetch_error",
                        "slices": [],
                        "error": f"{type(e).__name__}: {e}",
                    }
                _persist_result(result, state, out_f, counters, start)

        tasks = [asyncio.create_task(worker(sp)) for sp in todo]
        await asyncio.gather(*tasks, return_exceptions=False)

    out_f.close()
    log.info(
        "scan complete: %d paths, %d Mach-O slices, %d failing, "
        "%d no-narinfo, %d fetch-err, %d parse-err",
        counters.done,
        counters.macho_slices,
        counters.failing_slices,
        counters.no_narinfo,
        counters.fetch_errors,
        counters.parse_errors,
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    default_workers = max(1, (os.cpu_count() or 2) - 1)
    p = argparse.ArgumentParser(
        description="Scan an aarch64-darwin nixpkgs channel's cache for the NixOS/nixpkgs#507531 page-hash bug."
    )
    src = p.add_mutually_exclusive_group()
    src.add_argument(
        "--channel",
        default=None,
        help=f"Channel base URL; fetches <url>/store-paths.xz (default: {DEFAULT_CHANNEL})",
    )
    src.add_argument(
        "--paths-file",
        default=None,
        help="Local file with newline-separated /nix/store paths to scan, "
        "instead of fetching <channel>/store-paths.xz. Used by the synthetic "
        "`release` channel whose path list is generated by `nix-eval-jobs` "
        "against `release-25.11#legacyPackages.aarch64-darwin`.",
    )
    p.add_argument(
        "--cache",
        default=DEFAULT_CACHE,
        help=f"Binary cache URL (default: {DEFAULT_CACHE})",
    )
    p.add_argument(
        "--state",
        default="./darwin-cache-scan.state.db",
        help="SQLite state DB for resume (default: ./darwin-cache-scan.state.db)",
    )
    p.add_argument(
        "--out",
        default="./darwin-cache-scan.jsonl",
        help="JSONL output (append mode) (default: ./darwin-cache-scan.jsonl)",
    )
    p.add_argument(
        "--workers",
        type=int,
        default=default_workers,
        help=f"Worker processes for multiprocess mode (default: cpu_count()-1 = {default_workers}). "
        "0 = single-process (no mp.Pool), uses --concurrency instead.",
    )
    p.add_argument(
        "--batch-size",
        type=int,
        default=100,
        help="Paths per mp.Pool batch (default: 100). "
        "Lower = better load balance; higher = less per-batch overhead.",
    )
    p.add_argument(
        "--per-worker-concurrency",
        type=int,
        default=32,
        help="Concurrent HTTP requests in flight per worker process (default: 32). "
        "Total in-flight = workers * per-worker-concurrency.",
    )
    p.add_argument(
        "--concurrency",
        type=int,
        default=64,
        help="Single-process mode only: max concurrent in-flight (default: 64).",
    )
    p.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Limit paths scanned this run (0 = all; useful for smoke tests)",
    )
    p.add_argument(
        "--shard",
        type=int,
        default=0,
        help="This shard's index (0-based). Combined with --total-shards, "
        "restricts the scanner to paths[i] where i %% total_shards == shard. "
        "Default: 0 (process every path when total_shards is 1).",
    )
    p.add_argument(
        "--total-shards",
        type=int,
        default=1,
        help="Total number of shards. Default: 1 (no sharding). Used by the "
        "GitHub Actions matrix to fan the scan across parallel jobs so no "
        "single job hits the 6h per-job cap on public-repo hosted runners.",
    )
    p.add_argument(
        "--max-macho-bytes",
        type=int,
        default=2 << 30,
        help="Skip Mach-O files larger than this many bytes (default: 2 GiB)",
    )
    p.add_argument(
        "--log-level", default="INFO", help="Python logging level (default: INFO)"
    )
    return p.parse_args(argv)


def main() -> int:
    args = parse_args(sys.argv[1:])
    logging.basicConfig(
        level=args.log_level,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    if args.channel is None and args.paths_file is None:
        args.channel = DEFAULT_CHANNEL
    try:
        if args.workers > 0:
            _run_mp(args)
        else:
            asyncio.run(_run_single(args))
    except KeyboardInterrupt:
        return 130
    return 0


if __name__ == "__main__":
    sys.exit(main())
