# NixOS/nixpkgs#507531 darwin Mach-O page-hash scope

Generated: 2026-04-19 18:32:08 UTC

Daily scan across both darwin channels of the [NixOS/nixpkgs#507531](https://github.com/NixOS/nixpkgs/issues/507531) page-hash bug. Fix PR: [NixOS/nix#15638](https://github.com/NixOS/nix/pull/15638).

## Headline

| | stable | unstable |
|---|---:|---:|
| Channel label | nixpkgs-25.11-darwin @ d7de041fe507 (2026-04-19) | nixpkgs-unstable @ b86751bc4085 (2026-04-19) |
| Paths scanned | 172,952 | 376,114 |
| Mach-O slices | 223,603 | 286,182 |
| Page-hash-mismatch slices | 65 | 53 |
| Affected packages | 19 | 16 |

## Failing slices by signature shape

Classes `linker-signed`, `codesign ad-hoc`, and `ad-hoc with Entitlements + empty CMS wrapper` are fixed in place by `fixupMachoPageHashes` (NixOS/nix#15638). The `Developer-ID-signed` class is skipped with a warning: the embedded PKCS#7 payload commits to the `CodeDirectory`'s hash, and the signing identity is not recoverable from inside the daemon.

| Signature shape | stable | unstable | Total |
|---|---:|---:|---:|
| linker-signed ad-hoc, no CMS slot | 22 | 7 | 29 |
| codesign ad-hoc, empty 8 B CMS wrapper | 43 | 43 | 86 |
| ad-hoc with Entitlements + empty CMS wrapper | 0 | 1 | 1 |
| Developer-ID-signed (non-empty CMS payload) | 0 | 2 | 2 |
| **Total** | **65** | **53** | **118** |

## Drill-downs

- [stable channel report](stable/REPORT.md) — `nixpkgs-25.11-darwin @ d7de041fe507 (2026-04-19)`
- [unstable channel report](unstable/REPORT.md) — `nixpkgs-unstable @ b86751bc4085 (2026-04-19)`
- [Scanner source](scripts/scan-darwin-cache.py)
- [Aggregator source](scripts/aggregate-scan.py)

