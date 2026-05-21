# NixOS/nixpkgs#507531 darwin Mach-O page-hash scope

Generated: 2026-05-21 09:01:48 UTC

Daily scan across three darwin caches of the [NixOS/nixpkgs#507531](https://github.com/NixOS/nixpkgs/issues/507531) page-hash bug. Fix PR: [NixOS/nix#15638](https://github.com/NixOS/nix/pull/15638).

Lanes (one column per lane in the table below):

- `darwin` — `nixpkgs-25.11-darwin` channel (`store-paths.xz` published by Hydra's darwin-curated jobset; advances only when its darwin test-gate passes, so its rev can lag `release-25.11` tip).
- `release` — synthesised from `release-25.11` branch tip via `nix-eval-jobs --flake github:NixOS/nixpkgs/<tip>#legacyPackages.aarch64-darwin`, expanded to runtime closure via `cache.nixos.org` `narinfo.References` BFS. Captures cached darwin paths at the release-branch tip even when the curated darwin channel is gated on a poisoned-fish FTB.
- `unstable` — `nixpkgs-unstable` channel (trunk-combined, all-platforms; aarch64-darwin slice of fish here is on 4.6.0).

**Bistability note**: the bug's trigger depends on the Hydra worker's store state at build time — same source, two different drv hashes (driven by transitive stdenv churn), can yield opposite outcomes. The poisoned `fish-4.2.1` aarch64-darwin build at outpath `gngn7y9mn510m…` was the visible breakage that stuck the `nixpkgs-25.11-darwin` channel for ~7 days (2026-04-28 → 2026-05-05); the channel ratcheted past it after [`0c88e1f2bdb9`](https://github.com/NixOS/nixpkgs/commit/0c88e1f2bdb9) (staging-next-25.11 iteration 6, #513189) flipped fish's drv hash and Hydra's rebuild happened to land cleanly. The poisoned bytes remain in `cache.nixos.org` and still SIGKILL on first page-in for anyone pinned to a pre-pivot rev.

## Failure types

The bug's effect surfaces in three types of failure. Each type's membership and how we detect it:

1. **Direct failure** — cached binary's page hashes are stale; kernel SIGKILLs on first page-in. Detected by SHA-256/SHA-1 recomputation against every Mach-O slice in `cache.nixos.org`. Certain per binary.
2. **Load-time transitive** — binary is clean itself, but an `LC_LOAD_DYLIB` points at a direct-failing dylib; dyld maps the broken lib at process start, kernel SIGKILLs before `main()`. Detected by Mach-O load-command parse. Certain per binary.
3. **Build-time dependent** — package's nix expression directly declares a direct-failing package as `buildInputs` / `nativeBuildInputs` / `checkInputs` / `nativeCheckInputs`. Detected by evaluating the channel's nixpkgs aarch64-darwin package set and inspecting drv env vars. Graph-level only — not every listed package actually invokes the failing binary during build. Default view excludes `propagatedBuildInputs` (propagation threads the input forward, it isn't invoked).

| Type| darwin | release | unstable | Union |
|---|---:|---:|---:|---:|
| **1. Direct failure** (slices) | 54 | 17 | 79 | 150 |
| &emsp;↳ distinct packages | 17 | 11 | 35 | 23 |
| **2. Load-time transitive** (binaries) | 0 | 0 | 7 | 7 |
| &emsp;↳ distinct packages | 0 | 0 | 5 | 5 |
| **3. Build-time dependent** (packages, default view) | 0 | 0 | 1 | 1 |

## Canonical examples

- **Type 1 (direct)**: `fish-4.2.1/bin/fish` at outpath `gngn7y9mn510m…` SIGKILLs on launch on Apple Silicon — the bug's highest-profile case. End-user reports in [nixpkgs#208951](https://github.com/NixOS/nixpkgs/issues/208951). This particular cached binary is no longer referenced by the current `nixpkgs-25.11-darwin` channel pointer (rev advanced past it on 2026-05-05), but it remains in `cache.nixos.org` and still SIGKILLs for anyone pinned to a pre-pivot rev — illustrating the bistability point: a clean post-pivot fish build at `s87z9chym2j5…` happens to coexist in cache, same source, opposite Hydra-worker outcome.
- **Type 2 (load-time transitive)**: any Mach-O whose `LC_LOAD_DYLIB` points at e.g. `ffmpeg-8.0-lib/lib/libavformat.61.dylib` fails at process start — deterministic from kernel page-in semantics.
- **Type 3 (build-time dependent)**: `direnv` declares `nativeCheckInputs = [ fish ]` with `doCheck = true`; its `checkPhase` runs `fish ./test/direnv-test.fish`, fish SIGKILLs, direnv fails to build on Hydra. Origin of [nixpkgs#507531](https://github.com/NixOS/nixpkgs/issues/507531).

## Scan totals

| | darwin | release | unstable |
|---|---:|---:|---:|
| Channel label | nixpkgs-25.11-darwin @ 45a1ddc2fb77 (2026-05-21) | release-25.11 @ f28a5cbbf859 (2026-05-21) | nixpkgs-unstable @ d99b013d5d19 (2026-05-21) |
| Paths scanned | 179,256 | 124,155 | 493,327 |
| Mach-O slices | 229,575 | 126,003 | 381,484 |

## Direct-failure slices by signature shape

Classes `linker-signed`, `codesign ad-hoc`, and `ad-hoc with Entitlements + empty CMS wrapper` are fixed in place by `fixupMachoPageHashes` (NixOS/nix#15638). The `Developer-ID-signed` class is skipped with a warning: the embedded PKCS#7 payload commits to the `CodeDirectory`'s hash, and the signing identity is not recoverable from inside the daemon.

| Signature shape | darwin | release | unstable | Total |
|---|---:|---:|---:|---:|
| linker-signed ad-hoc, no CMS slot | 11 | 9 | 28 | 48 |
| codesign ad-hoc, empty 8 B CMS wrapper | 43 | 8 | 43 | 94 |
| ad-hoc with Entitlements + empty CMS wrapper | 0 | 0 | 5 | 5 |
| Developer-ID-signed (non-empty CMS payload) | 0 | 0 | 3 | 3 |
| **Total** | **54** | **17** | **79** | **150** |

## Affected packages

Flat alphabetical list of every package implicated by any tier, across all lanes. A package may appear on multiple rows if it hits more than one tier (e.g. `ffmpeg-8.0-lib` is directly broken AND its dylibs are load-time-linked by other packages).

| Package | Type | Channel(s) | Seeded by |
|---|---|---|---|
| `avalonia-ilspy-7.2-rc` | direct | darwin, unstable | — |
| `cliairplay-1.1` | load-time transitive | unstable | `ffmpeg-headless-8.0.1-lib` |
| `cmdargs-browser-0.1.4` | direct | darwin, release | — |
| `cyanrip-0.9.3.1` | load-time transitive | unstable | `ffmpeg-headless-8.0.1-lib` |
| `esy-0.8.0` | direct | darwin | — |
| `ffmpeg-headless-8.0.1-bin` | direct | unstable | — |
| `ffmpeg-headless-8.0.1-lib` | direct | unstable | — |
| `ffmpegthumbnailer-2.3.0` | load-time transitive | unstable | `ffmpeg-headless-8.0.1-lib` |
| `filen-cli-0.0.36` | direct | unstable | — |
| `gitlab-duo-8.89.0` | direct | unstable | — |
| `gst-libav-1.26.11` | load-time transitive | unstable | `ffmpeg-headless-8.0.1-lib` |
| `httptoolkit-1.24.4` | direct | darwin, release, unstable | — |
| `libtorch-2.9.0` | direct | darwin, release, unstable | — |
| `mmsyn7ukr-array-0.3.0.0` | direct | unstable | — |
| `musikcube-3.0.5` | load-time transitive | unstable | `ffmpeg-headless-8.0.1-lib` |
| `opencode-1.14.35` | direct | unstable | — |
| `opencode-1.14.48` | direct | unstable | — |
| `rimgo-1.4.2` | build-time transitive | unstable | `tailwindcss_4-4.3.0` |
| `shogihome-1.27.1` | direct | darwin, release, unstable | — |
| `shogihome-1.27.2` | direct | darwin, release, unstable | — |
| `swift-5.10.1` | direct | darwin, unstable | — |
| `swift-5.10.1-lib` | direct | darwin, release, unstable | — |
| `tailwindcss_4-4.1.18` | direct | darwin, release | — |
| `tailwindcss_4-4.2.4` | direct | unstable | — |
| `tailwindcss_4-4.3.0` | direct | unstable | — |
| `teams-for-linux-2.8.0` | direct | darwin, release | — |
| `teams-for-linux-2.8.1` | direct | unstable | — |
| `teams-for-linux-2.9.0` | direct | unstable | — |
| `vscode-extension-kilocode-Kilo-Code-7.2.20` | direct | unstable | — |

## Drill-downs

- [darwin channel report](darwin/REPORT.md) — `nixpkgs-25.11-darwin @ 45a1ddc2fb77 (2026-05-21)`
- [release channel report](release/REPORT.md) — `release-25.11 @ f28a5cbbf859 (2026-05-21)`
- [unstable channel report](unstable/REPORT.md) — `nixpkgs-unstable @ d99b013d5d19 (2026-05-21)`
- [Scanner source](scripts/scan-darwin-cache.py)
- [Type 2 analyzer](scripts/compute-load-time-dependents.py)
- [Type 3 analyzer](scripts/compute-build-time-dependents.py)

