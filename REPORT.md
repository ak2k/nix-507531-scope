# NixOS/nixpkgs#507531 darwin Mach-O page-hash scope

Generated: 2026-04-20 11:18:35 UTC

Daily scan across both darwin channels of the [NixOS/nixpkgs#507531](https://github.com/NixOS/nixpkgs/issues/507531) page-hash bug. Fix PR: [NixOS/nix#15638](https://github.com/NixOS/nix/pull/15638).

## Blast-radius tiers

The bug's effect surfaces in three distinguishable ways, in order of decreasing certainty per listed package. Each tier's membership and how we detect it:

1. **Direct failure** — cached binary's page hashes are stale; kernel SIGKILLs on first page-in. Detected by SHA-256/SHA-1 recomputation against every Mach-O slice in `cache.nixos.org`. Certain per binary.
2. **Load-time transitive** — binary is clean itself, but an `LC_LOAD_DYLIB` points at a direct-failing dylib; dyld maps the broken lib at process start, kernel SIGKILLs before `main()`. Detected by Mach-O load-command parse. Certain per binary.
3. **Build-time dependent** — package's nix expression directly declares a direct-failing package as `buildInputs` / `nativeBuildInputs` / `checkInputs` / `nativeCheckInputs`. Detected by evaluating the channel's nixpkgs aarch64-darwin package set and inspecting drv env vars. Graph-level only — not every listed package actually invokes the failing binary during build. Default view excludes `propagatedBuildInputs` (propagation threads the input forward, it isn't invoked).

| Tier| stable | unstable | Union |
|---|---:|---:|---:|
| **1. Direct failure** (slices) | 65 | 53 | 118 |
| &emsp;↳ distinct packages | 19 | 16 | 20 |
| **3. Build-time dependent** (packages, default view) | 11 | 1 | 12 |

## Canonical examples

- **Tier 1 (direct)**: `fish-4.2.1/bin/fish` SIGKILLs on launch on darwin. End-user reports in [nixpkgs#208951](https://github.com/NixOS/nixpkgs/issues/208951).
- **Tier 2 (load-time transitive)**: any Mach-O whose `LC_LOAD_DYLIB` points at e.g. `ffmpeg-8.0-lib/lib/libavformat.61.dylib` fails at process start — deterministic from kernel page-in semantics.
- **Tier 3 (build-time dependent)**: `direnv` declares `nativeCheckInputs = [ fish ]` with `doCheck = true`; its `checkPhase` runs `fish ./test/direnv-test.fish`, fish SIGKILLs, direnv fails to build on Hydra. Origin of [nixpkgs#507531](https://github.com/NixOS/nixpkgs/issues/507531).

## Scan totals

| | stable | unstable |
|---|---:|---:|
| Channel label | nixpkgs-25.11-darwin @ 755a5bb0f389 (2026-04-20) | nixpkgs-unstable @ b86751bc4085 (2026-04-20) |
| Paths scanned | 172,972 | 376,114 |
| Mach-O slices | 223,719 | 286,182 |

## Direct-failure slices by signature shape

Classes `linker-signed`, `codesign ad-hoc`, and `ad-hoc with Entitlements + empty CMS wrapper` are fixed in place by `fixupMachoPageHashes` (NixOS/nix#15638). The `Developer-ID-signed` class is skipped with a warning: the embedded PKCS#7 payload commits to the `CodeDirectory`'s hash, and the signing identity is not recoverable from inside the daemon.

| Signature shape | stable | unstable | Total |
|---|---:|---:|---:|
| linker-signed ad-hoc, no CMS slot | 22 | 7 | 29 |
| codesign ad-hoc, empty 8 B CMS wrapper | 43 | 43 | 86 |
| ad-hoc with Entitlements + empty CMS wrapper | 0 | 1 | 1 |
| Developer-ID-signed (non-empty CMS payload) | 0 | 2 | 2 |
| **Total** | **65** | **53** | **118** |

## Affected packages

Flat alphabetical list of every package implicated by any tier, across both channels. A package may appear on multiple rows if it hits more than one tier (e.g. `ffmpeg-8.0-lib` is directly broken AND its dylibs are load-time-linked by other packages).

| Package | Type | Channel(s) | Seeded by |
|---|---|---|---|
| `Agda-2.8.0` | direct | stable | — |
| `Agda-2.8.0-bin` | direct | stable | — |
| `agda2hs-1.4` | build-time transitive | stable | `Agda-2.8.0` |
| `arion-0.2.2.0` | direct | stable | — |
| `avalonia-ilspy-7.2-rc` | direct | stable, unstable | — |
| `bat-extras-2024.08.24-unstable-2025-02-22` | build-time transitive | stable | `fish-4.2.1` |
| `batdiff-2024.08.24-unstable-2025-02-22` | build-time transitive | stable | `fish-4.2.1` |
| `batman-2024.08.24-unstable-2025-02-22` | build-time transitive | stable | `fish-4.2.1` |
| `batpipe-2024.08.24-unstable-2025-02-22` | build-time transitive | stable | `fish-4.2.1` |
| `batwatch-2024.08.24-unstable-2025-02-22` | build-time transitive | stable | `fish-4.2.1` |
| `direnv-2.37.1` | build-time transitive | stable | `fish-4.2.1` |
| `esy-0.8.0` | direct | stable | — |
| `ffmpeg-8.0-bin` | direct | stable | — |
| `ffmpeg-8.0-lib` | direct | stable | — |
| `filen-cli-0.0.36` | direct | unstable | — |
| `fish-4.2.1` | direct | stable | — |
| `fish-lsp-1.0.10` | build-time transitive | stable | `fish-4.2.1` |
| `HCL-1.9` | direct | stable | — |
| `httptoolkit-1.24.4` | direct | stable, unstable | — |
| `kitty-0.44.0` | build-time transitive | stable | `fish-4.2.1` |
| `libtorch-2.9.0` | direct | stable, unstable | — |
| `oh-my-fish-unstable-2022-03-27` | build-time transitive | stable | `fish-4.2.1` |
| `opencode-1.4.6` | direct | unstable | — |
| `prettybat-2024.08.24-unstable-2025-02-22` | build-time transitive | stable | `fish-4.2.1` |
| `rimgo-1.4.1` | build-time transitive | unstable | `tailwindcss_4-4.2.2` |
| `shogihome-1.27.0` | direct | stable, unstable | — |
| `swift-5.10.1` | direct | stable, unstable | — |
| `swift-5.10.1-lib` | direct | stable, unstable | — |
| `tailwindcss_4-4.1.18` | direct | stable | — |
| `tailwindcss_4-4.2.2` | direct | unstable | — |
| `teams-for-linux-2.8.0` | direct | stable, unstable | — |
| `vscode-extension-kilocode-Kilo-Code-7.2.0` | direct | unstable | — |

## Drill-downs

- [stable channel report](stable/REPORT.md) — `nixpkgs-25.11-darwin @ 755a5bb0f389 (2026-04-20)`
- [unstable channel report](unstable/REPORT.md) — `nixpkgs-unstable @ b86751bc4085 (2026-04-20)`
- [Scanner source](scripts/scan-darwin-cache.py)
- [Tier 2 analyzer](scripts/compute-load-time-dependents.py)
- [Tier 3 analyzer](scripts/compute-build-time-dependents.py)

