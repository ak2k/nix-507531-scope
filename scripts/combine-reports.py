#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Combine per-channel aggregator outputs into a top-level REPORT.md and
summary.json that cover both darwin channels at once.

Usage:
  combine-reports.py [--channel LABEL:PATH ...] [--out REPORT.md] \\
                     [--summary-json summary.json]

Each --channel argument is a `label:path` pair where `path` points at a
channel's `summary.json` produced by aggregate-scan.py. The top-level
summary.json keeps backward-compatible shortcut fields
(`page_hash_mismatch.slices`, `paths_scanned`, `slices_total`) so
existing shields.io badges on the repo README keep rendering; those
fields now sum across all channels.
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


def sum_by_class(channels: list[dict]) -> dict[str, int]:
    out = {cls: 0 for cls in CLASS_ORDER}
    for ch in channels:
        by_cls = (ch["data"].get("page_hash_mismatch") or {}).get(
            "by_signature_class", {}
        )
        for cls, n in by_cls.items():
            out[cls] = out.get(cls, 0) + n
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

    # ------------------------------------------------------------- headline
    lines.append("## Headline")
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
    lines.append(row("Page-hash-mismatch slices",
                     lambda d: int((d.get("page_hash_mismatch") or {}).get("slices") or 0)))
    lines.append(row("Affected packages",
                     lambda d: int((d.get("page_hash_mismatch") or {}).get("packages") or 0)))
    lines.append("")

    # ----------------------------------------------------- classification x-tab
    lines.append("## Failing slices by signature shape")
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

    # ------------------------------------------------------------- drill-downs
    lines.append("## Drill-downs")
    lines.append("")
    for ch in channels:
        lines.append(
            f"- [{ch['label']} channel report]({ch['label']}/REPORT.md)"
            f" — `{ch['data'].get('channel_label', ch['label'])}`"
        )
    lines.append("- [Scanner source](scripts/scan-darwin-cache.py)")
    lines.append("- [Aggregator source](scripts/aggregate-scan.py)")
    lines.append("")

    return "\n".join(lines) + "\n"


def build_combined_summary(channels: list[dict]) -> dict:
    def s(k: str, ph: str | None = None) -> int:
        """Sum integer field `k` across channels (optionally nested under `ph`)."""
        total = 0
        for ch in channels:
            d = ch["data"]
            if ph:
                d = d.get(ph) or {}
            total += int(d.get(k) or 0)
        return total

    return {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "channels": {ch["label"]: ch["data"] for ch in channels},
        # Backward-compatible shortcut fields. Badges on README.md read these.
        "paths_scanned": s("paths_scanned"),
        "slices_total": s("slices_total"),
        "page_hash_mismatch": {
            "slices":   s("slices", "page_hash_mismatch"),
            "packages": s("packages", "page_hash_mismatch"),
            "by_signature_class": sum_by_class(channels),
        },
    }


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
        help="Per-channel `summary.json` path, e.g. `stable:stable/summary.json`."
        " Repeatable.",
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
    channels: list[dict] = []
    for raw in args.channel:
        label, path = parse_channel_arg(raw)
        if not path.exists():
            print(f"channel {label!r}: summary not found at {path}", file=sys.stderr)
            return 2
        channels.append(load_channel(label, path))

    md = render_markdown(channels)
    Path(args.out).write_text(md)

    summary = build_combined_summary(channels)
    Path(args.summary_json).write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )

    print(
        f"Wrote {args.out} and {args.summary_json} "
        f"({len(channels)} channel(s): "
        f"{', '.join(ch['label'] for ch in channels)})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
