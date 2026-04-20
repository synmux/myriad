"""Default-keep heuristic."""

from __future__ import annotations

from pathlib import Path

from movie_dedup.copies import Copy
from movie_dedup.probe import Bucket, ProbeResult
from movie_dedup.selection import choose_keeper, default_removals


def _copy(
    basename: str, size: int, bucket: Bucket, width: int = 0, ext: str = "mp4"
) -> Copy:
    return Copy(
        video_path=Path(f"/x/{basename}.{ext}"),
        basename=basename,
        size=size,
        probe=ProbeResult(
            width=width or _default_width(bucket),
            height=1000,
            codec="h264",
            bucket=bucket,
        ),
    )


def _default_width(bucket: Bucket) -> int:
    return {
        Bucket.SD: 900,
        Bucket.HD: 1280,
        Bucket.FULL_HD: 1920,
        Bucket.FOUR_K: 3840,
    }[bucket]


def test_4k_plus_1080p_keeps_1080p():
    copies = [
        _copy("Movie 4K", 20_000, Bucket.FOUR_K),
        _copy("Movie 1080p", 2_000, Bucket.FULL_HD),
    ]
    keeper = choose_keeper(copies)
    assert keeper is not None
    assert keeper.basename == "Movie 1080p"
    assert default_removals(copies) == {"/x/Movie 4K.mp4"}


def test_4k_plus_two_1080p_keeps_smallest_1080p():
    copies = [
        _copy("Movie 4K", 20_000, Bucket.FOUR_K),
        _copy("Movie 1080p AAC", 1_800, Bucket.FULL_HD),
        _copy("Movie 1080p AC3", 2_800, Bucket.FULL_HD),
    ]
    keeper = choose_keeper(copies)
    assert keeper is not None
    assert keeper.basename == "Movie 1080p AAC"
    assert default_removals(copies) == {"/x/Movie 4K.mp4", "/x/Movie 1080p AC3.mp4"}


def test_4k_only_keeps_smallest_4k():
    copies = [
        _copy("Movie 4K HDR", 30_000, Bucket.FOUR_K),
        _copy("Movie 4K SDR", 18_000, Bucket.FOUR_K),
    ]
    keeper = choose_keeper(copies)
    assert keeper is not None
    assert keeper.basename == "Movie 4K SDR"
    assert default_removals(copies) == {"/x/Movie 4K HDR.mp4"}


def test_720p_plus_480p_keeps_720p():
    copies = [
        _copy("Movie 720p", 900, Bucket.HD),
        _copy("Movie 480p", 400, Bucket.SD),
    ]
    keeper = choose_keeper(copies)
    assert keeper is not None
    assert keeper.basename == "Movie 720p"
    assert default_removals(copies) == {"/x/Movie 480p.mp4"}


def test_identical_sizes_are_tied_by_basename():
    copies = [
        _copy("Movie 1080p ZZZ", 2_000, Bucket.FULL_HD),
        _copy("Movie 1080p AAA", 2_000, Bucket.FULL_HD),
    ]
    keeper = choose_keeper(copies)
    assert keeper is not None
    assert keeper.basename == "Movie 1080p AAA"  # alphabetical tiebreak


def test_same_stem_different_extension_keeps_one():
    """Regression: two copies with identical stems but different extensions
    must not BOTH end up in the removal set. Keeper gets kept."""
    copies = [
        _copy("Batman 720p AAC", 820_000_000, Bucket.HD, ext="mp4"),
        _copy("Batman 720p AAC", 827_000_000, Bucket.HD, ext="mkv"),
    ]
    keeper = choose_keeper(copies)
    assert keeper is not None
    removals = default_removals(copies)
    assert str(keeper.video_path) not in removals
    # Exactly one of the two paths should be in removals.
    assert len(removals) == 1
    assert removals == {str(c.video_path) for c in copies if c is not keeper}


def test_same_stem_three_copies_keeps_one():
    """Three copies same stem, different extensions → keeper kept, two removed."""
    copies = [
        _copy("Foo 1080p AAC", 2_000, Bucket.FULL_HD, ext="mp4"),
        _copy("Foo 1080p AAC", 3_000, Bucket.FULL_HD, ext="mkv"),
        _copy("Foo 1080p AAC", 4_000, Bucket.FULL_HD, ext="avi"),
    ]
    keeper = choose_keeper(copies)
    assert keeper is not None
    assert keeper.size == 2_000  # smallest wins
    removals = default_removals(copies)
    assert len(removals) == 2
    assert str(keeper.video_path) not in removals


def test_no_probed_copies_returns_none():
    unprobed = Copy(video_path=Path("/x/foo.mp4"), basename="foo", size=100, probe=None)
    assert choose_keeper([unprobed]) is None
    assert default_removals([unprobed]) == set()
