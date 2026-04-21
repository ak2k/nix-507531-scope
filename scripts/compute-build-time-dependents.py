#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx[http2]>=0.27"]
# ///
"""
Compute Type 3 (build-time) dependents of direct-failing packages.

A package P is a "build-time dependent" if P's derivation directly declares
a direct-failing package as a build input — i.e. that failing package is
in P's `buildInputs`, `nativeBuildInputs`, `checkInputs`, or
`nativeCheckInputs` (the edges that put the failing binary on PATH during
P's build). If any of P's build phases invokes the failing binary, the
kernel SIGKILLs it on page-in and P's Hydra build fails. Since failed
builds never reach cache.nixos.org, these packages are invisible to the
cache scan.

**Default filter is 1-hop and excludes propagated-only edges.** We report
packages whose own nix expression declares the failing package as a build
input. Multi-hop transitive closures and `propagatedBuildInputs`-only
edges are both dropped from the default — a package deep in a toolchain
graph that happens to have fish in its transitive closure almost certainly
doesn't invoke fish during its own build, so including it would overstate.
The canonical 1-hop case is direnv (nixpkgs#507531): direnv's
`nativeCheckInputs = [ fish ]; doCheck = true;` — direnv's checkPhase runs
`fish ./test/direnv-test.fish`, fish SIGKILLs, direnv fails to build.

Inputs:
  - `--nixpkgs-flake <flakeref>`: the channel's nixpkgs revision as a flake
    reference (e.g. `github:nixos/nixpkgs/d7de041fe507`).
  - `--direct-failing-csv <path>`: Type 1 output from aggregate-scan.py.

Outputs:
  - `build-time-dependents.csv`: one row per (dependent package, edge kind,
    failing seed) tuple.
  - `build-time-summary.json`: aggregate counts.

Requires: `nix` CLI + `nix-eval-jobs` in PATH. Evaluation is metadata-only
(no building), so any platform works. On `ubuntu-latest` with a warm
cache, evaluating `legacyPackages.aarch64-darwin` takes 2-3 minutes.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
from pathlib import Path


# ---------------------------------------------------------------------------
# Edge kinds and default filter
# ---------------------------------------------------------------------------

# Env vars on a derivation corresponding to declared build inputs.
# Order matters for edge-kind attribution: if a seed path appears in
# multiple env vars, the first match wins (most direct edge).
EDGE_KINDS = [
    "nativeCheckInputs",
    "checkInputs",
    "nativeBuildInputs",
    "buildInputs",
    "propagatedNativeBuildInputs",
    "propagatedBuildInputs",
]

DEFAULT_TIGHT_EDGE_KINDS = {
    "nativeCheckInputs",
    "checkInputs",
    "nativeBuildInputs",
    "buildInputs",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_STORE_PATH_RE = re.compile(r"^/nix/store/[a-z0-9]{32}-(.+)$")


def pkg_name_of(store_path: str) -> str:
    """`/nix/store/abc-fish-4.2.1` → `fish-4.2.1`. Best-effort; never raises."""
    m = _STORE_PATH_RE.match(store_path)
    return m.group(1) if m else store_path


def ensure_tool(name: str) -> None:
    if not shutil.which(name):
        sys.exit(f"required tool not found on PATH: {name}")


# ---------------------------------------------------------------------------
# Nix evaluation — enumerate all darwin packages as (attr, drvPath, outputs)
# ---------------------------------------------------------------------------


def eval_darwin_package_set(
    flake: str, workers: int = 8, max_memory_mb: int = 4096
) -> list[dict]:
    """Run nix-eval-jobs against `${flake}#legacyPackages.aarch64-darwin`.

    Returns a list of {attr, drvPath, outputs, inputDrvs} dicts. Attrs
    that failed evaluation (unsupported system, broken, etc.) are dropped.

    `--show-input-drvs` lets us enumerate each attr's direct drv-level
    inputs in one streaming pass. Combined with the `outputs` field, we
    can locally determine which attrs transitively depend on any failing
    seed BEFORE calling `nix derivation show` on anything — the target-
    count for the follow-up step shrinks from ~66k to a few hundred.

    `max_memory_mb` is the per-worker memory ceiling passed to
    nix-eval-jobs as `--max-memory-size`. Total ceiling = workers ×
    max_memory_mb. Tune down on small runners.
    """
    # Note: `--no-instantiate` is incompatible with `--show-input-drvs`.
    # nix-eval-jobs requires drv files on disk to enumerate inputDrvs.
    # Cache footprint is therefore identical to the pre-hybrid approach
    # (~66k .drv files), but wall-clock time drops because the downstream
    # `nix derivation show` step only runs on ~500 candidates instead of
    # the full package set.
    cmd = [
        "nix-eval-jobs",
        "--flake",
        f"{flake}#legacyPackages.aarch64-darwin",
        "--workers",
        str(workers),
        "--max-memory-size",
        str(max_memory_mb),
        "--show-input-drvs",
        # Impure mode: allow nixpkgs' check-meta.nix to read NIXPKGS_ALLOW_*
        # env vars via builtins.getEnv. Without this, setting e.g.
        # NIXPKGS_ALLOW_UNFREE=1 in the environment has no effect — the
        # evaluator stays in pure mode and still rejects unfree packages
        # with 'has an unfree license' errors. We set UNFREE + INSECURE
        # from the workflow; BROKEN and UNSUPPORTED_SYSTEM are left off
        # intentionally (broken won't build regardless; unsupported-
        # system would evaluate ~30k linux-only packages on darwin that
        # can't build on darwin — pure noise).
        "--impure",
    ]
    print(
        f"evaluating {flake}#legacyPackages.aarch64-darwin with {workers} workers",
        file=sys.stderr,
    )
    # nix-eval-jobs writes progress/warnings to stderr. We drain it in a
    # daemon thread to (a) avoid the two-PIPE deadlock (if stderr fills
    # the kernel buffer, nix-eval-jobs blocks on write and so do its
    # workers), AND (b) surface nix-eval-jobs' own progress output to
    # the user so the eval phase isn't a black box.
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    def _drain_stderr(stream) -> None:
        try:
            for ln in stream:
                # Forward to our stderr verbatim; nix-eval-jobs emits
                # its own concise progress ("waiting for worker …",
                # "evaluation error …") which is exactly what the user
                # wants to see.
                sys.stderr.write(ln)
                sys.stderr.flush()
        except Exception:
            pass

    drainer = threading.Thread(
        target=_drain_stderr, args=(proc.stderr,), daemon=True
    )
    drainer.start()

    rows: list[dict] = []
    n_errors = 0
    assert proc.stdout is not None
    for line in proc.stdout:
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if rec.get("error"):
            n_errors += 1
            continue
        drv = rec.get("drvPath")
        attr = rec.get("attr") or ".".join(rec.get("attrPath", []))
        outs = rec.get("outputs", {}) or {}
        input_drvs = rec.get("inputDrvs", {}) or {}
        if not drv or not attr:
            continue
        rows.append(
            {
                "attr": attr,
                "drvPath": drv,
                "outputs": outs,
                "inputDrvs": input_drvs,
            }
        )
        # Cheap streaming progress signal. nix-eval-jobs itself already
        # emits a per-worker ticker on stderr, but this guarantees at
        # least one line of forward-progress evidence even on silent
        # workers or buffered-stderr environments.
        if len(rows) % 2000 == 0:
            print(
                f"  evaluated {len(rows)} attrs so far ({n_errors} eval errors)",
                file=sys.stderr,
            )
    rc = proc.wait()
    drainer.join(timeout=5)
    if rc != 0:
        print(
            f"nix-eval-jobs exited rc={rc}; {len(rows)} successful attrs, "
            f"{n_errors} errors",
            file=sys.stderr,
        )
    else:
        print(
            f"evaluated: {len(rows)} successful attrs, {n_errors} eval errors",
            file=sys.stderr,
        )
    return rows


# ---------------------------------------------------------------------------
# Nix derivation show — bulk fetch env + inputDrvs
# ---------------------------------------------------------------------------


def chunks(seq: list, n: int):
    for i in range(0, len(seq), n):
        yield seq[i : i + n]


def _merge_derivation_json(raw: dict, out: dict[str, dict]) -> None:
    """Merge `nix derivation show` JSON into `out` keyed by full drv path.

    Nix 2.19+ wraps output as `{"derivations": {...}, "version": N}` where
    the inner keys may be either full `/nix/store/...drv` paths or bare
    basenames depending on the version. Normalise to full paths.
    """
    derivs = raw.get("derivations") if isinstance(raw, dict) else None
    if not isinstance(derivs, dict):
        # Older nix: raw is the flat derivation map directly.
        derivs = raw
    for k, v in derivs.items():
        if k.startswith("/nix/store/"):
            out[k] = v
        else:
            out[f"/nix/store/{k}"] = v


def bulk_derivation_show(
    drv_paths: list[str], chunk_size: int = 500
) -> dict[str, dict]:
    """Call `nix derivation show <drv>...` in chunks. Returns merged JSON
    keyed by full drv path.

    `nix derivation show` wraps output in `{"derivations": {...}, "version": N}`.
    MAY exit non-zero if one drv in the batch fails, but stdout still
    contains valid JSON for successes — we parse regardless of exit code.
    """
    out: dict[str, dict] = {}
    total = len(drv_paths)
    done = 0
    for batch in chunks(drv_paths, chunk_size):
        cmd = ["nix", "derivation", "show"] + batch
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=300
            )
        except subprocess.TimeoutExpired:
            done += len(batch)
            print(
                f"  derivation show: {done}/{total} (batch timed out, skipped)",
                file=sys.stderr,
            )
            continue

        # Parse whatever valid JSON we got, regardless of exit code.
        parsed = False
        if result.stdout:
            try:
                _merge_derivation_json(json.loads(result.stdout), out)
                parsed = True
            except json.JSONDecodeError:
                pass

        if not parsed and result.returncode != 0:
            # Batch output was unparseable and the call failed. Fall back
            # to per-drv calls to salvage what we can.
            for single in batch:
                try:
                    r = subprocess.run(
                        ["nix", "derivation", "show", single],
                        capture_output=True,
                        text=True,
                        timeout=60,
                    )
                    if r.stdout:
                        try:
                            _merge_derivation_json(json.loads(r.stdout), out)
                        except json.JSONDecodeError:
                            pass
                except subprocess.TimeoutExpired:
                    pass
            done += len(batch)
            print(
                f"  derivation show: {done}/{total} (batch failed, per-drv fallback)",
                file=sys.stderr,
            )
            continue

        done += len(batch)
        if done % 5000 == 0 or done == total:
            print(f"  derivation show: {done}/{total}", file=sys.stderr)
    return out


# ---------------------------------------------------------------------------
# Edge classification
# ---------------------------------------------------------------------------


def classify_edge(env: dict[str, str], seed_store_path: str) -> str | None:
    """Return the edge kind by which env references seed_store_path, or None.

    Each env var may contain multiple space-separated store paths. We test
    for the seed path as a whitespace-bounded substring to avoid false
    matches on path prefixes (e.g. `fish-4.2.1` vs `fish-4.2.1-doc`).
    """
    for kind in EDGE_KINDS:
        val = env.get(kind)
        if not val:
            continue
        # Paths in the env are space-separated. A boundary-safe check
        # avoids matching `fish-4.2.1` inside `fish-4.2.1-doc`.
        tokens = val.split()
        if seed_store_path in tokens:
            return kind
    return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def compute(
    flake: str,
    failing_csv: Path,
    out_csv: Path,
    out_summary: Path,
    eval_workers: int,
    nix_eval_max_memory: int,
    include_propagated: bool,
) -> None:
    ensure_tool("nix")
    ensure_tool("nix-eval-jobs")

    # --- seeds ---------------------------------------------------------------
    # Failing STORE PATHS (from direct-failing.csv). We dedupe; a store path
    # with multiple failing slices counts once for Type 3.
    failing_store_paths: set[str] = set()
    with failing_csv.open() as f:
        for row in csv.DictReader(f):
            failing_store_paths.add(row["store_path"])
    print(
        f"direct-failing: {len(failing_store_paths)} distinct store paths",
        file=sys.stderr,
    )

    # --- package set ---------------------------------------------------------
    pkgs = eval_darwin_package_set(
        flake, workers=eval_workers, max_memory_mb=nix_eval_max_memory
    )
    if not pkgs:
        sys.exit("nix-eval-jobs returned no packages; cannot compute Type 3")

    # Index output store paths → (attr, drvPath). Every output of every attr
    # is a potential seed target.
    output_to_attr: dict[str, tuple[str, str]] = {}
    # Reverse index: drvPath → primary output store path. Used to resolve
    # seed store paths back to their drv paths so we can match against
    # each attr's inputDrvs graph (which references drv paths, not outs).
    drv_to_output: dict[str, str] = {}
    for p in pkgs:
        for out_name, out_path in (p.get("outputs") or {}).items():
            if isinstance(out_path, str) and out_path:
                output_to_attr[out_path] = (p["attr"], p["drvPath"])
                drv_to_output[p["drvPath"]] = out_path

    # Resolve failing store paths → (attr, drvPath) for reporting; some
    # failing paths may not correspond to any eval-jobs attr (e.g. a package
    # is darwin-reachable via a transitive path but isn't a top-level attr).
    # Those unknown seeds are still valid seeds for edge matching — we just
    # can't label them with an attr. The store path is the definitive
    # identity.
    seed_label: dict[str, str] = {
        sp: output_to_attr[sp][0] for sp in failing_store_paths if sp in output_to_attr
    }
    unlabeled = [sp for sp in failing_store_paths if sp not in output_to_attr]
    if unlabeled:
        print(
            f"  {len(unlabeled)} failing store paths have no corresponding "
            f"top-level attr (still used as seeds; labelled by path)",
            file=sys.stderr,
        )

    # --- resolve failing store paths → failing drv paths --------------------
    # For the hybrid candidate filter we need failing seeds as drv paths,
    # because nix-eval-jobs' `inputDrvs` field keys by drv path, not output
    # store path. Invert drv_to_output to find each seed's drv.
    seed_drvs: set[str] = set()
    for sp in failing_store_paths:
        for drv, out in drv_to_output.items():
            if out == sp:
                seed_drvs.add(drv)
                break
    print(
        f"  resolved {len(seed_drvs)}/{len(failing_store_paths)} seed store "
        f"paths to drv paths",
        file=sys.stderr,
    )

    # --- candidate filter ----------------------------------------------------
    # An attr is a Type-3 candidate if any of its direct inputDrvs is a
    # seed drv. We check this locally using the inputDrvs field already
    # captured by `--show-input-drvs`; no nix subprocess calls yet.
    candidates: list[dict] = []
    for p in pkgs:
        input_drvs = p.get("inputDrvs") or {}
        # Across nix-eval-jobs versions, inputDrvs is either a dict
        # `{drvPath: [output_names]}` or a plain list of drv paths.
        if isinstance(input_drvs, dict):
            inputs = set(input_drvs.keys())
        elif isinstance(input_drvs, list):
            inputs = set(input_drvs)
        else:
            inputs = set()
        matched = inputs & seed_drvs
        if matched:
            candidates.append({**p, "matched_seed_drvs": sorted(matched)})
    print(
        f"  {len(candidates)} Type-3 candidates (attrs with ≥1 inputDrv in the "
        f"seed-drv set); running targeted derivation show on each",
        file=sys.stderr,
    )

    # --- targeted derivation show on candidates only ------------------------
    candidate_drvs = sorted({c["drvPath"] for c in candidates})
    drv_json = bulk_derivation_show(candidate_drvs) if candidate_drvs else {}

    # --- edge matching -------------------------------------------------------
    # For each candidate attr, inspect its env vars for any failing seed.
    edge_filter = (
        set(EDGE_KINDS) if include_propagated else DEFAULT_TIGHT_EDGE_KINDS
    )
    rows: list[dict] = []
    dependent_attrs: set[str] = set()
    by_edge_kind: dict[str, int] = {}
    by_seed: dict[str, int] = {}

    # Iterate only over candidates (attrs that referenced a seed drv in
    # step 1); they're the only ones that can possibly match a seed env-
    # var check. Non-candidates are guaranteed no-match.
    for p in candidates:
        drv = p["drvPath"]
        attr = p["attr"]
        dinfo = drv_json.get(drv)
        if not dinfo:
            continue
        env = dinfo.get("env", {}) or {}
        # Only check the seeds the candidate pre-matched (in step 1) —
        # further narrows the inner loop from 19 seeds to ~1-3.
        for seed_drv in p.get("matched_seed_drvs", []):
            seed_sp = drv_to_output.get(seed_drv, "")
            if not seed_sp or seed_sp not in failing_store_paths:
                continue
            edge = classify_edge(env, seed_sp)
            if edge is None:
                continue
            if edge not in edge_filter:
                # Row still emitted (so CSV is complete) but marked as
                # propagated-only; default readers can filter it out.
                pass
            rows.append(
                {
                    "dependent_attr": attr,
                    "dependent_drv": drv,
                    "dependent_pkg": pkg_name_of(
                        dinfo.get("name", attr)
                    ),  # best-effort
                    "seed_store_path": seed_sp,
                    "seed_attr": seed_label.get(seed_sp, ""),
                    "seed_pkg": pkg_name_of(seed_sp),
                    "edge_kind": edge,
                    "in_default_view": edge in edge_filter,
                }
            )
            if edge in edge_filter:
                dependent_attrs.add(attr)
                by_edge_kind[edge] = by_edge_kind.get(edge, 0) + 1
                by_seed[seed_sp] = by_seed.get(seed_sp, 0) + 1

    # --- outputs -------------------------------------------------------------
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="") as f:
        fieldnames = [
            "dependent_attr",
            "dependent_drv",
            "dependent_pkg",
            "seed_store_path",
            "seed_attr",
            "seed_pkg",
            "edge_kind",
            "in_default_view",
        ]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    # Build per-dependent package lookup for the flat Affected-packages
    # table in combine-reports.py. For each default-view row, record the
    # dependent's versioned package name (from the drv name attr — more
    # table-friendly than the bare attr), together with the seed package
    # names it references. Multi-hit dedupes seeds per dependent.
    dependents_by_pkg_default_view: dict[str, list[str]] = {}
    for r in rows:
        if not r["in_default_view"]:
            continue
        dep_pkg = r["dependent_pkg"] or r["dependent_attr"]
        seed_pkg = r["seed_pkg"]
        dependents_by_pkg_default_view.setdefault(dep_pkg, [])
        if seed_pkg and seed_pkg not in dependents_by_pkg_default_view[dep_pkg]:
            dependents_by_pkg_default_view[dep_pkg].append(seed_pkg)
    for k in dependents_by_pkg_default_view:
        dependents_by_pkg_default_view[k].sort()

    summary = {
        "total_rows": len(rows),
        "rows_in_default_view": sum(1 for r in rows if r["in_default_view"]),
        "distinct_dependent_attrs_default_view": len(dependent_attrs),
        "distinct_seeds": len(failing_store_paths),
        "edge_filter_default": sorted(DEFAULT_TIGHT_EDGE_KINDS),
        "by_edge_kind_default_view": dict(
            sorted(by_edge_kind.items(), key=lambda kv: -kv[1])
        ),
        "by_seed_default_view": dict(
            sorted(
                ((pkg_name_of(k), v) for k, v in by_seed.items()),
                key=lambda kv: -kv[1],
            )
        ),
        "dependent_attrs_default_view": sorted(dependent_attrs),
        "dependents_by_pkg_default_view": dict(
            sorted(dependents_by_pkg_default_view.items())
        ),
    }
    with out_summary.open("w") as f:
        json.dump(summary, f, indent=2, sort_keys=False)
        f.write("\n")

    print(
        f"Type 3 (default view, 1-hop, build/check edges only): "
        f"{summary['distinct_dependent_attrs_default_view']} packages directly "
        f"declare at least one failing seed as a build/check input "
        f"({summary['rows_in_default_view']} rows)",
        file=sys.stderr,
    )
    print(
        f"Type 3 (all edges including propagated): {len(rows)} total rows",
        file=sys.stderr,
    )


def render_section(summary_path: Path, csv_path: Path, out_path: Path) -> None:
    """Emit a markdown fragment ready for inclusion in REPORT.md."""
    summary = json.loads(summary_path.read_text())
    lines: list[str] = []
    lines.append("## Build-time dependents")
    lines.append("")
    lines.append(
        "Packages whose nix expression **directly declares** a direct-failing "
        "package as `buildInputs`, `nativeBuildInputs`, `checkInputs`, or "
        "`nativeCheckInputs` (1-hop). If the failing binary is invoked during "
        "the package's build phase, Hydra fails and the package never reaches "
        "the cache. This is a graph-level relationship: whether each listed "
        "package actually invokes the failing binary during build is not "
        "statically determinable. The canonical confirmed case is direnv — "
        "its `nativeCheckInputs = [ fish ]` with a `checkPhase` running "
        "`fish ./test/direnv-test.fish`, origin of "
        "[nixpkgs#507531](https://github.com/NixOS/nixpkgs/issues/507531)."
    )
    lines.append("")
    lines.append(
        "Default view excludes `propagatedBuildInputs` / "
        "`propagatedNativeBuildInputs` edges (propagation threads the input "
        "forward; the listed package itself doesn't invoke it). The CSV "
        "includes all edge kinds for manual inspection."
    )
    lines.append("")
    lines.append("| Metric | Count |")
    lines.append("|---|---:|")
    lines.append(
        f"| Packages with failing seeds in declared build/check inputs "
        f"(default view) | {summary['distinct_dependent_attrs_default_view']} |"
    )
    lines.append(
        f"| Total direct-edge rows (default view) | "
        f"{summary['rows_in_default_view']} |"
    )
    lines.append(
        f"| Total rows including propagated edges | {summary['total_rows']} |"
    )
    lines.append(
        f"| Distinct failing seeds | {summary['distinct_seeds']} |"
    )
    lines.append("")

    if summary.get("by_edge_kind_default_view"):
        lines.append("Edges by kind (default view only):")
        lines.append("")
        lines.append("| Edge kind | Count |")
        lines.append("|---|---:|")
        for kind, count in summary["by_edge_kind_default_view"].items():
            lines.append(f"| `{kind}` | {count} |")
        lines.append("")

    if summary.get("by_seed_default_view"):
        lines.append("Top seed packages by downstream dependent count:")
        lines.append("")
        lines.append("| Seed package | Downstream dependents |")
        lines.append("|---|---:|")
        for pkg, count in list(summary["by_seed_default_view"].items())[:10]:
            lines.append(f"| `{pkg}` | {count} |")
        lines.append("")

    if summary.get("dependent_attrs_default_view"):
        lines.append(
            f"Dependent packages ({len(summary['dependent_attrs_default_view'])}): "
            + ", ".join(
                f"`{p}`" for p in summary["dependent_attrs_default_view"][:40]
            )
            + (
                ", …"
                if len(summary["dependent_attrs_default_view"]) > 40
                else ""
            )
        )
        lines.append("")

    lines.append(
        f"Full detail: [`{csv_path.name}`]({csv_path.name}) "
        "(one row per `(dependent, edge_kind, seed)` tuple; "
        "`in_default_view=true` marks default-filter rows)."
    )
    lines.append("")
    out_path.write_text("\n".join(lines))


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    p.add_argument(
        "--nixpkgs-flake",
        required=True,
        help="Flake reference for the channel's nixpkgs revision, e.g. "
        "'github:nixos/nixpkgs/d7de041fe507'.",
    )
    p.add_argument(
        "--direct-failing-csv",
        type=Path,
        required=True,
        help="direct-failing.csv produced by aggregate-scan.py.",
    )
    p.add_argument(
        "--out-csv",
        type=Path,
        default=Path("build-time-dependents.csv"),
    )
    p.add_argument(
        "--out-summary",
        type=Path,
        default=Path("build-time-summary.json"),
    )
    p.add_argument("--eval-workers", type=int, default=8)
    p.add_argument(
        "--nix-eval-max-memory",
        type=int,
        default=4096,
        help="Per-worker --max-memory-size passed to nix-eval-jobs, in MB. "
        "Total ceiling = eval-workers × nix-eval-max-memory. Default 4096 "
        "(4 GB). Tune down on 2-vCPU / ≤8 GB runners (e.g. 3072 on "
        "ubuntu-latest with 2 workers = 6 GB ceiling).",
    )
    p.add_argument(
        "--include-propagated",
        action="store_true",
        help="Include propagatedBuildInputs / propagatedNativeBuildInputs in "
        "the default-view count. Rows are always in the CSV either way.",
    )
    p.add_argument(
        "--out-section",
        type=Path,
        default=None,
        help="Write a markdown fragment for inclusion in REPORT.md.",
    )
    args = p.parse_args(argv)
    compute(
        flake=args.nixpkgs_flake,
        failing_csv=args.direct_failing_csv,
        out_csv=args.out_csv,
        out_summary=args.out_summary,
        eval_workers=args.eval_workers,
        nix_eval_max_memory=args.nix_eval_max_memory,
        include_propagated=args.include_propagated,
    )
    if args.out_section:
        render_section(args.out_summary, args.out_csv, args.out_section)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
