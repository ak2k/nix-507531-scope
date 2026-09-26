# NixOS/nixpkgs#507531 cache scan — nixpkgs-26.05-darwin @ 5157396cfd0b (2026-09-26)

Generated: 2026-09-26 07:32:38 UTC

## Summary

| Metric | Count |
|---|---:|
| Store paths scanned | 673,733 |
| Mach-O slices parsed | 976,810 |
| Page-hash mismatches (slices) | 247 |
| Page-hash mismatches (distinct packages) | 78 |
|   of which linker-signed (flags=0x20002) | 33 |
|   of which codesign-signed (flags=0x2) | 214 |
| Other signature-invalid (slices) | 0 |
| Other signature-invalid (distinct packages) | 0 |
| Type 2 — binaries linking a failing dylib | 0 |
| Type 2 — distinct packages | 0 |
| Type 3 — packages directly declaring a failing build input (default view) | 1 |

## By architecture

| Arch | Slices scanned | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned | Noise |
|---|---:|---:|---:|---:|---:|---:|
| `arm64` | 469,555 | 126 | 0 | 431,207 | 38,132 | 90 |
| `arm64e` | 260 | 0 | 0 | 100 | 0 | 160 |
| `x86_64` | 475,620 | 121 | 0 | 33,982 | 441,300 | 217 |
| `i386` | 783 | 0 | 0 | 452 | 323 | 8 |
| other/legacy (11 arch codes) | 30,592 | 0 | 0 | 8 | 32 | 30,552 |

## Fat vs thin Mach-O

| Kind | Slices | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned |
|---|---:|---:|---:|---:|---:|
| thin | 919,990 | 55 | 0 | 442,761 | 477,166 |
| fat | 56,820 | 192 | 0 | 22,988 | 2,621 |

Unique fat binary files: 43,296 in 2,640 packages. 23 of those packages contain at least one failing fat slice.

## Failing packages (page-hash mismatch)

Sorted alphabetically by package name.

| Package | Failing slices | Store path |
|---|---:|---|
| avalonia-ilspy-7.2-rc | 6 | `/nix/store/0idly66qjy09bncs64gl28xphwbg3nqf-avalonia-ilspy-7.2-rc` |
| avalonia-ilspy-7.2-rc | 6 | `/nix/store/2xpppd83pm1fmnm3h8gh5knwryxs6b3v-avalonia-ilspy-7.2-rc` |
| avalonia-ilspy-7.2-rc | 6 | `/nix/store/3y4p51ky7ybivbj9pq0mp7n573mqlfr0-avalonia-ilspy-7.2-rc` |
| avalonia-ilspy-7.2-rc | 6 | `/nix/store/ji5n2hj8x48dv1hxmx5mjwhvgd4zi4rs-avalonia-ilspy-7.2-rc` |
| avalonia-ilspy-7.2-rc | 6 | `/nix/store/xd1541snfzngnzwxll45msgff8b8gknv-avalonia-ilspy-7.2-rc` |
| filen-cli-0.0.36 | 1 | `/nix/store/0r8fwgnqldbpzd65fayyaa1d7ik2z3lc-filen-cli-0.0.36` |
| filen-cli-0.0.36 | 1 | `/nix/store/9v55fbprhg44fv9k4si4qbg6xaw7pjaa-filen-cli-0.0.36` |
| filen-cli-0.0.36 | 1 | `/nix/store/bafdp93s5pn591gxh96dynw54akmg0b7-filen-cli-0.0.36` |
| filen-cli-0.0.36 | 1 | `/nix/store/vrfabd48b3h6wi2dw16k21jzrqvr124a-filen-cli-0.0.36` |
| filen-cli-0.0.36 | 1 | `/nix/store/w8g0rcna42xlvbsn5jlqhsgc7hilqlbv-filen-cli-0.0.36` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/45sv48r91qgzi3fjsgwaa4h8714j769z-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/4ib2g566mvdk2d21099f6bhyqxyghis5-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/iz59kqpk17w1dag1c2knnv8902wsd25h-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/mpv2h988nygbjdadrfi667rw87r0qf5y-gitlab-duo-8.89.0` |
| httptoolkit-1.26.0 | 1 | `/nix/store/f8916ng5b41vy8zipihapni7ggjkmskj-httptoolkit-1.26.0` |
| httptoolkit-1.26.0 | 1 | `/nix/store/in4scnwyz4hn7xalw4jjcwqmpf6vrk9r-httptoolkit-1.26.0` |
| httptoolkit-1.27.1 | 1 | `/nix/store/23zjab0n5m33qfd1rqd99pfb0vngzm3z-httptoolkit-1.27.1` |
| httptoolkit-1.27.1 | 1 | `/nix/store/7a9zzfr8by69f107vnmikflygk7xcgpn-httptoolkit-1.27.1` |
| httptoolkit-1.27.1 | 1 | `/nix/store/bl45i4hnmy4xg7vcg9y4lf1gnqsi2cmw-httptoolkit-1.27.1` |
| libtorch-2.9.0 | 1 | `/nix/store/jxm3srv0dnhc20grghh56hycifsbvjaf-libtorch-2.9.0` |
| libtorch-2.9.0 | 1 | `/nix/store/lh7hw0zhm2fxhwpqbv3qqyzh4qqac1p8-libtorch-2.9.0` |
| libtorch-2.9.0 | 1 | `/nix/store/q130ghhjjwi675kjf7i8p2mwpylcwkpw-libtorch-2.9.0` |
| libtorch-2.9.0 | 1 | `/nix/store/r28bn7sm0i61lph6mnlcwdbwr4vdd48b-libtorch-2.9.0` |
| opencode-1.15.10 | 1 | `/nix/store/18jmwdml857xgwsnalfpy4922av79fzf-opencode-1.15.10` |
| opencode-1.15.10 | 1 | `/nix/store/44xkfcipvpwacbijj0aa0qxrsp779348-opencode-1.15.10` |
| opencode-1.15.10 | 1 | `/nix/store/7fwmgsh2zax604w9kpnxr6r55pw8jx6g-opencode-1.15.10` |
| opencode-1.15.10 | 1 | `/nix/store/9wrrk545kn212663a3f5h5qvd6icf3yd-opencode-1.15.10` |
| opencode-1.15.10 | 1 | `/nix/store/dfhfyi27m503mc3rlgvvf739pdd8lhba-opencode-1.15.10` |
| opencode-1.15.10 | 1 | `/nix/store/p5x7c6fdibscb7d55bzlm39sb4x6zxnl-opencode-1.15.10` |
| opencode-1.15.10 | 1 | `/nix/store/rnv5l1lm92bw9y76ac70i0iqs1y38yvd-opencode-1.15.10` |
| opencode-1.15.10 | 1 | `/nix/store/vkw7fd6j20w8ngkwi0mkfi0nn9prlapr-opencode-1.15.10` |
| renovate-44.79.2 | 1 | `/nix/store/grqiv3wddm3p2mzs5iakvdffrxhfj7an-renovate-44.79.2` |
| renovate-44.79.2 | 1 | `/nix/store/hmsgv9dcwymj9k72rvlg3c31xwc8350h-renovate-44.79.2` |
| renovate-44.79.2 | 1 | `/nix/store/jk1zlqaq7gdq7q6ppli8am75r524r2wl-renovate-44.79.2` |
| renovate-44.79.2 | 1 | `/nix/store/qgizxvxgb7j85hssr42m0wkmv7rh3j98-renovate-44.79.2` |
| shogihome-1.29.0 | 1 | `/nix/store/2hsj528qqf0qndxfmlqhwv989w6b4n7s-shogihome-1.29.0` |
| shogihome-1.29.0 | 1 | `/nix/store/2p6dqa178vs4dxiamkb3fsfbxv5jvl6b-shogihome-1.29.0` |
| shogihome-1.29.0 | 1 | `/nix/store/6019hnqs6wxxhjnyxgq5cyy0v8a9jhm6-shogihome-1.29.0` |
| shogihome-1.29.0 | 1 | `/nix/store/95wlkqxq6wxslrhzqjdidj42cfz83l8m-shogihome-1.29.0` |
| shogihome-1.29.0 | 1 | `/nix/store/mssk554g3siy8nkidw8pjzrkr107xkjn-shogihome-1.29.0` |
| swift-5.10.1 | 11 | `/nix/store/58bsbdami1xih25pjrhvhqz9h03xyb1v-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/5caplwxxb1qnjscim7cks1isnyklwaf5-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/b41yiwffs6sggc7spsnhd9a43p13c9xy-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/b6j0s3xi3ynmfpblp7yfc988gfvc10im-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/d9zbhg9ziyhhx3fpqkra7bizx9vsmjk8-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/g0k13ybkx22vrnlnsdnnwwv8639a8ca9-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/m8sgnwz34mh7kwjxrzrpq1vzkd006ipg-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/mhb6cdkybdjjxwfpqh8js4bjwqlmimvv-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/v3lby5bczj04g2m5v5jfg5yms4n4cxj7-swift-5.10.1` |
| swift-5.10.1-lib | 7 | `/nix/store/47647i01341gyqlnmcim9iyix1ibxgzr-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/ckspnycl8vzy37q525lr010ir9s4pqv9-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/gmrwrh1vjx65c9l0cqlc3lzm06ir1cj5-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/hq5lf91v8z5pp61gnwsmcq70k247qc31-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/irc9hd7qxzygqdq5aqn351m8q1mn884p-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/slwncp9gqbshba7r059j7ac0z4cm10a6-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/wwz8xckkf5pxhjp605q2w9976wh77p5w-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/wz5br160dmx8af0jp5y9vgkbyy9khnbh-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/zv9v2xv4xismvrp9rwsy4czqm5pi0hk6-swift-5.10.1-lib` |
| tailwindcss_4-4.3.1 | 1 | `/nix/store/27zcmbnd1ajsyagz46pm35z0hvl80bdz-tailwindcss_4-4.3.1` |
| tailwindcss_4-4.3.1 | 1 | `/nix/store/7j0iikv0gkh61bcqx1lzbpsbl08mwm4s-tailwindcss_4-4.3.1` |
| tailwindcss_4-4.3.1 | 1 | `/nix/store/d2kd5x80sgs8k4xw6yysd7qvhszagl59-tailwindcss_4-4.3.1` |
| tailwindcss_4-4.3.1 | 1 | `/nix/store/hj0jhinp9aisrz65anhwss4vnfl81mlw-tailwindcss_4-4.3.1` |
| tailwindcss_4-4.3.1 | 1 | `/nix/store/i196v0y1ikg78c782qi9qbjmr2pzia2l-tailwindcss_4-4.3.1` |
| tailwindcss_4-4.3.1 | 1 | `/nix/store/smw237jigl6xjsdbnwfsaz8gcdhd11rv-tailwindcss_4-4.3.1` |
| teams-for-linux-2.11.1 | 1 | `/nix/store/gls3gcn5fia3l0157pkd0lvp3dbl3amm-teams-for-linux-2.11.1` |
| teams-for-linux-2.11.1 | 1 | `/nix/store/l2738npx9g9wsb587qqkyaxgdal928k6-teams-for-linux-2.11.1` |
| teams-for-linux-2.17.1 | 1 | `/nix/store/4wqycxqf6r2mgjdx4p0arzax6s02sxfl-teams-for-linux-2.17.1` |
| teams-for-linux-2.17.1 | 1 | `/nix/store/jsb4s59mrx7kx6w5y8jpmdll72msz303-teams-for-linux-2.17.1` |
| teams-for-linux-2.22.0 | 1 | `/nix/store/1cga4x9wn0d0p8dq5d5zhyh50x4wz2hy-teams-for-linux-2.22.0` |
| teams-for-linux-2.22.0 | 1 | `/nix/store/4jzqm158wh2dd2abcsckkw48hf1n5x3c-teams-for-linux-2.22.0` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 1 | `/nix/store/4j2sgj1x9vc40x61iz99lriyzbz9lldn-vscode-extension-kilocode-Kilo-Code-7.2.20` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 1 | `/nix/store/8dl3r94rxjcjc3igap902ghjxh301wbc-vscode-extension-kilocode-Kilo-Code-7.2.20` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 1 | `/nix/store/h6lj87wg2waqrkgkc1fkiaaa2k4cafcc-vscode-extension-kilocode-Kilo-Code-7.2.20` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 1 | `/nix/store/k55s81c22s48gbnz8xzz5i45rdk358x7-vscode-extension-kilocode-Kilo-Code-7.2.20` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 1 | `/nix/store/qdahqy17jcg601fmzixxzv9hxckn1zb8-vscode-extension-kilocode-Kilo-Code-7.2.20` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 1 | `/nix/store/yfka18vhhs891gsnbvy4v9kbd0qhy9kv-vscode-extension-kilocode-Kilo-Code-7.2.20` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 1 | `/nix/store/z2xfrhnasqckxhaq3vpnnq4k9gd9jbcg-vscode-extension-kilocode-Kilo-Code-7.2.20` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 1 | `/nix/store/z68c59jkjhkg7c2dxaqxpryyfkksl5vx-vscode-extension-kilocode-Kilo-Code-7.2.20` |

## Slice classification

| Category | Count |
|---|---:|
| `page_hash_mismatch` | 247 |
| `other_sig_invalid` | 0 |
| `clean` (signed, verified) | 465,749 |
| `unsigned` (Mach-O without LC_CODE_SIGNATURE) | 479,787 |
| `not_real_macho` (Java .class, PPC big-endian, etc.) | 31,027 |
| `scanner_error` | 0 |

## Load-time transitive broken binaries

Binaries whose own code signatures are valid but which dyld cannot map at process start because their `LC_LOAD_DYLIB` / `LC_LOAD_WEAK_DYLIB` / `LC_REEXPORT_DYLIB` points at a direct-failing dylib. These SIGKILL at load, before `main()` runs — deterministic per slice.

| Metric | Count |
|---|---:|
| Binaries that link at least one failing dylib | 0 |
| Distinct packages containing such binaries | 0 |
| Failing dylibs that serve as seeds | 181 |
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
| Distinct failing seeds | 78 |

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

