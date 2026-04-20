"""In-memory + on-disk scan state. One scan's results live in a Scan object;
the latest scan is the "current" scan that the UI binds to.
"""

from __future__ import annotations

import datetime as _dt
import json
import threading
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .config import SCANS_DIR
from .copies import Copy
from .scanner import FlaggedDirectory
from .selection import default_removals


@dataclass(slots=True)
class CopyView:
    basename: str  # video stem (may collide with other copies)
    filename: str  # full video filename including extension (unique within dir)
    video_path: str  # absolute path — unique identity key
    size: int
    width: int | None
    height: int | None
    codec: str | None
    bucket: str | None
    companions: list[str]
    companion_bytes: int
    remove: bool  # current selection state

    @property
    def total_bytes(self) -> int:
        return self.size + self.companion_bytes


@dataclass(slots=True)
class DirectoryView:
    directory: str
    name: str
    copies: list[CopyView]


@dataclass(slots=True)
class Scan:
    scan_id: str
    started_at: str
    finished_at: str | None
    root: str
    directories: list[DirectoryView] = field(default_factory=list)
    total_dirs: int = 0
    scanned_dirs: int = 0
    running: bool = True

    @property
    def flagged_count(self) -> int:
        return len(self.directories)

    @property
    def total_removable_bytes(self) -> int:
        return sum(
            c.total_bytes for d in self.directories for c in d.copies if c.remove
        )

    def find_copy(self, directory: str, video_path: str) -> CopyView | None:
        for d in self.directories:
            if d.directory == directory:
                for c in d.copies:
                    if c.video_path == video_path:
                        return c
                return None
        return None


def _copy_to_view(c: Copy, remove: bool) -> CopyView:
    probe = c.probe
    return CopyView(
        basename=c.basename,
        filename=c.video_path.name,
        video_path=str(c.video_path),
        size=c.size,
        width=probe.width if probe else None,
        height=probe.height if probe else None,
        codec=probe.codec if probe else None,
        bucket=probe.bucket.value if probe else None,
        companions=[str(p) for p in c.companions],
        companion_bytes=c.companion_bytes,
        remove=remove,
    )


def flagged_to_view(fd: FlaggedDirectory) -> DirectoryView:
    removal_paths = default_removals(fd.copies)
    return DirectoryView(
        directory=str(fd.directory),
        name=fd.name,
        copies=[
            _copy_to_view(c, str(c.video_path) in removal_paths) for c in fd.copies
        ],
    )


class ScanStore:
    """Singleton-style holder for the current scan. Thread-safe for concurrent
    HTMX calls from the browser while a background scan is running."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._current: Scan | None = None

    def new_scan(self, root: Path) -> Scan:
        scan = Scan(
            scan_id=uuid.uuid4().hex,
            started_at=_dt.datetime.now().isoformat(timespec="seconds"),
            finished_at=None,
            root=str(root),
            running=True,
        )
        with self._lock:
            self._current = scan
        return scan

    def add_directory(self, scan_id: str, view: DirectoryView) -> None:
        with self._lock:
            if self._current is None or self._current.scan_id != scan_id:
                return
            self._current.directories.append(view)

    def update_progress(self, scan_id: str, scanned: int, total: int) -> None:
        with self._lock:
            if self._current is None or self._current.scan_id != scan_id:
                return
            self._current.scanned_dirs = scanned
            self._current.total_dirs = total

    def finish(self, scan_id: str) -> None:
        with self._lock:
            if self._current is None or self._current.scan_id != scan_id:
                return
            self._current.running = False
            self._current.finished_at = _dt.datetime.now().isoformat(timespec="seconds")
            self._persist_locked(self._current)

    def current(self) -> Scan | None:
        with self._lock:
            return self._current

    def set_removal(self, directory: str, video_path: str, remove: bool) -> bool:
        with self._lock:
            if self._current is None:
                return False
            copy = self._current.find_copy(directory, video_path)
            if copy is None:
                return False
            copy.remove = remove
            return True

    def apply_defaults(self, select: bool) -> None:
        """select=True → tick default removals; select=False → clear everything."""
        with self._lock:
            if self._current is None:
                return
            for d in self._current.directories:
                if not select:
                    for c in d.copies:
                        c.remove = False
                # (when select=True, we leave existing values — defaults were already applied at scan time)

    def _persist_locked(self, scan: Scan) -> None:
        SCANS_DIR.mkdir(parents=True, exist_ok=True)
        payload = {
            "scan_id": scan.scan_id,
            "started_at": scan.started_at,
            "finished_at": scan.finished_at,
            "root": scan.root,
            "total_dirs": scan.total_dirs,
            "directories": [
                {
                    "directory": d.directory,
                    "name": d.name,
                    "copies": [asdict(c) for c in d.copies],
                }
                for d in scan.directories
            ],
        }
        path = SCANS_DIR / f"{scan.started_at}-{scan.scan_id[:8]}.json"
        path.write_text(json.dumps(payload, indent=2))


STORE = ScanStore()
