#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""
Emit the synthetic `release` channel's path list.

Runs `nix-eval-jobs` against `<flake>#legacyPackages.aarch64-darwin`,
streams its JSON output, and writes deduplicated `/nix/store/...` paths
(every named output of every successful attr) to stdout, one per line.

Paired with scan-darwin-cache.py's `--paths-file` flag: the resulting
text file substitutes for the `store-paths.xz` that channels.nixos.org
publishes for the existing `darwin` and `unstable` channels.

Why this script exists: `release-25.11` is a branch ref, not a Hydra-
published channel slug. cache.nixos.org does hold the binaries Hydra
built for that branch (they're how `nh switch -u` works for users who
follow `release-25.11` directly), but no `store-paths.xz` enumerates
them. Evaluating the rev's `legacyPackages.aarch64-darwin` package set
gives the same enumeration that `nixpkgs-25.11-darwin/store-paths.xz`
would have given if Hydra published a darwin-flavoured channel for
release-25.11 tip.

Parallelism mirrors compute-build-time-dependents.py: `--workers` /
`--max-memory-size` are the same nix-eval-jobs knobs the Tier 3 step
already exercises. ubuntu-latest 2 vCPU runners default to `--workers 2`
to match the core count without overcommitting.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import threading


def eval_paths(flake: str, workers: int, max_memory_mb: int) -> set[str]:
    """Run nix-eval-jobs and return the set of `/nix/store/...` output
    paths across every output of every successfully-evaluated attr.
    Errored attrs (broken/insecure/unsupported-system) are silently
    dropped — same policy as compute-build-time-dependents.py."""
    cmd = [
        "nix-eval-jobs",
        "--flake",
        f"{flake}#legacyPackages.aarch64-darwin",
        "--workers",
        str(workers),
        "--max-memory-size",
        str(max_memory_mb),
        # `--impure` so nixpkgs' check-meta.nix can read NIXPKGS_ALLOW_*
        # env vars. Caller sets UNFREE + INSECURE; BROKEN /
        # UNSUPPORTED_SYSTEM intentionally left off (same rationale as
        # compute-build-time-dependents.py).
        "--impure",
    ]
    print(
        f"evaluating {flake}#legacyPackages.aarch64-darwin with {workers} workers",
        file=sys.stderr,
    )

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    # Drain stderr on a daemon thread so nix-eval-jobs workers don't
    # block on a full kernel pipe buffer (same trap as Tier 3).
    def _drain_stderr(stream) -> None:
        try:
            for ln in stream:
                sys.stderr.write(ln)
                sys.stderr.flush()
        except Exception:
            pass

    drainer = threading.Thread(
        target=_drain_stderr, args=(proc.stderr,), daemon=True
    )
    drainer.start()

    paths: set[str] = set()
    n_attrs = 0
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
        outs = rec.get("outputs") or {}
        if not isinstance(outs, dict):
            continue
        n_attrs += 1
        for v in outs.values():
            if isinstance(v, str) and v.startswith("/nix/store/"):
                paths.add(v)
        if n_attrs % 2000 == 0:
            print(
                f"  evaluated {n_attrs} attrs, {len(paths)} unique paths "
                f"({n_errors} eval errors)",
                file=sys.stderr,
            )

    rc = proc.wait()
    drainer.join(timeout=5)
    print(
        f"eval done: rc={rc}, {n_attrs} attrs, {len(paths)} unique paths, "
        f"{n_errors} eval errors",
        file=sys.stderr,
    )
    if rc != 0 and not paths:
        # Distinguish "Hydra has nothing built for this rev yet" (where
        # paths is non-empty but cache.nixos.org returns 404 for many)
        # from "evaluator catastrophically failed before producing any
        # output". Only the latter should fail the job.
        sys.exit(f"nix-eval-jobs failed catastrophically (rc={rc}, 0 paths)")
    return paths


def main() -> int:
    p = argparse.ArgumentParser(
        description=(
            "Evaluate `legacyPackages.aarch64-darwin` against a flake and "
            "emit one /nix/store path per line on stdout. Used to seed "
            "scan-darwin-cache.py's --paths-file for the synthetic "
            "`release` channel."
        )
    )
    p.add_argument(
        "--flake",
        required=True,
        help="Flake ref to evaluate, e.g. 'github:NixOS/nixpkgs/<rev>'",
    )
    p.add_argument(
        "--workers",
        type=int,
        default=2,
        help="nix-eval-jobs --workers (default: 2, sized for ubuntu-latest 2 vCPU)",
    )
    p.add_argument(
        "--max-memory-size",
        type=int,
        default=3072,
        help="nix-eval-jobs --max-memory-size in MB per worker (default: 3072)",
    )
    args = p.parse_args()

    paths = eval_paths(args.flake, args.workers, args.max_memory_size)
    for path in sorted(paths):
        print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
