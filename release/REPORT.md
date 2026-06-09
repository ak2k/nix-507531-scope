# NixOS/nixpkgs#507531 cache scan — release-25.11 @ e820eb4a444b (2026-06-09)

Generated: 2026-06-09 08:55:23 UTC

## Summary

| Metric | Count |
|---|---:|
| Store paths scanned | 238,722 |
| Mach-O slices parsed | 250,859 |
| Page-hash mismatches (slices) | 54 |
| Page-hash mismatches (distinct packages) | 21 |
|   of which linker-signed (flags=0x20002) | 16 |
|   of which codesign-signed (flags=0x2) | 38 |
| Other signature-invalid (slices) | 0 |
| Other signature-invalid (distinct packages) | 0 |
| Type 2 — binaries linking a failing dylib | 0 |
| Type 2 — distinct packages | 0 |
| Type 3 — packages directly declaring a failing build input (default view) | 0 |

## By architecture

| Arch | Slices scanned | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned | Noise |
|---|---:|---:|---:|---:|---:|---:|
| `arm64` | 234,417 | 54 | 0 | 217,106 | 17,233 | 24 |
| `arm64e` | 102 | 0 | 0 | 26 | 0 | 76 |
| `x86_64` | 7,664 | 0 | 0 | 4,924 | 2,656 | 84 |
| `i386` | 172 | 0 | 0 | 112 | 58 | 2 |
| other/legacy (10 arch codes) | 8,504 | 0 | 0 | 8 | 16 | 8,480 |

## Fat vs thin Mach-O

| Kind | Slices | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned |
|---|---:|---:|---:|---:|---:|
| thin | 235,606 | 18 | 0 | 216,232 | 19,352 |
| fat | 15,253 | 36 | 0 | 5,944 | 611 |

Unique fat binary files: 11,781 in 650 packages. 4 of those packages contain at least one failing fat slice.

## Failing packages (page-hash mismatch)

Sorted alphabetically by package name.

| Package | Failing slices | Store path |
|---|---:|---|
| agda2hs-1.4 | 1 | `/nix/store/zxrvxn6il658jlsqhfkkmyffb2mgbj2w-agda2hs-1.4` |
| cmdargs-browser-0.1.4 | 1 | `/nix/store/gfpx3q94dxsga2z9iakpci2vprbxmrxx-cmdargs-browser-0.1.4` |
| dhall-docs-1.0.12 | 2 | `/nix/store/a2f2sjj5ck084y8x00mmw50l80d99xv6-dhall-docs-1.0.12` |
| httptoolkit-1.24.4 | 1 | `/nix/store/63y47sm78b2fzjzljyd4zckqm9j2ljds-httptoolkit-1.24.4` |
| httptoolkit-1.24.4 | 1 | `/nix/store/hkfbkgns19ci16wjnizssn1m7idpb765-httptoolkit-1.24.4` |
| libtorch-2.9.0 | 1 | `/nix/store/jfcf9833px3lhy28lw8qys66gdgsm3np-libtorch-2.9.0` |
| libtorch-2.9.0 | 1 | `/nix/store/pr81jsxz62946kr72n3m0gxm1nkvwyps-libtorch-2.9.0` |
| shogihome-1.27.1 | 1 | `/nix/store/gsb5xp7asp9z88la7kwm6mgij6aygb43-shogihome-1.27.1` |
| shogihome-1.27.2 | 1 | `/nix/store/d0dk2sq2nanhkikqmdk54zlvv46g6sf6-shogihome-1.27.2` |
| shogihome-1.27.2 | 1 | `/nix/store/lbvvlkhp8yjbdm2j2nhc5avi2nabvvai-shogihome-1.27.2` |
| shogihome-1.27.3 | 1 | `/nix/store/461rm6i08wwy251inadwzxfgs21dxwa2-shogihome-1.27.3` |
| shogihome-1.27.3 | 1 | `/nix/store/wqc1661zdi4pg0blsqhycvqpva7nha2a-shogihome-1.27.3` |
| swift-5.10.1 | 11 | `/nix/store/25dxglbbwfh2gkrlfnrssa3nzvn8vbcv-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/cmlwmnf60kjj6j8l5k05z7761xjynp6r-swift-5.10.1` |
| swift-5.10.1-lib | 7 | `/nix/store/bdf7cvmgbyb5ism3a7p7v7arjr8m8alq-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/kiakz33bkfmg8gfs96j99agrp3s4dyib-swift-5.10.1-lib` |
| tailwindcss_4-4.1.18 | 1 | `/nix/store/ngh0kymzj2iis7qbv49rnavq4sz2zw5b-tailwindcss_4-4.1.18` |
| tailwindcss_4-4.1.18 | 1 | `/nix/store/p0qpifvs9lpm8797gzby7ip8hmzfdydq-tailwindcss_4-4.1.18` |
| teams-for-linux-2.8.0 | 1 | `/nix/store/ahd6q635mfpc7zidmisg3hbdncw10qgj-teams-for-linux-2.8.0` |
| teams-for-linux-2.8.0 | 1 | `/nix/store/iqkd5xy9n5zrcyxfhw5y8zw0zhjjdrgw-teams-for-linux-2.8.0` |
| teams-for-linux-2.8.0 | 1 | `/nix/store/xlpkh45gqki78zq030mw2z450b7pr1m4-teams-for-linux-2.8.0` |

## Slice classification

| Category | Count |
|---|---:|
| `page_hash_mismatch` | 54 |
| `other_sig_invalid` | 0 |
| `clean` (signed, verified) | 222,176 |
| `unsigned` (Mach-O without LC_CODE_SIGNATURE) | 19,963 |
| `not_real_macho` (Java .class, PPC big-endian, etc.) | 8,666 |
| `scanner_error` | 0 |

## Load-time transitive broken binaries

Binaries whose own code signatures are valid but which dyld cannot map at process start because their `LC_LOAD_DYLIB` / `LC_LOAD_WEAK_DYLIB` / `LC_REEXPORT_DYLIB` points at a direct-failing dylib. These SIGKILL at load, before `main()` runs — deterministic per slice.

| Metric | Count |
|---|---:|
| Binaries that link at least one failing dylib | 0 |
| Distinct packages containing such binaries | 0 |
| Failing dylibs that serve as seeds | 39 |
| Total (binary, failing-dylib) pairs | 0 |

Full detail: [`load-time-dependents.csv`](load-time-dependents.csv) (one row per `(binary, linked_failing_dylib)` pair).
## Build-time dependents

Packages whose nix expression **directly declares** a direct-failing package as `buildInputs`, `nativeBuildInputs`, `checkInputs`, or `nativeCheckInputs` (1-hop). If the failing binary is invoked during the package's build phase, Hydra fails and the package never reaches the cache. This is a graph-level relationship: whether each listed package actually invokes the failing binary during build is not statically determinable. The canonical confirmed case is direnv — its `nativeCheckInputs = [ fish ]` with a `checkPhase` running `fish ./test/direnv-test.fish`, origin of [nixpkgs#507531](https://github.com/NixOS/nixpkgs/issues/507531).

Default view excludes `propagatedBuildInputs` / `propagatedNativeBuildInputs` edges (propagation threads the input forward; the listed package itself doesn't invoke it). The CSV includes all edge kinds for manual inspection.

| Metric | Count |
|---|---:|
| Packages with failing seeds in declared build/check inputs (default view) | 0 |
| Total direct-edge rows (default view) | 0 |
| Total rows including propagated edges | 0 |
| Distinct failing seeds | 21 |

Full detail: [`build-time-dependents.csv`](build-time-dependents.csv) (one row per `(dependent, edge_kind, seed)` tuple; `in_default_view=true` marks default-filter rows).

## Methodology

- Input: `store-paths.xz` from the channel release URL.
- Per path: `<hash>.narinfo` → stream NAR over HTTP → decompress (xz/zstd/bz2) inline → walk entries, no on-disk NAR persistence.
- Per regular file: peek 4 bytes; buffer and analyze only if Mach-O magic matches.
- Per Mach-O slice (thin or fat): parse `LC_CODE_SIGNATURE`, pick the primary CodeDirectory (SHA-256 preferred over SHA-1 when both are present, matching the kernel's selection order), recompute per-page hash over `data[i*ps : min((i+1)*ps, code_limit)]` with the CD's own algorithm, compare against the stored hash slot.
- `page_hash_mismatch` is defined as: at least one computed per-page hash disagrees with its stored hash slot. This matches the kernel's page-in validator and `codesign -v` rejection criterion for adhoc-signed binaries.
- `other_sig_invalid` is defined as: LC_CODE_SIGNATURE is present but the signature blob is structurally unparseable (e.g. payload OOB, bad SuperBlob magic, unsupported hash type such as SHA-384).
- Scanner source: see the PR repo.

