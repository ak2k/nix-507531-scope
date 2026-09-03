# Scanner × codesign -v cross-validation

Generated: 2026-09-03 08:12:09 UTC

Each flagged package is signature- and content-verified by Nix itself
(`nix store verify` against the binary cache), restored with Nix's NAR
codec, NarHash-crosschecked, then every flagged slice is checked with
an independent signature verifier: `/home/runner/.nix-profile/bin/rcodesign verify`.

| Outcome | Count |
|---|---:|
| Scanner failing, verifier fails (agreement) | 98 |
| Scanner failing, verifier passes (disagreement — possible false positive) | 0 |
| Fetch/verify failed (could not check against cache) | 0 |
| **Total slices verified** | **98** |

## Substitution canary

One flagged package per run is pulled through real `nix-store -r` substitution and its flagged files byte-compared against the direct NAR restore, keeping the user-shaped path continuously exercised.

```json
{
  "store_path": "/nix/store/5g52w7dv6mll9f37aqgl79mwwprmmbi4-filen-cli-0.0.36",
  "status": "ok",
  "files_compared": 1
}
```

No disagreements: every scanner-flagged failure was independently confirmed by the verifier.

