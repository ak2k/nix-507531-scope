#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# ///
"""
Cross-validate every scanner-flagged failing slice against an independent
Mach-O signature verifier (`codesign -v` on darwin, `rcodesign verify` on
linux — both check page hashes in LC_CODE_SIGNATURE and report mismatch).

Reads the aggregator's `direct-failing.csv` plus the "other_sig_invalid" slices
from the JSONL (not in direct-failing.csv by design), then for each unique
store path:

  1. `nix store verify --store <cache>` — Nix's own C++ checks the narinfo
     signature against the trusted key AND the NAR content hash, streaming
     in memory: no closure, no disk.
  2. `nix store dump-path --store <cache> | nix-store --restore <tmpdir>` —
     materialize just this package (again Nix's NAR codec, independent of
     the scanner's Python parser). The NAR bytes are sha256-hashed in the
     pipe and compared against the narinfo NarHash, closing the window
     between the verified fetch (step 1) and this one.
  3. Run the Mach-O verifier on each flagged slice, then delete the tmpdir.

Peak disk is the largest single package, not the union of runtime closures —
realizing closures via `nix-store -r` needed ~22 GB for the release channel
and overflowed ubuntu-latest runners.

One package per run (the smallest, closure-capped) is additionally pulled
through real `nix-store -r` substitution as a canary, and its flagged files
are byte-compared against the direct restore. This keeps the user-shaped
production path (substitution into a real store, with signature enforcement)
continuously exercised, so "users actually receive these bytes through Nix
itself" stays a daily-proven claim.

Default verifier is auto-detected:
  - darwin  → /usr/bin/codesign -v
  - linux   → rcodesign verify
Override with --verifier.

Output: verify-results.jsonl (one row per verified slice)
        verify-summary.md    (agreement matrix + any disagreements)

Exit codes:
  0 — all slices verified, full agreement
  1 — scanner ↔ verifier disagreement (possible scanner false positive)
  2 — infrastructure/integrity failure: a path could not be fetched, Nix
      reported it corrupted/untrusted, the NarHash crosscheck failed, or
      the canary byte-comparison failed. Loud by design: the cache served
      these paths to the scanner hours earlier, so any of these is either
      a transient worth a rerun or a cache-integrity finding.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

CACHE_NIXOS_ORG_KEY = "cache.nixos.org-1:6NCHdD59X431o0gWypbMrAURkbJ16ZPMQFGspcDShjY="


def load_failing_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open() as f:
        return list(csv.DictReader(f))


def load_other_sig_from_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out: list[dict] = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        sp = r.get("store_path", "")
        for s in r.get("slices", []):
            if s.get("status") != "ok":
                continue
            if not s.get("has_code_signature"):
                continue
            if (s.get("n_mismatches") or 0) > 0:
                continue  # that's in direct-failing.csv
            if s.get("error"):
                out.append(
                    {
                        "store_path": sp,
                        "path": s.get("path"),
                        "arch": s.get("arch"),
                        "error": s.get("error"),
                        "is_fat": s.get("is_fat"),
                        "linker_signed": s.get("linker_signed"),
                        "scanner_category": "other_sig_invalid",
                    }
                )
    return out


def run_nix(args: list[str], timeout: int = 600) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["nix", "--extra-experimental-features", "nix-command", *args],
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def with_retry(fn, attempts: int = 3, delay: float = 10.0):
    last: Exception | None = None
    for i in range(attempts):
        try:
            return fn()
        except Exception as e:  # noqa: BLE001 — retried, then re-raised
            last = e
            if i + 1 < attempts:
                print(f"  retry {i + 1}/{attempts - 1} after: {e}", file=sys.stderr)
                time.sleep(delay)
    assert last is not None
    raise last


def path_info(sp: str, cache: str) -> dict:
    """narinfo metadata via Nix: narHash (SRI), narSize."""
    r = run_nix(["path-info", "--store", cache, "--json", sp])
    if r.returncode != 0:
        raise RuntimeError(f"path-info failed for {sp}: {r.stderr.strip()}")
    data = json.loads(r.stdout)
    if isinstance(data, dict):
        return data[sp]
    return next(x for x in data if x.get("path") == sp)


def narhash_hex(sri: str) -> str:
    """Convert a Nix SRI/base32 NarHash to hex via `nix hash convert`
    (no hand-rolled base32 decoding)."""
    r = run_nix(["hash", "convert", "--hash-algo", "sha256", "--to", "base16", sri])
    if r.returncode != 0:
        raise RuntimeError(f"nix hash convert failed for {sri}: {r.stderr.strip()}")
    return r.stdout.strip()


def nix_store_verify(sp: str, cache: str, trusted_key: str) -> tuple[str, str]:
    """Nix's own signature + content verification of a remote-store path.

    Returns (status, message); status in {ok, corrupted, untrusted, error}.
    Exit code is a bitmask: 1 = corrupted contents, 2 = untrusted (no valid
    sig from a trusted key), 4 = other errors.
    """
    r = run_nix(
        ["store", "verify", "--store", cache, "--trusted-public-keys", trusted_key, sp],
        timeout=1800,
    )
    msg = (r.stderr or r.stdout).strip()
    if r.returncode == 0:
        return "ok", ""
    if r.returncode & 1:
        return "corrupted", msg
    if r.returncode & 2:
        return "untrusted", msg
    return "error", msg


def fetch_and_restore(sp: str, cache: str, dest: Path, timeout: int = 1800) -> str:
    """Stream the package NAR (dump-path → restore, both Nix's NAR codec)
    and return the hex sha256 of the NAR bytes, hashed in the pipe."""
    if dest.exists():
        shutil.rmtree(dest)
    # stderr goes to spooled files, not PIPE: a PIPE that fills while this
    # process is busy pumping stdout→stdin would deadlock the pipeline.
    with tempfile.TemporaryFile() as dump_err, tempfile.TemporaryFile() as restore_err:
        dump = subprocess.Popen(
            [
                "nix",
                "--extra-experimental-features",
                "nix-command",
                "store",
                "dump-path",
                "--store",
                cache,
                sp,
            ],
            stdout=subprocess.PIPE,
            stderr=dump_err,
        )
        restore = subprocess.Popen(
            ["nix-store", "--restore", str(dest)],
            stdin=subprocess.PIPE,
            stderr=restore_err,
        )
        assert dump.stdout is not None and restore.stdin is not None
        h = hashlib.sha256()
        deadline = time.monotonic() + timeout

        def read_err(f) -> str:
            f.seek(0)
            return f.read().decode(errors="replace").strip()

        try:
            while chunk := dump.stdout.read(1 << 20):
                if time.monotonic() > deadline:
                    raise TimeoutError(f"fetch_and_restore timed out for {sp}")
                h.update(chunk)
                restore.stdin.write(chunk)
            restore.stdin.close()
            if dump.wait(timeout=60) != 0:
                raise RuntimeError(
                    f"nix store dump-path failed for {sp}: {read_err(dump_err)}"
                )
            if restore.wait(timeout=600) != 0:
                raise RuntimeError(
                    f"nix-store --restore failed for {sp}: {read_err(restore_err)}"
                )
        finally:
            for proc in (dump, restore):
                if proc.poll() is None:
                    proc.kill()
        return h.hexdigest()


def realize(store_path: str, cache_url: str, trusted_key: str) -> tuple[bool, str]:
    """Full `nix-store -r` substitution into the local store (canary only).
    Returns (ok, message)."""
    cmd = [
        "nix-store",
        "-r",
        store_path,
        "--option",
        "substituters",
        cache_url,
        "--option",
        "trusted-public-keys",
        trusted_key,
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
    except subprocess.TimeoutExpired:
        return False, "timeout"
    if r.returncode != 0:
        return False, (r.stderr or r.stdout).strip().splitlines()[-1] if (
            r.stderr or r.stdout
        ).strip() else "realize failed"
    return True, ""


def closure_nar_size(sp: str, cache: str) -> int:
    r = run_nix(["path-info", "--store", cache, "-r", "--json", sp])
    if r.returncode != 0:
        raise RuntimeError(f"closure path-info failed for {sp}: {r.stderr.strip()}")
    data = json.loads(r.stdout)
    infos = data.values() if isinstance(data, dict) else data
    return sum(i.get("narSize", 0) for i in infos)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def _auto_verifier() -> list[str]:
    if platform.system() == "Darwin":
        return ["/usr/bin/codesign", "-v"]
    # Linux / other
    rc = shutil.which("rcodesign")
    if rc:
        return [rc, "verify"]
    print(
        "no signature verifier found (need /usr/bin/codesign on darwin or "
        "`rcodesign` in PATH on linux). Try: nix shell nixpkgs#rcodesign",
        file=sys.stderr,
    )
    sys.exit(2)


def run_verifier(verifier: list[str], full_path: str) -> tuple[int, str]:
    try:
        r = subprocess.run(
            verifier + [full_path],
            capture_output=True,
            text=True,
            timeout=60,
        )
    except subprocess.TimeoutExpired:
        return 124, "verifier timeout"
    msg = (r.stderr or r.stdout).strip()
    return r.returncode, msg


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--failing-csv", default="./direct-failing.csv")
    p.add_argument("--jsonl", default="./full.jsonl")
    p.add_argument("--out", default="./verify-results.jsonl")
    p.add_argument("--summary", default="./verify-summary.md")
    p.add_argument("--cache", default="https://cache.nixos.org")
    p.add_argument("--trusted-key", default=CACHE_NIXOS_ORG_KEY)
    p.add_argument(
        "--verifier",
        nargs="+",
        default=None,
        help="Verifier command + flags (default: auto-detected by platform). "
        "E.g. --verifier /usr/bin/codesign -v  OR  --verifier rcodesign verify",
    )
    p.add_argument(
        "--canary",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Pull the smallest flagged package through real `nix-store -r` "
        "substitution and byte-compare its flagged files against the direct "
        "NAR restore.",
    )
    p.add_argument(
        "--canary-max-closure-bytes",
        type=int,
        default=5_000_000_000,
        help="Skip canary candidates whose runtime closure exceeds this "
        "(unpacked NAR bytes) to keep disk usage bounded.",
    )
    args = p.parse_args()
    verifier = args.verifier if args.verifier else _auto_verifier()
    print(f"verifier: {' '.join(verifier)}", file=sys.stderr)

    failing = load_failing_csv(Path(args.failing_csv))
    other_sig = load_other_sig_from_jsonl(Path(args.jsonl))

    # Normalize into a unified row shape
    rows: list[dict] = []
    for r in failing:
        rows.append(
            {
                "store_path": r["store_path"],
                "path": r["path"],
                "arch": r.get("arch"),
                "is_fat": r.get("is_fat"),
                "linker_signed": r.get("linker_signed"),
                "scanner_category": "page_hash_mismatch",
                "scanner_detail": f"n_mismatches={r.get('n_mismatches')} first_bad_page={r.get('first_bad_page')}",
            }
        )
    for r in other_sig:
        rows.append(r)

    if not rows:
        print("no failing slices to verify", file=sys.stderr)
        return 1

    by_package: dict[str, list[dict]] = {}
    for r in rows:
        by_package.setdefault(r["store_path"], []).append(r)
    unique_paths = sorted(by_package)

    print(
        f"verifying {len(rows)} slices from {len(unique_paths)} unique packages",
        file=sys.stderr,
    )

    # narinfo metadata up front: NarHash for the restore crosscheck,
    # NarSize for canary selection.
    print("fetching narinfo metadata...", file=sys.stderr)
    infos: dict[str, dict] = {}
    for sp in unique_paths:
        infos[sp] = with_retry(lambda sp=sp: path_info(sp, args.cache))

    canary_sp: str | None = None
    canary_result: dict | None = None
    if args.canary:
        for sp in sorted(unique_paths, key=lambda s: infos[s].get("narSize", 0)):
            try:
                closure = with_retry(lambda sp=sp: closure_nar_size(sp, args.cache))
            except Exception as e:  # noqa: BLE001
                print(f"canary: closure sizing failed for {sp}: {e}", file=sys.stderr)
                continue
            if closure <= args.canary_max_closure_bytes:
                canary_sp = sp
                print(
                    f"canary: {sp} (closure {closure / 1e9:.2f} GB unpacked)",
                    file=sys.stderr,
                )
                break
        if canary_sp is None:
            canary_result = {"status": "skipped_no_candidate_under_cap"}
            print(
                "canary: no flagged package has a closure under the cap — skipping",
                file=sys.stderr,
            )

    agreement = {
        "agree_fail": 0,
        "disagree_scanner_false_positive": 0,
        "fetch_failed": 0,
    }
    integrity_failures: list[str] = []
    results: list[dict] = []
    tmp_root = Path(
        tempfile.mkdtemp(prefix="verify-failures-", dir=os.environ.get("RUNNER_TEMP"))
    )

    def fail_package(sp: str, message: str) -> None:
        agreement["fetch_failed"] += len(by_package[sp])
        for r in by_package[sp]:
            results.append(
                {
                    **r,
                    "verifier_exit": None,
                    "verifier_message": message,
                    "verdict": "fetch_failed",
                }
            )

    slice_i = 0
    for pkg_i, sp in enumerate(unique_paths, 1):
        # 1. Nix's own verification: narinfo signature + NAR content hash.
        try:
            status, msg = with_retry(
                lambda sp=sp: nix_store_verify(sp, args.cache, args.trusted_key)
            )
        except Exception as e:  # noqa: BLE001
            status, msg = "error", str(e)
        if status != "ok":
            if status in ("corrupted", "untrusted"):
                # The cache is serving a path that fails Nix's own integrity
                # checks — a finding in itself, never a silent skip.
                integrity_failures.append(f"{sp}: nix store verify: {status}: {msg}")
            print(
                f"  [{pkg_i}/{len(unique_paths)}] VERIFY-{status.upper()} {sp}  {msg}",
                file=sys.stderr,
            )
            fail_package(sp, f"nix store verify: {status}: {msg}")
            slice_i += len(by_package[sp])
            continue

        # 2. Materialize the single package; crosscheck the streamed NAR
        # hash against the narinfo (closes the two-fetch window).
        dest = tmp_root / sp.rsplit("/", 1)[-1]
        try:
            nar_hex = with_retry(
                lambda sp=sp, dest=dest: fetch_and_restore(sp, args.cache, dest)
            )
            expected_hex = narhash_hex(infos[sp]["narHash"])
        except Exception as e:  # noqa: BLE001
            print(
                f"  [{pkg_i}/{len(unique_paths)}] FETCH-FAILED {sp}  {e}",
                file=sys.stderr,
            )
            fail_package(sp, f"fetch/restore failed: {e}")
            slice_i += len(by_package[sp])
            shutil.rmtree(dest, ignore_errors=True)
            continue
        if nar_hex != expected_hex:
            integrity_failures.append(
                f"{sp}: restored NAR sha256 {nar_hex} != narinfo NarHash {expected_hex}"
            )
            fail_package(sp, "NarHash mismatch between verified fetch and restore")
            slice_i += len(by_package[sp])
            shutil.rmtree(dest, ignore_errors=True)
            continue
        print(f"  [{pkg_i}/{len(unique_paths)}] OK  {sp}", file=sys.stderr)

        # 3. Independent Mach-O verifier on each flagged slice.
        for r in by_package[sp]:
            slice_i += 1
            full_path = dest / r["path"]
            if not full_path.exists():
                results.append(
                    {
                        **r,
                        "verifier_exit": None,
                        "verifier_message": "file not found in restored package",
                        "verdict": "file_missing",
                    }
                )
                agreement["fetch_failed"] += 1
                continue
            code, msg = run_verifier(verifier, str(full_path))
            if code != 0:
                verdict = "agree_fail"
                agreement["agree_fail"] += 1
            else:
                verdict = "disagree_scanner_false_positive"
                agreement["disagree_scanner_false_positive"] += 1
            results.append(
                {
                    **r,
                    "verifier_exit": code,
                    "verifier_message": msg,
                    "verdict": verdict,
                }
            )
            print(
                f"  [{slice_i}/{len(rows)}] {verdict}  {r['path']}  (rc={code})",
                file=sys.stderr,
            )

        # Canary: same package through real substitution, byte-compare
        # flagged files between the realized store path and our restore.
        if sp == canary_sp:
            ok, msg = realize(sp, args.cache, args.trusted_key)
            if not ok:
                canary_result = {
                    "store_path": sp,
                    "status": "realize_failed",
                    "message": msg,
                }
                integrity_failures.append(f"canary {sp}: nix-store -r failed: {msg}")
            else:
                mismatches = [
                    r["path"]
                    for r in by_package[sp]
                    if sha256_file(Path(sp) / r["path"])
                    != sha256_file(dest / r["path"])
                ]
                if mismatches:
                    integrity_failures.append(
                        f"canary {sp}: realized vs restored bytes differ: {mismatches}"
                    )
                    canary_result = {
                        "store_path": sp,
                        "status": "byte_mismatch",
                        "files": mismatches,
                    }
                else:
                    canary_result = {
                        "store_path": sp,
                        "status": "ok",
                        "files_compared": len(by_package[sp]),
                    }
            print(f"canary: {canary_result}", file=sys.stderr)

        shutil.rmtree(dest, ignore_errors=True)

    shutil.rmtree(tmp_root, ignore_errors=True)

    # Emit JSONL
    with open(args.out, "w") as f:
        for r in results:
            f.write(json.dumps(r, separators=(",", ":")) + "\n")

    # Summary markdown
    total = len(results)
    md: list[str] = []
    md.append("# Scanner × codesign -v cross-validation")
    md.append("")
    md.append(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
    md.append("")
    md.append("Each flagged package is signature- and content-verified by Nix itself")
    md.append("(`nix store verify` against the binary cache), restored with Nix's NAR")
    md.append("codec, NarHash-crosschecked, then every flagged slice is checked with")
    md.append(f"an independent signature verifier: `{' '.join(verifier)}`.")
    md.append("")
    md.append("| Outcome | Count |")
    md.append("|---|---:|")
    md.append(
        f"| Scanner failing, verifier fails (agreement) | {agreement['agree_fail']} |"
    )
    md.append(
        f"| Scanner failing, verifier passes (disagreement — possible false positive) | {agreement['disagree_scanner_false_positive']} |"
    )
    md.append(
        f"| Fetch/verify failed (could not check against cache) | {agreement['fetch_failed']} |"
    )
    md.append(f"| **Total slices verified** | **{total}** |")
    md.append("")
    if canary_result is not None:
        md.append("## Substitution canary")
        md.append("")
        md.append(
            "One flagged package per run is pulled through real `nix-store -r` "
            "substitution and its flagged files byte-compared against the direct "
            "NAR restore, keeping the user-shaped path continuously exercised."
        )
        md.append("")
        md.append("```json")
        md.append(json.dumps(canary_result, indent=2))
        md.append("```")
        md.append("")
    disagreements = [
        r for r in results if r["verdict"] == "disagree_scanner_false_positive"
    ]
    if disagreements:
        md.append("## Disagreements (possible scanner false positives)")
        md.append("")
        md.append("| Package | Path | Arch | Scanner detail | Verifier message |")
        md.append("|---|---|---|---|---|")
        for r in disagreements:
            pkg = (
                r["store_path"].rsplit("-", 1)[-1]
                if "-" in r["store_path"]
                else r["store_path"]
            )
            md.append(
                f"| {pkg} | `{r['path']}` | {r['arch']} | {r.get('scanner_detail', r.get('error', ''))} | `{r['verifier_message']}` |"
            )
        md.append("")
    if integrity_failures:
        md.append("## Integrity failures (cache served bytes Nix rejects)")
        md.append("")
        for line in integrity_failures:
            md.append(f"- {line}")
        md.append("")
    if not disagreements and not integrity_failures and not agreement["fetch_failed"]:
        md.append(
            "No disagreements: every scanner-flagged failure was independently confirmed by the verifier."
        )
        md.append("")

    Path(args.summary).write_text("\n".join(md) + "\n")

    print(f"\nResults: {args.out}", file=sys.stderr)
    print(f"Summary: {args.summary}", file=sys.stderr)
    print(
        f"\nAgreement: {agreement['agree_fail']}/{total} scanner failures confirmed by {' '.join(verifier)}"
    )
    if integrity_failures or agreement["fetch_failed"]:
        print(
            f"ERROR: {len(integrity_failures)} integrity failures, "
            f"{agreement['fetch_failed']} fetch-failed slices — see {args.summary}"
        )
        return 2
    if disagreements:
        print(f"WARNING: {len(disagreements)} disagreements — see {args.summary}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
