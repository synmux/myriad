"""Static configuration for the movie-dedup tool."""

from __future__ import annotations

import os
from pathlib import Path

LIBRARY_ROOT = Path(os.environ.get("MOVIE_DEDUP_LIBRARY", "/Volumes/Movies"))

STATE_DIR = Path(
    os.environ.get(
        "MOVIE_DEDUP_STATE",
        Path.home() / ".cache" / "movie-dedup",
    )
)
SCANS_DIR = STATE_DIR / "scans"
DELETIONS_DIR = STATE_DIR / "deletions"

HOST = os.environ.get("MOVIE_DEDUP_HOST", "127.0.0.1")
PORT = int(os.environ.get("MOVIE_DEDUP_PORT", "8765"))

VIDEO_EXTENSIONS: frozenset[str] = frozenset(
    {
        ".mkv",
        ".mp4",
        ".avi",
        ".mov",
        ".m4v",
        ".wmv",
        ".ts",
        ".m2ts",
    }
)

TRAILER_MARKERS: tuple[str, ...] = ("-trailer", ".trailer")

SHARED_ARTWORK_STEMS: frozenset[str] = frozenset(
    {
        "movie",
        "folder",
        "poster",
        "backdrop",
        "fanart",
        "banner",
        "landscape",
        "thumb",
        "clearart",
        "clearlogo",
        "disc",
        "discart",
        "keyart",
        "logo",
        "cover",
    }
)

SHARED_ARTWORK_PREFIXES: tuple[str, ...] = ("movieset-",)

SHARED_ARTWORK_DIRNAMES: frozenset[str] = frozenset({"extrathumbs"})

FFPROBE_CONCURRENCY = 8
