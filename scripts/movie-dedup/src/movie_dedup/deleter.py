"""Dry-run preview + hard-unlink execution of deletion sets.

Deletion is permanent (``Path.unlink``) — the library lives on a network
volume where ``send2trash`` cannot access a ``.Trashes`` directory, so
there is no safe Trash to fall back on. Because of that, the deleter
owns the ONLY security check: every path must pass ``is_safe_target``
before it is unlinked. The mandatory dry-run preview in the UI layer
is the user-facing safeguard against surprise deletions.
"""

from __future__ import annotations

import datetime as _dt
import json
from dataclasses import dataclass, field
from pathlib import Path

from . import config as _cfg


@dataclass(slots=True)
class Deletion:
    path: Path
    size: int
    outcome: str = "pending"  # pending | deleted | skipped | error
    error: str | None = None


@dataclass(slots=True)
class DeletionBatch:
    timestamp: str
    library_root: Path
    deletions: list[Deletion] = field(default_factory=list)

    @property
    def total_bytes(self) -> int:
        return sum(d.size for d in self.deletions)


def is_safe_target(path: Path, library_root: Path | None = None) -> bool:
    """Return True iff *path* is safe to send to the Trash.

    Guarantees:
      1. *path* must already exist on disk (strict resolution refuses phantoms).
      2. *path*, once resolved (symlinks followed), must live INSIDE
         *library_root* (also resolved). Equality with the root is NOT safe.
      3. A symlink whose target escapes the root is rejected (both sides
         are resolved before the containment check).
      4. Any OSError during resolution returns False — never raises.
    """
    root_path = library_root if library_root is not None else _cfg.LIBRARY_ROOT
    try:
        target = path.resolve(strict=True)
        root = root_path.resolve(strict=True)
    except (OSError, FileNotFoundError, RuntimeError):
        return False
    if target == root:
        return False
    return target.is_relative_to(root)


def preview(target_paths: list[Path]) -> DeletionBatch:
    """Build a DeletionBatch in memory without touching anything on disk."""
    ts = _dt.datetime.now().isoformat(timespec="seconds")
    batch = DeletionBatch(timestamp=ts, library_root=_cfg.LIBRARY_ROOT)
    for p in target_paths:
        try:
            size = p.stat().st_size if p.is_file() else 0
        except OSError:
            size = 0
        batch.deletions.append(Deletion(path=p, size=size))
    return batch


def execute(batch: DeletionBatch) -> DeletionBatch:
    """Permanently unlink each safe path in *batch* and write a persistent log.

    Uses ``Path.unlink`` (POSIX ``unlink(2)``) so the deletion works on
    network-mounted volumes where Trash is unavailable. ``is_safe_target``
    must return True for a path or that path is skipped.
    """
    deletions_dir = _cfg.DELETIONS_DIR
    deletions_dir.mkdir(parents=True, exist_ok=True)
    log_path = deletions_dir / f"{batch.timestamp}.log.json"

    for deletion in batch.deletions:
        if not is_safe_target(deletion.path, batch.library_root):
            deletion.outcome = "skipped"
            deletion.error = "failed safety check"
            continue
        try:
            deletion.path.unlink(missing_ok=False)
            deletion.outcome = "deleted"
        except FileNotFoundError:
            deletion.outcome = "skipped"
            deletion.error = "already gone"
        except OSError as err:
            deletion.outcome = "error"
            deletion.error = str(err)

    log_path.write_text(
        json.dumps(
            {
                "timestamp": batch.timestamp,
                "library_root": str(batch.library_root),
                "total_bytes": batch.total_bytes,
                "deletions": [
                    {
                        "path": str(d.path),
                        "size": d.size,
                        "outcome": d.outcome,
                        "error": d.error,
                    }
                    for d in batch.deletions
                ],
            },
            indent=2,
        )
    )
    return batch
