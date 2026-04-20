"""Default-selection heuristic: choose which copy to KEEP; mark the rest for removal."""

from __future__ import annotations

from .copies import Copy
from .probe import Bucket


def choose_keeper(copies: list[Copy]) -> Copy | None:
    """Return the copy that should be KEPT. Everything else is marked for removal.

    Rule: prefer the highest-resolution copy up to 1080p (so 1080p > 720p > SD,
    only falling back to 4K when nothing ≤ 1080p exists). Within the winning
    bucket, pick the smallest file size. Returns None if input is empty or no
    copy has a probe result.
    """
    probed = [c for c in copies if c.probe is not None]
    if not probed:
        return None

    non_4k = [
        c for c in probed if c.probe is not None and c.probe.bucket is not Bucket.FOUR_K
    ]
    candidates = non_4k if non_4k else probed

    target_bucket = max(
        (c.probe.bucket for c in candidates if c.probe is not None),
        key=lambda b: b.rank,
    )
    in_bucket = [
        c for c in candidates if c.probe is not None and c.probe.bucket is target_bucket
    ]

    return min(in_bucket, key=lambda c: (c.size, c.basename))


def default_removals(copies: list[Copy]) -> set[str]:
    """Return the set of video_path strings that default to REMOVED.

    Keyed by full video path (not basename) so that two copies sharing a stem
    — e.g. ``Foo 1080p AAC.mp4`` and ``Foo 1080p AAC.mkv`` — are distinguished.
    """
    keeper = choose_keeper(copies)
    if keeper is None:
        return set()
    return {str(c.video_path) for c in copies if c is not keeper}
