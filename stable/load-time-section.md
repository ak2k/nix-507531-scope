## Load-time transitive broken binaries

Binaries whose own code signatures are valid but which dyld cannot map at process start because their `LC_LOAD_DYLIB` / `LC_LOAD_WEAK_DYLIB` / `LC_REEXPORT_DYLIB` points at a direct-failing dylib. These SIGKILL at load, before `main()` runs — deterministic per slice.

| Metric | Count |
|---|---:|
| Binaries that link at least one failing dylib | 56 |
| Distinct packages containing such binaries | 37 |
| Failing dylibs that serve as seeds | 51 |
| Total (binary, failing-dylib) pairs | 752 |

Top failing dylibs by number of downstream binaries:

| Seed package | Downstream binaries |
|---|---:|
| `ffmpeg-8.0-lib` | 752 |

Dependent packages (37): `auto-editor-29.3.1`, `ccextractor-0.94-unstable-2025-05-20`, `contour-0.6.1.7494`, `corsix-th-0.69.2`, `ddnet-19.5`, `dosbox-x-2025.10.07`, `ffms-5.0`, `freerdp-3.23.0`, `harvid-0.9.1`, `keyfinder-cli-1.1.2`, `libopenshot-0.4.0`, `loudgain-0.6.8`, `megacmd-1.7.0`, `moc-2.6-alpha3-unstable-2019-09-14`, `moonlight-qt-6.1.0`, `mpd-0.24.6`, `netgen-6.2.2505`, `notcurses-3.0.17`, `opencv-4.12.0`, `opencv-4.12.0-package_tests`, `phira-unwrapped-0.6.7`, `pianobar-2024.12.21`, `pqiv-2.13.3`, `q2pro-0-unstable-2025-07-21`, `qtmultimedia-6.10.2`, `rsgain-3.6`, `scrcpy-3.3.4`, `spek-0.8.5`, `squeezelite-2.0.0.1541`, `survex-1.4.18`, `taterclient-ddnet-10.6.0`, `timg-1.6.3`, `vgmstream-2055`, `video-compare-20250928`, `vivictpp-1.3.1`, `vtk-9.5.2`, `wxsvg-1.5.25`

Full detail: [`load-time-dependents.csv`](load-time-dependents.csv) (one row per `(binary, linked_failing_dylib)` pair).
