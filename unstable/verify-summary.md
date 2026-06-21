# Scanner × codesign -v cross-validation

Generated: 2026-06-21 09:16:42 UTC

Each flagged package is signature- and content-verified by Nix itself
(`nix store verify` against the binary cache), restored with Nix's NAR
codec, NarHash-crosschecked, then every flagged slice is checked with
an independent signature verifier: `/home/runner/.nix-profile/bin/rcodesign verify`.

| Outcome | Count |
|---|---:|
| Scanner failing, verifier fails (agreement) | 186 |
| Scanner failing, verifier passes (disagreement — possible false positive) | 0 |
| Fetch/verify failed (could not check against cache) | 0 |
| **Total slices verified** | **186** |

## Substitution canary

One flagged package per run is pulled through real `nix-store -r` substitution and its flagged files byte-compared against the direct NAR restore, keeping the user-shaped path continuously exercised.

```json
{
  "store_path": "/nix/store/lg9r937b4q70s5qqvjhdkf7rnn5x4xvd-ffmpeg-headless-8.0.1-bin",
  "status": "ok",
  "files_compared": 2
}
```

No disagreements: every scanner-flagged failure was independently confirmed by the verifier.

