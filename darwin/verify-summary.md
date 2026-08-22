# Scanner × codesign -v cross-validation

Generated: 2026-08-22 08:09:33 UTC

Each flagged package is signature- and content-verified by Nix itself
(`nix store verify` against the binary cache), restored with Nix's NAR
codec, NarHash-crosschecked, then every flagged slice is checked with
an independent signature verifier: `/home/runner/.nix-profile/bin/rcodesign verify`.

| Outcome | Count |
|---|---:|
| Scanner failing, verifier fails (agreement) | 73 |
| Scanner failing, verifier passes (disagreement — possible false positive) | 0 |
| Fetch/verify failed (could not check against cache) | 0 |
| **Total slices verified** | **73** |

## Substitution canary

One flagged package per run is pulled through real `nix-store -r` substitution and its flagged files byte-compared against the direct NAR restore, keeping the user-shaped path continuously exercised.

```json
{
  "store_path": "/nix/store/3y4p51ky7ybivbj9pq0mp7n573mqlfr0-avalonia-ilspy-7.2-rc",
  "status": "ok",
  "files_compared": 6
}
```

No disagreements: every scanner-flagged failure was independently confirmed by the verifier.

