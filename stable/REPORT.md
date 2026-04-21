# NixOS/nixpkgs#507531 cache scan — nixpkgs-25.11-darwin @ 7a8c107078da (2026-04-21)

Generated: 2026-04-21 12:11:17 UTC

## Summary

| Metric | Count |
|---|---:|
| Store paths scanned | 316,948 |
| Mach-O slices parsed | 412,486 |
| Page-hash mismatches (slices) | 130 |
| Page-hash mismatches (distinct packages) | 20 |
|   of which linker-signed (flags=0x20002) | 44 |
|   of which codesign-signed (flags=0x2) | 86 |
| Other signature-invalid (slices) | 2 |
| Other signature-invalid (distinct packages) | 1 |
| Tier 2 — binaries linking a failing dylib | 56 |
| Tier 2 — distinct packages | 37 |
| Tier 3 — packages directly declaring a failing build input (default view) | 11 |

## By architecture

| Arch | Slices scanned | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned | Noise |
|---|---:|---:|---:|---:|---:|---:|
| `arm64` | 193,379 | 88 | 0 | 180,077 | 13,177 | 37 |
| `arm64e` | 98 | 0 | 0 | 24 | 0 | 74 |
| `x86_64` | 205,551 | 42 | 2 | 14,890 | 190,498 | 119 |
| `i386` | 320 | 0 | 0 | 220 | 96 | 4 |
| other/legacy (10 arch codes) | 13,138 | 0 | 0 | 4 | 16 | 13,118 |

## Fat vs thin Mach-O

| Kind | Slices | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned |
|---|---:|---:|---:|---:|---:|
| thin | 388,281 | 46 | 2 | 185,411 | 202,818 |
| fat | 24,205 | 84 | 0 | 9,804 | 969 |

Unique fat binary files: 10,420 in 566 packages. 6 of those packages contain at least one failing fat slice.

## Failing packages (page-hash mismatch)

Sorted alphabetically by package name.

| Package | Failing slices | Store path |
|---|---:|---|
| Agda-2.8.0 | 2 | `/nix/store/45cc6ms1las7q0dxy7yfipnpxi5hz428-Agda-2.8.0` |
| Agda-2.8.0-bin | 4 | `/nix/store/6aay4gf46sxh49241gvnbkv4xdx4f7q1-Agda-2.8.0-bin` |
| arion-0.2.2.0 | 2 | `/nix/store/isimvgg2hxw945jhkr68rj75hj67qhqn-arion-0.2.2.0` |
| avalonia-ilspy-7.2-rc | 6 | `/nix/store/47ckid3m6rwzij933sy4kiwlkcb0llbn-avalonia-ilspy-7.2-rc` |
| avalonia-ilspy-7.2-rc | 6 | `/nix/store/l4d6aspbcs27mlisx97fhp0qdij3i39z-avalonia-ilspy-7.2-rc` |
| esy-0.8.0 | 2 | `/nix/store/bc5vpiddskrdnfc04fjh6irf3p1pw4bh-esy-0.8.0` |
| esy-0.8.0 | 2 | `/nix/store/rjwifh8vrg0acrw439w1nqcpl0lfkna0-esy-0.8.0` |
| ffmpeg-8.0-bin | 6 | `/nix/store/6a5nr567sb4a36lisa6gydpp3bfij1vv-ffmpeg-8.0-bin` |
| ffmpeg-8.0-lib | 14 | `/nix/store/hn58l3pvn5iwq87p6ddp9wsw8ai9dl93-ffmpeg-8.0-lib` |
| fish-4.2.1 | 2 | `/nix/store/gngn7y9mn510mf1hkmr0l69qbpvxfbfh-fish-4.2.1` |
| HCL-1.9 | 2 | `/nix/store/zhla7p947b07blrc231jj21i0q67cj1r-HCL-1.9` |
| httptoolkit-1.24.4 | 2 | `/nix/store/g505c34pkapf2qf5i1fq7h0bkkznl8bi-httptoolkit-1.24.4` |
| libtorch-2.9.0 | 2 | `/nix/store/3hrcgmdqmhmz309fqq2rkisgzlxqh6jq-libtorch-2.9.0` |
| shogihome-1.27.0 | 2 | `/nix/store/f1spwbbqpcpx4bcdbj21rbx3psxwzc4v-shogihome-1.27.0` |
| swift-5.10.1 | 22 | `/nix/store/2bgfmhdq533vvasjzrq53adjvpadwrjp-swift-5.10.1` |
| swift-5.10.1 | 22 | `/nix/store/sjij55a15h4s5gwy9r439l2yxip12mhm-swift-5.10.1` |
| swift-5.10.1-lib | 14 | `/nix/store/3y322ka7bccpcnqcbrq8saywa48c1pnj-swift-5.10.1-lib` |
| swift-5.10.1-lib | 14 | `/nix/store/f3qdyspn3vc661lxa11wnp03y10x8cpd-swift-5.10.1-lib` |
| tailwindcss_4-4.1.18 | 2 | `/nix/store/8wy6d88k17bwpgr8wa9f82pjmc6w4as9-tailwindcss_4-4.1.18` |
| teams-for-linux-2.8.0 | 2 | `/nix/store/rm4pn5zx4kpdg7am4pc6qymmhgm6wj38-teams-for-linux-2.8.0` |

## Appendix — other signature-invalid binaries

Slices where the scanner found a structural signature problem (not a page-hash mismatch). These also fail `codesign -v`. Mechanism may or may not be the same as NixOS/nixpkgs#507531.

| Package | Slices | Error kind | Store path |
|---|---:|---|---|
| tailwindcss_4-4.1.18 | 2 | LC_CODE_SIGNATURE payload OOB | `/nix/store/ffs5qadbvnf3vs66q0nzpdfw0rbqyc52-tailwindcss_4-4.1.18` |

## Slice classification

| Category | Count |
|---|---:|
| `page_hash_mismatch` | 130 |
| `other_sig_invalid` | 2 |
| `clean` (signed, verified) | 195,215 |
| `unsigned` (Mach-O without LC_CODE_SIGNATURE) | 203,787 |
| `not_real_macho` (Java .class, PPC big-endian, etc.) | 13,352 |
| `scanner_error` | 0 |

## Load-time transitive broken binaries

Binaries whose own code signatures are valid but which dyld cannot map at process start because their `LC_LOAD_DYLIB` / `LC_LOAD_WEAK_DYLIB` / `LC_REEXPORT_DYLIB` points at a direct-failing dylib. These SIGKILL at load, before `main()` runs — deterministic per slice.

| Metric | Count |
|---|---:|
| Binaries that link at least one failing dylib | 56 |
| Distinct packages containing such binaries | 37 |
| Failing dylibs that serve as seeds | 51 |
| Total (binary, failing-dylib) pairs | 451 |

Top failing dylibs by number of downstream binaries:

| Seed package | Downstream binaries |
|---|---:|
| `ffmpeg-8.0-lib` | 451 |

Dependent packages (37): `auto-editor-29.3.1`, `ccextractor-0.94-unstable-2025-05-20`, `contour-0.6.1.7494`, `corsix-th-0.69.2`, `ddnet-19.5`, `dosbox-x-2025.10.07`, `ffms-5.0`, `freerdp-3.23.0`, `harvid-0.9.1`, `keyfinder-cli-1.1.2`, `libopenshot-0.4.0`, `loudgain-0.6.8`, `megacmd-1.7.0`, `moc-2.6-alpha3-unstable-2019-09-14`, `moonlight-qt-6.1.0`, `mpd-0.24.6`, `netgen-6.2.2505`, `notcurses-3.0.17`, `opencv-4.12.0`, `opencv-4.12.0-package_tests`, `phira-unwrapped-0.6.7`, `pianobar-2024.12.21`, `pqiv-2.13.3`, `q2pro-0-unstable-2025-07-21`, `qtmultimedia-6.10.2`, `rsgain-3.6`, `scrcpy-3.3.4`, `spek-0.8.5`, `squeezelite-2.0.0.1541`, `survex-1.4.18`, `taterclient-ddnet-10.6.0`, `timg-1.6.3`, `vgmstream-2055`, `video-compare-20250928`, `vivictpp-1.3.1`, `vtk-9.5.2`, `wxsvg-1.5.25`

Full detail: [`load-time-dependents.csv`](load-time-dependents.csv) (one row per `(binary, linked_failing_dylib)` pair).
## Build-time dependents

Packages whose nix expression **directly declares** a direct-failing package as `buildInputs`, `nativeBuildInputs`, `checkInputs`, or `nativeCheckInputs` (1-hop). If the failing binary is invoked during the package's build phase, Hydra fails and the package never reaches the cache. This is a graph-level relationship: whether each listed package actually invokes the failing binary during build is not statically determinable. The canonical confirmed case is direnv — its `nativeCheckInputs = [ fish ]` with a `checkPhase` running `fish ./test/direnv-test.fish`, origin of [nixpkgs#507531](https://github.com/NixOS/nixpkgs/issues/507531).

Default view excludes `propagatedBuildInputs` / `propagatedNativeBuildInputs` edges (propagation threads the input forward; the listed package itself doesn't invoke it). The CSV includes all edge kinds for manual inspection.

| Metric | Count |
|---|---:|
| Packages with failing seeds in declared build/check inputs (default view) | 11 |
| Total direct-edge rows (default view) | 11 |
| Total rows including propagated edges | 11 |
| Distinct failing seeds | 20 |

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

