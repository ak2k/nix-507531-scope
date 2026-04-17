#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# ///
"""
Cross-validate every scanner-flagged failing slice against an independent
Mach-O signature verifier (`codesign -v` on darwin, `rcodesign verify` on
linux — both check page hashes in LC_CODE_SIGNATURE and report mismatch).

Reads the aggregator's `failing.csv` plus the "other_sig_invalid" slices
from the JSONL (not in failing.csv by design), realizes each unique store
path from cache.nixos.org via nix-store -r, runs the verifier on each
flagged file, and records agreement.

Default verifier is auto-detected:
  - darwin  → /usr/bin/codesign -v
  - linux   → rcodesign verify
Override with --verifier.

Output: verify-results.jsonl (one row per verified slice)
        verify-summary.md    (agreement matrix + any disagreements)
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path


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
                continue  # that's in failing.csv
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


def realize(store_path: str, cache_url: str) -> tuple[bool, str]:
    """Return (ok, message)."""
    cmd = [
        "nix-store",
        "-r",
        store_path,
        "--option",
        "substituters",
        cache_url,
        "--option",
        "trusted-public-keys",
        "cache.nixos.org-1:6NCHdD59X431o0gWypbMrAURkbJ16ZPMQFGspcDShjY=",
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    except subprocess.TimeoutExpired:
        return False, "timeout"
    if r.returncode != 0:
        return False, (r.stderr or r.stdout).strip().splitlines()[-1] if (
            r.stderr or r.stdout
        ).strip() else "realize failed"
    return True, ""


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
    p.add_argument("--failing-csv", default="./failing.csv")
    p.add_argument("--jsonl", default="./full.jsonl")
    p.add_argument("--out", default="./verify-results.jsonl")
    p.add_argument("--summary", default="./verify-summary.md")
    p.add_argument("--cache", default="https://cache.nixos.org")
    p.add_argument(
        "--verifier",
        nargs="+",
        default=None,
        help="Verifier command + flags (default: auto-detected by platform). "
        "E.g. --verifier /usr/bin/codesign -v  OR  --verifier rcodesign verify",
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

    print(
        f"verifying {len(rows)} slices from {len({r['store_path'] for r in rows})} unique packages",
        file=sys.stderr,
    )

    # Realize each unique store path first (cache the downloads)
    unique_paths = sorted({r["store_path"] for r in rows})
    realized_ok: set[str] = set()
    print("realizing packages...", file=sys.stderr)
    for i, sp in enumerate(unique_paths, 1):
        ok, msg = realize(sp, args.cache)
        if ok:
            realized_ok.add(sp)
        print(
            f"  [{i}/{len(unique_paths)}] {'OK ' if ok else 'FAIL'} {sp}  {msg if not ok else ''}",
            file=sys.stderr,
        )

    # Run verifier on each row
    agreement = {
        "agree_fail": 0,
        "disagree_scanner_false_positive": 0,
        "realize_failed": 0,
    }
    results: list[dict] = []
    print(f"\nverifying with {' '.join(verifier)} ...", file=sys.stderr)
    for i, r in enumerate(rows, 1):
        sp = r["store_path"]
        full_path = f"{sp}/{r['path']}"
        if sp not in realized_ok:
            r2 = {
                **r,
                "verifier_exit": None,
                "verifier_message": "realize failed",
                "verdict": "realize_failed",
            }
            agreement["realize_failed"] += 1
            results.append(r2)
            continue
        if not os.path.exists(full_path):
            r2 = {
                **r,
                "verifier_exit": None,
                "verifier_message": "file not found in realized store path",
                "verdict": "file_missing",
            }
            agreement["realize_failed"] += 1
            results.append(r2)
            continue
        code, msg = run_verifier(verifier, full_path)
        if code != 0:
            verdict = "agree_fail"
            agreement["agree_fail"] += 1
        else:
            verdict = "disagree_scanner_false_positive"
            agreement["disagree_scanner_false_positive"] += 1
        r2 = {**r, "verifier_exit": code, "verifier_message": msg, "verdict": verdict}
        results.append(r2)
        print(
            f"  [{i}/{len(rows)}] {verdict}  {r['path']}  (rc={code})", file=sys.stderr
        )

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
    md.append("Verified every slice the scanner flagged as failing against an")
    md.append(f"independent signature verifier: `{' '.join(verifier)}`.")
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
        f"| Realize failed (could not fetch package from cache) | {agreement['realize_failed']} |"
    )
    md.append(f"| **Total slices verified** | **{total}** |")
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
    else:
        md.append(
            "No disagreements: every scanner-flagged failure was independently confirmed by the verifier."
        )
        md.append("")

    Path(args.summary).write_text("\n".join(md) + "\n")

    print(f"\nResults: {args.out}", file=sys.stderr)
    print(f"Summary: {args.summary}", file=sys.stderr)
    print(
        f"\nAgreement: {agreement['agree_fail']}/{total} scanner failures confirmed by codesign -v"
    )
    if disagreements:
        print(f"WARNING: {len(disagreements)} disagreements — see {args.summary}")
    return 0 if not disagreements else 1


if __name__ == "__main__":
    sys.exit(main())
