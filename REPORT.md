# NixOS/nixpkgs#507531 darwin Mach-O page-hash scope

Generated: 2026-04-20 07:47:37 UTC

Daily scan across both darwin channels of the [NixOS/nixpkgs#507531](https://github.com/NixOS/nixpkgs/issues/507531) page-hash bug. Fix PR: [NixOS/nix#15638](https://github.com/NixOS/nix/pull/15638).

## Blast-radius tiers

The bug's effect surfaces in three distinguishable ways, in order of decreasing certainty per listed package. Each tier's membership and how we detect it:

1. **Direct failure** — cached binary's page hashes are stale; kernel SIGKILLs on first page-in. Detected by SHA-256/SHA-1 recomputation against every Mach-O slice in `cache.nixos.org`. Certain per binary.
2. **Load-time transitive** — binary is clean itself, but an `LC_LOAD_DYLIB` points at a direct-failing dylib; dyld maps the broken lib at process start, kernel SIGKILLs before `main()`. Detected by Mach-O load-command parse. Certain per binary.
3. **Build-time dependent** — package's nix expression directly declares a direct-failing package as `buildInputs` / `nativeBuildInputs` / `checkInputs` / `nativeCheckInputs`. Detected by evaluating the channel's nixpkgs aarch64-darwin package set and inspecting drv env vars. Graph-level only — not every listed package actually invokes the failing binary during build. Default view excludes `propagatedBuildInputs` (propagation threads the input forward, it isn't invoked).

| Tier| stable | unstable | Union |
|---|---:|---:|---:|
| **1. Direct failure** (slices) | 65 | 53 | 118 |
| &emsp;↳ distinct packages | 19 | 16 | 35 |
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

## Drill-downs

- [stable channel report](stable/REPORT.md) — `nixpkgs-25.11-darwin @ 755a5bb0f389 (2026-04-20)`
- [unstable channel report](unstable/REPORT.md) — `nixpkgs-unstable @ b86751bc4085 (2026-04-20)`
- [Scanner source](scripts/scan-darwin-cache.py)
- [Tier 2 analyzer](scripts/compute-load-time-dependents.py)
- [Tier 3 analyzer](scripts/compute-build-time-dependents.py)

