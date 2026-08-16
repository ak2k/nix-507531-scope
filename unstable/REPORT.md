# NixOS/nixpkgs#507531 cache scan — nixpkgs-unstable @ 8be7bd0c83f1 (2026-08-16)

Generated: 2026-08-16 07:58:19 UTC

## Summary

| Metric | Count |
|---|---:|
| Store paths scanned | 315,231 |
| Mach-O slices parsed | 196,539 |
| Page-hash mismatches (slices) | 46 |
| Page-hash mismatches (distinct packages) | 14 |
|   of which linker-signed (flags=0x20002) | 7 |
|   of which codesign-signed (flags=0x2) | 39 |
| Other signature-invalid (slices) | 3 |
| Other signature-invalid (distinct packages) | 1 |
| Type 2 — binaries linking a failing dylib | 0 |
| Type 2 — distinct packages | 0 |
| Type 3 — packages directly declaring a failing build input (default view) | 1 |

## By architecture

| Arch | Slices scanned | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned | Noise |
|---|---:|---:|---:|---:|---:|---:|
| `arm64` | 137,485 | 46 | 0 | 127,068 | 10,338 | 33 |
| `arm64e` | 34 | 0 | 0 | 14 | 0 | 20 |
| `x86_64` | 6,648 | 0 | 2 | 3,032 | 3,561 | 53 |
| `i386` | 400 | 0 | 1 | 73 | 309 | 17 |
| other/legacy (14 arch codes) | 51,972 | 0 | 0 | 1 | 127 | 51,844 |

## Fat vs thin Mach-O

| Kind | Slices | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned |
|---|---:|---:|---:|---:|---:|
| thin | 139,538 | 10 | 3 | 125,906 | 13,440 |
| fat | 57,001 | 36 | 0 | 4,282 | 895 |

Unique fat binary files: 54,317 in 727 packages. 4 of those packages contain at least one failing fat slice.

## Failing packages (page-hash mismatch)

Sorted alphabetically by package name.

| Package | Failing slices | Store path |
|---|---:|---|
| filen-cli-0.0.36 | 1 | `/nix/store/h3hiral71d200cywyklf3w2672q7fkfc-filen-cli-0.0.36` |
| httptoolkit-1.26.0 | 1 | `/nix/store/qpzcwid5hr9s91azg6fmwwwyqxfc25dq-httptoolkit-1.26.0` |
| hunk-0.18.0 | 1 | `/nix/store/jkfdgl7bdd0dn5bcf2bqfzr37ymc05jd-hunk-0.18.0` |
| libtorch-2.9.0 | 1 | `/nix/store/l91spz32g5a5dzdcz18kb11a5b7xi9ks-libtorch-2.9.0` |
| renovate-44.24.3 | 1 | `/nix/store/hj4hv32i4w8f2h6pr4cswhlbrlq3ny7p-renovate-44.24.3` |
| renovate-44.24.3 | 1 | `/nix/store/vk7chz9c70a60rdbjgk11fbg2231fi8i-renovate-44.24.3` |
| shogihome-1.29.0 | 1 | `/nix/store/z1nv52627m8d3m7pz3lb9sbhcjys79ff-shogihome-1.29.0` |
| swift-5.10.1 | 11 | `/nix/store/76a3zzly7172nxr5ap5sij6rgwh65hqd-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/hzx2wsx2jrakws0zh8zrb6hn6i379fl9-swift-5.10.1` |
| swift-5.10.1-lib | 7 | `/nix/store/44h8zl9mm7vzq205n0fh9lwgs3gdsk5n-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/yn710d5q59c2j8y77w1cwbdvkh7x6jvq-swift-5.10.1-lib` |
| tailwindcss_4-4.3.3 | 1 | `/nix/store/6x7ip1f8fzy0asljzdkvppa6427spp0h-tailwindcss_4-4.3.3` |
| teams-for-linux-2.14.1 | 1 | `/nix/store/v7bib0qncfr3p0vgwbgh785rgl5k19p5-teams-for-linux-2.14.1` |
| vscode-extension-kilocode-Kilo-Code-7.4.16 | 1 | `/nix/store/smhfspqikyayf45jpz86rj9lbi6lmyc7-vscode-extension-kilocode-Kilo-Code-7.4.16` |

## Appendix — other signature-invalid binaries

Slices where the scanner found a structural signature problem (not a page-hash mismatch). These also fail `codesign -v`. Mechanism may or may not be the same as NixOS/nixpkgs#507531.

| Package | Slices | Error kind | Store path |
|---|---:|---|---|
| cvs-export | 3 | bad SuperBlob magic 0x00000000, bad SuperBlob magic 0x28000000, signature blob too small | `/nix/store/k2sl4knvf6qv31lzchazlbslsm3jzsgc-cvs-export` |

## Slice classification

| Category | Count |
|---|---:|
| `page_hash_mismatch` | 46 |
| `other_sig_invalid` | 3 |
| `clean` (signed, verified) | 130,188 |
| `unsigned` (Mach-O without LC_CODE_SIGNATURE) | 14,335 |
| `not_real_macho` (Java .class, PPC big-endian, etc.) | 51,967 |
| `scanner_error` | 0 |

## Load-time transitive broken binaries

Binaries whose own code signatures are valid but which dyld cannot map at process start because their `LC_LOAD_DYLIB` / `LC_LOAD_WEAK_DYLIB` / `LC_REEXPORT_DYLIB` points at a direct-failing dylib. These SIGKILL at load, before `main()` runs — deterministic per slice.

| Metric | Count |
|---|---:|
| Binaries that link at least one failing dylib | 0 |
| Distinct packages containing such binaries | 0 |
| Failing dylibs that serve as seeds | 37 |
| Total (binary, failing-dylib) pairs | 0 |

Full detail: [`load-time-dependents.csv`](load-time-dependents.csv) (one row per `(binary, linked_failing_dylib)` pair).
## Build-time dependents

Packages whose nix expression **directly declares** a direct-failing package as `buildInputs`, `nativeBuildInputs`, `checkInputs`, or `nativeCheckInputs` (1-hop). If the failing binary is invoked during the package's build phase, Hydra fails and the package never reaches the cache. This is a graph-level relationship: whether each listed package actually invokes the failing binary during build is not statically determinable. The canonical confirmed case is direnv — its `nativeCheckInputs = [ fish ]` with a `checkPhase` running `fish ./test/direnv-test.fish`, origin of [nixpkgs#507531](https://github.com/NixOS/nixpkgs/issues/507531).

Default view excludes `propagatedBuildInputs` / `propagatedNativeBuildInputs` edges (propagation threads the input forward; the listed package itself doesn't invoke it). The CSV includes all edge kinds for manual inspection.

| Metric | Count |
|---|---:|
| Packages with failing seeds in declared build/check inputs (default view) | 1 |
| Total direct-edge rows (default view) | 1 |
| Total rows including propagated edges | 1 |
| Distinct failing seeds | 14 |

Edges by kind (default view only):

| Edge kind | Count |
|---|---:|
| `nativeBuildInputs` | 1 |

Top seed packages by downstream dependent count:

| Seed package | Downstream dependents |
|---|---:|
| `tailwindcss_4-4.3.3` | 1 |

Dependent packages (1): `rimgo`

Full detail: [`build-time-dependents.csv`](build-time-dependents.csv) (one row per `(dependent, edge_kind, seed)` tuple; `in_default_view=true` marks default-filter rows).

## Methodology

- Input: `store-paths.xz` from the channel release URL.
- Per path: `<hash>.narinfo` → stream NAR over HTTP → decompress (xz/zstd/bz2) inline → walk entries, no on-disk NAR persistence.
- Per regular file: peek 4 bytes; buffer and analyze only if Mach-O magic matches.
- Per Mach-O slice (thin or fat): parse `LC_CODE_SIGNATURE`, pick the primary CodeDirectory (SHA-256 preferred over SHA-1 when both are present, matching the kernel's selection order), recompute per-page hash over `data[i*ps : min((i+1)*ps, code_limit)]` with the CD's own algorithm, compare against the stored hash slot.
- `page_hash_mismatch` is defined as: at least one computed per-page hash disagrees with its stored hash slot. This matches the kernel's page-in validator and `codesign -v` rejection criterion for adhoc-signed binaries.
- `other_sig_invalid` is defined as: LC_CODE_SIGNATURE is present but the signature blob is structurally unparseable (e.g. payload OOB, bad SuperBlob magic, unsupported hash type such as SHA-384).
- Scanner source: see the PR repo.

