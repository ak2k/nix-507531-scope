# NixOS/nixpkgs#507531 cache scan — nixpkgs-unstable @ 6368eda62c97 (2026-04-29)

Generated: 2026-04-29 08:11:58 UTC

## Summary

| Metric | Count |
|---|---:|
| Store paths scanned | 1,108,640 |
| Mach-O slices parsed | 824,132 |
| Page-hash mismatches (slices) | 179 |
| Page-hash mismatches (distinct packages) | 39 |
|   of which linker-signed (flags=0x20002) | 41 |
|   of which codesign-signed (flags=0x2) | 138 |
| Other signature-invalid (slices) | 0 |
| Other signature-invalid (distinct packages) | 0 |
| Type 2 — binaries linking a failing dylib | 6 |
| Type 2 — distinct packages | 4 |
| Type 3 — packages directly declaring a failing build input (default view) | 1 |

## By architecture

| Arch | Slices scanned | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned | Noise |
|---|---:|---:|---:|---:|---:|---:|
| `arm64` | 322,895 | 107 | 0 | 296,976 | 25,707 | 105 |
| `arm64e` | 187 | 0 | 0 | 73 | 0 | 114 |
| `x86_64` | 329,114 | 72 | 0 | 26,236 | 302,582 | 224 |
| `i386` | 923 | 0 | 0 | 391 | 520 | 12 |
| other/legacy (10 arch codes) | 171,013 | 0 | 0 | 6 | 291 | 170,716 |

## Fat vs thin Mach-O

| Kind | Slices | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned |
|---|---:|---:|---:|---:|---:|
| thin | 631,373 | 53 | 0 | 305,054 | 325,997 |
| fat | 192,759 | 126 | 0 | 18,628 | 3,103 |

Unique fat binary files: 122,854 in 2,029 packages. 10 of those packages contain at least one failing fat slice.

## Failing packages (page-hash mismatch)

Sorted alphabetically by package name.

| Package | Failing slices | Store path |
|---|---:|---|
| avalonia-ilspy-7.2-rc | 6 | `/nix/store/5pmyw4c0gk169hbydyklyffxs1w2l65b-avalonia-ilspy-7.2-rc` |
| avalonia-ilspy-7.2-rc | 12 | `/nix/store/7mhskg5xn99f3y19qrkc71swg6rm663m-avalonia-ilspy-7.2-rc` |
| ffmpeg-headless-8.0.1-bin | 4 | `/nix/store/lg9r937b4q70s5qqvjhdkf7rnn5x4xvd-ffmpeg-headless-8.0.1-bin` |
| ffmpeg-headless-8.0.1-lib | 14 | `/nix/store/04iq3b9rv98l2grc82mh53w1br70ms1b-ffmpeg-headless-8.0.1-lib` |
| filen-cli-0.0.36 | 1 | `/nix/store/11z5q863nnsvg66zpzn7dn78rwz3xgbv-filen-cli-0.0.36` |
| filen-cli-0.0.36 | 1 | `/nix/store/9bl5v7src87m9b44v08fcnxxn8vmpa0z-filen-cli-0.0.36` |
| filen-cli-0.0.36 | 2 | `/nix/store/c11s5hhq6xw02sig44j3q3zdgjgi30hj-filen-cli-0.0.36` |
| filen-cli-0.0.36 | 2 | `/nix/store/g9nm6w6hhjkpvxfiraaalqr0srqp5f1m-filen-cli-0.0.36` |
| httptoolkit-1.24.4 | 1 | `/nix/store/1bshc8sryl7xm80jinkhrf9vpypcyzf5-httptoolkit-1.24.4` |
| httptoolkit-1.24.4 | 1 | `/nix/store/47wl1p5bsk4c54r8vbkyhn3n2nm0588s-httptoolkit-1.24.4` |
| httptoolkit-1.24.4 | 1 | `/nix/store/i7rj354mccdjhlm6k6njms8h2xpwxc25-httptoolkit-1.24.4` |
| libtorch-2.9.0 | 1 | `/nix/store/p5qnfspgh425s92a9z8wwkfyk73s8gsb-libtorch-2.9.0` |
| libtorch-2.9.0 | 2 | `/nix/store/vla1rdlyipmbynck3vq0vr51gij4fryk-libtorch-2.9.0` |
| mmsyn7ukr-array-0.3.0.0 | 2 | `/nix/store/ffmz0x0yik7jgrw0ljlmg1n6y041fh2x-mmsyn7ukr-array-0.3.0.0` |
| opencode-1.14.20 | 1 | `/nix/store/z8a22ifh1k2xvcpwyv6cgpfhdpgd54jw-opencode-1.14.20` |
| opencode-1.14.25 | 1 | `/nix/store/0yxaszqkv99ax46bws5a1galvnvly8s0-opencode-1.14.25` |
| opencode-1.4.6 | 1 | `/nix/store/rnaz29q7npfcb123qkrjdgi8yjyc8gv5-opencode-1.4.6` |
| shogihome-1.27.0 | 1 | `/nix/store/aczrg2ihvdcckis5bpcv12a915kvrjsk-shogihome-1.27.0` |
| shogihome-1.27.0 | 1 | `/nix/store/dw23a0njkwp54zv29hf2jmyhpanad8cs-shogihome-1.27.0` |
| shogihome-1.27.0 | 1 | `/nix/store/gzr3vs4fzwgsj2470qs86ss41mgha7k3-shogihome-1.27.0` |
| swift-5.10.1 | 11 | `/nix/store/9xyq2rnlkz59p7rwbxbp38r0b7n5980a-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/cm4qi9frxy6p73sq1nsh6p8892cc010w-swift-5.10.1` |
| swift-5.10.1 | 22 | `/nix/store/p1fpxz9l7rc91fzp0ckwrsxmizqmbvc1-swift-5.10.1` |
| swift-5.10.1 | 22 | `/nix/store/qg9vqxfpaqq8cra97dpxk7l2ry1bsrax-swift-5.10.1` |
| swift-5.10.1-lib | 14 | `/nix/store/85sw2bgkpnqnsrj324cz61hxf7r57v5i-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/hbw00ibnsqpr625mnih2hmzf8irkj0ns-swift-5.10.1-lib` |
| swift-5.10.1-lib | 14 | `/nix/store/i7j1sls91fmn5vynqryfwhn463mv3jn0-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/yqc83j7j1fdcwxhnrk6s8ijh94lkdfs2-swift-5.10.1-lib` |
| tailwindcss_4-4.2.2 | 1 | `/nix/store/dwn6ifdgpj3f4wlk269s7rk9zqwvhpja-tailwindcss_4-4.2.2` |
| tailwindcss_4-4.2.2 | 1 | `/nix/store/jp4vvsn2dv1a6mcdhz62pr5cj9c1nl33-tailwindcss_4-4.2.2` |
| tailwindcss_4-4.2.3 | 2 | `/nix/store/jx6iq19sxvk6x0fwia0snjgdabngpfsv-tailwindcss_4-4.2.3` |
| tailwindcss_4-4.2.3 | 2 | `/nix/store/q48kqycpi71pqqx40zhawkq2pjbil41m-tailwindcss_4-4.2.3` |
| teams-for-linux-2.8.0 | 1 | `/nix/store/7w06ks21c23yn5x98v1m92c5ranrgxa8-teams-for-linux-2.8.0` |
| teams-for-linux-2.8.0 | 1 | `/nix/store/bnwccwicg7rv5mcsczi7wwrw2bqn5bjk-teams-for-linux-2.8.0` |
| teams-for-linux-2.8.0 | 1 | `/nix/store/dll4aiqz9ryv6jnchb76dgww5fc5f55j-teams-for-linux-2.8.0` |
| vscode-extension-kilocode-Kilo-Code-7.2.0 | 1 | `/nix/store/1y5adw7jbwsy6v8zy2shcjn7wlhnm5l1-vscode-extension-kilocode-Kilo-Code-7.2.0` |
| vscode-extension-kilocode-Kilo-Code-7.2.0 | 1 | `/nix/store/gw6y9jk18hxz3inch9fznygcay23vqjh-vscode-extension-kilocode-Kilo-Code-7.2.0` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 2 | `/nix/store/5p0fv320r59zjq0g8vdlszqc9m9a5cnc-vscode-extension-kilocode-Kilo-Code-7.2.20` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 2 | `/nix/store/rriv3xrcfw1pw899n7x3q34ijfd5wis3-vscode-extension-kilocode-Kilo-Code-7.2.20` |

## Slice classification

| Category | Count |
|---|---:|
| `page_hash_mismatch` | 179 |
| `other_sig_invalid` | 0 |
| `clean` (signed, verified) | 323,682 |
| `unsigned` (Mach-O without LC_CODE_SIGNATURE) | 329,100 |
| `not_real_macho` (Java .class, PPC big-endian, etc.) | 171,171 |
| `scanner_error` | 0 |

## Load-time transitive broken binaries

Binaries whose own code signatures are valid but which dyld cannot map at process start because their `LC_LOAD_DYLIB` / `LC_LOAD_WEAK_DYLIB` / `LC_REEXPORT_DYLIB` points at a direct-failing dylib. These SIGKILL at load, before `main()` runs — deterministic per slice.

| Metric | Count |
|---|---:|
| Binaries that link at least one failing dylib | 6 |
| Distinct packages containing such binaries | 4 |
| Failing dylibs that serve as seeds | 88 |
| Total (binary, failing-dylib) pairs | 45 |

Top failing dylibs by number of downstream binaries:

| Seed package | Downstream binaries |
|---|---:|
| `ffmpeg-headless-8.0.1-lib` | 45 |

Dependent packages (4): `cyanrip-0.9.3.1`, `ffmpegthumbnailer-2.3.0`, `gst-libav-1.26.11`, `musikcube-3.0.5`

Full detail: [`load-time-dependents.csv`](load-time-dependents.csv) (one row per `(binary, linked_failing_dylib)` pair).
## Build-time dependents

Packages whose nix expression **directly declares** a direct-failing package as `buildInputs`, `nativeBuildInputs`, `checkInputs`, or `nativeCheckInputs` (1-hop). If the failing binary is invoked during the package's build phase, Hydra fails and the package never reaches the cache. This is a graph-level relationship: whether each listed package actually invokes the failing binary during build is not statically determinable. The canonical confirmed case is direnv — its `nativeCheckInputs = [ fish ]` with a `checkPhase` running `fish ./test/direnv-test.fish`, origin of [nixpkgs#507531](https://github.com/NixOS/nixpkgs/issues/507531).

Default view excludes `propagatedBuildInputs` / `propagatedNativeBuildInputs` edges (propagation threads the input forward; the listed package itself doesn't invoke it). The CSV includes all edge kinds for manual inspection.

| Metric | Count |
|---|---:|
| Packages with failing seeds in declared build/check inputs (default view) | 1 |
| Total direct-edge rows (default view) | 1 |
| Total rows including propagated edges | 2 |
| Distinct failing seeds | 39 |

Edges by kind (default view only):

| Edge kind | Count |
|---|---:|
| `nativeBuildInputs` | 1 |

Top seed packages by downstream dependent count:

| Seed package | Downstream dependents |
|---|---:|
| `tailwindcss_4-4.2.3` | 1 |

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

