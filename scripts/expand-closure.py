#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "httpx[http2]>=0.27",
# ]
# ///
"""
Expand a list of /nix/store paths to its full runtime closure by
walking `narinfo.References` against a binary cache.

Output is the union of inputs plus everything those inputs runtime-
depend on (transitively), matching what Hydra publishes in a channel's
`store-paths.xz`. Without this pass, the synthetic `release` channel's
path list contains only `legacyPackages.aarch64-darwin.<attr>.outputs.*`
direct outputs (~107K paths); after this pass it covers the full runtime
closure (~170K paths), so Tier 1 page-hash scans don't miss runtime-only
dylibs and Tier 2 LC_LOAD_DYLIB classification doesn't underreport.

Closure semantics: `narinfo.References` is the runtime closure as Nix
records it (deps the executable would mmap or fork-exec). Build-time
inputs (dev tools, headers) are NOT included — same scope Hydra uses
for `store-paths.xz`. We don't pull from drvs / build inputs.

Paths returning 404 from the binary cache are silently dropped from the
expansion frontier — Hydra didn't build them, so there are no bytes to
fail page-hash verification on. The input path is still kept in the
output even on 404 so the scanner sees the same input it would
otherwise.

Concurrency: parallel httpx with HTTP/2 + connection pool. Default 64
in-flight matches scan-darwin-cache.py's per-worker concurrency.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
from typing import Iterable

import httpx


DEFAULT_CACHE = "https://cache.nixos.org"
log = logging.getLogger("expand")


def _hash_part(store_path: str) -> str:
    return os.path.basename(store_path).split("-", 1)[0]


def _parse_references(narinfo_text: str) -> list[str]:
    """narinfo `References:` is a single space-separated line of basenames
    (no `/nix/store/` prefix). Re-prefix and return as full paths."""
    for line in narinfo_text.splitlines():
        if line.startswith("References:"):
            tail = line[len("References:"):].strip()
            if not tail:
                return []
            return [f"/nix/store/{name}" for name in tail.split()]
    return []


async def _fetch_refs(
    client: httpx.AsyncClient, cache_url: str, store_path: str
) -> list[str] | None:
    """Return refs for `store_path`, or None on 404 (path not in cache).
    Other HTTP errors are also treated as None — log and skip; bombing
    the whole run for one transient 5xx isn't worth it."""
    url = f"{cache_url.rstrip('/')}/{_hash_part(store_path)}.narinfo"
    try:
        r = await client.get(url)
    except httpx.HTTPError as e:
        log.debug("fetch error %s: %s", store_path, e)
        return None
    if r.status_code == 404:
        return None
    if r.status_code >= 400:
        log.debug("fetch %s -> %d", store_path, r.status_code)
        return None
    return _parse_references(r.text)


async def expand(
    seeds: Iterable[str], cache_url: str, concurrency: int
) -> set[str]:
    """BFS expansion. Returns seeds ∪ everything reachable via
    transitive References."""
    seen: set[str] = set(seeds)
    frontier: set[str] = set(seen)
    n_404 = 0
    n_fetched = 0

    timeout = httpx.Timeout(connect=30.0, read=60.0, write=30.0, pool=None)
    limits = httpx.Limits(
        max_connections=concurrency * 2,
        max_keepalive_connections=concurrency,
    )

    async with httpx.AsyncClient(
        timeout=timeout,
        limits=limits,
        http2=True,
        follow_redirects=True,
        headers={"User-Agent": "nix-507531-scope-closure-expander/1"},
    ) as client:
        round_n = 0
        while frontier:
            round_n += 1
            log.info(
                "round %d: %d in frontier, %d total seen",
                round_n, len(frontier), len(seen)
            )
            sem = asyncio.Semaphore(concurrency)

            async def _bounded(p: str):
                async with sem:
                    return p, await _fetch_refs(client, cache_url, p)

            tasks = [_bounded(p) for p in frontier]
            new_refs: set[str] = set()
            for fut in asyncio.as_completed(tasks):
                path, refs = await fut
                n_fetched += 1
                if refs is None:
                    n_404 += 1
                    continue
                for r in refs:
                    if r not in seen:
                        new_refs.add(r)

            seen.update(new_refs)
            frontier = new_refs

    log.info(
        "expansion done: %d total paths, %d narinfos fetched, %d 404s",
        len(seen), n_fetched, n_404,
    )
    return seen


def main() -> int:
    p = argparse.ArgumentParser(
        description=(
            "Expand a /nix/store path list to its full runtime closure "
            "by walking narinfo.References against a binary cache. "
            "Mirrors what Hydra publishes in a channel's store-paths.xz."
        )
    )
    p.add_argument(
        "--in",
        dest="in_path",
        required=True,
        help="Newline-separated /nix/store paths to use as the seed set",
    )
    p.add_argument(
        "--out",
        dest="out_path",
        required=True,
        help="Output file (sorted, deduplicated, one path per line). "
        "OK to use the same value as --in (read fully before write).",
    )
    p.add_argument(
        "--cache-url",
        default=DEFAULT_CACHE,
        help=f"Binary cache URL (default: {DEFAULT_CACHE})",
    )
    p.add_argument(
        "--concurrency",
        type=int,
        default=64,
        help="Parallel narinfo fetches (default: 64)",
    )
    p.add_argument(
        "--log-level", default="INFO", help="Python logging level"
    )
    args = p.parse_args()
    logging.basicConfig(
        level=args.log_level,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    with open(args.in_path) as f:
        seeds = [
            ln.strip()
            for ln in f
            if ln.strip() and ln.lstrip().startswith("/nix/store/")
        ]
    log.info("loaded %d seed paths from %s", len(seeds), args.in_path)

    expanded = asyncio.run(expand(seeds, args.cache_url, args.concurrency))

    with open(args.out_path, "w") as f:
        for path in sorted(expanded):
            f.write(path + "\n")
    log.info("wrote %d paths to %s", len(expanded), args.out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
