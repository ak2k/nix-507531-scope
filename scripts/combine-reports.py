#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Combine per-channel aggregator outputs into a top-level REPORT.md and
summary.json that cover both darwin channels at once.

Usage:
  combine-reports.py [--channel LABEL:PATH ...] [--out REPORT.md] \\
                     [--summary-json summary.json] \\
                     [--channel-tier2 LABEL:PATH ...] \\
                     [--channel-tier3 LABEL:PATH ...]

`--channel` points at a channel's `summary.json` produced by
aggregate-scan.py (Tier 1). `--channel-tier2` and `--channel-tier3` are
optional per-channel Tier-2 / Tier-3 summary paths; when provided, the
headline table and drill-down links are extended with those tiers.

The top-level summary.json keeps backward-compatible shortcut fields
(`page_hash_mismatch.slices`, `paths_scanned`, `slices_total`) so
existing shields.io badges on the repo README keep rendering.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path


CLASS_ORDER = ["L", "C2", "B7-empty", "B7-real", "unknown"]
CLASS_DESC = {
    "L":        "linker-signed ad-hoc, no CMS slot",
    "C2":       "codesign ad-hoc, empty 8 B CMS wrapper",
    "B7-empty": "ad-hoc with Entitlements + empty CMS wrapper",
    "B7-real":  "Developer-ID-signed (non-empty CMS payload)",
    "unknown":  "unknown (pre-enrichment scanner output)",
}


def load_channel(label: str, path: Path) -> dict:
    return {"label": label, "data": json.loads(path.read_text())}


def load_tier_summary(path: Path | None) -> dict | None:
    if path is None or not path.exists():
        return None
    return json.loads(path.read_text())


def sum_by_class(channels: list[dict]) -> dict[str, int]:
    out = {cls: 0 for cls in CLASS_ORDER}
    for ch in channels:
        by_cls = (ch["data"].get("page_hash_mismatch") or {}).get(
            "by_signature_class", {}
        )
        for cls, n in by_cls.items():
            out[cls] = out.get(cls, 0) + n
    return out


import re as _re

# Strip the `-unstable-YYYY-MM-DD` tail that nixpkgs appends to
# packages pinned to a post-release commit (e.g. `batman-2024.08.24-
# unstable-2025-02-22` → `batman-2024.08.24`). The suffix is packaging
# metadata — the nixpkgs pin date — not a semantic version. Keeping it
# in the flat table makes rows unscannable; the full form is preserved
# in the per-tier CSV drill-downs for anyone who needs it.
_UNSTABLE_SUFFIX = _re.compile(r"-unstable-\d{4}-\d{2}-\d{2}$")


def _strip_unstable_suffix(pkg: str) -> str:
    return _UNSTABLE_SUFFIX.sub("", pkg)


def render_affected_packages_rows(channels: list[dict]) -> list[dict]:
    """Flat alphabetical (package, tier) row list across channels.

    Keys emitted per row: `package`, `tier` (one of "direct" / "load-time
    transitive" / "build-time transitive"), `channels` (comma-joined),
    `seeded_by` (comma-joined seed package names, or "—" for direct).

    Package names are normalised: the `-unstable-YYYY-MM-DD` pin-date tail
    is stripped so readers scan `batman-2024.08.24` rather than the raw
    nixpkgs form.
    """
    # Triple-keyed accumulator: {(package, tier): {"channels": set[str],
    # "seeds": set[str]}}
    entries: dict[tuple[str, str], dict] = {}

    def bump(pkg: str, tier: str, channel: str, seeds: list[str]) -> None:
        pkg = _strip_unstable_suffix(pkg)
        key = (pkg, tier)
        e = entries.setdefault(key, {"channels": set(), "seeds": set()})
        e["channels"].add(channel)
        for s in seeds:
            if s:
                e["seeds"].add(_strip_unstable_suffix(s))

    for ch in channels:
        label = ch["label"]
        data = ch["data"]

        # Tier 1 (direct): `page_hash_mismatch.packages_list`.
        for pkg in (data.get("page_hash_mismatch") or {}).get("packages_list", []):
            bump(pkg, "direct", label, [])

        # Tier 2 (load-time): `tier2_summary.dependents_by_package`.
        t2 = ch.get("tier2_summary") or {}
        for pkg, seeds in (t2.get("dependents_by_package") or {}).items():
            bump(pkg, "load-time transitive", label, list(seeds))

        # Tier 3 (build-time, default view only): `tier3_summary.
        # dependents_by_pkg_default_view`.
        t3 = ch.get("tier3_summary") or {}
        for pkg, seeds in (t3.get("dependents_by_pkg_default_view") or {}).items():
            bump(pkg, "build-time transitive", label, list(seeds))

    # Order: alphabetical by package (case-insensitive), then
    # direct-before-load-time-before-build-time so multi-tier packages
    # read naturally top-to-bottom.
    TIER_ORDER = {"direct": 0, "load-time transitive": 1, "build-time transitive": 2}
    ordered = sorted(
        entries.items(),
        key=lambda kv: (kv[0][0].lower(), TIER_ORDER.get(kv[0][1], 99)),
    )

    out: list[dict] = []
    for (pkg, tier), e in ordered:
        channels_str = ", ".join(sorted(e["channels"]))
        seeds_str = (
            ", ".join(f"`{s}`" for s in sorted(e["seeds"])) if e["seeds"] else "—"
        )
        out.append(
            {
                "package": pkg,
                "tier": tier,
                "channels": channels_str,
                "seeded_by": seeds_str,
            }
        )
    return out


def render_markdown(channels: list[dict]) -> str:
    lines: list[str] = []
    lines.append("# NixOS/nixpkgs#507531 darwin Mach-O page-hash scope")
    lines.append("")
    lines.append(
        f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}"
    )
    lines.append("")
    lines.append(
        "Daily scan across both darwin channels of the "
        "[NixOS/nixpkgs#507531](https://github.com/NixOS/nixpkgs/issues/507531) "
        "page-hash bug. Fix PR: "
        "[NixOS/nix#15638](https://github.com/NixOS/nix/pull/15638)."
    )
    lines.append("")

    # ----------------------------------------------------- three-tier headline
    lines.append("## Blast-radius tiers")
    lines.append("")
    lines.append(
        "The bug's effect surfaces in three types of failure. Each tier's "
        "membership and how we detect it:"
    )
    lines.append("")
    lines.append(
        "1. **Direct failure** — cached binary's page hashes are stale; "
        "kernel SIGKILLs on first page-in. Detected by SHA-256/SHA-1 "
        "recomputation against every Mach-O slice in `cache.nixos.org`. "
        "Certain per binary."
    )
    lines.append(
        "2. **Load-time transitive** — binary is clean itself, but an "
        "`LC_LOAD_DYLIB` points at a direct-failing dylib; dyld maps the "
        "broken lib at process start, kernel SIGKILLs before `main()`. "
        "Detected by Mach-O load-command parse. Certain per binary."
    )
    lines.append(
        "3. **Build-time dependent** — package's nix expression directly "
        "declares a direct-failing package as `buildInputs` / "
        "`nativeBuildInputs` / `checkInputs` / `nativeCheckInputs`. "
        "Detected by evaluating the channel's nixpkgs aarch64-darwin "
        "package set and inspecting drv env vars. Graph-level only — "
        "not every listed package actually invokes the failing binary "
        "during build. Default view excludes `propagatedBuildInputs` "
        "(propagation threads the input forward, it isn't invoked)."
    )
    lines.append("")

    # Two-channel × three-tier table
    header_cells = ["| Tier"] + [f" {ch['label']} " for ch in channels] + [" Union |"]
    header = "|".join(header_cells)
    sep = "|---|" + "---:|" * (len(channels) + 1)
    lines.append(header)
    lines.append(sep)

    # Tier 1
    t1_counts = [
        int((ch["data"].get("page_hash_mismatch") or {}).get("slices") or 0)
        for ch in channels
    ]
    t1_pkgs = [
        int((ch["data"].get("page_hash_mismatch") or {}).get("packages") or 0)
        for ch in channels
    ]
    t1_union_pkgs = len(
        set().union(
            *[
                set((ch["data"].get("page_hash_mismatch") or {}).get("packages_list") or [])
                for ch in channels
            ]
        )
    ) or sum(t1_pkgs)  # fallback when packages_list not populated
    lines.append(
        "| **1. Direct failure** (slices) |"
        + "|".join(f" {n} " for n in t1_counts)
        + f"| {sum(t1_counts)} |"
    )
    lines.append(
        "| &emsp;↳ distinct packages |"
        + "|".join(f" {n} " for n in t1_pkgs)
        + f"| {t1_union_pkgs} |"
    )

    # Tier 2
    t2_counts_bins = []
    t2_counts_pkgs = []
    t2_pkgs_lists = []
    for ch in channels:
        t2 = ch.get("tier2_summary") or {}
        t2_counts_bins.append(int(t2.get("distinct_binaries") or 0))
        t2_counts_pkgs.append(int(t2.get("distinct_dependent_packages") or 0))
        t2_pkgs_lists.append(set(t2.get("dependent_packages") or []))
    t2_union_pkgs = len(set().union(*t2_pkgs_lists)) if any(t2_pkgs_lists) else sum(t2_counts_pkgs)
    if any(t2_counts_bins) or any(t2_counts_pkgs):
        lines.append(
            "| **2. Load-time transitive** (binaries) |"
            + "|".join(f" {n} " for n in t2_counts_bins)
            + f"| {sum(t2_counts_bins)} |"
        )
        lines.append(
            "| &emsp;↳ distinct packages |"
            + "|".join(f" {n} " for n in t2_counts_pkgs)
            + f"| {t2_union_pkgs} |"
        )

    # Tier 3
    t3_counts = []
    t3_pkgs_lists = []
    for ch in channels:
        t3 = ch.get("tier3_summary") or {}
        t3_counts.append(int(t3.get("distinct_dependent_attrs_default_view") or 0))
        t3_pkgs_lists.append(set(t3.get("dependent_attrs_default_view") or []))
    t3_union_pkgs = len(set().union(*t3_pkgs_lists)) if any(t3_pkgs_lists) else sum(t3_counts)
    if any(t3_counts):
        lines.append(
            "| **3. Build-time dependent** (packages, default view) |"
            + "|".join(f" {n} " for n in t3_counts)
            + f"| {t3_union_pkgs} |"
        )
    lines.append("")

    # Canonical-example block — anchored to specific reports.
    lines.append("## Canonical examples")
    lines.append("")
    lines.append(
        "- **Tier 1 (direct)**: `fish-4.2.1/bin/fish` SIGKILLs on launch on "
        "darwin. End-user reports in "
        "[nixpkgs#208951](https://github.com/NixOS/nixpkgs/issues/208951)."
    )
    lines.append(
        "- **Tier 2 (load-time transitive)**: any Mach-O whose "
        "`LC_LOAD_DYLIB` points at e.g. "
        "`ffmpeg-8.0-lib/lib/libavformat.61.dylib` fails at process start — "
        "deterministic from kernel page-in semantics."
    )
    lines.append(
        "- **Tier 3 (build-time dependent)**: `direnv` declares "
        "`nativeCheckInputs = [ fish ]` with `doCheck = true`; its "
        "`checkPhase` runs `fish ./test/direnv-test.fish`, fish SIGKILLs, "
        "direnv fails to build on Hydra. Origin of "
        "[nixpkgs#507531](https://github.com/NixOS/nixpkgs/issues/507531)."
    )
    lines.append("")

    # ------------------------------------------------------------- headline
    lines.append("## Scan totals")
    lines.append("")
    header = "| |" + "".join(f" {ch['label']} |" for ch in channels)
    sep = "|---|" + "---:|" * len(channels)
    lines.append(header)
    lines.append(sep)

    def row(label: str, extract) -> str:
        vals = [extract(ch["data"]) for ch in channels]
        return "| " + label + " | " + " | ".join(f"{v:,}" if isinstance(v, int) else str(v) for v in vals) + " |"

    lines.append(row("Channel label",       lambda d: d.get("channel_label", "—")))
    lines.append(row("Paths scanned",       lambda d: int(d.get("paths_scanned") or 0)))
    lines.append(row("Mach-O slices",       lambda d: int(d.get("slices_total") or 0)))
    lines.append("")

    # ----------------------------------------------------- classification x-tab
    lines.append("## Direct-failure slices by signature shape")
    lines.append("")
    lines.append(
        "Classes `linker-signed`, `codesign ad-hoc`, and `ad-hoc with "
        "Entitlements + empty CMS wrapper` are fixed in place by "
        "`fixupMachoPageHashes` (NixOS/nix#15638). The "
        "`Developer-ID-signed` class is skipped with a warning: the "
        "embedded PKCS#7 payload commits to the `CodeDirectory`'s hash, "
        "and the signing identity is not recoverable from inside the "
        "daemon."
    )
    lines.append("")
    header = "| Signature shape |" + "".join(f" {ch['label']} |" for ch in channels) + " Total |"
    sep = "|---|" + "---:|" * (len(channels) + 1)
    lines.append(header)
    lines.append(sep)

    present_classes = set()
    for ch in channels:
        by_cls = (ch["data"].get("page_hash_mismatch") or {}).get(
            "by_signature_class", {}
        )
        present_classes.update(by_cls.keys())

    rows = [cls for cls in CLASS_ORDER if cls in present_classes]
    totals = [0] * len(channels)
    for cls in rows:
        per_ch = []
        for i, ch in enumerate(channels):
            by_cls = (ch["data"].get("page_hash_mismatch") or {}).get(
                "by_signature_class", {}
            )
            n = int(by_cls.get(cls, 0))
            per_ch.append(n)
            totals[i] += n
        row_total = sum(per_ch)
        lines.append(
            "| "
            + CLASS_DESC.get(cls, cls)
            + " | "
            + " | ".join(str(n) for n in per_ch)
            + f" | {row_total} |"
        )
    grand_total = sum(totals)
    lines.append(
        "| **Total** | "
        + " | ".join(f"**{n}**" for n in totals)
        + f" | **{grand_total}** |"
    )
    lines.append("")

    # ------------------------------------------------------ affected packages
    lines.append("## Affected packages")
    lines.append("")
    lines.append(
        "Flat alphabetical list of every package implicated by any tier, "
        "across both channels. A package may appear on multiple rows if it "
        "hits more than one tier (e.g. `ffmpeg-8.0-lib` is directly broken "
        "AND its dylibs are load-time-linked by other packages)."
    )
    lines.append("")
    lines.append("| Package | Type | Channel(s) | Seeded by |")
    lines.append("|---|---|---|---|")
    for row in render_affected_packages_rows(channels):
        lines.append(
            f"| `{row['package']}` | {row['tier']} | {row['channels']} | "
            f"{row['seeded_by']} |"
        )
    lines.append("")

    # ------------------------------------------------------------- drill-downs
    lines.append("## Drill-downs")
    lines.append("")
    for ch in channels:
        lines.append(
            f"- [{ch['label']} channel report]({ch['label']}/REPORT.md)"
            f" — `{ch['data'].get('channel_label', ch['label'])}`"
        )
    lines.append("- [Scanner source](scripts/scan-darwin-cache.py)")
    lines.append("- [Tier 2 analyzer](scripts/compute-load-time-dependents.py)")
    lines.append("- [Tier 3 analyzer](scripts/compute-build-time-dependents.py)")
    lines.append("")

    return "\n".join(lines) + "\n"


def build_combined_summary(channels: list[dict]) -> dict:
    def s(k: str, ph: str | None = None) -> int:
        total = 0
        for ch in channels:
            d = ch["data"]
            if ph:
                d = d.get(ph) or {}
            total += int(d.get(k) or 0)
        return total

    # Union sets across channels for per-tier cross-channel totals.
    # Packages that fail on BOTH channels count once in the union.
    t1_union: set[str] = set()
    t2_union: set[str] = set()
    t3_union: set[str] = set()
    for ch in channels:
        t1 = (ch["data"].get("page_hash_mismatch") or {})
        t2 = ch.get("tier2_summary") or {}
        t3 = ch.get("tier3_summary") or {}
        t1_union.update(t1.get("packages_list") or [])
        t2_union.update(t2.get("dependent_packages") or [])
        t3_union.update(t3.get("dependent_attrs_default_view") or [])

    out = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "channels": {},
        "paths_scanned": s("paths_scanned"),
        "slices_total": s("slices_total"),
        "page_hash_mismatch": {
            # Slices are per-scan-unique across channels, so sum is correct.
            "slices":   s("slices", "page_hash_mismatch"),
            # Packages MUST be deduped — the same package can fail in both
            # channels. The old sum-across-channels number double-counted
            # those and misled the README badge.
            "packages": len(t1_union),
            "by_signature_class": sum_by_class(channels),
        },
    }
    for ch in channels:
        block = dict(ch["data"])
        if ch.get("tier2_summary"):
            block["load_time_transitive"] = ch["tier2_summary"]
        if ch.get("tier3_summary"):
            block["build_time_dependents"] = ch["tier3_summary"]
        out["channels"][ch["label"]] = block

    # Deduped union counts + lists per tier. Badges read the *_count
    # scalars; the *_packages lists are for tooling that wants names.
    out["union"] = {
        "direct_packages": sorted(t1_union),
        "direct_packages_count": len(t1_union),
        "load_time_packages": sorted(t2_union),
        "load_time_packages_count": len(t2_union),
        "build_time_packages_default_view": sorted(t3_union),
        "build_time_packages_default_view_count": len(t3_union),
    }

    return out


def parse_channel_arg(raw: str) -> tuple[str, Path]:
    if ":" not in raw:
        raise ValueError(f"--channel argument must be LABEL:PATH, got {raw!r}")
    label, _, path = raw.partition(":")
    return label, Path(path)


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--channel",
        action="append",
        required=True,
        metavar="LABEL:PATH",
        help="Per-channel Tier-1 `summary.json` path. Repeatable.",
    )
    p.add_argument(
        "--channel-tier2",
        action="append",
        default=[],
        metavar="LABEL:PATH",
        help="Per-channel Tier-2 (load-time) summary JSON path. Repeatable.",
    )
    p.add_argument(
        "--channel-tier3",
        action="append",
        default=[],
        metavar="LABEL:PATH",
        help="Per-channel Tier-3 (build-time) summary JSON path. Repeatable.",
    )
    p.add_argument("--out", default="REPORT.md", help="Combined markdown report path")
    p.add_argument(
        "--summary-json",
        default="summary.json",
        help="Combined JSON summary path",
    )
    return p.parse_args(argv)


def main() -> int:
    args = parse_args(sys.argv[1:])

    # Index Tier 2 / Tier 3 paths by channel label.
    t2_map = {
        parse_channel_arg(raw)[0]: parse_channel_arg(raw)[1]
        for raw in args.channel_tier2
    }
    t3_map = {
        parse_channel_arg(raw)[0]: parse_channel_arg(raw)[1]
        for raw in args.channel_tier3
    }

    channels: list[dict] = []
    for raw in args.channel:
        label, path = parse_channel_arg(raw)
        if not path.exists():
            print(f"channel {label!r}: summary not found at {path}", file=sys.stderr)
            return 2
        ch = load_channel(label, path)
        ch["tier2_summary"] = load_tier_summary(t2_map.get(label))
        ch["tier3_summary"] = load_tier_summary(t3_map.get(label))
        channels.append(ch)

    md = render_markdown(channels)
    Path(args.out).write_text(md)

    summary = build_combined_summary(channels)
    Path(args.summary_json).write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )

    tier_coverage = [
        f"t2={'y' if ch['tier2_summary'] else 'n'}"
        f" t3={'y' if ch['tier3_summary'] else 'n'}"
        for ch in channels
    ]
    print(
        f"Wrote {args.out} and {args.summary_json} "
        f"({len(channels)} channel(s): "
        + ", ".join(
            f"{ch['label']}[{cov}]"
            for ch, cov in zip(channels, tier_coverage)
        )
        + ")"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
