# NixOS/nixpkgs#507531 cache scan — nixpkgs-26.05-darwin @ 6062ba1a1b8b (2026-08-24)

Generated: 2026-08-24 08:19:47 UTC

## Summary

| Metric | Count |
|---|---:|
| Store paths scanned | 334,220 |
| Mach-O slices parsed | 465,377 |
| Page-hash mismatches (slices) | 123 |
| Page-hash mismatches (distinct packages) | 33 |
|   of which linker-signed (flags=0x20002) | 12 |
|   of which codesign-signed (flags=0x2) | 111 |
| Other signature-invalid (slices) | 0 |
| Other signature-invalid (distinct packages) | 0 |
| Type 2 — binaries linking a failing dylib | 0 |
| Type 2 — distinct packages | 0 |
| Type 3 — packages directly declaring a failing build input (default view) | 0 |

## By architecture

| Arch | Slices scanned | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned | Noise |
|---|---:|---:|---:|---:|---:|---:|
| `arm64` | 222,451 | 56 | 0 | 204,244 | 18,107 | 44 |
| `arm64e` | 130 | 0 | 0 | 50 | 0 | 80 |
| `x86_64` | 227,234 | 67 | 0 | 16,518 | 210,541 | 108 |
| `i386` | 378 | 0 | 0 | 226 | 148 | 4 |
| other/legacy (11 arch codes) | 15,184 | 0 | 0 | 4 | 16 | 15,164 |

## Fat vs thin Mach-O

| Kind | Slices | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned |
|---|---:|---:|---:|---:|---:|
| thin | 437,582 | 21 | 0 | 209,902 | 227,655 |
| fat | 27,795 | 102 | 0 | 11,140 | 1,157 |

Unique fat binary files: 21,290 in 1,222 packages. 12 of those packages contain at least one failing fat slice.

## Failing packages (page-hash mismatch)

Sorted alphabetically by package name.

| Package | Failing slices | Store path |
|---|---:|---|
| avalonia-ilspy-7.2-rc | 6 | `/nix/store/0idly66qjy09bncs64gl28xphwbg3nqf-avalonia-ilspy-7.2-rc` |
| avalonia-ilspy-7.2-rc | 6 | `/nix/store/3y4p51ky7ybivbj9pq0mp7n573mqlfr0-avalonia-ilspy-7.2-rc` |
| filen-cli-0.0.36 | 1 | `/nix/store/0r8fwgnqldbpzd65fayyaa1d7ik2z3lc-filen-cli-0.0.36` |
| filen-cli-0.0.36 | 1 | `/nix/store/w8g0rcna42xlvbsn5jlqhsgc7hilqlbv-filen-cli-0.0.36` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/iz59kqpk17w1dag1c2knnv8902wsd25h-gitlab-duo-8.89.0` |
| httptoolkit-1.26.0 | 1 | `/nix/store/f8916ng5b41vy8zipihapni7ggjkmskj-httptoolkit-1.26.0` |
| httptoolkit-1.26.0 | 1 | `/nix/store/in4scnwyz4hn7xalw4jjcwqmpf6vrk9r-httptoolkit-1.26.0` |
| libtorch-2.9.0 | 1 | `/nix/store/lh7hw0zhm2fxhwpqbv3qqyzh4qqac1p8-libtorch-2.9.0` |
| libtorch-2.9.0 | 1 | `/nix/store/r28bn7sm0i61lph6mnlcwdbwr4vdd48b-libtorch-2.9.0` |
| opencode-1.15.10 | 1 | `/nix/store/18jmwdml857xgwsnalfpy4922av79fzf-opencode-1.15.10` |
| opencode-1.15.10 | 1 | `/nix/store/9wrrk545kn212663a3f5h5qvd6icf3yd-opencode-1.15.10` |
| opencode-1.15.10 | 1 | `/nix/store/dfhfyi27m503mc3rlgvvf739pdd8lhba-opencode-1.15.10` |
| opencode-1.15.10 | 1 | `/nix/store/rnv5l1lm92bw9y76ac70i0iqs1y38yvd-opencode-1.15.10` |
| shogihome-1.29.0 | 1 | `/nix/store/2hsj528qqf0qndxfmlqhwv989w6b4n7s-shogihome-1.29.0` |
| shogihome-1.29.0 | 1 | `/nix/store/mssk554g3siy8nkidw8pjzrkr107xkjn-shogihome-1.29.0` |
| swift-5.10.1 | 11 | `/nix/store/58bsbdami1xih25pjrhvhqz9h03xyb1v-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/5caplwxxb1qnjscim7cks1isnyklwaf5-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/b41yiwffs6sggc7spsnhd9a43p13c9xy-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/m8sgnwz34mh7kwjxrzrpq1vzkd006ipg-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/mhb6cdkybdjjxwfpqh8js4bjwqlmimvv-swift-5.10.1` |
| swift-5.10.1-lib | 7 | `/nix/store/47647i01341gyqlnmcim9iyix1ibxgzr-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/gmrwrh1vjx65c9l0cqlc3lzm06ir1cj5-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/irc9hd7qxzygqdq5aqn351m8q1mn884p-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/slwncp9gqbshba7r059j7ac0z4cm10a6-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/wz5br160dmx8af0jp5y9vgkbyy9khnbh-swift-5.10.1-lib` |
| tailwindcss_4-4.3.1 | 1 | `/nix/store/27zcmbnd1ajsyagz46pm35z0hvl80bdz-tailwindcss_4-4.3.1` |
| tailwindcss_4-4.3.1 | 1 | `/nix/store/i196v0y1ikg78c782qi9qbjmr2pzia2l-tailwindcss_4-4.3.1` |
| teams-for-linux-2.11.1 | 1 | `/nix/store/gls3gcn5fia3l0157pkd0lvp3dbl3amm-teams-for-linux-2.11.1` |
| teams-for-linux-2.11.1 | 1 | `/nix/store/l2738npx9g9wsb587qqkyaxgdal928k6-teams-for-linux-2.11.1` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 1 | `/nix/store/4j2sgj1x9vc40x61iz99lriyzbz9lldn-vscode-extension-kilocode-Kilo-Code-7.2.20` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 1 | `/nix/store/8dl3r94rxjcjc3igap902ghjxh301wbc-vscode-extension-kilocode-Kilo-Code-7.2.20` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 1 | `/nix/store/k55s81c22s48gbnz8xzz5i45rdk358x7-vscode-extension-kilocode-Kilo-Code-7.2.20` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 1 | `/nix/store/z2xfrhnasqckxhaq3vpnnq4k9gd9jbcg-vscode-extension-kilocode-Kilo-Code-7.2.20` |

## Slice classification

| Category | Count |
|---|---:|
| `page_hash_mismatch` | 123 |
| `other_sig_invalid` | 0 |
| `clean` (signed, verified) | 221,042 |
| `unsigned` (Mach-O without LC_CODE_SIGNATURE) | 228,812 |
| `not_real_macho` (Java .class, PPC big-endian, etc.) | 15,400 |
| `scanner_error` | 0 |

## Load-time transitive broken binaries

Binaries whose own code signatures are valid but which dyld cannot map at process start because their `LC_LOAD_DYLIB` / `LC_LOAD_WEAK_DYLIB` / `LC_REEXPORT_DYLIB` points at a direct-failing dylib. These SIGKILL at load, before `main()` runs — deterministic per slice.

| Metric | Count |
|---|---:|
| Binaries that link at least one failing dylib | 0 |
| Distinct packages containing such binaries | 0 |
| Failing dylibs that serve as seeds | 98 |
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
| Distinct failing seeds | 33 |

Full detail: [`build-time-dependents.csv`](build-time-dependents.csv) (one row per `(dependent, edge_kind, seed)` tuple; `in_default_view=true` marks default-filter rows).

## Methodology

- Input: `store-paths.xz` from the channel release URL.
- Per path: `<hash>.narinfo` → stream NAR over HTTP → decompress (xz/zstd/bz2) inline → walk entries, no on-disk NAR persistence.
- Per regular file: peek 4 bytes; buffer and analyze only if Mach-O magic matches.
- Per Mach-O slice (thin or fat): parse `LC_CODE_SIGNATURE`, pick the primary CodeDirectory (SHA-256 preferred over SHA-1 when both are present, matching the kernel's selection order), recompute per-page hash over `data[i*ps : min((i+1)*ps, code_limit)]` with the CD's own algorithm, compare against the stored hash slot.
- `page_hash_mismatch` is defined as: at least one computed per-page hash disagrees with its stored hash slot. This matches the kernel's page-in validator and `codesign -v` rejection criterion for adhoc-signed binaries.
- `other_sig_invalid` is defined as: LC_CODE_SIGNATURE is present but the signature blob is structurally unparseable (e.g. payload OOB, bad SuperBlob magic, unsupported hash type such as SHA-384).
- Scanner source: see the PR repo.

