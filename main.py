from __future__ import annotations

import argparse
import logging
import shutil
from dataclasses import dataclass
from pathlib import Path

from mutagen import File as MutagenFile
from mutagen import MutagenError

SUPPORTED_EXTENSIONS = {".m4a", ".mp3", ".flac"}


@dataclass
class Stats:
    scanned_files: int = 0
    matched_files: int = 0
    processed_files: int = 0
    dry_run_files: int = 0
    skipped_existing: int = 0
    errors: int = 0


def _parse_positive_int(raw_value: object) -> int | None:
    try:
        value = int(str(raw_value))
    except (TypeError, ValueError):
        return None
    return value if value > 0 else None


def probe_audio_profile(source_path: Path) -> tuple[int | None, int | None]:
    audio = MutagenFile(source_path)
    if audio is None or getattr(audio, "info", None) is None:
        return None, None

    info = audio.info
    sample_rate = _parse_positive_int(getattr(info, "sample_rate", None))
    bit_depth = _parse_positive_int(getattr(info, "bits_per_sample", None))
    return bit_depth, sample_rate


def build_bucket_name(
    source_path: Path, bit_depth: int | None, sample_rate: int | None
) -> str:
    ext = source_path.suffix.lower().lstrip(".")
    depth_part = str(bit_depth) if bit_depth is not None else "unknown"
    sample_rate_part = str(sample_rate) if sample_rate is not None else "unknown"
    return f"{ext}.{depth_part}.{sample_rate_part}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Split .m4a/.mp3/.flac files from an input directory into top-level "
            "extension.bit_depth.sample_rate directories while preserving relative paths."
        )
    )
    parser.add_argument(
        "input_dir",
        nargs="?",
        type=Path,
        default=Path("input"),
        help="Directory to scan recursively (default: input)",
    )
    parser.add_argument(
        "--mv",
        action="store_true",
        help="Move files instead of copying them",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without changing the filesystem",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )
    return parser


# noinspection PyBroadException,D
def run(input_dir: Path, move_files: bool, dry_run: bool) -> int:
    logger = logging.getLogger("extsplit")
    stats = Stats()
    action_word = "move" if move_files else "copy"
    action_past_tense = "Moved" if move_files else "Copied"

    if not input_dir.exists():
        logger.error("Input directory does not exist: %s", input_dir)
        return 2

    if not input_dir.is_dir():
        logger.error("Input path is not a directory: %s", input_dir)
        return 2

    logger.info(
        "Starting: input=%s mode=%s dry_run=%s",
        input_dir,
        action_word,
        dry_run,
    )

    for source_path in sorted(input_dir.rglob("*")):
        if not source_path.is_file():
            continue

        stats.scanned_files += 1
        extension = source_path.suffix.lower()
        if extension not in SUPPORTED_EXTENSIONS:
            continue

        stats.matched_files += 1
        try:
            bit_depth, sample_rate = probe_audio_profile(source_path)
        except MutagenError:
            stats.errors += 1
            logger.exception("mutagen failed to read metadata for: %s", source_path)
            continue

        bucket = build_bucket_name(
            source_path=source_path,
            bit_depth=bit_depth,
            sample_rate=sample_rate,
        )
        if bit_depth is None or sample_rate is None:
            logger.warning(
                "Metadata incomplete for %s (bit_depth=%s sample_rate=%s); using bucket '%s'",
                source_path,
                bit_depth if bit_depth is not None else "unknown",
                sample_rate if sample_rate is not None else "unknown",
                bucket,
            )

        relative_path = source_path.relative_to(input_dir)
        destination_path = Path(bucket) / relative_path

        if destination_path.exists():
            stats.skipped_existing += 1
            logger.warning(
                "Skipping existing destination: %s -> %s",
                source_path,
                destination_path,
            )
            continue

        if dry_run:
            stats.dry_run_files += 1
            logger.info(
                "[DRY-RUN] would %s: %s -> %s",
                action_word,
                source_path,
                destination_path,
            )
            continue

        try:
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            if move_files:
                shutil.move(str(source_path), str(destination_path))
            else:
                shutil.copy2(source_path, destination_path)
            stats.processed_files += 1
            logger.info(
                "%s: %s -> %s", action_past_tense, source_path, destination_path
            )
        except Exception:
            stats.errors += 1
            logger.exception("Failed to process file: %s", source_path)

    logger.info(
        "Done: scanned=%d matched=%d processed=%d dry_run=%d skipped_existing=%d errors=%d",
        stats.scanned_files,
        stats.matched_files,
        stats.processed_files,
        stats.dry_run_files,
        stats.skipped_existing,
        stats.errors,
    )
    return 1 if stats.errors else 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )
    return run(input_dir=args.input_dir, move_files=args.mv, dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
