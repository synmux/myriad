"""Companion-file attribution, trailer exclusion, and shared-artwork protection."""

from __future__ import annotations

from pathlib import Path

import pytest
from movie_dedup.copies import (
    attribute_companions,
    discover_copies,
    is_shared_artwork,
    is_trailer,
)


@pytest.fixture
def kodi_dir(tmp_path: Path) -> Path:
    """Build a fixture resembling a real Kodi/Plex movie dir with two copies,
    a trailer, per-copy companions, and shared directory artwork."""
    d = tmp_path / "28 Weeks Later (2007)"
    d.mkdir()
    names = [
        # copies
        "28 Weeks Later (2007) 1080p AAC.mp4",
        "28 Weeks Later (2007) 1080p AC3.mp4",
        # trailer (not a copy)
        "28 Weeks Later (2007) 1080p AAC-trailer.mp4",
        # AAC companions
        "28 Weeks Later (2007) 1080p AAC.nfo",
        "28 Weeks Later (2007) 1080p AAC.eng.srt",
        "28 Weeks Later (2007) 1080p AAC-poster.jpg",
        "28 Weeks Later (2007) 1080p AAC-fanart12.jpg",
        "28 Weeks Later (2007) 1080p AAC-mediainfo.xml",
        # AC3 companions
        "28 Weeks Later (2007) 1080p AC3.nfo",
        "28 Weeks Later (2007) 1080p AC3-poster.jpg",
        # shared artwork (never a companion)
        "movie.nfo",
        "folder.jpg",
        "poster.jpg",
        "backdrop.jpg",
        "fanart.jpg",
        "movieset-poster.jpg",
        "movieset-fanart.jpg",
    ]
    for n in names:
        (d / n).write_bytes(b"x")
    (d / "extrathumbs").mkdir()
    (d / "extrathumbs" / "thumb1.jpg").write_bytes(b"x")
    return d


def test_discover_copies_excludes_trailer(kodi_dir: Path) -> None:
    copies = discover_copies(kodi_dir)
    basenames = {c.basename for c in copies}
    assert basenames == {
        "28 Weeks Later (2007) 1080p AAC",
        "28 Weeks Later (2007) 1080p AC3",
    }


def test_attribute_companions_routes_to_correct_copy(kodi_dir: Path) -> None:
    copies = discover_copies(kodi_dir)
    attribute_companions(kodi_dir, copies)

    by_base = {c.basename: c for c in copies}
    aac = by_base["28 Weeks Later (2007) 1080p AAC"]
    ac3 = by_base["28 Weeks Later (2007) 1080p AC3"]

    aac_companion_names = {p.name for p in aac.companions}
    assert "28 Weeks Later (2007) 1080p AAC.nfo" in aac_companion_names
    assert "28 Weeks Later (2007) 1080p AAC.eng.srt" in aac_companion_names
    assert "28 Weeks Later (2007) 1080p AAC-poster.jpg" in aac_companion_names
    assert "28 Weeks Later (2007) 1080p AAC-trailer.mp4" in aac_companion_names

    ac3_companion_names = {p.name for p in ac3.companions}
    assert "28 Weeks Later (2007) 1080p AC3.nfo" in ac3_companion_names
    assert "28 Weeks Later (2007) 1080p AC3-poster.jpg" in ac3_companion_names

    # No crossover.
    assert not (aac_companion_names & ac3_companion_names)


def test_shared_artwork_never_attributed(kodi_dir: Path) -> None:
    copies = discover_copies(kodi_dir)
    attribute_companions(kodi_dir, copies)

    all_companion_names = {p.name for c in copies for p in c.companions}
    for shared in {
        "movie.nfo",
        "folder.jpg",
        "poster.jpg",
        "backdrop.jpg",
        "fanart.jpg",
        "movieset-poster.jpg",
        "movieset-fanart.jpg",
    }:
        assert shared not in all_companion_names


def test_extrathumbs_dir_ignored(kodi_dir: Path) -> None:
    copies = discover_copies(kodi_dir)
    attribute_companions(kodi_dir, copies)
    all_companion_paths = [p for c in copies for p in c.companions]
    assert all("extrathumbs" not in p.parts for p in all_companion_paths)


def test_is_trailer_patterns(tmp_path: Path) -> None:
    assert is_trailer(tmp_path / "Foo 1080p-trailer.mp4")
    assert is_trailer(tmp_path / "Foo 1080p.trailer.mp4")
    assert not is_trailer(tmp_path / "Foo 1080p.mp4")


def test_same_stem_shared_companions_not_attributed(tmp_path: Path) -> None:
    """Two copies with same stem but different extensions share companions.
    Those companions must NOT be attributed to either copy — they're treated
    as shared so they survive when only one stemmate is removed."""
    d = tmp_path / "Batman (2019)"
    d.mkdir()
    (d / "Batman (2019) 720p AAC.mp4").write_bytes(b"x")
    (d / "Batman (2019) 720p AAC.mkv").write_bytes(b"x")
    (d / "Batman (2019) 720p AAC.nfo").write_bytes(b"x")  # ambiguous
    (d / "Batman (2019) 720p AAC-poster.jpg").write_bytes(b"x")  # ambiguous
    (d / "Batman (2019) 720p AAC.en.srt").write_bytes(b"x")  # ambiguous

    copies = discover_copies(d)
    attribute_companions(d, copies)

    # Two copies discovered (different extensions yield different video_paths).
    assert len(copies) == 2
    # Neither copy has any companion — every "companion" is ambiguous.
    for c in copies:
        assert c.companions == []
        assert c.companion_bytes == 0


def test_is_shared_artwork(tmp_path: Path) -> None:
    assert is_shared_artwork(tmp_path / "poster.jpg")
    assert is_shared_artwork(tmp_path / "folder.jpg")
    assert is_shared_artwork(tmp_path / "movieset-poster.jpg")
    assert not is_shared_artwork(tmp_path / "Foo 1080p AAC-poster.jpg")
