#!/usr/bin/env bash
# Export the stable-release pin from channels.json into $GITHUB_ENV, so every
# job derives the darwin channel URL and the release branch from one place.
# No job may hardcode the version. (Some CLI defaults and docstrings under
# scripts/ still name a release; none of them are on a workflow code path.)
#
# Exports: STABLE, DARWIN_URL, RELEASE_BRANCH.
set -euo pipefail

STABLE=$(jq -er '.stable' channels.json)
case "$STABLE" in
  [0-9][0-9].[0-9][0-9]) ;;
  *) echo "::error::channels.json: stable is '$STABLE', want YY.MM" >&2; exit 1 ;;
esac

{
  echo "STABLE=$STABLE"
  echo "DARWIN_URL=https://channels.nixos.org/nixpkgs-$STABLE-darwin"
  echo "RELEASE_BRANCH=release-$STABLE"
} >> "${GITHUB_ENV:-/dev/stdout}"

echo "stable pin: $STABLE"
