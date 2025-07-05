"""File operations for copying and moving classified images."""

import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional

import structlog

logger = structlog.get_logger(__name__)


class FileHandler:
    """Handles file operations for classified images."""

    def __init__(self, dry_run: bool = False):
        """Initialize file handler.

        Args:
            dry_run: If True, only log operations without executing them
        """
        self.dry_run = dry_run

    def organize_files(
        self, results: List[Dict[str, Any]], target_dir: Path, operation: str = "copy"
    ) -> Dict[str, Any]:
        """Organize files based on classification results.

        Args:
            results: List of classification results
            target_dir: Target directory for organization
            operation: 'copy' or 'move'

        Returns:
            Summary of operations performed
        """
        if operation not in ["copy", "move"]:
            raise ValueError("Operation must be 'copy' or 'move'")

        target_dir = Path(target_dir)
        screenshots_dir = target_dir / "screenshots"
        other_dir = target_dir / "other"

        summary = {
            "total_files": len(results),
            "screenshots_moved": 0,
            "other_moved": 0,
            "errors": 0,
            "skipped": 0,
            "operation": operation,
            "dry_run": self.dry_run,
        }

        if not self.dry_run:
            screenshots_dir.mkdir(parents=True, exist_ok=True)
            other_dir.mkdir(parents=True, exist_ok=True)
        else:
            logger.info(
                "DRY RUN: Would create directories",
                screenshots_dir=str(screenshots_dir),
                other_dir=str(other_dir),
            )

        for result in results:
            source_path = Path(result["file_path"])
            classification = result["classification"]

            if not source_path.exists():
                logger.warning("Source file not found", source=str(source_path))
                summary["errors"] += 1
                continue

            if classification == "screenshot":
                dest_dir = screenshots_dir
                summary["screenshots_moved"] += 1
            elif classification == "other":
                dest_dir = other_dir
                summary["other_moved"] += 1
            else:
                logger.warning(
                    "Skipping file with unknown classification",
                    source=str(source_path),
                    classification=classification,
                )
                summary["skipped"] += 1
                continue

            dest_path = dest_dir / source_path.name

            if dest_path.exists():
                dest_path = self._get_unique_path(dest_path)

            try:
                if self.dry_run:
                    logger.info(
                        f"DRY RUN: Would {operation} file",
                        source=str(source_path),
                        destination=str(dest_path),
                        classification=classification,
                    )
                else:
                    if operation == "copy":
                        shutil.copy2(source_path, dest_path)
                        logger.info(
                            "Copied file",
                            source=str(source_path),
                            destination=str(dest_path),
                            classification=classification,
                        )
                    else:  # move
                        shutil.move(str(source_path), str(dest_path))
                        logger.info(
                            "Moved file",
                            source=str(source_path),
                            destination=str(dest_path),
                            classification=classification,
                        )

            except Exception as e:
                logger.error(
                    f"Failed to {operation} file",
                    source=str(source_path),
                    destination=str(dest_path),
                    error=str(e),
                )
                summary["errors"] += 1

        logger.info("File organization completed", summary=summary)

        return summary

    def _get_unique_path(self, path: Path) -> Path:
        """Get a unique path by adding a counter if file exists.

        Args:
            path: Original path

        Returns:
            Unique path
        """
        if not path.exists():
            return path

        counter = 1
        stem = path.stem
        suffix = path.suffix
        parent = path.parent

        while True:
            new_name = f"{stem}_{counter:03d}{suffix}"
            new_path = parent / new_name

            if not new_path.exists():
                return new_path

            counter += 1

            if counter > 999:
                raise RuntimeError(f"Could not create unique path for {path}")

    def validate_target_directory(self, target_dir: Path) -> bool:
        """Validate that target directory can be used.

        Args:
            target_dir: Target directory path

        Returns:
            True if directory is valid
        """
        target_dir = Path(target_dir)

        if target_dir.exists():
            if not target_dir.is_dir():
                logger.error(
                    "Target exists but is not a directory", target=str(target_dir)
                )
                return False

            if not self.dry_run:
                try:
                    test_file = target_dir / ".test_write"
                    test_file.touch()
                    test_file.unlink()
                except Exception as e:
                    logger.error(
                        "Target directory is not writable",
                        target=str(target_dir),
                        error=str(e),
                    )
                    return False
        else:
            if not self.dry_run:
                try:
                    target_dir.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    logger.error(
                        "Cannot create target directory",
                        target=str(target_dir),
                        error=str(e),
                    )
                    return False

        return True

    def estimate_space_needed(self, results: List[Dict[str, Any]]) -> Dict[str, int]:
        """Estimate disk space needed for file operations.

        Args:
            results: List of classification results

        Returns:
            Dictionary with space estimates in bytes
        """
        total_size = 0
        screenshot_size = 0
        other_size = 0

        for result in results:
            source_path = Path(result["file_path"])
            classification = result["classification"]

            if source_path.exists():
                file_size = source_path.stat().st_size
                total_size += file_size

                if classification == "screenshot":
                    screenshot_size += file_size
                elif classification == "other":
                    other_size += file_size

        return {
            "total_bytes": total_size,
            "screenshot_bytes": screenshot_size,
            "other_bytes": other_size,
            "total_mb": total_size / (1024 * 1024),
            "screenshot_mb": screenshot_size / (1024 * 1024),
            "other_mb": other_size / (1024 * 1024),
        }

    def get_operation_summary(self, results: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get summary of what operations would be performed.

        Args:
            results: List of classification results

        Returns:
            Summary dictionary
        """
        summary = {
            "total_files": len(results),
            "screenshots": 0,
            "other": 0,
            "errors": 0,
            "unknown": 0,
        }

        for result in results:
            classification = result["classification"]

            if classification == "screenshot":
                summary["screenshots"] += 1
            elif classification == "other":
                summary["other"] += 1
            elif classification is None:
                summary["errors"] += 1
            else:
                summary["unknown"] += 1

        return summary
