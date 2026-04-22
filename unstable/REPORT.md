# NixOS/nixpkgs#507531 cache scan — nixpkgs-unstable @ b86751bc4085 (2026-04-22)

Generated: 2026-04-22 07:32:38 UTC

## Summary

| Metric | Count |
|---|---:|
| Store paths scanned | 376,114 |
| Mach-O slices parsed | 286,182 |
| Page-hash mismatches (slices) | 53 |
| Page-hash mismatches (distinct packages) | 16 |
|   of which linker-signed (flags=0x20002) | 7 |
|   of which codesign-signed (flags=0x2) | 46 |
| Other signature-invalid (slices) | 0 |
| Other signature-invalid (distinct packages) | 0 |
| Type 2 — binaries linking a failing dylib | 0 |
| Type 2 — distinct packages | 0 |
| Type 3 — packages directly declaring a failing build input (default view) | 1 |

## By architecture

| Arch | Slices scanned | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned | Noise |
|---|---:|---:|---:|---:|---:|---:|
| `arm64` | 112,528 | 29 | 0 | 103,540 | 8,925 | 34 |
| `arm64e` | 65 | 0 | 0 | 25 | 0 | 40 |
| `x86_64` | 116,136 | 24 | 0 | 8,898 | 107,138 | 76 |
| `i386` | 310 | 0 | 0 | 131 | 175 | 4 |
| other/legacy (10 arch codes) | 57,143 | 0 | 0 | 2 | 98 | 57,043 |

## Fat vs thin Mach-O

| Kind | Slices | Page-hash mismatch | Other sig-invalid | Clean (signed) | Unsigned |
|---|---:|---:|---:|---:|---:|
| thin | 221,617 | 11 | 0 | 106,202 | 115,314 |
| fat | 64,565 | 42 | 0 | 6,394 | 1,022 |

Unique fat binary files: 60,616 in 903 packages. 5 of those packages contain at least one failing fat slice.

## Failing packages (page-hash mismatch)

Sorted alphabetically by package name.

| Package | Failing slices | Store path |
|---|---:|---|
| avalonia-ilspy-7.2-rc | 6 | `/nix/store/5pmyw4c0gk169hbydyklyffxs1w2l65b-avalonia-ilspy-7.2-rc` |
| filen-cli-0.0.36 | 1 | `/nix/store/11z5q863nnsvg66zpzn7dn78rwz3xgbv-filen-cli-0.0.36` |
| filen-cli-0.0.36 | 1 | `/nix/store/9bl5v7src87m9b44v08fcnxxn8vmpa0z-filen-cli-0.0.36` |
| httptoolkit-1.24.4 | 1 | `/nix/store/i7rj354mccdjhlm6k6njms8h2xpwxc25-httptoolkit-1.24.4` |
| libtorch-2.9.0 | 1 | `/nix/store/p5qnfspgh425s92a9z8wwkfyk73s8gsb-libtorch-2.9.0` |
| opencode-1.4.6 | 1 | `/nix/store/rnaz29q7npfcb123qkrjdgi8yjyc8gv5-opencode-1.4.6` |
| shogihome-1.27.0 | 1 | `/nix/store/aczrg2ihvdcckis5bpcv12a915kvrjsk-shogihome-1.27.0` |
| swift-5.10.1 | 11 | `/nix/store/9xyq2rnlkz59p7rwbxbp38r0b7n5980a-swift-5.10.1` |
| swift-5.10.1 | 11 | `/nix/store/cm4qi9frxy6p73sq1nsh6p8892cc010w-swift-5.10.1` |
| swift-5.10.1-lib | 7 | `/nix/store/hbw00ibnsqpr625mnih2hmzf8irkj0ns-swift-5.10.1-lib` |
| swift-5.10.1-lib | 7 | `/nix/store/yqc83j7j1fdcwxhnrk6s8ijh94lkdfs2-swift-5.10.1-lib` |
| tailwindcss_4-4.2.2 | 1 | `/nix/store/dwn6ifdgpj3f4wlk269s7rk9zqwvhpja-tailwindcss_4-4.2.2` |
| tailwindcss_4-4.2.2 | 1 | `/nix/store/jp4vvsn2dv1a6mcdhz62pr5cj9c1nl33-tailwindcss_4-4.2.2` |
| teams-for-linux-2.8.0 | 1 | `/nix/store/dll4aiqz9ryv6jnchb76dgww5fc5f55j-teams-for-linux-2.8.0` |
| vscode-extension-kilocode-Kilo-Code-7.2.0 | 1 | `/nix/store/1y5adw7jbwsy6v8zy2shcjn7wlhnm5l1-vscode-extension-kilocode-Kilo-Code-7.2.0` |
| vscode-extension-kilocode-Kilo-Code-7.2.0 | 1 | `/nix/store/gw6y9jk18hxz3inch9fznygcay23vqjh-vscode-extension-kilocode-Kilo-Code-7.2.0` |

## Slice classification

| Category | Count |
|---|---:|
| `page_hash_mismatch` | 53 |
| `other_sig_invalid` | 0 |
| `clean` (signed, verified) | 112,596 |
| `unsigned` (Mach-O without LC_CODE_SIGNATURE) | 116,336 |
| `not_real_macho` (Java .class, PPC big-endian, etc.) | 57,197 |
| `scanner_error` | 0 |

## Load-time transitive broken binaries

Binaries whose own code signatures are valid but which dyld cannot map at process start because their `LC_LOAD_DYLIB` / `LC_LOAD_WEAK_DYLIB` / `LC_REEXPORT_DYLIB` points at a direct-failing dylib. These SIGKILL at load, before `main()` runs — deterministic per slice.

| Metric | Count |
|---|---:|
| Binaries that link at least one failing dylib | 0 |
| Distinct packages containing such binaries | 0 |
| Failing dylibs that serve as seeds | 40 |
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
| Distinct failing seeds | 16 |

Edges by kind (default view only):

| Edge kind | Count |
|---|---:|
| `nativeBuildInputs` | 1 |

Top seed packages by downstream dependent count:

| Seed package | Downstream dependents |
|---|---:|
| `tailwindcss_4-4.2.2` | 1 |

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

