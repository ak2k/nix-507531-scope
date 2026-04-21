#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# ///
"""
Compute Type 2 (load-time transitive) dependents of direct-failing dylibs.

A Mach-O binary that embeds an LC_LOAD_DYLIB / LC_LOAD_WEAK_DYLIB /
LC_REEXPORT_DYLIB pointing at a direct-failing dylib will SIGKILL at
process start: dyld maps every dylib referenced by those commands at
load time, and the kernel validates the mapped pages against the dylib's
CodeDirectory. A broken dylib's pages fail validation, dyld aborts, the
caller never runs main().

This is a strong claim — kernel behavior at process start is deterministic
per slice. It's disjoint from Type 1 (direct failures): a binary whose
OWN hashes are stale fails before dyld even runs its dylib dispatch.
Dependent binaries listed here are clean themselves; they fail because
of what they load.

Inputs:
  - Scan JSONL (per-slice scan data with `linked_dylibs`).
  - `direct-failing.csv` (Type 1 output).

Outputs:
  - `load-time-dependents.csv`: one row per (dependent-binary, failing-dylib) pair.
  - `load-time-summary.json`: aggregate counts for the per-channel + combined
    REPORT.md to consume.

Coverage note: LC_LOAD_UPWARD_DYLIB is NOT included. It's used for
circular-dylib-within-a-framework cases (AppKit ↔ Foundation); no nixpkgs
Mach-O in either channel scan has been observed to use it, and the runtime
semantics differ enough (upward deps are forward-declared, bound lazily)
that conflating with LC_LOAD_DYLIB would overstate.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import posixpath
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Store-path helpers
# ---------------------------------------------------------------------------

_STORE_PATH_RE = re.compile(r"^/nix/store/[a-z0-9]{32}-(.+?)(?:/|$)")

# Strip a trailing `.N[.M[.P...]]` version tail before `.dylib`. macOS dylibs
# ship as `libX.1.2.3.dylib` (actual file) with symlinks `libX.1.dylib` and
# `libX.dylib` in the same directory; LC_LOAD_DYLIB entries typically
# reference the compat-version symlink (`libX.1.dylib`), which our scan
# never sees directly because the scanner reads the versioned file.
# Normalising both sides to the stem + directory makes the match robust.
_DYLIB_VERSION_RE = re.compile(r"(\.\d[\d.]*)?\.dylib$")


def store_path_prefix(path: str) -> str | None:
    """Given `/nix/store/abc-fish-4.2.1/bin/fish`, return
    `/nix/store/abc-fish-4.2.1`. Returns None if not a valid store path.
    """
    parts = path.split("/")
    if len(parts) < 4 or parts[1] != "nix" or parts[2] != "store":
        return None
    return "/".join(parts[:4])


def package_name(store_path: str) -> str | None:
    """Extract the `<name>-<version>` segment from a store path."""
    m = _STORE_PATH_RE.match(store_path + "/")
    return m.group(1) if m else None


def dylib_key(full_path: str) -> tuple[str, str, str] | None:
    """Produce a matchable key for a dylib path:
    (store_prefix, containing_directory, library_stem)

    The stem drops any `.N.M.P.dylib` version tail. Example:
      `/nix/store/abc-ffmpeg/lib/libavcodec.62.11.100.dylib`
        → (`/nix/store/abc-ffmpeg`, `/nix/store/abc-ffmpeg/lib`, `libavcodec`)
      `/nix/store/abc-ffmpeg/lib/libavcodec.62.dylib`    (the symlink)
        → (`/nix/store/abc-ffmpeg`, `/nix/store/abc-ffmpeg/lib`, `libavcodec`)
      `/nix/store/abc-ffmpeg/lib/libavcodec.dylib`       (the unversioned symlink)
        → (`/nix/store/abc-ffmpeg`, `/nix/store/abc-ffmpeg/lib`, `libavcodec`)

    Returns None for non-dylib or non-store-path inputs.
    """
    if not full_path.startswith("/nix/store/") or not full_path.endswith(".dylib"):
        return None
    sp = store_path_prefix(full_path)
    if sp is None:
        return None
    directory = posixpath.dirname(full_path)
    basename = posixpath.basename(full_path)
    stem = _DYLIB_VERSION_RE.sub("", basename)
    return (sp, directory, stem)


# ---------------------------------------------------------------------------
# Failing-dylib seed set
# ---------------------------------------------------------------------------


def load_failing_dylib_seeds(csv_path: Path) -> dict[tuple[str, str, str], dict]:
    """Read direct-failing.csv; keep rows that look like dylibs.

    Returns a dict keyed by `dylib_key()`: a tuple of
    `(store_prefix, containing_directory, library_stem)` that matches
    across the actual versioned file, `lib.N.dylib` compat symlink, and
    `lib.dylib` unversioned symlink. Values include the seed's store path,
    relative path, and package name.

    Non-dylib failing binaries (e.g. `bin/fish`) are dropped — nothing
    LC_LOAD_DYLIBs an executable.
    """
    seeds: dict[tuple[str, str, str], dict] = {}
    with csv_path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            rel = row["path"]
            if not (rel.endswith(".dylib") or "/Frameworks/" in rel):
                continue
            sp = row["store_path"]
            full = f"{sp}/{rel}"
            key = dylib_key(full)
            if key is None:
                continue
            # If two failing dylibs share the same stem (possible if one
            # is itself a symlink the scanner happened to read through —
            # rare), keep the first and record the version-conflict
            # (informational only).
            seeds.setdefault(
                key,
                {
                    "seed_store_path": sp,
                    "seed_path": rel,
                    "seed_full_path": full,
                    "seed_package": package_name(sp) or "unknown",
                    "seed_arch": row.get("arch", ""),
                },
            )
    return seeds


# ---------------------------------------------------------------------------
# JSONL walk
# ---------------------------------------------------------------------------


def iter_slices(jsonl_path: Path):
    """Yield (store_path, slice_dict) for every Mach-O slice in the scan."""
    with jsonl_path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            for s in rec.get("slices", []):
                if s.get("status") != "ok":
                    continue
                yield rec.get("store_path", ""), s


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def compute(
    jsonl_path: Path,
    failing_csv_path: Path,
    out_csv: Path,
    out_summary: Path,
) -> None:
    seeds = load_failing_dylib_seeds(failing_csv_path)
    if not seeds:
        print(
            f"No failing dylibs in {failing_csv_path}; Type 2 will be empty.",
            file=sys.stderr,
        )

    # Direct-failing (path, slice-arch) set: skip these in Type 2 output
    # (they fail at their own page-in, not at dylib dispatch).
    direct_failing_keys: set[tuple[str, str]] = set()
    with failing_csv_path.open() as f:
        for row in csv.DictReader(f):
            direct_failing_keys.add(
                (f"{row['store_path']}/{row['path']}", row.get("arch", ""))
            )

    rows: list[dict] = []
    binary_keys: set[tuple[str, str, str]] = set()  # (sp, path, arch)
    dependent_packages: set[str] = set()
    binaries_by_seed_pkg: dict[str, int] = {}

    for store_path, s in iter_slices(jsonl_path):
        rel = s.get("path", "")
        arch = s.get("arch", "")
        full_path = f"{store_path}/{rel}"
        # Type 2 is only for binaries whose own hashes are clean. A slice
        # that is itself direct-failing is covered by Type 1; listing it
        # here would double-count.
        if (full_path, arch) in direct_failing_keys:
            continue
        linked = s.get("linked_dylibs") or []
        for dep in linked:
            key = dylib_key(dep)
            if key is None:
                continue
            seed = seeds.get(key)
            if seed is None:
                continue
            rows.append(
                {
                    "store_path": store_path,
                    "path": rel,
                    "arch": arch,
                    "size": s.get("size", 0),
                    "linked_dylib": dep,
                    "seed_store_path": seed["seed_store_path"],
                    "seed_path": seed["seed_path"],
                    "seed_package": seed["seed_package"],
                    "seed_arch": seed["seed_arch"],
                }
            )
            binary_keys.add((store_path, rel, arch))
            pkg = package_name(store_path)
            if pkg:
                dependent_packages.add(pkg)
            binaries_by_seed_pkg[seed["seed_package"]] = (
                binaries_by_seed_pkg.get(seed["seed_package"], 0) + 1
            )

    # Write CSV
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="") as f:
        if rows:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        else:
            # Preserve the schema even when empty, so downstream consumers
            # don't fall over parsing a zero-byte file.
            f.write(
                "store_path,path,arch,size,linked_dylib,"
                "seed_store_path,seed_path,seed_package,seed_arch\n"
            )

    # Build per-dependent → seed-packages map for the flat Affected-
    # packages table in combine-reports.py. Each dependent package may
    # link multiple failing dylibs; dedupe to unique seed package names.
    dependents_by_package: dict[str, list[str]] = {}
    for row in rows:
        pkg = package_name(row["store_path"])
        seed_pkg = row["seed_package"]
        if pkg:
            dependents_by_package.setdefault(pkg, [])
            if seed_pkg not in dependents_by_package[pkg]:
                dependents_by_package[pkg].append(seed_pkg)
    for k in dependents_by_package:
        dependents_by_package[k].sort()

    # Write summary JSON
    summary = {
        "total_rows": len(rows),
        "distinct_binaries": len(binary_keys),
        "distinct_dependent_packages": len(dependent_packages),
        "distinct_seed_dylibs": len(seeds),
        "by_seed_package": dict(
            sorted(binaries_by_seed_pkg.items(), key=lambda kv: -kv[1])
        ),
        "dependent_packages": sorted(dependent_packages),
        "dependents_by_package": dict(sorted(dependents_by_package.items())),
    }
    with out_summary.open("w") as f:
        json.dump(summary, f, indent=2, sort_keys=False)
        f.write("\n")

    print(
        f"Type 2: {summary['distinct_binaries']} distinct binaries across "
        f"{summary['distinct_dependent_packages']} packages link at least one "
        f"of {summary['distinct_seed_dylibs']} failing dylibs "
        f"({summary['total_rows']} total (binary, failing-dylib) pairs)",
        file=sys.stderr,
    )


def render_section(summary_path: Path, csv_path: Path, out_path: Path) -> None:
    """Emit a markdown fragment ready for inclusion in REPORT.md."""
    summary = json.loads(summary_path.read_text())
    lines: list[str] = []
    lines.append("## Load-time transitive broken binaries")
    lines.append("")
    lines.append(
        "Binaries whose own code signatures are valid but which dyld cannot "
        "map at process start because their `LC_LOAD_DYLIB` / "
        "`LC_LOAD_WEAK_DYLIB` / `LC_REEXPORT_DYLIB` points at a direct-failing "
        "dylib. These SIGKILL at load, before `main()` runs — deterministic "
        "per slice."
    )
    lines.append("")
    lines.append("| Metric | Count |")
    lines.append("|---|---:|")
    lines.append(
        f"| Binaries that link at least one failing dylib | {summary['distinct_binaries']} |"
    )
    lines.append(
        f"| Distinct packages containing such binaries | {summary['distinct_dependent_packages']} |"
    )
    lines.append(
        f"| Failing dylibs that serve as seeds | {summary['distinct_seed_dylibs']} |"
    )
    lines.append(
        f"| Total (binary, failing-dylib) pairs | {summary['total_rows']} |"
    )
    lines.append("")

    if summary.get("by_seed_package"):
        lines.append("Top failing dylibs by number of downstream binaries:")
        lines.append("")
        lines.append("| Seed package | Downstream binaries |")
        lines.append("|---|---:|")
        for pkg, count in list(summary["by_seed_package"].items())[:10]:
            lines.append(f"| `{pkg}` | {count} |")
        lines.append("")

    if summary.get("dependent_packages"):
        lines.append(
            f"Dependent packages ({len(summary['dependent_packages'])}): "
            + ", ".join(f"`{p}`" for p in summary["dependent_packages"][:40])
            + (
                ", …"
                if len(summary["dependent_packages"]) > 40
                else ""
            )
        )
        lines.append("")

    lines.append(
        f"Full detail: [`{csv_path.name}`]({csv_path.name}) "
        "(one row per `(binary, linked_failing_dylib)` pair)."
    )
    lines.append("")
    out_path.write_text("\n".join(lines))


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    p.add_argument("jsonl", type=Path, help="Scan JSONL from scan-darwin-cache.py")
    p.add_argument(
        "direct_failing_csv",
        type=Path,
        help="direct-failing.csv from aggregate-scan.py",
    )
    p.add_argument(
        "--out-csv",
        type=Path,
        default=Path("load-time-dependents.csv"),
    )
    p.add_argument(
        "--out-summary",
        type=Path,
        default=Path("load-time-summary.json"),
    )
    p.add_argument(
        "--out-section",
        type=Path,
        default=None,
        help="Write a markdown fragment for inclusion in REPORT.md.",
    )
    args = p.parse_args(argv)
    compute(args.jsonl, args.direct_failing_csv, args.out_csv, args.out_summary)
    if args.out_section:
        render_section(args.out_summary, args.out_csv, args.out_section)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
