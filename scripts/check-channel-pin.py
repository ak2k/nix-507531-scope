#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# ///
"""
Fail the run when `channels.json`'s `stable` pin has fallen behind nixpkgs.

Two independent checks, because they catch the drift at different moments:

  1. **A newer release branch exists.** `release-YY.MM` branches appear on
     NixOS/nixpkgs at branch-off, weeks before the old release goes EOL. This
     is the early warning: it fires while the pinned channel is still healthy,
     which is the window in which bumping is cheap.

  2. **The pinned darwin channel has stopped advancing.** Hydra republishes
     `nixpkgs-<stable>-darwin` every few days; the `store-paths.xz`
     `Last-Modified` header is when it last did. Once a release goes EOL the
     pointer freezes and the scan silently re-reads identical bytes forever.
     This is the backstop for the case nobody acted on check 1.

Check 2 is what we lacked: `nixpkgs-25.11-darwin` froze on 2026-07-02 and the
daily scan stayed green for 42 days, re-scanning `0921fdb3e13e` 33 times.

Exit codes:
  0 — pin is current
  1 — pin is stale (a newer release exists, or the channel has frozen)
  2 — could not determine (network, parse, or missing config) — never a
      silent pass, since "the check didn't run" reads exactly like "the pin
      is fine" on a green run.
"""

from __future__ import annotations

import argparse
import email.utils
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

NIXPKGS = "https://github.com/NixOS/nixpkgs"
CHANNELS = "https://channels.nixos.org"
RELEASE_RE = re.compile(r"^release-(\d{2})\.(\d{2})$")


def release_key(name: str) -> tuple[int, int] | None:
    """`release-26.05` -> (26, 5). None if not a release branch."""
    m = RELEASE_RE.match(name)
    return (int(m.group(1)), int(m.group(2))) if m else None


def latest_release_branch() -> tuple[str, tuple[int, int]]:
    """Newest `release-YY.MM` branch on nixpkgs."""
    r = subprocess.run(
        ["git", "ls-remote", "--heads", NIXPKGS, "release-*"],
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    if r.returncode != 0:
        raise RuntimeError(f"git ls-remote failed: {r.stderr.strip()}")
    best: tuple[str, tuple[int, int]] | None = None
    for line in r.stdout.splitlines():
        _, _, ref = line.partition("refs/heads/")
        key = release_key(ref.strip())
        if key and (best is None or key > best[1]):
            best = (ref.strip(), key)
    if best is None:
        raise RuntimeError("no release-YY.MM branches found — parse or network problem")
    return best


def channel_last_modified(channel: str) -> datetime:
    """`Last-Modified` of a channel's store-paths.xz, as an aware UTC datetime."""
    url = f"{CHANNELS}/{channel}/store-paths.xz"
    req = urllib.request.Request(url, method="HEAD")
    with urllib.request.urlopen(req, timeout=120) as resp:
        raw = resp.headers.get("Last-Modified")
    if not raw:
        raise RuntimeError(f"{url}: no Last-Modified header")
    dt = email.utils.parsedate_to_datetime(raw)
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def channel_published(channel: str) -> bool:
    """Has Hydra published this channel yet?

    A `release-YY.MM` branch appears at branch-off, weeks before the matching
    darwin channel exists. Bumping the pin in that window points the darwin
    lane at a 404, so check 1 must know the difference between "you are behind"
    and "the successor is not ready yet".
    """
    url = f"{CHANNELS}/{channel}/store-paths.xz"
    req = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=120):
            return True
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False
        raise


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    p.add_argument("--config", type=Path, default=Path("channels.json"))
    p.add_argument(
        "--now",
        help="ISO-8601 UTC instant to age against (testing hook; default: now)",
    )
    args = p.parse_args()

    try:
        cfg = json.loads(args.config.read_text())
        pin: str = cfg["stable"]
        grace: int = int(cfg["stale_after_days"])
    except Exception as e:  # noqa: BLE001
        print(f"::error::cannot read {args.config}: {e}")
        return 2
    if release_key(f"release-{pin}") is None:
        print(f"::error::{args.config}: `stable` is {pin!r}, want YY.MM")
        return 2

    now = (
        datetime.fromisoformat(args.now).astimezone(timezone.utc)
        if args.now
        else datetime.now(timezone.utc)
    )

    try:
        newest, newest_key = latest_release_branch()
        channel = f"nixpkgs-{pin}-darwin"
        published = channel_last_modified(channel)
    except (
        RuntimeError,
        urllib.error.URLError,
        OSError,
        subprocess.SubprocessError,
    ) as e:
        print(f"::error::channel pin check could not run: {e}")
        return 2

    age_days = (now - published).days
    pinned_key = release_key(f"release-{pin}")
    assert pinned_key is not None  # validated above

    print(f"pinned stable:      {pin}")
    print(f"newest on nixpkgs:  {newest.removeprefix('release-')}")
    print(f"{channel} last published: {published:%Y-%m-%d} ({age_days}d ago)")

    stale: list[str] = []
    if newest_key > pinned_key:
        successor = f"nixpkgs-{newest.removeprefix('release-')}-darwin"
        if channel_published(successor):
            stale.append(
                f"nixpkgs has {newest} but channels.json pins {pin}. "
                f"Bump `stable` in channels.json."
            )
        else:
            # Branched but not published: bumping now would point the darwin
            # lane at a 404. Visible, but not yet actionable.
            print(
                f"::warning::{newest} exists but {successor} is not published "
                f"yet — not bumping. Check 2 stays the EOL backstop."
            )
    if age_days > grace:
        stale.append(
            f"{channel} has not been republished in {age_days} days "
            f"(> {grace}d grace). The lane is re-scanning frozen bytes."
        )

    if stale:
        for msg in stale:
            print(f"::error::{msg}")
        return 1

    print("pin is current")
    return 0


if __name__ == "__main__":
    sys.exit(main())
