# NixOS/nixpkgs#507531 cache scan — nixpkgs-unstable @ 4100e830e085 (2026-05-29)

Generated: 2026-05-29 08:32:09 UTC

## Summary

| Metric | Count |
|---|---:|
| Store paths scanned | 924,820 |
| Mach-O slices parsed | 692,702 |
| Page-hash mismatches (slices) | 144 |
| Page-hash mismatches (distinct packages) | 63 |
|   of which linker-signed (flags=0x20002) | 45 |
|   of which codesign-signed (flags=0x2) | 99 |
| Other signature-invalid (slices) | 0 |
| Other signature-invalid (distinct packages) | 0 |
| Type 2 — binaries linking a failing dylib | 7 |
| Type 2 — distinct packages | 5 |
| Type 3 — packages directly declaring a failing build input (default view) | 2 |

## By architecture

| Arch | Slices scanned | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned | Noise |
|---|---:|---:|---:|---:|---:|---:|
| `arm64` | 284,284 | 89 | 0 | 259,472 | 24,631 | 92 |
| `arm64e` | 130 | 0 | 0 | 50 | 0 | 80 |
| `x86_64` | 284,000 | 55 | 0 | 19,490 | 264,306 | 149 |
| `i386` | 802 | 0 | 0 | 279 | 503 | 20 |
| other/legacy (11 arch codes) | 123,486 | 0 | 0 | 6 | 123 | 123,357 |

## Fat vs thin Mach-O

| Kind | Slices | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned |
|---|---:|---:|---:|---:|---:|
| thin | 550,516 | 60 | 0 | 263,967 | 286,306 |
| fat | 142,186 | 84 | 0 | 15,330 | 3,257 |

Unique fat binary files: 132,393 in 2,827 packages. 10 of those packages contain at least one failing fat slice.

## Failing packages (page-hash mismatch)

Sorted alphabetically by package name.

| Package | Failing slices | Store path |
|---|---:|---|
| avalonia-ilspy-7.2-rc | 6 | `/nix/store/7mhskg5xn99f3y19qrkc71swg6rm663m-avalonia-ilspy-7.2-rc` |
| avalonia-ilspy-7.2-rc | 6 | `/nix/store/lxabgj4a939bv2s4wdxjrgb3yqfq4yjj-avalonia-ilspy-7.2-rc` |
| ffmpeg-headless-8.0.1-bin | 2 | `/nix/store/lg9r937b4q70s5qqvjhdkf7rnn5x4xvd-ffmpeg-headless-8.0.1-bin` |
| ffmpeg-headless-8.0.1-lib | 7 | `/nix/store/04iq3b9rv98l2grc82mh53w1br70ms1b-ffmpeg-headless-8.0.1-lib` |
| filen-cli-0.0.36 | 1 | `/nix/store/5595x11jf389bj955gngxzpx11lara5n-filen-cli-0.0.36` |
| filen-cli-0.0.36 | 1 | `/nix/store/md6winyqwbjwq94fw7zj8jfjz9klxjhf-filen-cli-0.0.36` |
| filen-cli-0.0.36 | 1 | `/nix/store/mg7c9jnrr3704l55vjw6y55sgf0imhh1-filen-cli-0.0.36` |
| filen-cli-0.0.36 | 1 | `/nix/store/yv5dpd687w0qkkk829861cb3g9diq8zs-filen-cli-0.0.36` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/1xakdirg2mk3pk1qpyrk5p1hqs6m7yaq-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/516v4myw7xx03knkf3alcn62j7lcac37-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/6pzd3yz3x8ib4vv4ky9i8v00q8q2nd5w-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/6v6qv6c6ix4pdshb00i4w476b9svaffi-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/73sbgp26iy1v29ygq3yf07x4ckmim21w-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/8acx3f6s0dnwizwbv74f0x5zdvah0dvv-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/aikmh7rgqwnrwawffpbdcvw0akf9nlbw-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/c8i3ml8rqbrmxpwc1p6cmxpjzllg9gw9-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/jq1vw06zzsy83i1x4f13zf60168psbqb-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/r91sl334r0k4f7f73k0g8r3in62kj212-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/vijmlhfcw3n8bil836rwz1k0jnwfqab2-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/w3jakkvd5dkaycb0b55z4hpgl0cfg8z4-gitlab-duo-8.89.0` |
| httptoolkit-1.24.4 | 1 | `/nix/store/2s8sjmvjwammxn1kmxh65xz96qdhvzhs-httptoolkit-1.24.4` |
| httptoolkit-1.24.4 | 1 | `/nix/store/47wl1p5bsk4c54r8vbkyhn3n2nm0588s-httptoolkit-1.24.4` |
| httptoolkit-1.24.4 | 1 | `/nix/store/rjxrkxzfp47bskl0543cakbx80indwm1-httptoolkit-1.24.4` |
| httptoolkit-1.26.0 | 1 | `/nix/store/x5l1x55hk5qvgiwshl5bakr7n2sj4ndr-httptoolkit-1.26.0` |
| libtorch-2.9.0 | 1 | `/nix/store/jd0fnglnhz9pf6vyqsdl22z65cidmz21-libtorch-2.9.0` |
| libtorch-2.9.0 | 1 | `/nix/store/vla1rdlyipmbynck3vq0vr51gij4fryk-libtorch-2.9.0` |
| mmsyn7ukr-array-0.3.0.0 | 1 | `/nix/store/ffmz0x0yik7jgrw0ljlmg1n6y041fh2x-mmsyn7ukr-array-0.3.0.0` |
| opencode-1.14.35 | 1 | `/nix/store/g1r8yb5n0k1kpy13k16a3vw8w6admpyi-opencode-1.14.35` |
| opencode-1.14.35 | 1 | `/nix/store/npqyfwp0j1172ypv11zmzx0qias179wd-opencode-1.14.35` |
| opencode-1.14.35 | 1 | `/nix/store/q95hrhjnsk49f6h70p0hym0a3pk73v9q-opencode-1.14.35` |
| opencode-1.14.48 | 1 | `/nix/store/js2z13p2d8ym7j3x6dx58vdkk2z36bpa-opencode-1.14.48` |
| opencode-1.15.10 | 1 | `/nix/store/wlwjm1g4qgqpnxkddzrxkz0wbgwjcj5p-opencode-1.15.10` |
| opencode-1.15.11 | 1 | `/nix/store/cpc1xsvv08azx11c8y6zp68xv1czdkfr-opencode-1.15.11` |
| opencode-1.15.5 | 1 | `/nix/store/r0xz5ic3z79r3anfssz60j8bbjls6n4d-opencode-1.15.5` |
| opencode-1.15.7 | 1 | `/nix/store/swvx6k42qawwj376byi0fxjiy3yf9yb9-opencode-1.15.7` |
| shogihome-1.27.1 | 1 | `/nix/store/rhagbi0fyfqfnizrdhag5j6cmyqym4jx-shogihome-1.27.1` |
| shogihome-1.27.2 | 1 | `/nix/store/1cwb73vi5aa1nlpbr7ychywlbmkpl19l-shogihome-1.27.2` |
| shogihome-1.27.2 | 1 | `/nix/store/5xvqqb06qb22vz2jfz8mn80w9ma2fzby-shogihome-1.27.2` |
| shogihome-1.27.3 | 1 | `/nix/store/63fx8404ppm6n773sdkcwvwhfwggai5g-shogihome-1.27.3` |
| stache-2.3.4 | 1 | `/nix/store/19vf8xbrlh0i4qqvqvvqpc1jxy1klvz8-stache-2.3.4` |
| swift-5.10.1 | 11 | `/nix/store/f7d3lcdzanmqw5icnxkgcx6kqha1ibif-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/g8ifnf6b7v65bp2hl78i5mrjc8kbblaw-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/p1fpxz9l7rc91fzp0ckwrsxmizqmbvc1-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/qg9vqxfpaqq8cra97dpxk7l2ry1bsrax-swift-5.10.1` |
| swift-5.10.1-lib | 7 | `/nix/store/1vpqmjivp6j62rcpkrr86pirpn12fzaq-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/85sw2bgkpnqnsrj324cz61hxf7r57v5i-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/h2zz94xy40rnil834vjvikkvrxcsc96n-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/i7j1sls91fmn5vynqryfwhn463mv3jn0-swift-5.10.1-lib` |
| tailwindcss_4-4.2.4 | 1 | `/nix/store/36fkkxav9kvwn0g3571gf3cay92vwyix-tailwindcss_4-4.2.4` |
| tailwindcss_4-4.2.4 | 1 | `/nix/store/fpcmaqm4a8df6c38wzh5lz7s7d12178q-tailwindcss_4-4.2.4` |
| tailwindcss_4-4.3.0 | 1 | `/nix/store/1ir3rnq4a4z963c81sz3mcab35jflm43-tailwindcss_4-4.3.0` |
| tailwindcss_4-4.3.0 | 1 | `/nix/store/8mfvp0gg4igjs62dj457rprvx0lnwxv2-tailwindcss_4-4.3.0` |
| tailwindcss_4-4.3.0 | 1 | `/nix/store/m01q2947z343bhqh59fdc1xzsi9ni8h9-tailwindcss_4-4.3.0` |
| tailwindcss_4-4.3.0 | 1 | `/nix/store/rcdpbw2hfzljsmvrdcjny1brix3xy1fv-tailwindcss_4-4.3.0` |
| teams-for-linux-2.10.0 | 1 | `/nix/store/4qsz50ns5gj04lvfbfjji53lxbqnw3fp-teams-for-linux-2.10.0` |
| teams-for-linux-2.10.0 | 1 | `/nix/store/q2dbgmblhxcc0dq5a5yv1adyz0i5hfzm-teams-for-linux-2.10.0` |
| teams-for-linux-2.8.1 | 1 | `/nix/store/a36aakz4z3ihzamlvkq6384c3vqp8pcb-teams-for-linux-2.8.1` |
| teams-for-linux-2.9.0 | 1 | `/nix/store/f1r0hs7dgi6wfv59ms698gnlv76n09wb-teams-for-linux-2.9.0` |
| teams-for-linux-2.9.0 | 1 | `/nix/store/kdjbkgsi89f7n9ldhfvfficl76593vlg-teams-for-linux-2.9.0` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 1 | `/nix/store/5p0fv320r59zjq0g8vdlszqc9m9a5cnc-vscode-extension-kilocode-Kilo-Code-7.2.20` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 1 | `/nix/store/pdf6h2gw3a1m466w03j4ibxrfbd289ms-vscode-extension-kilocode-Kilo-Code-7.2.20` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 1 | `/nix/store/pgpzrqgvw4h1285bhmvsxy7kcl7ivb74-vscode-extension-kilocode-Kilo-Code-7.2.20` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 1 | `/nix/store/rriv3xrcfw1pw899n7x3q34ijfd5wis3-vscode-extension-kilocode-Kilo-Code-7.2.20` |

## Slice classification

| Category | Count |
|---|---:|
| `page_hash_mismatch` | 144 |
| `other_sig_invalid` | 0 |
| `clean` (signed, verified) | 279,297 |
| `unsigned` (Mach-O without LC_CODE_SIGNATURE) | 289,563 |
| `not_real_macho` (Java .class, PPC big-endian, etc.) | 123,698 |
| `scanner_error` | 0 |

## Load-time transitive broken binaries

Binaries whose own code signatures are valid but which dyld cannot map at process start because their `LC_LOAD_DYLIB` / `LC_LOAD_WEAK_DYLIB` / `LC_REEXPORT_DYLIB` points at a direct-failing dylib. These SIGKILL at load, before `main()` runs — deterministic per slice.

| Metric | Count |
|---|---:|
| Binaries that link at least one failing dylib | 7 |
| Distinct packages containing such binaries | 5 |
| Failing dylibs that serve as seeds | 88 |
| Total (binary, failing-dylib) pairs | 153 |

Top failing dylibs by number of downstream binaries:

| Seed package | Downstream binaries |
|---|---:|
| `ffmpeg-headless-8.0.1-lib` | 153 |

Dependent packages (5): `cliairplay-1.1-unstable-2026-03-16`, `cyanrip-0.9.3.1`, `ffmpegthumbnailer-2.3.0`, `gst-libav-1.26.11`, `musikcube-3.0.5`

Full detail: [`load-time-dependents.csv`](load-time-dependents.csv) (one row per `(binary, linked_failing_dylib)` pair).
## Build-time dependents

Packages whose nix expression **directly declares** a direct-failing package as `buildInputs`, `nativeBuildInputs`, `checkInputs`, or `nativeCheckInputs` (1-hop). If the failing binary is invoked during the package's build phase, Hydra fails and the package never reaches the cache. This is a graph-level relationship: whether each listed package actually invokes the failing binary during build is not statically determinable. The canonical confirmed case is direnv — its `nativeCheckInputs = [ fish ]` with a `checkPhase` running `fish ./test/direnv-test.fish`, origin of [nixpkgs#507531](https://github.com/NixOS/nixpkgs/issues/507531).

Default view excludes `propagatedBuildInputs` / `propagatedNativeBuildInputs` edges (propagation threads the input forward; the listed package itself doesn't invoke it). The CSV includes all edge kinds for manual inspection.

| Metric | Count |
|---|---:|
| Packages with failing seeds in declared build/check inputs (default view) | 2 |
| Total direct-edge rows (default view) | 2 |
| Total rows including propagated edges | 5 |
| Distinct failing seeds | 63 |

Edges by kind (default view only):

| Edge kind | Count |
|---|---:|
| `buildInputs` | 1 |
| `nativeBuildInputs` | 1 |

Top seed packages by downstream dependent count:

| Seed package | Downstream dependents |
|---|---:|
| `stache-2.3.4` | 1 |
| `tailwindcss_4-4.3.0` | 1 |

Dependent packages (2): `haskellPackages.mmark-cli`, `rimgo`

Full detail: [`build-time-dependents.csv`](build-time-dependents.csv) (one row per `(dependent, edge_kind, seed)` tuple; `in_default_view=true` marks default-filter rows).

## Methodology

- Input: `store-paths.xz` from the channel release URL.
- Per path: `<hash>.narinfo` → stream NAR over HTTP → decompress (xz/zstd/bz2) inline → walk entries, no on-disk NAR persistence.
- Per regular file: peek 4 bytes; buffer and analyze only if Mach-O magic matches.
- Per Mach-O slice (thin or fat): parse `LC_CODE_SIGNATURE`, pick the primary CodeDirectory (SHA-256 preferred over SHA-1 when both are present, matching the kernel's selection order), recompute per-page hash over `data[i*ps : min((i+1)*ps, code_limit)]` with the CD's own algorithm, compare against the stored hash slot.
- `page_hash_mismatch` is defined as: at least one computed per-page hash disagrees with its stored hash slot. This matches the kernel's page-in validator and `codesign -v` rejection criterion for adhoc-signed binaries.
- `other_sig_invalid` is defined as: LC_CODE_SIGNATURE is present but the signature blob is structurally unparseable (e.g. payload OOB, bad SuperBlob magic, unsupported hash type such as SHA-384).
- Scanner source: see the PR repo.

