"""ffprobe wrapper + resolution bucket classification.

Uses asyncio subprocess helpers that pass argv as a list (no shell interpretation)
so user-controlled filenames cannot be used to inject commands.
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class Bucket(str, Enum):
    FOUR_K = "4K"
    FULL_HD = "1080p"
    HD = "720p"
    SD = "SD"

    @property
    def rank(self) -> int:
        return {"SD": 0, "720p": 1, "1080p": 2, "4K": 3}[self.value]


@dataclass(frozen=True, slots=True)
class ProbeResult:
    width: int
    height: int
    codec: str
    bucket: Bucket


def classify(width: int) -> Bucket:
    if width >= 3200:
        return Bucket.FOUR_K
    if width >= 1800:
        return Bucket.FULL_HD
    if width >= 1200:
        return Bucket.HD
    return Bucket.SD


_FFPROBE_ARGS: tuple[str, ...] = (
    "-v",
    "error",
    "-select_streams",
    "v:0",
    "-show_entries",
    "stream=width,height,codec_name",
    "-of",
    "json",
)


async def probe(path: Path) -> ProbeResult | None:
    """Run ffprobe on *path*. Return None on any failure."""
    argv = ("ffprobe", *_FFPROBE_ARGS, str(path))
    proc = await asyncio.subprocess.create_subprocess_exec(
        *argv,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, _ = await proc.communicate()
    if proc.returncode != 0:
        return None
    try:
        payload = json.loads(stdout)
        stream = payload["streams"][0]
        width = int(stream["width"])
        height = int(stream["height"])
        codec = str(stream.get("codec_name", "unknown"))
    except (KeyError, IndexError, ValueError, json.JSONDecodeError):
        return None
    return ProbeResult(width=width, height=height, codec=codec, bucket=classify(width))


async def probe_many(
    paths: list[Path], concurrency: int
) -> dict[Path, ProbeResult | None]:
    """Probe *paths* in parallel, bounded by *concurrency*. Returns a {path: result} map."""
    semaphore = asyncio.Semaphore(concurrency)

    async def _one(p: Path) -> tuple[Path, ProbeResult | None]:
        async with semaphore:
            return p, await probe(p)

    pairs = await asyncio.gather(*(_one(p) for p in paths))
    return dict(pairs)
