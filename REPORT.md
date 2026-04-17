# nixpkgs#507531 cache scan — nixpkgs-25.11-darwin @ 76410a99a2c5 (hydra eval 1824540)

Generated: 2026-04-17 20:51:31 UTC

## Summary

| Metric | Count |
|---|---:|
| Store paths scanned | 172,961 |
| Mach-O slices parsed | 223,604 |
| Page-hash mismatches (slices) | 65 |
| Page-hash mismatches (distinct packages) | 19 |
|   of which linker-signed (flags=0x20002) | 22 |
|   of which codesign-signed (flags=0x2) | 43 |
| Other signature-invalid (slices) | 1 |
| Other signature-invalid (distinct packages) | 1 |

## By architecture

| Arch | Slices scanned | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned | Noise |
|---|---:|---:|---:|---:|---:|---:|
| `arm64` | 104,719 | 44 | 0 | 96,881 | 7,776 | 18 |
| `arm64e` | 53 | 0 | 0 | 13 | 0 | 40 |
| `x86_64` | 111,176 | 21 | 1 | 8,160 | 102,931 | 63 |
| `i386` | 169 | 0 | 0 | 113 | 54 | 2 |
| other/legacy (10 arch codes) | 7,487 | 0 | 0 | 2 | 8 | 7,477 |

## Fat vs thin Mach-O

| Kind | Slices | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned |
|---|---:|---:|---:|---:|---:|
| thin | 210,325 | 23 | 1 | 100,039 | 110,260 |
| fat | 13,279 | 42 | 0 | 5,130 | 509 |

Unique fat binary files: 10,281 in 531 packages. 5 of those packages contain at least one failing fat slice.

## Failing packages (page-hash mismatch)

Sorted by number of failing slices.

| Package | Failing slices | Store path |
|---|---:|---|
| swift-5.10.1 | 11 | `/nix/store/2bgfmhdq533vvasjzrq53adjvpadwrjp-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/sjij55a15h4s5gwy9r439l2yxip12mhm-swift-5.10.1` |
| swift-5.10.1-lib | 7 | `/nix/store/3y322ka7bccpcnqcbrq8saywa48c1pnj-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/f3qdyspn3vc661lxa11wnp03y10x8cpd-swift-5.10.1-lib` |
| ffmpeg-8.0-lib | 7 | `/nix/store/hn58l3pvn5iwq87p6ddp9wsw8ai9dl93-ffmpeg-8.0-lib` |
| avalonia-ilspy-7.2-rc | 6 | `/nix/store/l4d6aspbcs27mlisx97fhp0qdij3i39z-avalonia-ilspy-7.2-rc` |
| ffmpeg-8.0-bin | 3 | `/nix/store/6a5nr567sb4a36lisa6gydpp3bfij1vv-ffmpeg-8.0-bin` |
| Agda-2.8.0-bin | 2 | `/nix/store/6aay4gf46sxh49241gvnbkv4xdx4f7q1-Agda-2.8.0-bin` |
| libtorch-2.9.0 | 1 | `/nix/store/3hrcgmdqmhmz309fqq2rkisgzlxqh6jq-libtorch-2.9.0` |
| Agda-2.8.0 | 1 | `/nix/store/45cc6ms1las7q0dxy7yfipnpxi5hz428-Agda-2.8.0` |
| tailwindcss_4-4.1.18 | 1 | `/nix/store/8wy6d88k17bwpgr8wa9f82pjmc6w4as9-tailwindcss_4-4.1.18` |
| esy-0.8.0 | 1 | `/nix/store/bc5vpiddskrdnfc04fjh6irf3p1pw4bh-esy-0.8.0` |
| shogihome-1.27.0 | 1 | `/nix/store/f1spwbbqpcpx4bcdbj21rbx3psxwzc4v-shogihome-1.27.0` |
| httptoolkit-1.24.4 | 1 | `/nix/store/g505c34pkapf2qf5i1fq7h0bkkznl8bi-httptoolkit-1.24.4` |
| fish-4.2.1 | 1 | `/nix/store/gngn7y9mn510mf1hkmr0l69qbpvxfbfh-fish-4.2.1` |
| arion-0.2.2.0 | 1 | `/nix/store/isimvgg2hxw945jhkr68rj75hj67qhqn-arion-0.2.2.0` |
| esy-0.8.0 | 1 | `/nix/store/rjwifh8vrg0acrw439w1nqcpl0lfkna0-esy-0.8.0` |
| teams-for-linux-2.8.0 | 1 | `/nix/store/rm4pn5zx4kpdg7am4pc6qymmhgm6wj38-teams-for-linux-2.8.0` |
| HCL-1.9 | 1 | `/nix/store/zhla7p947b07blrc231jj21i0q67cj1r-HCL-1.9` |

## Appendix — other signature-invalid binaries

Slices where the scanner found a structural signature problem (not a page-hash mismatch). These also fail `codesign -v`. Mechanism may or may not be the same as nixpkgs#507531.

| Package | Slices | Error kind | Store path |
|---|---:|---|---|
| tailwindcss_4-4.1.18 | 1 | LC_CODE_SIGNATURE payload OOB | `/nix/store/ffs5qadbvnf3vs66q0nzpdfw0rbqyc52-tailwindcss_4-4.1.18` |

## Slice classification

| Category | Count |
|---|---:|
| `page_hash_mismatch` | 65 |
| `other_sig_invalid` | 1 |
| `clean` (signed, verified) | 105,169 |
| `unsigned` (Mach-O without LC_CODE_SIGNATURE) | 110,769 |
| `not_real_macho` (Java .class, PPC big-endian, etc.) | 7,600 |
| `scanner_error` | 0 |

## Methodology

- Input: `store-paths.xz` from the channel release URL.
- Per path: `<hash>.narinfo` → stream NAR over HTTP → decompress (xz/zstd/bz2) inline → walk entries, no on-disk NAR persistence.
- Per regular file: peek 4 bytes; buffer and analyze only if Mach-O magic matches.
- Per Mach-O slice (thin or fat): parse `LC_CODE_SIGNATURE`, find the SHA-256 CodeDirectory, recompute per-page SHA-256 over `data[i*ps : min((i+1)*ps, code_limit)]`, compare against the stored hash slot.
- `page_hash_mismatch` is defined as: at least one computed per-page SHA-256 disagrees with its stored hash slot. This matches the kernel's page-in validator and `codesign -v` rejection criterion for adhoc-signed binaries.
- `other_sig_invalid` is defined as: LC_CODE_SIGNATURE is present but the signature blob is structurally unparseable (e.g. payload OOB, bad SuperBlob magic, unsupported hash type).
- Scanner source: see the PR repo.

