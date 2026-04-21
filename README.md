# nix-507531-scope

[![direct failures](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fak2k%2Fnix-507531-scope%2Fmain%2Fsummary.json&query=%24.union.direct_packages_count&label=direct%20failures&color=red)](REPORT.md#affected-packages)
[![load-time transitive](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fak2k%2Fnix-507531-scope%2Fmain%2Fsummary.json&query=%24.union.load_time_packages_count&label=load-time%20transitive&color=orange)](REPORT.md#affected-packages)
[![build-time dependent](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fak2k%2Fnix-507531-scope%2Fmain%2Fsummary.json&query=%24.union.build_time_packages_default_view_count&label=build-time%20dependent&color=yellow)](REPORT.md#affected-packages)
[![paths scanned](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fak2k%2Fnix-507531-scope%2Fmain%2Fsummary.json&query=%24.paths_scanned&label=paths%20scanned&color=blue)](REPORT.md)
[![Mach-O slices](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fak2k%2Fnix-507531-scope%2Fmain%2Fsummary.json&query=%24.slices_total&label=Mach-O%20slices&color=blue)](REPORT.md)

Daily empirical-prevalence check of the **darwin Mach-O page-hash bug** (NixOS/nixpkgs#507531, fix PR: [NixOS/nix#15638](https://github.com/NixOS/nix/pull/15638)) across the `cache.nixos.org` binary cache.

## What the bug is, briefly

The Nix daemon's `RewritingSink` performs byte-level scratch-path → final-hash substitution inside output binaries *after* they have been code-signed. On darwin, those signed bytes live inside the pages covered by per-page SHA-256 hashes in `LC_CODE_SIGNATURE.CodeDirectory`. The substitution leaves the page hashes stale, and the kernel SIGKILLs the binary at first page-in with `cs_invalid_page`.

Full technical detail: [issue](https://github.com/NixOS/nixpkgs/issues/507531), [fix PR](https://github.com/NixOS/nix/pull/15638), [reproducer](https://github.com/ak2k/nix-507531-repro).

## What this repo does

A daily GitHub Actions workflow walks **both** darwin channels (`nixpkgs-25.11-darwin` stable and `nixpkgs-unstable`) in parallel and reports three types of failure, each with a distinct certainty level:

1. **Direct failures** (`direct-failing.csv`) — cached binary's page hashes are stale; the kernel SIGKILLs on first page-in. Scanner streams every path's NAR from `cache.nixos.org`, parses Mach-O, and recomputes per-page SHA-256 (or SHA-1 when the CD carries it) against stored CodeDirectory hashes. Cross-validated against `rcodesign verify` — 100% agreement.
2. **Load-time transitive** (`load-time-dependents.csv`) — binary is clean itself, but `LC_LOAD_DYLIB` points at a direct-failing dylib; dyld maps the broken lib at process start, kernel SIGKILLs before `main()`. Detected by Mach-O load-command parse.
3. **Build-time dependents** (`build-time-dependents.csv`) — package directly declares a direct-failing package as `buildInputs` / `nativeBuildInputs` / `checkInputs` / `nativeCheckInputs`. If the failing binary is invoked during build, Hydra fails and the package never reaches the cache. Canonical case: direnv (the literal [nixpkgs#507531](https://github.com/NixOS/nixpkgs/issues/507531)). Detected by evaluating the channel's nixpkgs aarch64-darwin set and inspecting drv env vars.

Direct failures are further classified by SuperBlob shape (linker-signed / codesign ad-hoc / ad-hoc + Entitlements / Developer-ID-signed) so the [NixOS/nix#15638](https://github.com/NixOS/nix/pull/15638) fix-up can be evaluated per-class.

Outputs (all auto-committed by the workflow):

| File | What it is |
|---|---|
| [`REPORT.md`](REPORT.md) | Combined cross-channel summary: three-type headline, classification cross-tab, canonical examples, drill-down links |
| [`summary.json`](summary.json) | Combined machine-readable counts (badges, dashboards); back-compat shortcut fields at `$.page_hash_mismatch.slices` etc. sum across channels |
| [`stable/`](stable/) | Per-channel detail for `nixpkgs-25.11-darwin`: `REPORT.md`, `summary.json`, `direct-failing.csv` (Type 1), `load-time-dependents.csv` (Type 2), `build-time-dependents.csv` (Type 3), `verify-summary.md`, `verify-results.jsonl` |
| [`unstable/`](unstable/) | Per-channel detail for `nixpkgs-unstable`: same files as above |

## Current status

The workflow commits fresh outputs on every run. For the latest numbers:

- [**REPORT.md**](REPORT.md) — combined cross-channel view
- [`stable/REPORT.md`](stable/REPORT.md) — stable channel drill-down (tables: signer split, arch breakdown, fat vs thin, failing packages)
- [`unstable/REPORT.md`](unstable/REPORT.md) — unstable channel drill-down
- `stable/verify-summary.md` / `unstable/verify-summary.md` — scanner × `rcodesign` agreement matrix per channel (should always be 100%)

## How it works

```
store-paths.xz (channel)
        │
        ▼
scripts/scan-darwin-cache.py           ← Type 1 + LC_LOAD_DYLIB capture
   · Multiprocess (Pool.imap_unordered) for CPU parallelism
   · Each worker runs asyncio + httpx, streams NARs from cache.nixos.org
   · Decompresses xz/zstd/bz2 inline, probes 4 bytes per file for Mach-O magic
   · Buffers only Mach-O files, parses LC_CODE_SIGNATURE + LC_LOAD_DYLIBs,
     SHA-256 (or SHA-1) per page
   · Writes per-slice results to JSONL, per-path status to SQLite (resumable)
        │
        ▼
scripts/aggregate-scan.py              ← Type 1 report + direct-failing.csv
        │
        ├────▶ scripts/compute-load-time-dependents.py   ← Type 2 CSV + section
        │        · reads JSONL linked_dylibs per slice
        │        · emits load-time-dependents.csv
        │
        ├────▶ scripts/compute-build-time-dependents.py  ← Type 3 CSV + section
        │        · runs nix-eval-jobs against channel's nixpkgs aarch64-darwin
        │        · inspects each drv env for direct-failing store paths
        │        · emits build-time-dependents.csv
        │
        ├────▶ scripts/render-channel-report.py          ← splices Type 2 + 3
        │        into per-channel REPORT.md
        │
        └────▶ scripts/verify-failures.py                ← cross-validate Type 1
                  against rcodesign verify / codesign -v

        │
        ▼
scripts/combine-reports.py             ← top-level REPORT.md + summary.json
                                         across both channels, all three types
```

## Run locally

Any darwin or Linux machine with Nix + `uv` + `rcodesign` (Linux) or `/usr/bin/codesign` (darwin). Type 3 additionally requires `nix-eval-jobs`.

```bash
# Per-channel full scan (~1–2 h stable, ~2–4 h unstable cold, bandwidth-heavy).
for ch_label in stable unstable; do
  case "$ch_label" in
    stable)   URL=https://channels.nixos.org/nixpkgs-25.11-darwin ;;
    unstable) URL=https://channels.nixos.org/nixpkgs-unstable ;;
  esac
  mkdir -p "$ch_label"
  REV=$(curl -sL "$URL/git-revision")

  # Type 1: page-hash scan + classification
  uv run scripts/scan-darwin-cache.py --channel "$URL" \
    --workers 5 --per-worker-concurrency 48 --batch-size 100 \
    --state "$ch_label/full.db" --out "$ch_label/full.jsonl"
  uv run scripts/aggregate-scan.py "$ch_label/full.jsonl" \
    --out "$ch_label/REPORT.md" \
    --summary-json "$ch_label/summary.json" \
    --direct-failing-csv "$ch_label/direct-failing.csv" \
    --channel-label "$ch_label"

  # Type 2: LC_LOAD_DYLIB transitive dependents
  uv run scripts/compute-load-time-dependents.py \
    "$ch_label/full.jsonl" "$ch_label/direct-failing.csv" \
    --out-csv "$ch_label/load-time-dependents.csv" \
    --out-summary "$ch_label/load-time-summary.json" \
    --out-section "$ch_label/load-time-section.md"

  # Type 3: nixpkgs drv input-closure dependents
  uv run scripts/compute-build-time-dependents.py \
    --nixpkgs-flake "github:nixos/nixpkgs/$REV" \
    --direct-failing-csv "$ch_label/direct-failing.csv" \
    --out-csv "$ch_label/build-time-dependents.csv" \
    --out-summary "$ch_label/build-time-summary.json" \
    --out-section "$ch_label/build-time-section.md"

  # Splice Type 2 + 3 sections into the per-channel REPORT
  uv run scripts/render-channel-report.py \
    --report "$ch_label/REPORT.md" \
    --tier2-section "$ch_label/load-time-section.md" \
    --tier3-section "$ch_label/build-time-section.md" \
    --tier2-summary "$ch_label/load-time-summary.json" \
    --tier3-summary "$ch_label/build-time-summary.json"

  # Type 1 cross-validation (scanner vs rcodesign/codesign)
  uv run scripts/verify-failures.py \
    --failing-csv "$ch_label/direct-failing.csv" --jsonl "$ch_label/full.jsonl" \
    --out "$ch_label/verify-results.jsonl" --summary "$ch_label/verify-summary.md"
done

# Merge both channels' summaries into top-level combined view.
uv run scripts/combine-reports.py \
  --channel stable:stable/summary.json \
  --channel unstable:unstable/summary.json \
  --channel-tier2 stable:stable/load-time-summary.json \
  --channel-tier2 unstable:unstable/load-time-summary.json \
  --channel-tier3 stable:stable/build-time-summary.json \
  --channel-tier3 unstable:unstable/build-time-summary.json \
  --out REPORT.md --summary-json summary.json

# Quick smoke test against the first 100 paths (~15 s).
uv run scripts/scan-darwin-cache.py --limit 100 \
  --state smoke.db --out smoke.jsonl
```

## Scope — what each type claims, by evidence level

- **Channels scanned**: both `nixpkgs-25.11-darwin` (stable) and `nixpkgs-unstable`, in parallel every night.
- **Type 1 — direct** (certain per binary). Per-page hash mismatches in the primary CodeDirectory, SHA-256 or SHA-1 as carried by the CD. Detection is agnostic to the `linker-signed` flag — both `ld -adhoc_codesign` (linker-signed shape) and `codesign -f -s -` (codesign-adhoc shape) surface. Structural signature errors (`LC_CODE_SIGNATURE` payload OOB, bad SuperBlob magic, unsupported hash types, etc.) land in a separate `other_sig_invalid` bucket, not the headline.
- **Type 2 — load-time transitive** (certain per binary). Mach-O parse extracts `LC_LOAD_DYLIB` / `LC_LOAD_WEAK_DYLIB` / `LC_REEXPORT_DYLIB` install-names per slice; any slice that is itself clean but references a Type-1 dylib is marked broken. dyld maps every `LC_LOAD_DYLIB` target at process start and the kernel validates the mapped pages, so the failure is deterministic before `main()` runs. `LC_LOAD_UPWARD_DYLIB` is excluded (rare, lazy, ambiguous — would overstate).
- **Type 3 — build-time dependent** (graph-level only). `nix-eval-jobs` enumerates the channel's aarch64-darwin package set; we inspect each drv's env for direct-failing store paths in `buildInputs` / `nativeBuildInputs` / `checkInputs` / `nativeCheckInputs`. The default view is 1-hop and excludes `propagatedBuildInputs` / `propagatedNativeBuildInputs` (propagation threads the input forward; the listed package itself doesn't invoke it). **Membership does not guarantee build failure** — the graph shows the failing binary is on PATH during build, but whether a build phase actually invokes it is not statically determinable. The confirmed case is direnv, whose `nativeCheckInputs = [ fish ]` with a `checkPhase` running `fish ./test/direnv-test.fish` produces the exact failure in nixpkgs#507531's bug report. CSV includes all edge kinds (`in_default_view=true` for tight-filter rows) so readers can inspect propagated edges if they want.
- **State-dependent lower bound on Type 1**: the bug's trigger depends on the Hydra worker's store state at build time (sibling/self outputs present → fallback scratch path → `RewritingSink` fires). Packages with the structural setup for the bug (multi-output, binaries embedding `$out` or sibling store paths — `zsh`, `git`, `bash`, `curl`, etc.) are all at risk even if they don't appear in the current list; they just happened not to trigger the rewrite on their most recent Hydra build.
- **What the scanner correctly ignores as non-Mach-O**: Java `.class` files (share `0xcafebabe` magic with Mach-O fat headers), PPC big-endian legacy binaries, unsigned Mach-O, all Linux ELFs.
- **Out of scope** (reachable only with data sources we don't have):
  - Build-time failures via *undeclared* invocation (a drv that calls `/nix/store/...-fish` via a literal path not in `{build,check}Inputs`). Rare nixpkgs bug and hard to survey without full-tree static analysis.
  - Runtime subprocess failures where the caller binary loads cleanly but its `fork-exec` of a broken binary fails situationally (e.g. a CLI that optionally invokes fish).
  - Hydra build-log evidence of `SIGKILL` / `cs_invalid_page` on packages that fail to build. Those packages never reach the cache, so cache-walking can't find them; systematic enumeration would need Hydra log grep.

## Related

- [NixOS/nix#15638](https://github.com/NixOS/nix/pull/15638) — the fix
- [NixOS/nixpkgs#507531](https://github.com/NixOS/nixpkgs/issues/507531) — the original issue
- [NixOS/nix#6065](https://github.com/NixOS/nix/issues/6065) — the long-running CA-only report
- [ak2k/nix-507531-repro](https://github.com/ak2k/nix-507531-repro) — flake reproducer for the bug (A/B with the patched daemon)

## License

MIT.
