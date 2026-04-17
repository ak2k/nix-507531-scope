# Scanner × codesign -v cross-validation

Generated: 2026-04-17 20:54:46 UTC

Verified every slice the scanner flagged as failing against an
independent signature verifier: `/nix/store/1g3gfvn82v1w0ld5h5szdv2hjydj6l4r-rcodesign-0.29.0/bin/rcodesign verify`.

| Outcome | Count |
|---|---:|
| Scanner failing, verifier fails (agreement) | 66 |
| Scanner failing, verifier passes (disagreement — possible false positive) | 0 |
| Realize failed (could not fetch package from cache) | 0 |
| **Total slices verified** | **66** |

No disagreements: every scanner-flagged failure was independently confirmed by the verifier.

