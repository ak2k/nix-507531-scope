# NixOS/nixpkgs#507531 cache scan — release-26.05 @ 7486293a941f (2026-09-25)

Generated: 2026-09-25 07:40:44 UTC

## Summary

| Metric | Count |
|---|---:|
| Store paths scanned | 485,602 |
| Mach-O slices parsed | 476,567 |
| Page-hash mismatches (slices) | 100 |
| Page-hash mismatches (distinct packages) | 36 |
|   of which linker-signed (flags=0x20002) | 24 |
|   of which codesign-signed (flags=0x2) | 76 |
| Other signature-invalid (slices) | 0 |
| Other signature-invalid (distinct packages) | 0 |
| Type 2 — binaries linking a failing dylib | 0 |
| Type 2 — distinct packages | 0 |
| Type 3 — packages directly declaring a failing build input (default view) | 1 |

## By architecture

| Arch | Slices scanned | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned | Noise |
|---|---:|---:|---:|---:|---:|---:|
| `arm64` | 448,669 | 100 | 0 | 412,665 | 35,865 | 39 |
| `arm64e` | 229 | 0 | 0 | 77 | 0 | 152 |
| `x86_64` | 12,655 | 0 | 0 | 8,168 | 4,323 | 164 |
| `i386` | 317 | 0 | 0 | 175 | 139 | 3 |
| other/legacy (11 arch codes) | 14,697 | 0 | 0 | 15 | 31 | 14,651 |

## Fat vs thin Mach-O

| Kind | Slices | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned |
|---|---:|---:|---:|---:|---:|
| thin | 450,230 | 28 | 0 | 410,871 | 39,323 |
| fat | 26,337 | 72 | 0 | 10,229 | 1,035 |

Unique fat binary files: 20,348 in 1,224 packages. 8 of those packages contain at least one failing fat slice.

## Failing packages (page-hash mismatch)

Sorted alphabetically by package name.

| Package | Failing slices | Store path |
|---|---:|---|
| filen-cli-0.0.36 | 1 | `/nix/store/0r8fwgnqldbpzd65fayyaa1d7ik2z3lc-filen-cli-0.0.36` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/45sv48r91qgzi3fjsgwaa4h8714j769z-gitlab-duo-8.89.0` |
| httptoolkit-1.26.0 | 1 | `/nix/store/f8916ng5b41vy8zipihapni7ggjkmskj-httptoolkit-1.26.0` |
| httptoolkit-1.26.0 | 1 | `/nix/store/in4scnwyz4hn7xalw4jjcwqmpf6vrk9r-httptoolkit-1.26.0` |
| httptoolkit-1.26.0 | 1 | `/nix/store/kglqi3s566b97y0mp4jamgp153v710fi-httptoolkit-1.26.0` |
| httptoolkit-1.27.1 | 1 | `/nix/store/23zjab0n5m33qfd1rqd99pfb0vngzm3z-httptoolkit-1.27.1` |
| httptoolkit-1.27.1 | 1 | `/nix/store/bl45i4hnmy4xg7vcg9y4lf1gnqsi2cmw-httptoolkit-1.27.1` |
| libtorch-2.9.0 | 1 | `/nix/store/jxm3srv0dnhc20grghh56hycifsbvjaf-libtorch-2.9.0` |
| libtorch-2.9.0 | 1 | `/nix/store/lh7hw0zhm2fxhwpqbv3qqyzh4qqac1p8-libtorch-2.9.0` |
| libtorch-2.9.0 | 1 | `/nix/store/q130ghhjjwi675kjf7i8p2mwpylcwkpw-libtorch-2.9.0` |
| libtorch-2.9.0 | 1 | `/nix/store/r28bn7sm0i61lph6mnlcwdbwr4vdd48b-libtorch-2.9.0` |
| opencode-1.15.10 | 1 | `/nix/store/18jmwdml857xgwsnalfpy4922av79fzf-opencode-1.15.10` |
| opencode-1.15.10 | 1 | `/nix/store/7fwmgsh2zax604w9kpnxr6r55pw8jx6g-opencode-1.15.10` |
| opencode-1.15.10 | 1 | `/nix/store/9wrrk545kn212663a3f5h5qvd6icf3yd-opencode-1.15.10` |
| shogihome-1.29.0 | 1 | `/nix/store/2hsj528qqf0qndxfmlqhwv989w6b4n7s-shogihome-1.29.0` |
| shogihome-1.29.0 | 1 | `/nix/store/2p6dqa178vs4dxiamkb3fsfbxv5jvl6b-shogihome-1.29.0` |
| shogihome-1.29.0 | 1 | `/nix/store/6019hnqs6wxxhjnyxgq5cyy0v8a9jhm6-shogihome-1.29.0` |
| shogihome-1.29.0 | 1 | `/nix/store/95wlkqxq6wxslrhzqjdidj42cfz83l8m-shogihome-1.29.0` |
| shogihome-1.29.0 | 1 | `/nix/store/mssk554g3siy8nkidw8pjzrkr107xkjn-shogihome-1.29.0` |
| swift-5.10.1 | 11 | `/nix/store/5caplwxxb1qnjscim7cks1isnyklwaf5-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/b6j0s3xi3ynmfpblp7yfc988gfvc10im-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/d9zbhg9ziyhhx3fpqkra7bizx9vsmjk8-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/m8sgnwz34mh7kwjxrzrpq1vzkd006ipg-swift-5.10.1` |
| swift-5.10.1-lib | 7 | `/nix/store/ckspnycl8vzy37q525lr010ir9s4pqv9-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/slwncp9gqbshba7r059j7ac0z4cm10a6-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/wwz8xckkf5pxhjp605q2w9976wh77p5w-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/wz5br160dmx8af0jp5y9vgkbyy9khnbh-swift-5.10.1-lib` |
| tailwindcss_4-4.3.1 | 1 | `/nix/store/7j0iikv0gkh61bcqx1lzbpsbl08mwm4s-tailwindcss_4-4.3.1` |
| tailwindcss_4-4.3.1 | 1 | `/nix/store/d2kd5x80sgs8k4xw6yysd7qvhszagl59-tailwindcss_4-4.3.1` |
| tailwindcss_4-4.3.1 | 1 | `/nix/store/i196v0y1ikg78c782qi9qbjmr2pzia2l-tailwindcss_4-4.3.1` |
| teams-for-linux-2.11.1 | 1 | `/nix/store/gls3gcn5fia3l0157pkd0lvp3dbl3amm-teams-for-linux-2.11.1` |
| teams-for-linux-2.11.1 | 1 | `/nix/store/l2738npx9g9wsb587qqkyaxgdal928k6-teams-for-linux-2.11.1` |
| teams-for-linux-2.17.1 | 1 | `/nix/store/4wqycxqf6r2mgjdx4p0arzax6s02sxfl-teams-for-linux-2.17.1` |
| teams-for-linux-2.22.0 | 1 | `/nix/store/4jzqm158wh2dd2abcsckkw48hf1n5x3c-teams-for-linux-2.22.0` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 1 | `/nix/store/4j2sgj1x9vc40x61iz99lriyzbz9lldn-vscode-extension-kilocode-Kilo-Code-7.2.20` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 1 | `/nix/store/8dl3r94rxjcjc3igap902ghjxh301wbc-vscode-extension-kilocode-Kilo-Code-7.2.20` |

## Slice classification

| Category | Count |
|---|---:|
| `page_hash_mismatch` | 100 |
| `other_sig_invalid` | 0 |
| `clean` (signed, verified) | 421,100 |
| `unsigned` (Mach-O without LC_CODE_SIGNATURE) | 40,358 |
| `not_real_macho` (Java .class, PPC big-endian, etc.) | 15,009 |
| `scanner_error` | 0 |

## Load-time transitive broken binaries

Binaries whose own code signatures are valid but which dyld cannot map at process start because their `LC_LOAD_DYLIB` / `LC_LOAD_WEAK_DYLIB` / `LC_REEXPORT_DYLIB` points at a direct-failing dylib. These SIGKILL at load, before `main()` runs — deterministic per slice.

| Metric | Count |
|---|---:|
| Binaries that link at least one failing dylib | 0 |
| Distinct packages containing such binaries | 0 |
| Failing dylibs that serve as seeds | 76 |
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
| Distinct failing seeds | 36 |

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

