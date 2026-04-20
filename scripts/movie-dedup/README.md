# movie-dedup

Local web tool for finding and removing duplicate movie copies in a Kodi/Plex-style library.

For a movie library where each film lives in its own subdirectory and may contain multiple video copies (different resolutions, different audio codecs), `movie-dedup`:

1. **Scans** the library for directories with ≥ 2 video copies.
2. **Probes** each copy with `ffprobe` to determine actual resolution (filename labels are often inaccurate — 1080p content crops to 1920×696 cinematically).
3. **Recommends** which copy to keep — the smallest file in the highest bucket up to 1080p, falling back to 4K only if no ≤ 1080p copy exists.
4. **Previews** the full deletion set (video + companion files like `.nfo`, `.srt`, artwork) so you can audit before anything leaves disk.
5. **Deletes** selected files permanently with `Path.unlink` (the library is a
   network volume where Trash is unavailable — the mandatory dry-run preview
   is the safety net instead).
6. **Rescans** to confirm the library is clean.

## Install and run

Requires `uv` and `ffprobe`.

```bash
cd /Users/dave/work/movie-dedup
uv sync
uv run uvicorn movie_dedup.app:app --host 127.0.0.1 --port 8765
```

Open `http://127.0.0.1:8765/` and click **Scan**.

### Override defaults

| Env var               | Default                |
| --------------------- | ---------------------- |
| `MOVIE_DEDUP_LIBRARY` | `/Volumes/Movies`      |
| `MOVIE_DEDUP_STATE`   | `~/.cache/movie-dedup` |
| `MOVIE_DEDUP_HOST`    | `127.0.0.1`            |
| `MOVIE_DEDUP_PORT`    | `8765`                 |

## Tests

```bash
uv run pytest
```

23 tests cover resolution bucketing, companion-file attribution, the default-keep heuristic, and the deletion path-safety check (including symlink escape attempts).

## What counts as a "copy"

Any file in a movie directory matching one of:
`.mkv .mp4 .avi .mov .m4v .wmv .ts .m2ts`

…except files whose basename contains `-trailer` or `.trailer`. Those are attached to the nearest copy as companions and only deleted when that copy is removed.

## What counts as a "companion"

Any non-video file whose name starts with a copy's basename followed by `.` or `-`. Attribution uses **longest-prefix match**, so `Movie 1080p AAC-poster.jpg` is never misattributed to the AC3 copy.

Files that are never touched:

- Shared directory artwork without a movie prefix: `movie.nfo`, `folder.jpg`, `poster.jpg`, `backdrop.jpg`, `fanart.jpg`, `banner.jpg`, etc.
- Movie-set artwork: `movieset-*`
- The `extrathumbs/` subdirectory

## Safety

Two layers protect against mistakes:

1. **Dry-run mandatory.** Every click path goes through a preview step showing exactly which files would be deleted and the reclaimed bytes total.
2. **Path containment check.** `is_safe_target()` resolves symlinks (strict existence required) and requires the target to live inside the configured library root — otherwise it refuses to touch the path.

Deletions are **permanent** — `Path.unlink` removes the inode directly, because the library lives on a network mount where the macOS Trash is unavailable. Every deletion is logged to `~/.cache/movie-dedup/deletions/<timestamp>.log.json` for audit.

## Licence

Private project for personal use.
