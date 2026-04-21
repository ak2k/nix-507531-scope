#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# ///
"""
Assemble the final per-channel REPORT.md by splicing Type 2 and Type 3
markdown fragments into the Type 1 report produced by aggregate-scan.py.

Fragments are inserted immediately before the "## Methodology" heading,
preserving the existing structure. If a fragment file is missing, its
section is simply omitted (useful when Type 3 eval is skipped, e.g. during
local iteration).

Also extends the top summary table to include per-type counts when the
tier summary JSONs are available.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


METHODOLOGY_HEADING = "## Methodology"


def insert_before_methodology(report: str, fragments: list[str]) -> str:
    """Insert each fragment (joined by blank lines) before the Methodology heading."""
    if not fragments:
        return report
    payload = "\n".join(f.rstrip() for f in fragments) + "\n\n"
    idx = report.find(METHODOLOGY_HEADING)
    if idx == -1:
        # no methodology heading — just append
        return report.rstrip() + "\n\n" + payload
    return report[:idx] + payload + report[idx:]


def extend_top_summary_table(
    report: str,
    tier2: dict | None,
    tier3: dict | None,
) -> str:
    """Add two rows to the top "Summary" table with Type 2/3 headline counts.

    The Type 1 table ends with an explicit count row (e.g. 'Other signature-
    invalid (slices) | N'). We insert after that block; if we can't find a
    clean anchor, leave the report alone.
    """
    if not (tier2 or tier3):
        return report

    extra_rows: list[str] = []
    if tier2:
        extra_rows.append(
            f"| Type 2 — binaries linking a failing dylib | "
            f"{tier2.get('distinct_binaries', 0)} |"
        )
        extra_rows.append(
            f"| Type 2 — distinct packages | "
            f"{tier2.get('distinct_dependent_packages', 0)} |"
        )
    if tier3:
        extra_rows.append(
            f"| Type 3 — packages directly declaring a failing build input "
            f"(default view) | {tier3.get('distinct_dependent_attrs_default_view', 0)} |"
        )

    if not extra_rows:
        return report

    # Anchor: last row of the Type-1 summary table, which begins with
    # "| Other signature-invalid" (hardcoded shape).
    lines = report.splitlines(keepends=True)
    anchor_idx = None
    for i, line in enumerate(lines):
        if line.startswith("| Other signature-invalid"):
            # Include this line + any immediately-following continuation row.
            anchor_idx = i
    if anchor_idx is None:
        return report

    # Insert extra rows after the last anchor line.
    insertion = "".join(r + "\n" for r in extra_rows)
    return "".join(lines[: anchor_idx + 1]) + insertion + "".join(lines[anchor_idx + 1 :])


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    p.add_argument("--report", type=Path, required=True, help="Input Type-1 REPORT.md (edited in place).")
    p.add_argument(
        "--tier2-section",
        type=Path,
        default=None,
        help="Type 2 markdown fragment (from compute-load-time-dependents.py --out-section).",
    )
    p.add_argument(
        "--tier3-section",
        type=Path,
        default=None,
        help="Type 3 markdown fragment (from compute-build-time-dependents.py --out-section).",
    )
    p.add_argument(
        "--tier2-summary",
        type=Path,
        default=None,
        help="Type 2 summary JSON, used to extend the top-summary table.",
    )
    p.add_argument(
        "--tier3-summary",
        type=Path,
        default=None,
        help="Type 3 summary JSON, used to extend the top-summary table.",
    )
    args = p.parse_args(argv)

    if not args.report.exists():
        sys.exit(f"report not found: {args.report}")

    report = args.report.read_text()

    fragments: list[str] = []
    if args.tier2_section and args.tier2_section.exists():
        fragments.append(args.tier2_section.read_text())
    if args.tier3_section and args.tier3_section.exists():
        fragments.append(args.tier3_section.read_text())

    tier2 = (
        json.loads(args.tier2_summary.read_text())
        if (args.tier2_summary and args.tier2_summary.exists())
        else None
    )
    tier3 = (
        json.loads(args.tier3_summary.read_text())
        if (args.tier3_summary and args.tier3_summary.exists())
        else None
    )

    report = extend_top_summary_table(report, tier2, tier3)
    report = insert_before_methodology(report, fragments)
    args.report.write_text(report)
    print(
        f"rendered {args.report} "
        f"(+{len(fragments)} tier sections, "
        f"tier2_counts={'yes' if tier2 else 'no'}, "
        f"tier3_counts={'yes' if tier3 else 'no'})",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
