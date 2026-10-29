# NixOS/nixpkgs#507531 cache scan — release-26.05 @ 8d871ad73126 (2026-10-29)

Generated: 2026-10-29 07:37:48 UTC

## Summary

| Metric | Count |
|---|---:|
| Store paths scanned | 727,906 |
| Mach-O slices parsed | 781,906 |
| Page-hash mismatches (slices) | 165 |
| Page-hash mismatches (distinct packages) | 69 |
|   of which linker-signed (flags=0x20002) | 49 |
|   of which codesign-signed (flags=0x2) | 116 |
| Other signature-invalid (slices) | 0 |
| Other signature-invalid (distinct packages) | 0 |
| Type 2 — binaries linking a failing dylib | 0 |
| Type 2 — distinct packages | 0 |
| Type 3 — packages directly declaring a failing build input (default view) | 1 |

## By architecture

| Arch | Slices scanned | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned | Noise |
|---|---:|---:|---:|---:|---:|---:|
| `arm64` | 735,485 | 165 | 0 | 676,055 | 59,201 | 64 |
| `arm64e` | 337 | 0 | 0 | 109 | 0 | 228 |
| `x86_64` | 21,599 | 0 | 0 | 14,282 | 7,066 | 251 |
| `i386` | 464 | 0 | 0 | 241 | 217 | 6 |
| other/legacy (11 arch codes) | 24,021 | 0 | 0 | 24 | 48 | 23,949 |

## Fat vs thin Mach-O

| Kind | Slices | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned |
|---|---:|---:|---:|---:|---:|
| thin | 738,060 | 57 | 0 | 673,192 | 64,799 |
| fat | 43,846 | 108 | 0 | 17,519 | 1,733 |

Unique fat binary files: 33,696 in 1,994 packages. 12 of those packages contain at least one failing fat slice.

## Failing packages (page-hash mismatch)

Sorted alphabetically by package name.

| Package | Failing slices | Store path |
|---|---:|---|
| filen-cli-0.0.36 | 1 | `/nix/store/0r8fwgnqldbpzd65fayyaa1d7ik2z3lc-filen-cli-0.0.36` |
| filen-cli-0.0.36 | 1 | `/nix/store/n830q9qdkqd8wb50r5i5gc6vhfi35447-filen-cli-0.0.36` |
| filen-cli-0.0.36 | 1 | `/nix/store/ry4whmv7rirq6h23b1xfzfrr6k73n1sq-filen-cli-0.0.36` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/60zbrz834i5p0r0z181x0wfy9wg4fnwi-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/hkxwa89zsjaprxfqgfihmyip1n1avsrl-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/ilhfsqvskam95aidmxs75w63666lhxda-gitlab-duo-8.89.0` |
| httptoolkit-1.26.0 | 1 | `/nix/store/f8916ng5b41vy8zipihapni7ggjkmskj-httptoolkit-1.26.0` |
| httptoolkit-1.26.0 | 1 | `/nix/store/in4scnwyz4hn7xalw4jjcwqmpf6vrk9r-httptoolkit-1.26.0` |
| httptoolkit-1.26.0 | 1 | `/nix/store/kglqi3s566b97y0mp4jamgp153v710fi-httptoolkit-1.26.0` |
| httptoolkit-1.27.1 | 1 | `/nix/store/0mig56495glb099xx1yzlmbw454xhmlq-httptoolkit-1.27.1` |
| httptoolkit-1.27.1 | 1 | `/nix/store/23zjab0n5m33qfd1rqd99pfb0vngzm3z-httptoolkit-1.27.1` |
| httptoolkit-1.27.1 | 1 | `/nix/store/7a9zzfr8by69f107vnmikflygk7xcgpn-httptoolkit-1.27.1` |
| httptoolkit-1.27.1 | 1 | `/nix/store/9wp1shrsad0aws4g7619q3h5ld0cp9n3-httptoolkit-1.27.1` |
| httptoolkit-1.27.1 | 1 | `/nix/store/iq00sx2ybsd5sn5l2lp89ymp6dpm8la6-httptoolkit-1.27.1` |
| httptoolkit-1.27.1 | 1 | `/nix/store/x09cnkw5mrbwpi24xsr38691saccr7a6-httptoolkit-1.27.1` |
| libtorch-2.9.0 | 1 | `/nix/store/hclj167mjxz756a4irwl7w3ln0m996l5-libtorch-2.9.0` |
| libtorch-2.9.0 | 1 | `/nix/store/jxm3srv0dnhc20grghh56hycifsbvjaf-libtorch-2.9.0` |
| libtorch-2.9.0 | 1 | `/nix/store/lh7hw0zhm2fxhwpqbv3qqyzh4qqac1p8-libtorch-2.9.0` |
| libtorch-2.9.0 | 1 | `/nix/store/m0g6yfvzwfhzinms9pg5xcf3gm5mcxxx-libtorch-2.9.0` |
| libtorch-2.9.0 | 1 | `/nix/store/q130ghhjjwi675kjf7i8p2mwpylcwkpw-libtorch-2.9.0` |
| libtorch-2.9.0 | 1 | `/nix/store/r28bn7sm0i61lph6mnlcwdbwr4vdd48b-libtorch-2.9.0` |
| opencode-1.15.10 | 1 | `/nix/store/18jmwdml857xgwsnalfpy4922av79fzf-opencode-1.15.10` |
| opencode-1.15.10 | 1 | `/nix/store/44xkfcipvpwacbijj0aa0qxrsp779348-opencode-1.15.10` |
| opencode-1.15.10 | 1 | `/nix/store/7fwmgsh2zax604w9kpnxr6r55pw8jx6g-opencode-1.15.10` |
| opencode-1.15.10 | 1 | `/nix/store/9wrrk545kn212663a3f5h5qvd6icf3yd-opencode-1.15.10` |
| opencode-1.15.10 | 1 | `/nix/store/p5x7c6fdibscb7d55bzlm39sb4x6zxnl-opencode-1.15.10` |
| renovate-44.79.2 | 1 | `/nix/store/lsy6zjpskbmvjbfv142vw4ypdni8x76x-renovate-44.79.2` |
| renovate-44.79.2 | 1 | `/nix/store/pdx5zycp8pq3sclphybgdd1xq9qjgrl4-renovate-44.79.2` |
| shogihome-1.29.0 | 1 | `/nix/store/2hsj528qqf0qndxfmlqhwv989w6b4n7s-shogihome-1.29.0` |
| shogihome-1.29.0 | 1 | `/nix/store/95wlkqxq6wxslrhzqjdidj42cfz83l8m-shogihome-1.29.0` |
| shogihome-1.29.0 | 1 | `/nix/store/mssk554g3siy8nkidw8pjzrkr107xkjn-shogihome-1.29.0` |
| shogihome-1.29.1 | 1 | `/nix/store/akpvvjz4d3wqbayc88l43ncnafc2d9b0-shogihome-1.29.1` |
| shogihome-1.29.1 | 1 | `/nix/store/mccds0sai2mhpf9h2myzid1hwx87g03j-shogihome-1.29.1` |
| shogihome-1.29.1 | 1 | `/nix/store/q9cbh3hcdgmz5dnfy58gnlp6rjjmpirb-shogihome-1.29.1` |
| shogihome-1.29.1 | 1 | `/nix/store/yzm9xhns7w7av03avd71hcwb3wjznv4b-shogihome-1.29.1` |
| swift-5.10.1 | 11 | `/nix/store/5caplwxxb1qnjscim7cks1isnyklwaf5-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/b6j0s3xi3ynmfpblp7yfc988gfvc10im-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/d9zbhg9ziyhhx3fpqkra7bizx9vsmjk8-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/f5s3bcx03904sf2pqx7wgkfyg9dfi7xd-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/m8sgnwz34mh7kwjxrzrpq1vzkd006ipg-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/znyjxshv5i2xhyi19ja3i2zwsqxl323r-swift-5.10.1` |
| swift-5.10.1-lib | 7 | `/nix/store/1n6bby8i1dlwdrsyhcrykyldy2y7xqps-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/23xp0z2wa1vaaqxkfm2k0vrly2klqff6-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/ckspnycl8vzy37q525lr010ir9s4pqv9-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/slwncp9gqbshba7r059j7ac0z4cm10a6-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/wwz8xckkf5pxhjp605q2w9976wh77p5w-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/wz5br160dmx8af0jp5y9vgkbyy9khnbh-swift-5.10.1-lib` |
| tailwindcss_4-4.3.1 | 1 | `/nix/store/7j0iikv0gkh61bcqx1lzbpsbl08mwm4s-tailwindcss_4-4.3.1` |
| tailwindcss_4-4.3.1 | 1 | `/nix/store/d2kd5x80sgs8k4xw6yysd7qvhszagl59-tailwindcss_4-4.3.1` |
| tailwindcss_4-4.3.1 | 1 | `/nix/store/i196v0y1ikg78c782qi9qbjmr2pzia2l-tailwindcss_4-4.3.1` |
| tailwindcss_4-4.3.1 | 1 | `/nix/store/lcc2bchg50si03g3djl4wqd5lzrf1hdh-tailwindcss_4-4.3.1` |
| tailwindcss_4-4.3.1 | 1 | `/nix/store/zng32ingb4dldqaf1c36f0zqlcz17jzx-tailwindcss_4-4.3.1` |
| teams-for-linux-2.11.1 | 1 | `/nix/store/gls3gcn5fia3l0157pkd0lvp3dbl3amm-teams-for-linux-2.11.1` |
| teams-for-linux-2.11.1 | 1 | `/nix/store/l2738npx9g9wsb587qqkyaxgdal928k6-teams-for-linux-2.11.1` |
| teams-for-linux-2.17.1 | 1 | `/nix/store/4wqycxqf6r2mgjdx4p0arzax6s02sxfl-teams-for-linux-2.17.1` |
| teams-for-linux-2.17.1 | 1 | `/nix/store/jsb4s59mrx7kx6w5y8jpmdll72msz303-teams-for-linux-2.17.1` |
| teams-for-linux-2.22.0 | 1 | `/nix/store/1cga4x9wn0d0p8dq5d5zhyh50x4wz2hy-teams-for-linux-2.22.0` |
| teams-for-linux-2.22.0 | 1 | `/nix/store/4jzqm158wh2dd2abcsckkw48hf1n5x3c-teams-for-linux-2.22.0` |
| teams-for-linux-2.23.0 | 1 | `/nix/store/g51mdmhzazp10dp309f2accbwxh7w5fk-teams-for-linux-2.23.0` |
| teams-for-linux-2.25.0 | 1 | `/nix/store/1qv1yz8wl3dqs8rh1r0c5nzy6ivrhghb-teams-for-linux-2.25.0` |
| teams-for-linux-2.25.0 | 1 | `/nix/store/4kwfkpfkvbaxmxsha6nal27r8723fx6p-teams-for-linux-2.25.0` |
| teams-for-linux-2.25.0 | 1 | `/nix/store/axjjfhd4izws60sigb9fmcrkdvlhb5dn-teams-for-linux-2.25.0` |
| teams-for-linux-2.25.0 | 1 | `/nix/store/s5clv8n9gi844rc9384vwda8zcjfpirl-teams-for-linux-2.25.0` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 1 | `/nix/store/4j2sgj1x9vc40x61iz99lriyzbz9lldn-vscode-extension-kilocode-Kilo-Code-7.2.20` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 1 | `/nix/store/8dl3r94rxjcjc3igap902ghjxh301wbc-vscode-extension-kilocode-Kilo-Code-7.2.20` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 1 | `/nix/store/g1xpic0i2kymmviqv5n5wb91mvzpi2rm-vscode-extension-kilocode-Kilo-Code-7.2.20` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 1 | `/nix/store/iw0hy633a4xv5334j7slyvd9v7jvys86-vscode-extension-kilocode-Kilo-Code-7.2.20` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 1 | `/nix/store/qdahqy17jcg601fmzixxzv9hxckn1zb8-vscode-extension-kilocode-Kilo-Code-7.2.20` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 1 | `/nix/store/z68c59jkjhkg7c2dxaqxpryyfkksl5vx-vscode-extension-kilocode-Kilo-Code-7.2.20` |

## Slice classification

| Category | Count |
|---|---:|
| `page_hash_mismatch` | 165 |
| `other_sig_invalid` | 0 |
| `clean` (signed, verified) | 690,711 |
| `unsigned` (Mach-O without LC_CODE_SIGNATURE) | 66,532 |
| `not_real_macho` (Java .class, PPC big-endian, etc.) | 24,498 |
| `scanner_error` | 0 |

## Load-time transitive broken binaries

Binaries whose own code signatures are valid but which dyld cannot map at process start because their `LC_LOAD_DYLIB` / `LC_LOAD_WEAK_DYLIB` / `LC_REEXPORT_DYLIB` points at a direct-failing dylib. These SIGKILL at load, before `main()` runs — deterministic per slice.

| Metric | Count |
|---|---:|
| Binaries that link at least one failing dylib | 0 |
| Distinct packages containing such binaries | 0 |
| Failing dylibs that serve as seeds | 114 |
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
| Distinct failing seeds | 69 |

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

