# NixOS/nixpkgs#507531 cache scan — nixpkgs-unstable @ b3da656039dc (2026-05-10)

Generated: 2026-05-10 08:39:00 UTC

## Summary

| Metric | Count |
|---|---:|
| Store paths scanned | 412,541 |
| Mach-O slices parsed | 298,010 |
| Page-hash mismatches (slices) | 67 |
| Page-hash mismatches (distinct packages) | 23 |
|   of which linker-signed (flags=0x20002) | 20 |
|   of which codesign-signed (flags=0x2) | 47 |
| Other signature-invalid (slices) | 0 |
| Other signature-invalid (distinct packages) | 0 |
| Type 2 — binaries linking a failing dylib | 7 |
| Type 2 — distinct packages | 5 |
| Type 3 — packages directly declaring a failing build input (default view) | 1 |

## By architecture

| Arch | Slices scanned | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned | Noise |
|---|---:|---:|---:|---:|---:|---:|
| `arm64` | 119,516 | 42 | 0 | 109,105 | 10,329 | 40 |
| `arm64e` | 65 | 0 | 0 | 25 | 0 | 40 |
| `x86_64` | 119,924 | 25 | 0 | 8,929 | 110,900 | 70 |
| `i386` | 353 | 0 | 0 | 141 | 204 | 8 |
| other/legacy (10 arch codes) | 58,152 | 0 | 0 | 2 | 65 | 58,085 |

## Fat vs thin Mach-O

| Kind | Slices | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned |
|---|---:|---:|---:|---:|---:|
| thin | 232,259 | 25 | 0 | 111,839 | 120,302 |
| fat | 65,751 | 42 | 0 | 6,363 | 1,196 |

Unique fat binary files: 61,735 in 1,079 packages. 5 of those packages contain at least one failing fat slice.

## Failing packages (page-hash mismatch)

Sorted alphabetically by package name.

| Package | Failing slices | Store path |
|---|---:|---|
| avalonia-ilspy-7.2-rc | 6 | `/nix/store/7mhskg5xn99f3y19qrkc71swg6rm663m-avalonia-ilspy-7.2-rc` |
| ffmpeg-headless-8.0.1-bin | 2 | `/nix/store/lg9r937b4q70s5qqvjhdkf7rnn5x4xvd-ffmpeg-headless-8.0.1-bin` |
| ffmpeg-headless-8.0.1-lib | 7 | `/nix/store/04iq3b9rv98l2grc82mh53w1br70ms1b-ffmpeg-headless-8.0.1-lib` |
| filen-cli-0.0.36 | 1 | `/nix/store/md6winyqwbjwq94fw7zj8jfjz9klxjhf-filen-cli-0.0.36` |
| filen-cli-0.0.36 | 1 | `/nix/store/mg7c9jnrr3704l55vjw6y55sgf0imhh1-filen-cli-0.0.36` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/aikmh7rgqwnrwawffpbdcvw0akf9nlbw-gitlab-duo-8.89.0` |
| gitlab-duo-8.89.0 | 1 | `/nix/store/w3jakkvd5dkaycb0b55z4hpgl0cfg8z4-gitlab-duo-8.89.0` |
| httptoolkit-1.24.4 | 1 | `/nix/store/47wl1p5bsk4c54r8vbkyhn3n2nm0588s-httptoolkit-1.24.4` |
| libtorch-2.9.0 | 1 | `/nix/store/vla1rdlyipmbynck3vq0vr51gij4fryk-libtorch-2.9.0` |
| mmsyn7ukr-array-0.3.0.0 | 1 | `/nix/store/ffmz0x0yik7jgrw0ljlmg1n6y041fh2x-mmsyn7ukr-array-0.3.0.0` |
| opencode-1.14.35 | 1 | `/nix/store/g1r8yb5n0k1kpy13k16a3vw8w6admpyi-opencode-1.14.35` |
| opencode-1.14.35 | 1 | `/nix/store/npqyfwp0j1172ypv11zmzx0qias179wd-opencode-1.14.35` |
| opencode-1.14.35 | 1 | `/nix/store/q95hrhjnsk49f6h70p0hym0a3pk73v9q-opencode-1.14.35` |
| shogihome-1.27.1 | 1 | `/nix/store/rhagbi0fyfqfnizrdhag5j6cmyqym4jx-shogihome-1.27.1` |
| swift-5.10.1 | 11 | `/nix/store/p1fpxz9l7rc91fzp0ckwrsxmizqmbvc1-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/qg9vqxfpaqq8cra97dpxk7l2ry1bsrax-swift-5.10.1` |
| swift-5.10.1-lib | 7 | `/nix/store/85sw2bgkpnqnsrj324cz61hxf7r57v5i-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/i7j1sls91fmn5vynqryfwhn463mv3jn0-swift-5.10.1-lib` |
| tailwindcss_4-4.2.4 | 1 | `/nix/store/36fkkxav9kvwn0g3571gf3cay92vwyix-tailwindcss_4-4.2.4` |
| tailwindcss_4-4.2.4 | 1 | `/nix/store/fpcmaqm4a8df6c38wzh5lz7s7d12178q-tailwindcss_4-4.2.4` |
| teams-for-linux-2.8.1 | 1 | `/nix/store/a36aakz4z3ihzamlvkq6384c3vqp8pcb-teams-for-linux-2.8.1` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 1 | `/nix/store/5p0fv320r59zjq0g8vdlszqc9m9a5cnc-vscode-extension-kilocode-Kilo-Code-7.2.20` |
| vscode-extension-kilocode-Kilo-Code-7.2.20 | 1 | `/nix/store/rriv3xrcfw1pw899n7x3q34ijfd5wis3-vscode-extension-kilocode-Kilo-Code-7.2.20` |

## Slice classification

| Category | Count |
|---|---:|
| `page_hash_mismatch` | 67 |
| `other_sig_invalid` | 0 |
| `clean` (signed, verified) | 118,202 |
| `unsigned` (Mach-O without LC_CODE_SIGNATURE) | 121,498 |
| `not_real_macho` (Java .class, PPC big-endian, etc.) | 58,243 |
| `scanner_error` | 0 |

## Load-time transitive broken binaries

Binaries whose own code signatures are valid but which dyld cannot map at process start because their `LC_LOAD_DYLIB` / `LC_LOAD_WEAK_DYLIB` / `LC_REEXPORT_DYLIB` points at a direct-failing dylib. These SIGKILL at load, before `main()` runs — deterministic per slice.

| Metric | Count |
|---|---:|
| Binaries that link at least one failing dylib | 7 |
| Distinct packages containing such binaries | 5 |
| Failing dylibs that serve as seeds | 48 |
| Total (binary, failing-dylib) pairs | 70 |

Top failing dylibs by number of downstream binaries:

| Seed package | Downstream binaries |
|---|---:|
| `ffmpeg-headless-8.0.1-lib` | 70 |

Dependent packages (5): `cliairplay-1.1-unstable-2026-03-16`, `cyanrip-0.9.3.1`, `ffmpegthumbnailer-2.3.0`, `gst-libav-1.26.11`, `musikcube-3.0.5`

Full detail: [`load-time-dependents.csv`](load-time-dependents.csv) (one row per `(binary, linked_failing_dylib)` pair).
## Build-time dependents

Packages whose nix expression **directly declares** a direct-failing package as `buildInputs`, `nativeBuildInputs`, `checkInputs`, or `nativeCheckInputs` (1-hop). If the failing binary is invoked during the package's build phase, Hydra fails and the package never reaches the cache. This is a graph-level relationship: whether each listed package actually invokes the failing binary during build is not statically determinable. The canonical confirmed case is direnv — its `nativeCheckInputs = [ fish ]` with a `checkPhase` running `fish ./test/direnv-test.fish`, origin of [nixpkgs#507531](https://github.com/NixOS/nixpkgs/issues/507531).

Default view excludes `propagatedBuildInputs` / `propagatedNativeBuildInputs` edges (propagation threads the input forward; the listed package itself doesn't invoke it). The CSV includes all edge kinds for manual inspection.

| Metric | Count |
|---|---:|
| Packages with failing seeds in declared build/check inputs (default view) | 1 |
| Total direct-edge rows (default view) | 1 |
| Total rows including propagated edges | 2 |
| Distinct failing seeds | 23 |

Edges by kind (default view only):

| Edge kind | Count |
|---|---:|
| `nativeBuildInputs` | 1 |

Top seed packages by downstream dependent count:

| Seed package | Downstream dependents |
|---|---:|
| `tailwindcss_4-4.2.4` | 1 |

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

