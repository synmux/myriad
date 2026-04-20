# AGENTS.md — movie-dedup

Context for AI agents (Claude, Codex, etc.) working in this repo.

## What this is

A local Python web tool that scans a Kodi/Plex-style movie library (default `/Volumes/Movies`) for directories containing more than one video copy of the same movie, lets the user pick which copies to keep via a web UI, then permanently deletes the rest.

## Runtime

- Python 3.12, managed with `uv`
- FastAPI + Jinja2 + HTMX (no SPA)
- `ffprobe` (homebrew) for video metadata
- `Path.unlink` for deletion (the library is a network mount; Trash is
  unavailable on SMB/AFP shares, so removals are permanent)

## Run

```bash
cd /Users/dave/work/movie-dedup
uv sync
uv run uvicorn movie_dedup.app:app --host 127.0.0.1 --port 8765
# then open http://127.0.0.1:8765/
```

Override the library with `MOVIE_DEDUP_LIBRARY=<path>`; override state dir with `MOVIE_DEDUP_STATE=<path>`.

## Tests

```bash
uv run pytest
```

## Architecture (single pass)

- `probe.py`: `ffprobe` subprocess wrapper (argv-only, never a shell). `classify(width)` buckets into `SD / 720p / 1080p / 4K`. Width-based, because 1080p cinematic crops often have height 696.
- `copies.py`: `Copy` dataclass. `discover_copies(dir)` lists non-trailer videos. `attribute_companions(dir, copies)` uses **longest-prefix match** against basenames so a file like `Movie 1080p AAC-poster.jpg` is attributed only to the AAC copy, not the AC3 copy. Shared artwork (`movie.nfo`, `folder.jpg`, `movieset-*`, `extrathumbs/`, etc.) is never attributed to any copy.
- `selection.py`: `choose_keeper(copies)` picks the copy to KEEP — highest bucket ≤ 1080p, smallest size, alphabetical basename tiebreaker. Falls back to smallest 4K if nothing ≤ 1080p exists.
- `scanner.py`: walks the library, emits `FlaggedDirectory` for every dir with ≥ 2 copies. Optimised to skip ffprobe for single-video dirs.
- `state.py`: thread-safe in-memory store for the current scan + on-disk JSON snapshot under `~/.cache/movie-dedup/scans/`.
- `deleter.py`: `is_safe_target(path, root)` — **the** security guard. Uses `path.resolve(strict=True)` + `is_relative_to(root)`. Only paths that resolve inside the library (and aren't the root itself) pass. `execute(batch)` iterates, calls `Path.unlink(missing_ok=False)` (permanent — no Trash available on the network mount), logs a JSON audit under `~/.cache/movie-dedup/deletions/`.
- `app.py`: routes `/`, `/scan`, `/results`, `/scan/progress`, `/toggle`, `/clear`, `/preview`, `/delete`. Scan runs as an `asyncio.create_task` background coroutine; HTMX polls `/scan/progress` every second.

## Workflow constraints

- The user's global CLAUDE.md says: conventional commits with gitmoji, British English, no React, no silent failures. Respect these.
- The deleter's safety check is the **last** defence before a file is permanently (well, "Trashable") gone. Do not loosen `is_safe_target` without strong justification.
- Never have ffprobe or any subprocess invocation go through `shell=True`. Always argv lists.
- The scanner is read-only. Do not let it write into the library.
