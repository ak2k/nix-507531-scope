#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# ///
"""
Aggregate the JSONL output from scan-darwin-cache.py into:
  - REPORT.md           — human-readable, PR-pasteable markdown
  - summary.json        — machine-readable counts (for CI badges, trend
                          tracking, diffing between runs)
  - failing.csv         — one row per failing Mach-O slice (optional)

Classification scheme (per scanned Mach-O slice):

  page_hash_mismatch    status=ok, has_code_signature, n_mismatches > 0
                        → the NixOS/nixpkgs#507531 bug proper. Always in the
                          headline count. These are slices whose stored
                          per-page SHA-256 in the CodeDirectory disagrees
                          with the actual SHA-256 of the covered page
                          bytes. codesign -v reports
                          "invalid signature (code or signature have been
                          modified)".

  other_sig_invalid     status=ok, has_code_signature, error indicates a
                        structural signature problem (OOB signature,
                        unsupported hash type, truncated LINKEDIT, etc.)
                        → codesign -v would reject. The mechanism may or
                        may not be the same as the page-hash case; counted
                        separately.

  not_real_macho        Java .class files (shared cafebabe magic),
                        big-endian PPC, or other non-modern-darwin
                        formats. Correctly rejected by scanner. Noise.

  unsigned              Valid Mach-O with no LC_CODE_SIGNATURE. Typical
                        for x86_64 objects that the linker didn't adhoc
                        sign. Not affected by the bug.

  clean                 Signed Mach-O with no mismatches. Pass.

  scanner_error         status != ok (too_large, analyze_error). Rare.

Usage:
  aggregate-scan.py <input.jsonl> [--out REPORT.md] [--summary-json summary.json]
                                   [--failing-csv failing.csv]
                                   [--channel-label 'nixpkgs-25.11-darwin @ <rev>']
"""

from __future__ import annotations

import argparse
import collections
import csv
import json
import sys
import time
from pathlib import Path


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------


def classify_signature(s: dict) -> str:
    """Classify a failing slice by its SuperBlob shape. Requires scanner
    output from 2026-04-18 or later (fields `cms_blob_length`,
    `has_entitlements`, `has_entitlements_der`). Older scans lack these
    fields and will always land in "unknown".

    Returns one of:
      * "L"         — linker-signed ad-hoc; no CMS slot. The helper FIXES.
      * "C2"        — codesign ad-hoc; empty 8 B CMS wrapper, no Entitlements.
                      Helper FIXES.
      * "B7-empty"  — ad-hoc with Entitlements + empty CMS wrapper
                      (e.g. self-signed tools). Helper FIXES.
      * "B7-real"   — embedded PKCS#7 payload (Developer ID / App Store).
                      Helper SKIPS (the signer's cdhash commitment would
                      otherwise be invalidated).
      * "unknown"   — pre-enrichment scanner output, or a class we don't
                      recognize yet.
    """
    cms = s.get("cms_blob_length")
    if cms is None:
        return "unknown"
    if s.get("linker_signed"):
        return "L"
    if cms > 8:
        return "B7-real"
    if cms == 8 and s.get("has_entitlements") and s.get("has_entitlements_der"):
        return "B7-empty"
    if cms == 8:
        return "C2"
    return "unknown"


def classify_slice(s: dict) -> str:
    """Return one of: page_hash_mismatch, other_sig_invalid, not_real_macho,
    unsigned, clean, scanner_error."""
    status = s.get("status")
    if status != "ok":
        return "scanner_error"
    err = s.get("error")
    if not s.get("has_code_signature", False):
        # Either not signed, or scanner rejected before CD parsing.
        # Some "not_real_macho" cases land here (Java .class files, etc.).
        if err:
            noise_markers = (
                "implausible fat",
                "big-endian",
                "truncated mach_header",
                "bad mach_header",
                "bad fat header",
                "bad fat_arch",
                "fat_arch out-of-bounds",
                "fat_arch OOB",
                "implausible nfat",
                "scanner only handles little-endian",
            )
            if any(m in err for m in noise_markers):
                return "not_real_macho"
        return "unsigned"

    n_mis = s.get("n_mismatches") or 0
    if n_mis > 0:
        return "page_hash_mismatch"
    if err:
        # Has a code signature and scanner errored → structural issue that
        # codesign -v would also reject.
        return "other_sig_invalid"
    return "clean"


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------


def load(path: Path):
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def aggregate(input_path: Path):
    paths_scanned = 0
    paths_by_status = collections.Counter()
    slices_by_arch = collections.Counter()
    buckets = collections.Counter()
    buckets_by_arch: dict[str, collections.Counter] = collections.defaultdict(
        collections.Counter
    )
    linker_vs_codesign = collections.Counter()  # for page_hash_mismatch slices
    buckets_by_signature_class = collections.Counter()  # for page_hash_mismatch slices

    # Fat vs thin split (both for all slices, and for failing slices only)
    buckets_by_kind: dict[str, collections.Counter] = collections.defaultdict(
        collections.Counter
    )
    fat_files: set[tuple[str, str]] = set()  # unique (store_path, path)
    fat_packages: set[str] = set()  # packages containing any fat binary
    fat_failing_packages: set[str] = set()  # fat binaries with at least one mismatch

    # Per-package aggregation (only for problem buckets)
    pkg_page_hash: dict[str, int] = collections.Counter()
    pkg_other_sig: dict[str, int] = collections.Counter()

    failing_rows: list[dict] = []  # page_hash_mismatch slice rows
    other_sig_rows: list[dict] = []  # other_sig_invalid slice rows
    error_samples: dict[str, dict] = {}  # keyed by error text prefix

    for r in load(input_path):
        paths_scanned += 1
        paths_by_status[r.get("status", "unknown")] += 1
        sp = r.get("store_path", "")
        for s in r.get("slices", []):
            arch = s.get("arch", "unknown")
            slices_by_arch[arch] += 1
            b = classify_slice(s)
            buckets[b] += 1
            buckets_by_arch[arch][b] += 1

            kind = "fat" if s.get("is_fat") else "thin"
            buckets_by_kind[kind][b] += 1
            if kind == "fat":
                fat_files.add((sp, s.get("path") or ""))
                fat_packages.add(sp)
                if b == "page_hash_mismatch":
                    fat_failing_packages.add(sp)

            if b == "page_hash_mismatch":
                linker_vs_codesign[
                    "linker_signed" if s.get("linker_signed") else "codesign_signed"
                ] += 1
                pkg_page_hash[sp] += 1
                sig_class = classify_signature(s)
                buckets_by_signature_class[sig_class] += 1
                failing_rows.append(
                    {
                        "store_path": sp,
                        "path": s.get("path"),
                        "arch": arch,
                        "size": s.get("size"),
                        "linker_signed": s.get("linker_signed"),
                        "cd_flags": s.get("cd_flags"),
                        "page_size": s.get("page_size"),
                        "n_code_slots": s.get("n_code_slots"),
                        "code_limit": s.get("code_limit"),
                        "n_mismatches": s.get("n_mismatches"),
                        "first_bad_page": s.get("first_bad_page"),
                        "first_bad_offset": s.get("first_bad_offset"),
                        # Enriched fields (scanner 2026-04-18+); "" on older scans.
                        "fat_variant": s.get("fat_variant", ""),
                        "cms_blob_length": s.get("cms_blob_length", ""),
                        "has_entitlements": s.get("has_entitlements", ""),
                        "has_entitlements_der": s.get("has_entitlements_der", ""),
                        "n_alternate_cds": len(s.get("alternate_cds", []) or []),
                        "signature_class": sig_class,
                    }
                )
            elif b == "other_sig_invalid":
                pkg_other_sig[sp] += 1
                other_sig_rows.append(
                    {
                        "store_path": sp,
                        "path": s.get("path"),
                        "arch": arch,
                        "error": s.get("error"),
                    }
                )
                key = (s.get("error") or "").split(":")[0].strip() or "unknown"
                error_samples.setdefault(
                    key,
                    {"store_path": sp, "path": s.get("path"), "error": s.get("error")},
                )

    return {
        "paths_scanned": paths_scanned,
        "paths_by_status": dict(paths_by_status),
        "slices_by_arch": dict(slices_by_arch),
        "buckets": dict(buckets),
        "buckets_by_arch": {a: dict(c) for a, c in buckets_by_arch.items()},
        "buckets_by_kind": {k: dict(c) for k, c in buckets_by_kind.items()},
        "fat_unique_files": len(fat_files),
        "fat_packages": len(fat_packages),
        "fat_failing_packages": len(fat_failing_packages),
        "linker_vs_codesign": dict(linker_vs_codesign),
        "buckets_by_signature_class": dict(buckets_by_signature_class),
        "pkg_page_hash": pkg_page_hash,
        "pkg_other_sig": pkg_other_sig,
        "failing_rows": failing_rows,
        "other_sig_rows": other_sig_rows,
        "error_samples": error_samples,
    }


# ---------------------------------------------------------------------------
# Markdown report
# ---------------------------------------------------------------------------


def _pkg_name(store_path: str) -> str:
    # /nix/store/<hash>-<name>  → <name>
    base = store_path.rsplit("/", 1)[-1]
    parts = base.split("-", 1)
    return parts[1] if len(parts) == 2 else base


def _fmt_n(n: int) -> str:
    return f"{n:,}"


def _plural(n: int, singular: str, plural: str | None = None) -> str:
    return singular if n == 1 else (plural or singular + "s")


# Architectures we want to show as individual rows; everything else is
# collapsed into "other / legacy".
_PRIMARY_ARCHES = {"arm64", "arm64e", "x86_64", "i386"}


def render_markdown(agg: dict, channel_label: str) -> str:
    buckets = agg["buckets"]
    by_arch = agg["buckets_by_arch"]
    lines: list[str] = []

    page_hash_pkgs = len(agg["pkg_page_hash"])
    page_hash_slices = buckets.get("page_hash_mismatch", 0)
    other_pkgs = len(agg["pkg_other_sig"])
    other_slices = buckets.get("other_sig_invalid", 0)

    # Header
    lines.append(f"# NixOS/nixpkgs#507531 cache scan — {channel_label}")
    lines.append("")
    lines.append(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
    lines.append("")

    # Summary counts
    lines.append("## Summary")
    lines.append("")
    ls = agg["linker_vs_codesign"]
    ls_linker = ls.get("linker_signed", 0)
    ls_codesign = ls.get("codesign_signed", 0)
    lines.append("| Metric | Count |")
    lines.append("|---|---:|")
    lines.append(f"| Store paths scanned | {_fmt_n(agg['paths_scanned'])} |")
    lines.append(
        f"| Mach-O slices parsed | {_fmt_n(sum(agg['slices_by_arch'].values()))} |"
    )
    lines.append(f"| Page-hash mismatches (slices) | {_fmt_n(page_hash_slices)} |")
    lines.append(
        f"| Page-hash mismatches (distinct packages) | {_fmt_n(page_hash_pkgs)} |"
    )
    lines.append(f"|   of which linker-signed (flags=0x20002) | {_fmt_n(ls_linker)} |")
    lines.append(f"|   of which codesign-signed (flags=0x2) | {_fmt_n(ls_codesign)} |")
    lines.append(f"| Other signature-invalid (slices) | {_fmt_n(other_slices)} |")
    lines.append(
        f"| Other signature-invalid (distinct packages) | {_fmt_n(other_pkgs)} |"
    )
    lines.append("")

    # Arch breakdown (primary archs + a collapsed "other/legacy" row)
    def _collapse_arches(arch_counts: dict) -> list[tuple[str, collections.Counter]]:
        # Returns [(label, counter), ...] with primary archs as individual
        # rows (in a stable, useful order) followed by a single aggregate
        # row for everything else.
        rows: list[tuple[str, collections.Counter]] = []
        order = ["arm64", "arm64e", "x86_64", "i386"]
        for a in order:
            if a in arch_counts:
                rows.append((a, by_arch.get(a, collections.Counter())))
        other_total = collections.Counter()
        other_labels = []
        for a, c in arch_counts.items():
            if a in _PRIMARY_ARCHES:
                continue
            other_total.update(by_arch.get(a, collections.Counter()))
            other_labels.append(a)
        if other_total:
            rows.append((f"other/legacy ({len(other_labels)} arch codes)", other_total))
        return rows

    # Arch breakdown
    lines.append("## By architecture")
    lines.append("")
    lines.append(
        "| Arch | Slices scanned | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned | Noise |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for arch_label, bc in _collapse_arches(agg["slices_by_arch"]):
        total = (
            bc.get("page_hash_mismatch", 0)
            + bc.get("other_sig_invalid", 0)
            + bc.get("clean", 0)
            + bc.get("unsigned", 0)
            + bc.get("not_real_macho", 0)
            + bc.get("scanner_error", 0)
        )
        lines.append(
            "| {}{}{} | {} | {} | {} | {} | {} | {} |".format(
                "`" if arch_label in _PRIMARY_ARCHES else "",
                arch_label,
                "`" if arch_label in _PRIMARY_ARCHES else "",
                _fmt_n(total),
                _fmt_n(bc.get("page_hash_mismatch", 0)),
                _fmt_n(bc.get("other_sig_invalid", 0)),
                _fmt_n(bc.get("clean", 0)),
                _fmt_n(bc.get("unsigned", 0)),
                _fmt_n(bc.get("not_real_macho", 0) + bc.get("scanner_error", 0)),
            )
        )
    lines.append("")

    # Fat vs thin split
    bk = agg["buckets_by_kind"]
    fat_c = (
        bk.get("fat", collections.Counter())
        if isinstance(bk.get("fat"), dict)
        else collections.Counter(bk.get("fat", {}))
    )
    thin_c = (
        bk.get("thin", collections.Counter())
        if isinstance(bk.get("thin"), dict)
        else collections.Counter(bk.get("thin", {}))
    )
    lines.append("## Fat vs thin Mach-O")
    lines.append("")
    lines.append(
        "| Kind | Slices | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|")
    for kind_label, c in (("thin", thin_c), ("fat", fat_c)):
        total = sum(c.values())
        lines.append(
            "| {} | {} | {} | {} | {} | {} |".format(
                kind_label,
                _fmt_n(total),
                _fmt_n(c.get("page_hash_mismatch", 0)),
                _fmt_n(c.get("other_sig_invalid", 0)),
                _fmt_n(c.get("clean", 0)),
                _fmt_n(c.get("unsigned", 0)),
            )
        )
    lines.append("")
    lines.append(
        f"Unique fat binary files: {_fmt_n(agg['fat_unique_files'])} in "
        f"{_fmt_n(agg['fat_packages'])} packages. "
        f"{_fmt_n(agg['fat_failing_packages'])} of those packages contain at "
        "least one failing fat slice."
    )
    lines.append("")

    # Failing packages table — sorted alphabetically by package name for
    # stable diffs between daily runs. Readers typically want "is X in the
    # list?" rather than "who is worst?"; the Failing slices column still
    # conveys per-row severity.
    if page_hash_pkgs:
        lines.append("## Failing packages (page-hash mismatch)")
        lines.append("")
        lines.append("Sorted alphabetically by package name.")
        lines.append("")
        lines.append("| Package | Failing slices | Store path |")
        lines.append("|---|---:|---|")
        for sp, n in sorted(
            agg["pkg_page_hash"].items(), key=lambda x: (_pkg_name(x[0]).lower(), x[0])
        ):
            lines.append(f"| {_pkg_name(sp)} | {n} | `{sp}` |")
        lines.append("")

    # Other sig-invalid packages (appendix)
    if other_pkgs:
        lines.append("## Appendix — other signature-invalid binaries")
        lines.append("")
        lines.append(
            "Slices where the scanner found a structural signature problem"
            " (not a page-hash mismatch). These also fail `codesign -v`."
            " Mechanism may or may not be the same as NixOS/nixpkgs#507531."
        )
        lines.append("")
        lines.append("| Package | Slices | Error kind | Store path |")
        lines.append("|---|---:|---|---|")
        # Group by package
        by_pkg: dict[str, list[dict]] = collections.defaultdict(list)
        for row in agg["other_sig_rows"]:
            by_pkg[row["store_path"]].append(row)
        for sp, rows in sorted(
            by_pkg.items(), key=lambda x: (_pkg_name(x[0]).lower(), x[0])
        ):
            err_kinds = sorted(
                {(r.get("error") or "").split(":")[0].strip() for r in rows}
            )
            lines.append(
                f"| {_pkg_name(sp)} | {len(rows)} | {', '.join(err_kinds)} | `{sp}` |"
            )
        lines.append("")

    # Slice classification counts
    lines.append("## Slice classification")
    lines.append("")
    lines.append("| Category | Count |")
    lines.append("|---|---:|")
    lines.append(
        f"| `page_hash_mismatch` | {_fmt_n(buckets.get('page_hash_mismatch', 0))} |"
    )
    lines.append(
        f"| `other_sig_invalid` | {_fmt_n(buckets.get('other_sig_invalid', 0))} |"
    )
    lines.append(f"| `clean` (signed, verified) | {_fmt_n(buckets.get('clean', 0))} |")
    lines.append(
        f"| `unsigned` (Mach-O without LC_CODE_SIGNATURE) | {_fmt_n(buckets.get('unsigned', 0))} |"
    )
    lines.append(
        f"| `not_real_macho` (Java .class, PPC big-endian, etc.) | {_fmt_n(buckets.get('not_real_macho', 0))} |"
    )
    lines.append(f"| `scanner_error` | {_fmt_n(buckets.get('scanner_error', 0))} |")
    lines.append("")

    # Methodology
    lines.append("## Methodology")
    lines.append("")
    lines.append("- Input: `store-paths.xz` from the channel release URL.")
    lines.append(
        "- Per path: `<hash>.narinfo` → stream NAR over HTTP → decompress (xz/zstd/bz2)"
        " inline → walk entries, no on-disk NAR persistence."
    )
    lines.append(
        "- Per regular file: peek 4 bytes; buffer and analyze only if Mach-O magic matches."
    )
    lines.append(
        "- Per Mach-O slice (thin or fat): parse `LC_CODE_SIGNATURE`, find the SHA-256"
        " CodeDirectory, recompute per-page SHA-256 over"
        " `data[i*ps : min((i+1)*ps, code_limit)]`, compare against the stored hash slot."
    )
    lines.append(
        "- `page_hash_mismatch` is defined as: at least one computed per-page SHA-256"
        " disagrees with its stored hash slot. This matches the kernel's page-in"
        " validator and `codesign -v` rejection criterion for adhoc-signed binaries."
    )
    lines.append(
        "- `other_sig_invalid` is defined as: LC_CODE_SIGNATURE is present but the"
        " signature blob is structurally unparseable (e.g. payload OOB, bad SuperBlob"
        " magic, unsupported hash type)."
    )
    lines.append("- Scanner source: see the PR repo.")
    lines.append("")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# JSON summary
# ---------------------------------------------------------------------------


def build_summary(agg: dict, channel_label: str) -> dict:
    buckets = agg["buckets"]
    return {
        "channel_label": channel_label,
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "paths_scanned": agg["paths_scanned"],
        "paths_by_status": agg["paths_by_status"],
        "slices_total": sum(agg["slices_by_arch"].values()),
        "slices_by_arch": agg["slices_by_arch"],
        "buckets": buckets,
        "buckets_by_arch": agg["buckets_by_arch"],
        "page_hash_mismatch": {
            "slices": buckets.get("page_hash_mismatch", 0),
            "packages": len(agg["pkg_page_hash"]),
            "by_signer": agg["linker_vs_codesign"],
            "by_signature_class": agg["buckets_by_signature_class"],
        },
        "other_sig_invalid": {
            "slices": buckets.get("other_sig_invalid", 0),
            "packages": len(agg["pkg_other_sig"]),
        },
        "coverage": {
            "sha1_only_cds": 0,
            "page_size_zero_cds": 0,
            "not_real_macho": buckets.get("not_real_macho", 0),
            "scanner_errors": buckets.get("scanner_error", 0),
        },
    }


# ---------------------------------------------------------------------------
# CSV of failing slices (optional)
# ---------------------------------------------------------------------------


def write_failing_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    fieldnames = [
        "store_path",
        "path",
        "arch",
        "size",
        "linker_signed",
        "cd_flags",
        "page_size",
        "n_code_slots",
        "code_limit",
        "n_mismatches",
        "first_bad_page",
        "first_bad_offset",
        # Enriched (scanner 2026-04-18+); blank on older scans.
        "fat_variant",
        "cms_blob_length",
        "has_entitlements",
        "has_entitlements_der",
        "n_alternate_cds",
        "signature_class",
    ]
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("input", help="Scan JSONL file")
    p.add_argument("--out", default="REPORT.md", help="Markdown report output path")
    p.add_argument(
        "--summary-json", default="summary.json", help="JSON summary output path"
    )
    p.add_argument(
        "--failing-csv",
        default="",
        help="Optional CSV of failing slices (page-hash mismatches)",
    )
    p.add_argument(
        "--channel-label",
        default="nixpkgs-25.11-darwin",
        help="Human label for the scanned channel (used in report header)",
    )
    return p.parse_args(argv)


def main() -> int:
    args = parse_args(sys.argv[1:])
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"input not found: {input_path}", file=sys.stderr)
        return 2
    agg = aggregate(input_path)

    md = render_markdown(agg, args.channel_label)
    Path(args.out).write_text(md)
    summary = build_summary(agg, args.channel_label)
    Path(args.summary_json).write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    if args.failing_csv:
        write_failing_csv(Path(args.failing_csv), agg["failing_rows"])

    # Brief terminal summary
    b = agg["buckets"]
    print(f"Paths scanned:              {agg['paths_scanned']}")
    print(f"Mach-O slices:              {sum(agg['slices_by_arch'].values())}")
    print(
        f"Page-hash mismatch slices:  {b.get('page_hash_mismatch', 0)}  ({len(agg['pkg_page_hash'])} packages)"
    )
    print(
        f"Other sig-invalid slices:   {b.get('other_sig_invalid', 0)}  ({len(agg['pkg_other_sig'])} packages)"
    )
    print(f"Clean signed:               {b.get('clean', 0)}")
    print(f"Unsigned:                   {b.get('unsigned', 0)}")
    print(f"Noise (non-Mach-O cafebabe, PPC BE, etc.): {b.get('not_real_macho', 0)}")
    print(f"Scanner errors:             {b.get('scanner_error', 0)}")
    print(
        f"\nWrote: {args.out}, {args.summary_json}"
        + (f", {args.failing_csv}" if args.failing_csv else "")
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
