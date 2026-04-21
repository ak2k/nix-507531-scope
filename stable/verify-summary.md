# Scanner × codesign -v cross-validation

Generated: 2026-04-21 12:21:31 UTC

Verified every slice the scanner flagged as failing against an
independent signature verifier: `/home/runner/.nix-profile/bin/rcodesign verify`.

| Outcome | Count |
|---|---:|
| Scanner failing, verifier fails (agreement) | 132 |
| Scanner failing, verifier passes (disagreement — possible false positive) | 0 |
| Realize failed (could not fetch package from cache) | 0 |
| **Total slices verified** | **132** |

No disagreements: every scanner-flagged failure was independently confirmed by the verifier.

