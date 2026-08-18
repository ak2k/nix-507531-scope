# NixOS/nixpkgs#507531 cache scan — release-26.05 @ 29d87be2ee9a (2026-08-18)

Generated: 2026-08-18 08:11:26 UTC

## Summary

| Metric | Count |
|---|---:|
| Store paths scanned | 126,156 |
| Mach-O slices parsed | 127,316 |
| Page-hash mismatches (slices) | 26 |
| Page-hash mismatches (distinct packages) | 10 |
|   of which linker-signed (flags=0x20002) | 7 |
|   of which codesign-signed (flags=0x2) | 19 |
| Other signature-invalid (slices) | 0 |
| Other signature-invalid (distinct packages) | 0 |
| Type 2 — binaries linking a failing dylib | 0 |
| Type 2 — distinct packages | 0 |
| Type 3 — packages directly declaring a failing build input (default view) | 1 |

## By architecture

| Arch | Slices scanned | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned | Noise |
|---|---:|---:|---:|---:|---:|---:|
| `arm64` | 119,100 | 26 | 0 | 109,199 | 9,864 | 11 |
| `arm64e` | 58 | 0 | 0 | 20 | 0 | 38 |
| `x86_64` | 3,852 | 0 | 0 | 2,512 | 1,298 | 42 |
| `i386` | 95 | 0 | 0 | 56 | 38 | 1 |
| other/legacy (11 arch codes) | 4,211 | 0 | 0 | 4 | 8 | 4,199 |

## Fat vs thin Mach-O

| Kind | Slices | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned |
|---|---:|---:|---:|---:|---:|
| thin | 119,617 | 8 | 0 | 108,695 | 10,912 |
| fat | 7,699 | 18 | 0 | 3,096 | 296 |

Unique fat binary files: 5,897 in 343 packages. 2 of those packages contain at least one failing fat slice.

## Failing packages (page-hash mismatch)

Sorted alphabetically by package name.

| Package | Failing slices | Store path |
|---|---:|---|
| filen-cli-0.0.36 | 1 | `/nix/store/0r8fwgnqldbpzd65fayyaa1d7ik2z3lc-filen-cli-0.0.36` |
| httptoolkit-1.26.0 | 1 | `/nix/store/f8916ng5b41vy8zipihapni7ggjkmskj-httptoolkit-1.26.0` |
| libtorch-2.9.0 | 1 | `/nix/store/lh7hw0zhm2fxhwpqbv3qqyzh4qqac1p8-libtorch-2.9.0` |
| opencode-1.15.10 | 1 | `/nix/store/18jmwdml857xgwsnalfpy4922av79fzf-opencode-1.15.10` |
| shogihome-1.29.0 | 1 | `/nix/store/2hsj528qqf0qndxfmlqhwv989w6b4n7s-shogihome-1.29.0` |
| swift-5.10.1 | 11 | `/nix/store/5caplwxxb1qnjscim7cks1isnyklwaf5-swift-5.10.1` |
| swift-5.10.1-lib | 7 | `/nix/store/wz5br160dmx8af0jp5y9vgkbyy9khnbh-swift-5.10.1-lib` |
| tailwindcss_4-4.3.1 | 1 | `/nix/store/i196v0y1ikg78c782qi9qbjmr2pzia2l-tailwindcss_4-4.3.1` |
| teams-for-linux-2.11.1 | 1 | `/nix/store/l2738npx9g9wsb587qqkyaxgdal928k6-teams-for-linux-2.11.1` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 1 | `/nix/store/4j2sgj1x9vc40x61iz99lriyzbz9lldn-vscode-extension-kilocode-Kilo-Code-7.2.20` |

## Slice classification

| Category | Count |
|---|---:|
| `page_hash_mismatch` | 26 |
| `other_sig_invalid` | 0 |
| `clean` (signed, verified) | 111,791 |
| `unsigned` (Mach-O without LC_CODE_SIGNATURE) | 11,208 |
| `not_real_macho` (Java .class, PPC big-endian, etc.) | 4,291 |
| `scanner_error` | 0 |

## Load-time transitive broken binaries

Binaries whose own code signatures are valid but which dyld cannot map at process start because their `LC_LOAD_DYLIB` / `LC_LOAD_WEAK_DYLIB` / `LC_REEXPORT_DYLIB` points at a direct-failing dylib. These SIGKILL at load, before `main()` runs — deterministic per slice.

| Metric | Count |
|---|---:|
| Binaries that link at least one failing dylib | 0 |
| Distinct packages containing such binaries | 0 |
| Failing dylibs that serve as seeds | 19 |
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
| Distinct failing seeds | 10 |

Edges by kind (default view only):

| Edge kind | Count |
|---|---:|
| `nativeBuildInputs` | 1 |

Top seed packages by downstream dependent count:

| Seed package | Downstream dependents |
|---|---:|
| `tailwindcss_4-4.3.1` | 1 |

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

