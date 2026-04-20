"""Copy + companion-file model and attribution logic."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .config import (
    SHARED_ARTWORK_DIRNAMES,
    SHARED_ARTWORK_PREFIXES,
    SHARED_ARTWORK_STEMS,
    TRAILER_MARKERS,
    VIDEO_EXTENSIONS,
)
from .probe import ProbeResult


@dataclass(slots=True)
class Copy:
    """One video copy + all of its companion files."""

    video_path: Path
    basename: str  # video filename stem (no extension)
    size: int  # size of the video file
    probe: ProbeResult | None = None
    companions: list[Path] = field(default_factory=list)
    companion_bytes: int = 0

    @property
    def total_bytes(self) -> int:
        return self.size + self.companion_bytes

    @property
    def all_paths(self) -> list[Path]:
        return [self.video_path, *self.companions]


def is_video(path: Path) -> bool:
    return path.suffix.lower() in VIDEO_EXTENSIONS


def is_trailer(path: Path) -> bool:
    name = path.stem.lower()
    return any(marker in name for marker in TRAILER_MARKERS)


def is_shared_artwork(path: Path) -> bool:
    """Shared directory-level files that belong to the directory, not a copy."""
    name_lower = path.name.lower()
    if path.stem.lower() in SHARED_ARTWORK_STEMS:
        return True
    return any(name_lower.startswith(prefix) for prefix in SHARED_ARTWORK_PREFIXES)


def discover_copies(directory: Path) -> list[Copy]:
    """Return all non-trailer video files in *directory* as bare Copy objects.

    Size is populated; probe + companions are not yet filled in.
    """
    copies: list[Copy] = []
    for entry in directory.iterdir():
        if not entry.is_file():
            continue
        if not is_video(entry):
            continue
        if is_trailer(entry):
            continue
        try:
            size = entry.stat().st_size
        except OSError:
            continue
        copies.append(
            Copy(
                video_path=entry,
                basename=entry.stem,
                size=size,
            )
        )
    copies.sort(key=lambda c: c.basename)
    return copies


def attribute_companions(directory: Path, copies: list[Copy]) -> None:
    """Assign every non-video, non-shared file in *directory* to one copy via
    longest-prefix match against the copies' basenames.

    When multiple copies share a basename (e.g. ``Foo 1080p AAC.mp4`` and
    ``Foo 1080p AAC.mkv``), companion files matching that shared basename
    cannot be unambiguously attributed to any single copy. They are treated
    as **shared** (like directory-level artwork) and attributed to none —
    they will not be deleted when any single stemmate is removed.

    Mutates *copies* in place: populates `companions` and `companion_bytes`.
    """
    if not copies:
        return

    basename_counts: dict[str, int] = {}
    for c in copies:
        basename_counts[c.basename] = basename_counts.get(c.basename, 0) + 1

    basenames_by_length = sorted(
        ((c.basename, c) for c in copies),
        key=lambda pair: len(pair[0]),
        reverse=True,
    )

    for entry in directory.iterdir():
        if entry.is_dir():
            if entry.name.lower() in SHARED_ARTWORK_DIRNAMES:
                continue
            continue
        if not entry.is_file():
            continue
        if any(entry == c.video_path for c in copies):
            continue
        if is_shared_artwork(entry):
            continue
        match = _longest_prefix_match(entry.name, basenames_by_length)
        if match is None:
            continue
        matched_basename, owner = match
        # When the matched basename is shared by multiple copies, the companion
        # is ambiguous — do not attribute it to any copy.
        if basename_counts.get(matched_basename, 0) > 1:
            continue
        try:
            size = entry.stat().st_size
        except OSError:
            size = 0
        owner.companions.append(entry)
        owner.companion_bytes += size


def _longest_prefix_match(
    filename: str,
    basenames_by_length: list[tuple[str, "Copy"]],
) -> tuple[str, "Copy"] | None:
    for basename, copy in basenames_by_length:
        if filename == basename:
            return basename, copy
        if filename.startswith(basename + ".") or filename.startswith(basename + "-"):
            return basename, copy
    return None
