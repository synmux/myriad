"""Library-walking scanner that produces a full flagged-directory report."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Callable
from dataclasses import dataclass, field
from pathlib import Path

from .config import FFPROBE_CONCURRENCY, LIBRARY_ROOT
from .copies import Copy, attribute_companions, discover_copies
from .probe import probe_many


@dataclass(slots=True)
class FlaggedDirectory:
    directory: Path
    copies: list[Copy] = field(default_factory=list)

    @property
    def name(self) -> str:
        return self.directory.name


@dataclass(slots=True)
class ScanProgress:
    total_dirs: int
    scanned_dirs: int
    flagged_count: int
    current: str


async def scan_library(
    root: Path = LIBRARY_ROOT,
    progress_cb: Callable[[ScanProgress], None] | None = None,
) -> list[FlaggedDirectory]:
    """Walk *root*, return every directory with ≥ 2 non-trailer video copies.

    Runs ffprobe (bounded concurrency) on each copy so buckets are known.
    """
    subdirs: list[Path] = sorted(
        p for p in root.iterdir() if p.is_dir() and not p.name.startswith(".")
    )

    total = len(subdirs)
    flagged: list[FlaggedDirectory] = []

    for index, subdir in enumerate(subdirs, start=1):
        try:
            copies = discover_copies(subdir)
        except (PermissionError, FileNotFoundError):
            copies = []
        if len(copies) < 2:
            if progress_cb:
                progress_cb(ScanProgress(total, index, len(flagged), subdir.name))
            continue

        attribute_companions(subdir, copies)

        results = await probe_many(
            [c.video_path for c in copies],
            concurrency=FFPROBE_CONCURRENCY,
        )
        for c in copies:
            c.probe = results.get(c.video_path)

        flagged.append(FlaggedDirectory(directory=subdir, copies=copies))

        if progress_cb:
            progress_cb(ScanProgress(total, index, len(flagged), subdir.name))

    return flagged


async def iter_flagged_dirs(
    root: Path = LIBRARY_ROOT,
) -> AsyncIterator[FlaggedDirectory]:
    """Streaming variant — yields each flagged directory as soon as it's probed."""
    subdirs = sorted(
        p for p in root.iterdir() if p.is_dir() and not p.name.startswith(".")
    )
    for subdir in subdirs:
        try:
            copies = discover_copies(subdir)
        except (PermissionError, FileNotFoundError):
            continue
        if len(copies) < 2:
            continue
        attribute_companions(subdir, copies)
        results = await probe_many(
            [c.video_path for c in copies],
            concurrency=FFPROBE_CONCURRENCY,
        )
        for c in copies:
            c.probe = results.get(c.video_path)
        yield FlaggedDirectory(directory=subdir, copies=copies)


async def _amain() -> None:
    """Small manual smoke-test harness: `uv run python -m movie_dedup.scanner`."""

    def pb(p: ScanProgress) -> None:
        print(
            f"[{p.scanned_dirs}/{p.total_dirs}] flagged={p.flagged_count} :: {p.current}"
        )

    flagged = await scan_library(progress_cb=pb)
    print(f"\n{len(flagged)} flagged directories")
    for fd in flagged[:10]:
        print(f"  {fd.name}: {len(fd.copies)} copies")


if __name__ == "__main__":
    asyncio.run(_amain())
