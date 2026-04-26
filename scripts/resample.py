#!/usr/bin/env python3
"""Standardise music files to 44.1 kHz / 16-bit.

Walks an input tree, inspects each audio file with ffprobe, and:
  - skips files already at 44.1 kHz (and 16-bit, where applicable)
  - transcodes lossy inputs (MP3, AAC) to MP3 320 kbps CBR
  - transcodes lossless inputs (FLAC, ALAC) to FLAC, max compression, 16-bit

Output mirrors the input directory layout under the output root.
Existing files are never overwritten: a short random suffix is appended
to the stem if the target path already exists.

Environment variables:
  MUSIC_IN_DIR   override input directory  (default: ~/Music/In/Resample)
  MUSIC_OUT_DIR  override output directory (default: ~/Music/Out/Resample)
"""

from __future__ import annotations

import json
import os
import secrets
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_INPUT = "~/Music/In/Resample"
DEFAULT_OUTPUT = "~/Music/Out/Resample"

TARGET_SAMPLE_RATE = 44_100
TARGET_BIT_DEPTH = 16

LOSSY_CODECS = frozenset({"mp3", "aac"})
LOSSLESS_CODECS = frozenset({"flac", "alac"})

AUDIO_EXTENSIONS = frozenset({".mp3", ".m4a", ".aac", ".flac"})


def probe(path: Path) -> dict:
    """Return the first audio stream's metadata via ffprobe."""
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_streams",
            "-select_streams",
            "a:0",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    streams = json.loads(result.stdout).get("streams") or []
    if not streams:
        raise RuntimeError(f"no audio stream in {path}")
    stream = streams[0]
    bit_depth_raw = (
        stream.get("bits_per_raw_sample") or stream.get("bits_per_sample") or 0
    )
    return {
        "codec": (stream.get("codec_name") or "").lower(),
        "sample_rate": int(stream.get("sample_rate") or 0),
        "bit_depth": int(bit_depth_raw),
    }


def needs_resample(info: dict) -> bool:
    """True if the file is not already at the target spec.

    Lossy codecs only require the sample-rate check (bit depth is meaningless
    for compressed audio). Lossless codecs require both."""
    if info["sample_rate"] != TARGET_SAMPLE_RATE:
        return True
    if info["codec"] in LOSSLESS_CODECS:
        if info["bit_depth"] and info["bit_depth"] != TARGET_BIT_DEPTH:
            return True
    return False


def unique_path(target: Path) -> Path:
    """Return a non-colliding path; appends a random hex suffix on collision."""
    if not target.exists():
        return target
    while True:
        candidate = target.with_stem(f"{target.stem}-{secrets.token_hex(3)}")
        if not candidate.exists():
            return candidate


def transcode_to_mp3(src: Path, dst: Path) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(src),
            "-vn",
            "-codec:a",
            "libmp3lame",
            "-b:a",
            "320k",
            "-ar",
            str(TARGET_SAMPLE_RATE),
            str(dst),
        ],
        check=True,
    )


def transcode_to_flac(src: Path, dst: Path) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(src),
            "-vn",
            "-codec:a",
            "flac",
            "-compression_level",
            "12",
            "-sample_fmt",
            "s16",
            "-ar",
            str(TARGET_SAMPLE_RATE),
            str(dst),
        ],
        check=True,
    )


def process_file(src: Path, input_root: Path, output_root: Path) -> str:
    rel = src.relative_to(input_root)
    info = probe(src)

    if not needs_resample(info):
        return f"skip   {rel}  ({info['codec']} {info['sample_rate']}Hz)"

    if info["codec"] in LOSSY_CODECS:
        target_ext, action = ".mp3", transcode_to_mp3
    elif info["codec"] in LOSSLESS_CODECS:
        target_ext, action = ".flac", transcode_to_flac
    else:
        return f"warn   {rel}  (unsupported codec '{info['codec']}')"

    dst = unique_path((output_root / rel).with_suffix(target_ext))
    dst.parent.mkdir(parents=True, exist_ok=True)
    action(src, dst)
    return f"resamp {rel}  ->  {dst.relative_to(output_root)}"


def main() -> int:
    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        print("error: ffmpeg and ffprobe must be on PATH", file=sys.stderr)
        return 1

    input_root = Path(
        os.path.expanduser(os.environ.get("MUSIC_IN_DIR", DEFAULT_INPUT))
    ).resolve()
    output_root = Path(
        os.path.expanduser(os.environ.get("MUSIC_OUT_DIR", DEFAULT_OUTPUT))
    ).resolve()

    if not input_root.is_dir():
        print(f"error: input directory does not exist: {input_root}", file=sys.stderr)
        return 1

    output_root.mkdir(parents=True, exist_ok=True)

    print(f"input:  {input_root}")
    print(f"output: {output_root}")

    files = sorted(
        p
        for p in input_root.rglob("*")
        if p.is_file() and p.suffix.lower() in AUDIO_EXTENSIONS
    )
    if not files:
        print("no audio files found")
        return 0

    failures = 0
    for src in files:
        try:
            print(process_file(src, input_root, output_root), flush=True)
        except subprocess.CalledProcessError as exc:
            failures += 1
            print(
                f"error  {src.relative_to(input_root)}: ffmpeg/ffprobe exit {exc.returncode}",
                file=sys.stderr,
            )
        except Exception as exc:
            failures += 1
            print(f"error  {src.relative_to(input_root)}: {exc}", file=sys.stderr)

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
