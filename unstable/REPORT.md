# NixOS/nixpkgs#507531 cache scan — nixpkgs-unstable @ 00455b0a3690 (2026-09-24)

Generated: 2026-09-24 07:43:01 UTC

## Summary

| Metric | Count |
|---|---:|
| Store paths scanned | 1,212,628 |
| Mach-O slices parsed | 744,949 |
| Page-hash mismatches (slices) | 125 |
| Page-hash mismatches (distinct packages) | 61 |
|   of which linker-signed (flags=0x20002) | 39 |
|   of which codesign-signed (flags=0x2) | 86 |
| Other signature-invalid (slices) | 3 |
| Other signature-invalid (distinct packages) | 1 |
| Type 2 — binaries linking a failing dylib | 0 |
| Type 2 — distinct packages | 0 |
| Type 3 — packages directly declaring a failing build input (default view) | 1 |

## By architecture

| Arch | Slices scanned | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned | Noise |
|---|---:|---:|---:|---:|---:|---:|
| `arm64` | 523,925 | 125 | 0 | 487,040 | 36,646 | 114 |
| `arm64e` | 105 | 0 | 0 | 45 | 0 | 60 |
| `x86_64` | 25,895 | 0 | 2 | 10,753 | 14,986 | 154 |
| `i386` | 915 | 0 | 1 | 229 | 653 | 32 |
| other/legacy (14 arch codes) | 194,109 | 0 | 0 | 3 | 240 | 193,866 |

## Fat vs thin Mach-O

| Kind | Slices | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned |
|---|---:|---:|---:|---:|---:|
| thin | 531,135 | 53 | 3 | 481,929 | 48,788 |
| fat | 213,814 | 72 | 0 | 16,141 | 3,737 |

Unique fat binary files: 203,515 in 3,006 packages. 8 of those packages contain at least one failing fat slice.

## Failing packages (page-hash mismatch)

Sorted alphabetically by package name.

| Package | Failing slices | Store path |
|---|---:|---|
| filen-cli-0.0.36 | 1 | `/nix/store/5g52w7dv6mll9f37aqgl79mwwprmmbi4-filen-cli-0.0.36` |
| filen-cli-0.0.36 | 1 | `/nix/store/h3hiral71d200cywyklf3w2672q7fkfc-filen-cli-0.0.36` |
| filen-cli-0.0.36 | 1 | `/nix/store/x9lq8fx27pyy9rk8yhgwj5cgk4i6k5va-filen-cli-0.0.36` |
| gitlab-duo-9.6.0 | 1 | `/nix/store/cwvbp8klabprr1h57n6zmmh9z06r12gj-gitlab-duo-9.6.0` |
| httptoolkit-1.26.0 | 1 | `/nix/store/0dgwk9vdd4g1x8p4snq5zm68yl1lj7dj-httptoolkit-1.26.0` |
| httptoolkit-1.26.0 | 1 | `/nix/store/qpzcwid5hr9s91azg6fmwwwyqxfc25dq-httptoolkit-1.26.0` |
| httptoolkit-1.26.0 | 1 | `/nix/store/xi594ayfmlvbippjm2c8yd9xlyg0k548-httptoolkit-1.26.0` |
| httptoolkit-1.27.1 | 1 | `/nix/store/6hp6j1pbjvbxpwlia9x2sdjn1wgkg63h-httptoolkit-1.27.1` |
| httptoolkit-1.27.1 | 1 | `/nix/store/7zrz5z40yjkrhc8n6hh7f23bhrrxr915-httptoolkit-1.27.1` |
| httptoolkit-1.27.1 | 1 | `/nix/store/ag6v0cxzjq7dxywdjsw7bxmnv4sxvwgl-httptoolkit-1.27.1` |
| httptoolkit-1.27.1 | 1 | `/nix/store/favv764pxkhnw6cg44drbvpj9f4maknp-httptoolkit-1.27.1` |
| hunk-0.18.0 | 1 | `/nix/store/jkfdgl7bdd0dn5bcf2bqfzr37ymc05jd-hunk-0.18.0` |
| hunk-0.19.0 | 1 | `/nix/store/93zjdjlgzrynci7yqa6xnmbmdas1zn60-hunk-0.19.0` |
| hunk-0.20.1 | 1 | `/nix/store/sl1xbk7k4zswddrw8yak7wyc1dkg5z9m-hunk-0.20.1` |
| kilo-7.3.40 | 1 | `/nix/store/gmbringgqwny38w9dz61x2n6x67cww4q-kilo-7.3.40` |
| libtorch-2.9.0 | 1 | `/nix/store/1ax5gvpnbzgiwn4yab9b7ix7xdyx2kb5-libtorch-2.9.0` |
| libtorch-2.9.0 | 1 | `/nix/store/5gywyn45iw286c8888n15s8mz5gv5mmb-libtorch-2.9.0` |
| libtorch-2.9.0 | 1 | `/nix/store/l91spz32g5a5dzdcz18kb11a5b7xi9ks-libtorch-2.9.0` |
| renovate-44.104.0 | 1 | `/nix/store/4nik2aw4a45h5xss1snsciwj4kmij48y-renovate-44.104.0` |
| renovate-44.24.3 | 1 | `/nix/store/hj4hv32i4w8f2h6pr4cswhlbrlq3ny7p-renovate-44.24.3` |
| renovate-44.24.3 | 1 | `/nix/store/vk7chz9c70a60rdbjgk11fbg2231fi8i-renovate-44.24.3` |
| renovate-44.37.1 | 1 | `/nix/store/fzrbllw3wdv2c78h26wmhvw13gg43pym-renovate-44.37.1` |
| renovate-44.37.1 | 1 | `/nix/store/gbyl4z0pasqy2c4lrgghdyx4jayb1cqi-renovate-44.37.1` |
| renovate-44.37.1 | 1 | `/nix/store/gqfmfrh2clzjgc705ync1c6jvrscgjm0-renovate-44.37.1` |
| renovate-44.37.1 | 1 | `/nix/store/wlmcdc16gkl1m59s0fcgvwkwhb0mgp06-renovate-44.37.1` |
| renovate-44.52.0 | 1 | `/nix/store/ndryz6vdpz3if51vbs5nlqk9pg15mmpa-renovate-44.52.0` |
| renovate-44.52.0 | 1 | `/nix/store/slqcs1h1c3rzd191fqvzia6f1dndilki-renovate-44.52.0` |
| renovate-44.79.2 | 1 | `/nix/store/2903h4h6c1qiqkmm28ialr69p7zg60m1-renovate-44.79.2` |
| renovate-44.79.2 | 1 | `/nix/store/jf608vanjqrwi92fk5lm3d63871rh7ph-renovate-44.79.2` |
| shogihome-1.29.0 | 1 | `/nix/store/19j1vnlwm6w9csv4ra3mys4p2yx5nh9w-shogihome-1.29.0` |
| shogihome-1.29.0 | 1 | `/nix/store/5m2az6j0p8v55iy2mwpx8lqn1b7sfs76-shogihome-1.29.0` |
| shogihome-1.29.0 | 1 | `/nix/store/hhpgi8gmzrc2hbk2636pyhwaqw8f4zwp-shogihome-1.29.0` |
| shogihome-1.29.0 | 1 | `/nix/store/nn6fyhvds6fid5kxgrfz86siv2zpryd5-shogihome-1.29.0` |
| shogihome-1.29.0 | 1 | `/nix/store/z1nv52627m8d3m7pz3lb9sbhcjys79ff-shogihome-1.29.0` |
| shogihome-1.29.0 | 1 | `/nix/store/zjg8s4nbdrrga9y0d8y66rlc5ijy9wmb-shogihome-1.29.0` |
| swift-5.10.1 | 11 | `/nix/store/76a3zzly7172nxr5ap5sij6rgwh65hqd-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/axsf0q79gyf45lk6w2jyj15qf75g8fsi-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/hzx2wsx2jrakws0zh8zrb6hn6i379fl9-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/kizr84lcbyp2wpa4sxg8v0f3fzr3b2j1-swift-5.10.1` |
| swift-5.10.1-lib | 7 | `/nix/store/44h8zl9mm7vzq205n0fh9lwgs3gdsk5n-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/bw4gdz76gqi9bs03rkwmm7gzq8p3xd1m-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/y8nwl67lfi039720jxqy9yl89h775yxs-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/yn710d5q59c2j8y77w1cwbdvkh7x6jvq-swift-5.10.1-lib` |
| tailwindcss_4-4.3.3 | 1 | `/nix/store/46daiz6mhh2w2crwj46sh1ga9mav3sc7-tailwindcss_4-4.3.3` |
| tailwindcss_4-4.3.3 | 1 | `/nix/store/6x7ip1f8fzy0asljzdkvppa6427spp0h-tailwindcss_4-4.3.3` |
| tailwindcss_4-4.3.3 | 1 | `/nix/store/9g5rzbap9317df9vmzmlwgbmpqjc6i8i-tailwindcss_4-4.3.3` |
| teams-for-linux-2.14.1 | 1 | `/nix/store/v7bib0qncfr3p0vgwbgh785rgl5k19p5-teams-for-linux-2.14.1` |
| teams-for-linux-2.15.0 | 1 | `/nix/store/wi3q2584mcl1ppbnlggz6y75d7gf14d2-teams-for-linux-2.15.0` |
| teams-for-linux-2.17.1 | 1 | `/nix/store/fiamlg04nh1qff6hlnp7gzkyq8r62q7k-teams-for-linux-2.17.1` |
| teams-for-linux-2.17.1 | 1 | `/nix/store/yi5yir902ma925v56qcbx0k5ij3vhnnf-teams-for-linux-2.17.1` |
| teams-for-linux-2.18.1 | 1 | `/nix/store/29qsm41lx49za1lbkf08zncc9dck7wsr-teams-for-linux-2.18.1` |
| teams-for-linux-2.18.1 | 1 | `/nix/store/5nf3qbb0qsd1f0yid237gfhp2awgmr0l-teams-for-linux-2.18.1` |
| teams-for-linux-2.18.1 | 1 | `/nix/store/arhpalvx6xqlk5lp9nvp1amh2h44y3c2-teams-for-linux-2.18.1` |
| teams-for-linux-2.18.1 | 1 | `/nix/store/i182gbab43ygnigcql012ch1j6x1g83k-teams-for-linux-2.18.1` |
| teams-for-linux-2.20.0 | 1 | `/nix/store/dg6fm7ba120j9z83nmy3iz2qaxy52dzs-teams-for-linux-2.20.0` |
| teams-for-linux-2.22.0 | 1 | `/nix/store/p0ykw3rx9pvz8dgd6hfw8mmhmwmrn3zq-teams-for-linux-2.22.0` |
| vscode-extension-kilocode-Kilo-Code-7.4.16 | 1 | `/nix/store/f2r9lh1sch92zfl1dd41b6cvp6hzj4v7-vscode-extension-kilocode-Kilo-Code-7.4.16` |
| vscode-extension-kilocode-Kilo-Code-7.4.16 | 1 | `/nix/store/smhfspqikyayf45jpz86rj9lbi6lmyc7-vscode-extension-kilocode-Kilo-Code-7.4.16` |
| vscode-extension-kilocode-Kilo-Code-7.5.9 | 1 | `/nix/store/hdlfqcx3g1z1wqjh7cyy1krj1wsbqdbi-vscode-extension-kilocode-Kilo-Code-7.5.9` |
| vscode-extension-kilocode-Kilo-Code-7.5.9 | 1 | `/nix/store/p870rfga3rj44l6xwlpkrrcsbnfykkga-vscode-extension-kilocode-Kilo-Code-7.5.9` |
| vscode-extension-kilocode-Kilo-Code-7.6.2 | 1 | `/nix/store/i5jz403qbcz2v4hngx58vggxlsjnknhm-vscode-extension-kilocode-Kilo-Code-7.6.2` |

## Appendix — other signature-invalid binaries

Slices where the scanner found a structural signature problem (not a page-hash mismatch). These also fail `codesign -v`. Mechanism may or may not be the same as NixOS/nixpkgs#507531.

| Package | Slices | Error kind | Store path |
|---|---:|---|---|
| cvs-export | 3 | bad SuperBlob magic 0x00000000, bad SuperBlob magic 0x28000000, signature blob too small | `/nix/store/k2sl4knvf6qv31lzchazlbslsm3jzsgc-cvs-export` |

## Slice classification

| Category | Count |
|---|---:|
| `page_hash_mismatch` | 125 |
| `other_sig_invalid` | 3 |
| `clean` (signed, verified) | 498,070 |
| `unsigned` (Mach-O without LC_CODE_SIGNATURE) | 52,525 |
| `not_real_macho` (Java .class, PPC big-endian, etc.) | 194,226 |
| `scanner_error` | 0 |

## Load-time transitive broken binaries

Binaries whose own code signatures are valid but which dyld cannot map at process start because their `LC_LOAD_DYLIB` / `LC_LOAD_WEAK_DYLIB` / `LC_REEXPORT_DYLIB` points at a direct-failing dylib. These SIGKILL at load, before `main()` runs — deterministic per slice.

| Metric | Count |
|---|---:|
| Binaries that link at least one failing dylib | 0 |
| Distinct packages containing such binaries | 0 |
| Failing dylibs that serve as seeds | 75 |
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
| Distinct failing seeds | 61 |

Edges by kind (default view only):

| Edge kind | Count |
|---|---:|
| `nativeBuildInputs` | 1 |

Top seed packages by downstream dependent count:

| Seed package | Downstream dependents |
|---|---:|
| `tailwindcss_4-4.3.3` | 1 |

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

