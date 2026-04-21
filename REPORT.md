# NixOS/nixpkgs#507531 darwin Mach-O page-hash scope

Generated: 2026-04-21 22:55:48 UTC

Daily scan across both darwin channels of the [NixOS/nixpkgs#507531](https://github.com/NixOS/nixpkgs/issues/507531) page-hash bug. Fix PR: [NixOS/nix#15638](https://github.com/NixOS/nix/pull/15638).

## Failure types

The bug's effect surfaces in three types of failure. Each type's membership and how we detect it:

1. **Direct failure** — cached binary's page hashes are stale; kernel SIGKILLs on first page-in. Detected by SHA-256/SHA-1 recomputation against every Mach-O slice in `cache.nixos.org`. Certain per binary.
2. **Load-time transitive** — binary is clean itself, but an `LC_LOAD_DYLIB` points at a direct-failing dylib; dyld maps the broken lib at process start, kernel SIGKILLs before `main()`. Detected by Mach-O load-command parse. Certain per binary.
3. **Build-time dependent** — package's nix expression directly declares a direct-failing package as `buildInputs` / `nativeBuildInputs` / `checkInputs` / `nativeCheckInputs`. Detected by evaluating the channel's nixpkgs aarch64-darwin package set and inspecting drv env vars. Graph-level only — not every listed package actually invokes the failing binary during build. Default view excludes `propagatedBuildInputs` (propagation threads the input forward, it isn't invoked).

| Type| stable | unstable | Union |
|---|---:|---:|---:|
| **1. Direct failure** (slices) | 130 | 53 | 183 |
| &emsp;↳ distinct packages | 20 | 16 | 20 |
| **2. Load-time transitive** (binaries) | 56 | 0 | 56 |
| &emsp;↳ distinct packages | 37 | 0 | 37 |
| **3. Build-time dependent** (packages, default view) | 11 | 1 | 12 |

## Canonical examples

- **Type 1 (direct)**: `fish-4.2.1/bin/fish` SIGKILLs on launch on darwin. End-user reports in [nixpkgs#208951](https://github.com/NixOS/nixpkgs/issues/208951).
- **Type 2 (load-time transitive)**: any Mach-O whose `LC_LOAD_DYLIB` points at e.g. `ffmpeg-8.0-lib/lib/libavformat.61.dylib` fails at process start — deterministic from kernel page-in semantics.
- **Type 3 (build-time dependent)**: `direnv` declares `nativeCheckInputs = [ fish ]` with `doCheck = true`; its `checkPhase` runs `fish ./test/direnv-test.fish`, fish SIGKILLs, direnv fails to build on Hydra. Origin of [nixpkgs#507531](https://github.com/NixOS/nixpkgs/issues/507531).

## Scan totals

| | stable | unstable |
|---|---:|---:|
| Channel label | nixpkgs-25.11-darwin @ 7a8c107078da (2026-04-21) | nixpkgs-unstable @ b86751bc4085 (2026-04-21) |
| Paths scanned | 316,948 | 376,114 |
| Mach-O slices | 412,486 | 286,182 |

## Direct-failure slices by signature shape

Classes `linker-signed`, `codesign ad-hoc`, and `ad-hoc with Entitlements + empty CMS wrapper` are fixed in place by `fixupMachoPageHashes` (NixOS/nix#15638). The `Developer-ID-signed` class is skipped with a warning: the embedded PKCS#7 payload commits to the `CodeDirectory`'s hash, and the signing identity is not recoverable from inside the daemon.

| Signature shape | stable | unstable | Total |
|---|---:|---:|---:|
| linker-signed ad-hoc, no CMS slot | 44 | 7 | 51 |
| codesign ad-hoc, empty 8 B CMS wrapper | 86 | 43 | 129 |
| ad-hoc with Entitlements + empty CMS wrapper | 0 | 1 | 1 |
| Developer-ID-signed (non-empty CMS payload) | 0 | 2 | 2 |
| **Total** | **130** | **53** | **183** |

## Affected packages

Flat alphabetical list of every package implicated by any tier, across both channels. A package may appear on multiple rows if it hits more than one tier (e.g. `ffmpeg-8.0-lib` is directly broken AND its dylibs are load-time-linked by other packages).

| Package | Type | Channel(s) | Seeded by |
|---|---|---|---|
| `Agda-2.8.0` | direct | stable | — |
| `Agda-2.8.0-bin` | direct | stable | — |
| `agda2hs-1.4` | build-time transitive | stable | `Agda-2.8.0` |
| `arion-0.2.2.0` | direct | stable | — |
| `auto-editor-29.3.1` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `avalonia-ilspy-7.2-rc` | direct | stable, unstable | — |
| `bat-extras-2024.08.24` | build-time transitive | stable | `fish-4.2.1` |
| `batdiff-2024.08.24` | build-time transitive | stable | `fish-4.2.1` |
| `batman-2024.08.24` | build-time transitive | stable | `fish-4.2.1` |
| `batpipe-2024.08.24` | build-time transitive | stable | `fish-4.2.1` |
| `batwatch-2024.08.24` | build-time transitive | stable | `fish-4.2.1` |
| `ccextractor-0.94` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `contour-0.6.1.7494` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `corsix-th-0.69.2` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `ddnet-19.5` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `direnv-2.37.1` | build-time transitive | stable | `fish-4.2.1` |
| `dosbox-x-2025.10.07` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `esy-0.8.0` | direct | stable | — |
| `ffmpeg-8.0-bin` | direct | stable | — |
| `ffmpeg-8.0-lib` | direct | stable | — |
| `ffms-5.0` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `filen-cli-0.0.36` | direct | unstable | — |
| `fish-4.2.1` | direct | stable | — |
| `fish-lsp-1.0.10` | build-time transitive | stable | `fish-4.2.1` |
| `freerdp-3.23.0` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `harvid-0.9.1` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `HCL-1.9` | direct | stable | — |
| `httptoolkit-1.24.4` | direct | stable, unstable | — |
| `keyfinder-cli-1.1.2` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `kitty-0.44.0` | build-time transitive | stable | `fish-4.2.1` |
| `libopenshot-0.4.0` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `libtorch-2.9.0` | direct | stable, unstable | — |
| `loudgain-0.6.8` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `megacmd-1.7.0` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `moc-2.6-alpha3` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `moonlight-qt-6.1.0` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `mpd-0.24.6` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `netgen-6.2.2505` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `notcurses-3.0.17` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `oh-my-fish` | build-time transitive | stable | `fish-4.2.1` |
| `opencode-1.4.6` | direct | unstable | — |
| `opencv-4.12.0` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `opencv-4.12.0-package_tests` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `phira-unwrapped-0.6.7` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `pianobar-2024.12.21` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `pqiv-2.13.3` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `prettybat-2024.08.24` | build-time transitive | stable | `fish-4.2.1` |
| `q2pro-0` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `qtmultimedia-6.10.2` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `rimgo-1.4.1` | build-time transitive | unstable | `tailwindcss_4-4.2.2` |
| `rsgain-3.6` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `scrcpy-3.3.4` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `shogihome-1.27.0` | direct | stable, unstable | — |
| `spek-0.8.5` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `squeezelite-2.0.0.1541` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `survex-1.4.18` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `swift-5.10.1` | direct | stable, unstable | — |
| `swift-5.10.1-lib` | direct | stable, unstable | — |
| `tailwindcss_4-4.1.18` | direct | stable | — |
| `tailwindcss_4-4.2.2` | direct | unstable | — |
| `taterclient-ddnet-10.6.0` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `teams-for-linux-2.8.0` | direct | stable, unstable | — |
| `timg-1.6.3` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `vgmstream-2055` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `video-compare-20250928` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `vivictpp-1.3.1` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `vscode-extension-kilocode-Kilo-Code-7.2.0` | direct | unstable | — |
| `vtk-9.5.2` | load-time transitive | stable | `ffmpeg-8.0-lib` |
| `wxsvg-1.5.25` | load-time transitive | stable | `ffmpeg-8.0-lib` |

## Drill-downs

- [stable channel report](stable/REPORT.md) — `nixpkgs-25.11-darwin @ 7a8c107078da (2026-04-21)`
- [unstable channel report](unstable/REPORT.md) — `nixpkgs-unstable @ b86751bc4085 (2026-04-21)`
- [Scanner source](scripts/scan-darwin-cache.py)
- [Type 2 analyzer](scripts/compute-load-time-dependents.py)
- [Type 3 analyzer](scripts/compute-build-time-dependents.py)

