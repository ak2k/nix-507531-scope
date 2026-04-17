# nix-507531-scope

Daily empirical-prevalence check of the **darwin Mach-O page-hash bug** (nixpkgs#507531, fix PR: [NixOS/nix#15638](https://github.com/NixOS/nix/pull/15638)) across the `cache.nixos.org` binary cache.

## What the bug is, briefly

The Nix daemon's `RewritingSink` performs byte-level scratch-path → final-hash substitution inside output binaries *after* they have been code-signed. On darwin, those signed bytes live inside the pages covered by per-page SHA-256 hashes in `LC_CODE_SIGNATURE.CodeDirectory`. The substitution leaves the page hashes stale, and the kernel SIGKILLs the binary at first page-in with `cs_invalid_page`.

Full technical detail: [issue](https://github.com/NixOS/nixpkgs/issues/507531), [fix PR](https://github.com/NixOS/nix/pull/15638), [reproducer](https://github.com/ak2k/nix-507531-repro).

## What this repo does

A daily GitHub Actions workflow walks the `nixpkgs-25.11-darwin` channel's `store-paths.xz` list, streams every path's NAR from `cache.nixos.org`, and for every Mach-O file it finds, recomputes per-page SHA-256 and compares against the stored CodeDirectory hashes. Any mismatch is the bug.

Results are cross-validated by running `rcodesign verify` on every scanner-flagged slice — zero disagreements in the baseline run means the scanner's findings match Apple's reference semantics exactly.

Outputs (all auto-committed by the workflow):

| File | What it is |
|---|---|
| [`REPORT.md`](REPORT.md) | Human-readable summary of the current scan |
| [`summary.json`](summary.json) | Machine-readable bucket counts for dashboards / badges / trend tracking |
| [`failing.csv`](failing.csv) | One row per Mach-O slice with a page-hash mismatch |
| [`verify-summary.md`](verify-summary.md) | rcodesign cross-validation agreement matrix |
| [`verify-results.jsonl`](verify-results.jsonl) | Per-slice verifier exit code + message |

## Baseline

First full scan of `nixpkgs-25.11-darwin @ 76410a99a2c5` (hydra eval 1824540):

- **172,961 paths scanned**, 223,604 Mach-O slices parsed
- **65 page-hash mismatches across 19 distinct packages** — every one independently confirmed by `rcodesign verify`
- **0 scanner false positives** (66/66 agreement with rcodesign)
- Signer split: 22 linker-signed (`ld -adhoc_codesign`) + 43 codesign-signed (`codesign -f -s -`) — the bug hits both signing paths
- Fat-binary split: 42 of 65 failures (65%) are inside universal/fat Mach-O containers; the current draft of the fix in nix#15638 handles only thin Mach-O and would leave these unfixed
- Prominent affected packages: `swift-5.10.1` (11 + 11 slices across two outputs), `swift-5.10.1-lib` (7+7), `ffmpeg-8.0-lib` (7), `fish-4.2.1` (the flagship case), `libtorch-2.9.0`, `Agda-2.8.0`, `tailwindcss_4-4.1.18`, `httptoolkit-1.24.4`, `avalonia-ilspy`, `esy-0.8.0`, `shogihome-1.27.0`, `arion-0.2.2.0`

Full details in [REPORT.md](REPORT.md).

## How it works

```
store-paths.xz (channel)
        │
        ▼
scripts/scan-darwin-cache.py
   · Multiprocess (Pool.imap_unordered) for CPU parallelism
   · Each worker runs asyncio + httpx, streams NARs from cache.nixos.org
   · Decompresses xz/zstd/bz2 inline, probes 4 bytes per file for Mach-O magic
   · Buffers only Mach-O files, parses LC_CODE_SIGNATURE, SHA-256s each page
   · Writes per-slice results to JSONL, per-path status to SQLite (resumable)
        │
        ▼
scripts/aggregate-scan.py
   · Classifies each slice: page_hash_mismatch / other_sig_invalid /
     clean / unsigned / not_real_macho / scanner_error
   · Emits REPORT.md (factual tables only, no editorial claims),
     summary.json, failing.csv
        │
        ▼
scripts/verify-failures.py
   · Realizes each affected store path from cache.nixos.org via nix-store -r
   · Runs rcodesign verify (Linux) or codesign -v (darwin) on every
     scanner-flagged slice
   · Emits verify-summary.md: agreement matrix + any disagreements
   · Fails the workflow if scanner ↔ verifier ever disagree
```

## Run locally

Any darwin or Linux machine with Nix + `uv` + `rcodesign` (Linux) or `/usr/bin/codesign` (darwin):

```bash
# Full channel scan (~45-60 min cold, bandwidth-heavy — ~1 TB for the seed).
uv run scripts/scan-darwin-cache.py \
  --channel https://channels.nixos.org/nixpkgs-25.11-darwin \
  --workers 3 --per-worker-concurrency 24 --batch-size 100 \
  --state full.db --out full.jsonl

# Quick smoke test against the first 100 paths (~15 s).
uv run scripts/scan-darwin-cache.py --limit 100 \
  --state smoke.db --out smoke.jsonl

# Aggregate the JSONL into the reports.
uv run scripts/aggregate-scan.py full.jsonl \
  --out REPORT.md --summary-json summary.json --failing-csv failing.csv

# Cross-validate every flagged failure against Apple codesign semantics.
# Needs nix profile install nixpkgs#rcodesign on Linux.
uv run scripts/verify-failures.py \
  --failing-csv failing.csv --jsonl full.jsonl \
  --out verify-results.jsonl --summary verify-summary.md
```

## Scope notes

- **Only `nixpkgs-25.11-darwin`** for now. `nixpkgs-unstable` would also be interesting but is multi-system (contains Linux paths), and there is no darwin-only unstable channel at `channels.nixos.org`. A future version could either (a) filter `nixpkgs-unstable` via the `Deriver` system field in narinfos, or (b) pull a darwin-only path list from the `nixpkgs-unstable-aarch64-darwin` hydra jobset (aarch64-only, misses x86_64-darwin). Adding this isn't blocked on any missing code — just a decision about which path.
- **What the scanner catches**: page-hash mismatches in the SHA-256 CodeDirectory, plus structural signature errors (`LC_CODE_SIGNATURE` payload OOB, etc.). Detection is conservative and agnostic to the `linker-signed` flag — both `ld -adhoc_codesign` and `codesign -f -s -` outputs fall out cleanly.
- **What the scanner correctly skips**: Java `.class` files (share `0xcafebabe` magic with Mach-O fat headers), PPC big-endian legacy binaries, unsigned Mach-O, all Linux ELFs. Non-coverage gaps.
- **What the scanner does not catch** (and nothing in the baseline channel exhibited these, so they're not blind spots *for this channel*): SHA-1-only CodeDirectories, `page_size=0` (whole-file-hashed) binaries, special-slot hash mismatches, CodeDirectory self-hash corruption. These can be added to the scanner easily if any future channel surfaces them.

## Related

- [NixOS/nix#15638](https://github.com/NixOS/nix/pull/15638) — the fix
- [nixpkgs#507531](https://github.com/NixOS/nixpkgs/issues/507531) — the original issue
- [NixOS/nix#6065](https://github.com/NixOS/nix/issues/6065) — the long-running CA-only report
- [ak2k/nix-507531-repro](https://github.com/ak2k/nix-507531-repro) — flake reproducer for the bug (A/B with the patched daemon)

## License

MIT.
