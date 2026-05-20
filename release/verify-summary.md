# Scanner × codesign -v cross-validation

Generated: 2026-05-20 08:37:14 UTC

Verified every slice the scanner flagged as failing against an
independent signature verifier: `/home/runner/.nix-profile/bin/rcodesign verify`.

| Outcome | Count |
|---|---:|
| Scanner failing, verifier fails (agreement) | 14 |
| Scanner failing, verifier passes (disagreement — possible false positive) | 0 |
| Realize failed (could not fetch package from cache) | 0 |
| **Total slices verified** | **14** |

No disagreements: every scanner-flagged failure was independently confirmed by the verifier.

