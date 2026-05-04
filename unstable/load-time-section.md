## Load-time transitive broken binaries

Binaries whose own code signatures are valid but which dyld cannot map at process start because their `LC_LOAD_DYLIB` / `LC_LOAD_WEAK_DYLIB` / `LC_REEXPORT_DYLIB` points at a direct-failing dylib. These SIGKILL at load, before `main()` runs — deterministic per slice.

| Metric | Count |
|---|---:|
| Binaries that link at least one failing dylib | 6 |
| Distinct packages containing such binaries | 4 |
| Failing dylibs that serve as seeds | 88 |
| Total (binary, failing-dylib) pairs | 153 |

Top failing dylibs by number of downstream binaries:

| Seed package | Downstream binaries |
|---|---:|
| `ffmpeg-headless-8.0.1-lib` | 153 |

Dependent packages (4): `cyanrip-0.9.3.1`, `ffmpegthumbnailer-2.3.0`, `gst-libav-1.26.11`, `musikcube-3.0.5`

Full detail: [`load-time-dependents.csv`](load-time-dependents.csv) (one row per `(binary, linked_failing_dylib)` pair).
