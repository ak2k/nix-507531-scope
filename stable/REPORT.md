# NixOS/nixpkgs#507531 cache scan — nixpkgs-25.11-darwin @ 755a5bb0f389 (2026-04-20)

Generated: 2026-04-20 11:06:06 UTC

## Summary

| Metric | Count |
|---|---:|
| Store paths scanned | 172,972 |
| Mach-O slices parsed | 223,719 |
| Page-hash mismatches (slices) | 65 |
| Page-hash mismatches (distinct packages) | 19 |
|   of which linker-signed (flags=0x20002) | 22 |
|   of which codesign-signed (flags=0x2) | 43 |
| Other signature-invalid (slices) | 1 |
| Other signature-invalid (distinct packages) | 1 |
| Tier 2 — binaries linking a failing dylib | 0 |
| Tier 2 — distinct packages | 0 |
| Tier 3 — packages directly declaring a failing build input (default view) | 11 |

## By architecture

| Arch | Slices scanned | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned | Noise |
|---|---:|---:|---:|---:|---:|---:|
| `arm64` | 104,774 | 44 | 0 | 96,936 | 7,776 | 18 |
| `arm64e` | 53 | 0 | 0 | 13 | 0 | 40 |
| `x86_64` | 111,236 | 21 | 1 | 8,196 | 102,955 | 63 |
| `i386` | 169 | 0 | 0 | 113 | 54 | 2 |
| other/legacy (10 arch codes) | 7,487 | 0 | 0 | 2 | 8 | 7,477 |

## Fat vs thin Mach-O

| Kind | Slices | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned |
|---|---:|---:|---:|---:|---:|
| thin | 210,400 | 23 | 1 | 100,090 | 110,284 |
| fat | 13,319 | 42 | 0 | 5,170 | 509 |

Unique fat binary files: 10,301 in 535 packages. 5 of those packages contain at least one failing fat slice.

## Failing packages (page-hash mismatch)

Sorted alphabetically by package name.

| Package | Failing slices | Store path |
|---|---:|---|
| Agda-2.8.0 | 1 | `/nix/store/45cc6ms1las7q0dxy7yfipnpxi5hz428-Agda-2.8.0` |
| Agda-2.8.0-bin | 2 | `/nix/store/6aay4gf46sxh49241gvnbkv4xdx4f7q1-Agda-2.8.0-bin` |
| arion-0.2.2.0 | 1 | `/nix/store/isimvgg2hxw945jhkr68rj75hj67qhqn-arion-0.2.2.0` |
| avalonia-ilspy-7.2-rc | 6 | `/nix/store/l4d6aspbcs27mlisx97fhp0qdij3i39z-avalonia-ilspy-7.2-rc` |
| esy-0.8.0 | 1 | `/nix/store/bc5vpiddskrdnfc04fjh6irf3p1pw4bh-esy-0.8.0` |
| esy-0.8.0 | 1 | `/nix/store/rjwifh8vrg0acrw439w1nqcpl0lfkna0-esy-0.8.0` |
| ffmpeg-8.0-bin | 3 | `/nix/store/6a5nr567sb4a36lisa6gydpp3bfij1vv-ffmpeg-8.0-bin` |
| ffmpeg-8.0-lib | 7 | `/nix/store/hn58l3pvn5iwq87p6ddp9wsw8ai9dl93-ffmpeg-8.0-lib` |
| fish-4.2.1 | 1 | `/nix/store/gngn7y9mn510mf1hkmr0l69qbpvxfbfh-fish-4.2.1` |
| HCL-1.9 | 1 | `/nix/store/zhla7p947b07blrc231jj21i0q67cj1r-HCL-1.9` |
| httptoolkit-1.24.4 | 1 | `/nix/store/g505c34pkapf2qf5i1fq7h0bkkznl8bi-httptoolkit-1.24.4` |
| libtorch-2.9.0 | 1 | `/nix/store/3hrcgmdqmhmz309fqq2rkisgzlxqh6jq-libtorch-2.9.0` |
| shogihome-1.27.0 | 1 | `/nix/store/f1spwbbqpcpx4bcdbj21rbx3psxwzc4v-shogihome-1.27.0` |
| swift-5.10.1 | 11 | `/nix/store/2bgfmhdq533vvasjzrq53adjvpadwrjp-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/sjij55a15h4s5gwy9r439l2yxip12mhm-swift-5.10.1` |
| swift-5.10.1-lib | 7 | `/nix/store/3y322ka7bccpcnqcbrq8saywa48c1pnj-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/f3qdyspn3vc661lxa11wnp03y10x8cpd-swift-5.10.1-lib` |
| tailwindcss_4-4.1.18 | 1 | `/nix/store/8wy6d88k17bwpgr8wa9f82pjmc6w4as9-tailwindcss_4-4.1.18` |
| teams-for-linux-2.8.0 | 1 | `/nix/store/rm4pn5zx4kpdg7am4pc6qymmhgm6wj38-teams-for-linux-2.8.0` |

## Appendix — other signature-invalid binaries

Slices where the scanner found a structural signature problem (not a page-hash mismatch). These also fail `codesign -v`. Mechanism may or may not be the same as NixOS/nixpkgs#507531.

| Package | Slices | Error kind | Store path |
|---|---:|---|---|
| tailwindcss_4-4.1.18 | 1 | LC_CODE_SIGNATURE payload OOB | `/nix/store/ffs5qadbvnf3vs66q0nzpdfw0rbqyc52-tailwindcss_4-4.1.18` |

## Slice classification

| Category | Count |
|---|---:|
| `page_hash_mismatch` | 65 |
| `other_sig_invalid` | 1 |
| `clean` (signed, verified) | 105,260 |
| `unsigned` (Mach-O without LC_CODE_SIGNATURE) | 110,793 |
| `not_real_macho` (Java .class, PPC big-endian, etc.) | 7,600 |
| `scanner_error` | 0 |

## Load-time transitive broken binaries

Binaries whose own code signatures are valid but which dyld cannot map at process start because their `LC_LOAD_DYLIB` / `LC_LOAD_WEAK_DYLIB` / `LC_REEXPORT_DYLIB` points at a direct-failing dylib. These SIGKILL at load, before `main()` runs — deterministic per slice.

| Metric | Count |
|---|---:|
| Binaries that link at least one failing dylib | 0 |
| Distinct packages containing such binaries | 0 |
| Failing dylibs that serve as seeds | 48 |
| Total (binary, failing-dylib) pairs | 0 |

Full detail: [`load-time-dependents.csv`](load-time-dependents.csv) (one row per `(binary, linked_failing_dylib)` pair).
## Build-time dependents

Packages whose nix expression **directly declares** a direct-failing package as `buildInputs`, `nativeBuildInputs`, `checkInputs`, or `nativeCheckInputs` (1-hop). If the failing binary is invoked during the package's build phase, Hydra fails and the package never reaches the cache. This is a graph-level relationship: whether each listed package actually invokes the failing binary during build is not statically determinable. The canonical confirmed case is direnv — its `nativeCheckInputs = [ fish ]` with a `checkPhase` running `fish ./test/direnv-test.fish`, origin of [nixpkgs#507531](https://github.com/NixOS/nixpkgs/issues/507531).

Default view excludes `propagatedBuildInputs` / `propagatedNativeBuildInputs` edges (propagation threads the input forward; the listed package itself doesn't invoke it). The CSV includes all edge kinds for manual inspection.

| Metric | Count |
|---|---:|
| Packages with failing seeds in declared build/check inputs (default view) | 11 |
| Total direct-edge rows (default view) | 11 |
| Total rows including propagated edges | 11 |
| Distinct failing seeds | 19 |

Edges by kind (default view only):

| Edge kind | Count |
|---|---:|
| `nativeBuildInputs` | 9 |
| `buildInputs` | 2 |

Top seed packages by downstream dependent count:

| Seed package | Downstream dependents |
|---|---:|
| `fish-4.2.1` | 10 |
| `Agda-2.8.0` | 1 |

Dependent packages (11): `bat-extras.batdiff`, `bat-extras.batman`, `bat-extras.batpipe`, `bat-extras.batwatch`, `bat-extras.core`, `bat-extras.prettybat`, `direnv`, `fish-lsp`, `haskellPackages.agda2hs`, `kitty`, `oh-my-fish`

Full detail: [`build-time-dependents.csv`](build-time-dependents.csv) (one row per `(dependent, edge_kind, seed)` tuple; `in_default_view=true` marks default-filter rows).

## Methodology

- Input: `store-paths.xz` from the channel release URL.
- Per path: `<hash>.narinfo` → stream NAR over HTTP → decompress (xz/zstd/bz2) inline → walk entries, no on-disk NAR persistence.
- Per regular file: peek 4 bytes; buffer and analyze only if Mach-O magic matches.
- Per Mach-O slice (thin or fat): parse `LC_CODE_SIGNATURE`, pick the primary CodeDirectory (SHA-256 preferred over SHA-1 when both are present, matching the kernel's selection order), recompute per-page hash over `data[i*ps : min((i+1)*ps, code_limit)]` with the CD's own algorithm, compare against the stored hash slot.
- `page_hash_mismatch` is defined as: at least one computed per-page hash disagrees with its stored hash slot. This matches the kernel's page-in validator and `codesign -v` rejection criterion for adhoc-signed binaries.
- `other_sig_invalid` is defined as: LC_CODE_SIGNATURE is present but the signature blob is structurally unparseable (e.g. payload OOB, bad SuperBlob magic, unsupported hash type such as SHA-384).
- Scanner source: see the PR repo.

