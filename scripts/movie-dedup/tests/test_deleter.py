"""Path-safety check in the deleter."""

from __future__ import annotations

import os
from pathlib import Path

from movie_dedup.deleter import execute, is_safe_target, preview


def test_allows_file_inside_root(tmp_path: Path) -> None:
    root = tmp_path / "lib"
    root.mkdir()
    target = root / "a" / "b.mp4"
    target.parent.mkdir()
    target.write_bytes(b"x")
    assert is_safe_target(target, root) is True


def test_rejects_file_outside_root(tmp_path: Path) -> None:
    root = tmp_path / "lib"
    root.mkdir()
    outside = tmp_path / "other.mp4"
    outside.write_bytes(b"x")
    assert is_safe_target(outside, root) is False


def test_rejects_the_root_itself(tmp_path: Path) -> None:
    root = tmp_path / "lib"
    root.mkdir()
    assert is_safe_target(root, root) is False


def test_rejects_nonexistent_path(tmp_path: Path) -> None:
    root = tmp_path / "lib"
    root.mkdir()
    assert is_safe_target(root / "never_existed.mp4", root) is False


def test_rejects_symlink_that_escapes(tmp_path: Path) -> None:
    root = tmp_path / "lib"
    root.mkdir()
    outside = tmp_path / "secret.mp4"
    outside.write_bytes(b"x")
    sneaky = root / "decoy.mp4"
    os.symlink(outside, sneaky)
    assert is_safe_target(sneaky, root) is False


def test_allows_symlink_inside_root(tmp_path: Path) -> None:
    root = tmp_path / "lib"
    root.mkdir()
    real_target = root / "nested" / "actual.mp4"
    real_target.parent.mkdir()
    real_target.write_bytes(b"x")
    link = root / "alias.mp4"
    os.symlink(real_target, link)
    assert is_safe_target(link, root) is True


def test_execute_unlinks_files_permanently(tmp_path, monkeypatch) -> None:
    """execute() must actually remove the files from disk (not move them)."""
    from movie_dedup import config as cfg

    root = tmp_path / "lib"
    root.mkdir()
    (root / "kept.mp4").write_bytes(b"keep")
    doomed = root / "doomed.mp4"
    doomed.write_bytes(b"bye")

    monkeypatch.setattr(cfg, "LIBRARY_ROOT", root)
    monkeypatch.setattr(cfg, "DELETIONS_DIR", tmp_path / "del_logs")

    batch = preview([doomed])
    batch.library_root = root
    result = execute(batch)

    assert not doomed.exists()  # gone for good
    assert (root / "kept.mp4").exists()  # untouched
    assert result.deletions[0].outcome == "deleted"
    assert result.deletions[0].error is None
    # Audit log was written.
    logs = list((tmp_path / "del_logs").glob("*.log.json"))
    assert len(logs) == 1


def test_execute_skips_unsafe_targets(tmp_path, monkeypatch) -> None:
    """A path that fails is_safe_target must be skipped, never unlinked."""
    from movie_dedup import config as cfg

    root = tmp_path / "lib"
    root.mkdir()
    outside = tmp_path / "outside.mp4"
    outside.write_bytes(b"precious")

    monkeypatch.setattr(cfg, "LIBRARY_ROOT", root)
    monkeypatch.setattr(cfg, "DELETIONS_DIR", tmp_path / "del_logs")

    batch = preview([outside])
    batch.library_root = root
    execute(batch)

    assert outside.exists()  # safety check prevented delete
    assert batch.deletions[0].outcome == "skipped"
    assert batch.deletions[0].error == "failed safety check"
