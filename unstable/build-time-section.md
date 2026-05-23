## Build-time dependents

Packages whose nix expression **directly declares** a direct-failing package as `buildInputs`, `nativeBuildInputs`, `checkInputs`, or `nativeCheckInputs` (1-hop). If the failing binary is invoked during the package's build phase, Hydra fails and the package never reaches the cache. This is a graph-level relationship: whether each listed package actually invokes the failing binary during build is not statically determinable. The canonical confirmed case is direnv — its `nativeCheckInputs = [ fish ]` with a `checkPhase` running `fish ./test/direnv-test.fish`, origin of [nixpkgs#507531](https://github.com/NixOS/nixpkgs/issues/507531).

Default view excludes `propagatedBuildInputs` / `propagatedNativeBuildInputs` edges (propagation threads the input forward; the listed package itself doesn't invoke it). The CSV includes all edge kinds for manual inspection.

| Metric | Count |
|---|---:|
| Packages with failing seeds in declared build/check inputs (default view) | 2 |
| Total direct-edge rows (default view) | 2 |
| Total rows including propagated edges | 5 |
| Distinct failing seeds | 55 |

Edges by kind (default view only):

| Edge kind | Count |
|---|---:|
| `buildInputs` | 1 |
| `nativeBuildInputs` | 1 |

Top seed packages by downstream dependent count:

| Seed package | Downstream dependents |
|---|---:|
| `stache-2.3.4` | 1 |
| `tailwindcss_4-4.3.0` | 1 |

Dependent packages (2): `haskellPackages.mmark-cli`, `rimgo`

Full detail: [`build-time-dependents.csv`](build-time-dependents.csv) (one row per `(dependent, edge_kind, seed)` tuple; `in_default_view=true` marks default-filter rows).
