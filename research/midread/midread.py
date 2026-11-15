#!/usr/bin/env python3
"""Time a 1 MiB read from the middle of a file, to test partial-download cloud storage.

Usage: midread.py [path]

Each step's timing prints as soon as the step finishes. Python sets no timeout on
the read; if it blocks, press Ctrl-C to see which step it was stuck in and for how long.
"""

import fcntl
import os
import sys
import time

DEFAULT_PATH = "/Volumes/Helumi/bigfile.tar.syn@syn.as.age"
READ_SIZE = 1024 * 1024


def main() -> None:
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH
    start = time.perf_counter()
    previous = start
    current_step = "stat"

    def mark(next_step: str) -> None:
        nonlocal previous, current_step
        now = time.perf_counter()
        print(
            f"{current_step:<6} {now - previous:>12.6f} {now - start:>12.6f}",
            flush=True,
        )
        previous = now
        current_step = next_step

    print(f"file:   {path}")
    print(f"{'step':<6} {'step (s)':>12} {'total (s)':>12}", flush=True)
    try:
        file_size = os.stat(path).st_size
        midpoint = file_size // 2
        mark("open")

        # buffering=0: no Python-side buffer, so we ask the OS for exactly what we read
        handle = open(path, "rb", buffering=0)
        # Bypass the macOS page cache so repeat runs aren't served from RAM
        fcntl.fcntl(handle.fileno(), fcntl.F_NOCACHE, 1)
        mark("seek")

        handle.seek(midpoint)
        mark("read")

        data = bytearray()
        while len(data) < READ_SIZE:
            chunk = handle.read(READ_SIZE - len(data))
            if not chunk:
                break
            data += chunk
        mark("close")

        handle.close()
        mark("done")
    except KeyboardInterrupt:
        now = time.perf_counter()
        sys.exit(
            f"\ninterrupted during {current_step} after {now - previous:.1f}s ({now - start:.1f}s total)"
        )

    print(f"size:   {file_size:,} bytes ({file_size / 1024**3:.2f} GiB)")
    print(f"offset: {midpoint:,} bytes")
    print(f"read:   {len(data):,} bytes")
    if len(data) < READ_SIZE:
        sys.exit(
            f"short read: got {len(data)} of {READ_SIZE} bytes (file smaller than expected?)"
        )


if __name__ == "__main__":
    main()
