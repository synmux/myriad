"""
Directory scanning functionality for finding image files.
"""

from pathlib import Path
from typing import Iterator, List

import structlog

from .utils import is_image_file


class DirectoryScanner:
    """Scans directories for image files recursively."""

    def __init__(self, logger: structlog.BoundLogger):
        """
        Initialize the directory scanner.

        Args:
            logger: Structured logger instance
        """
        self.logger = logger
        self.failed_files: List[str] = []
        self.skipped_files: List[str] = []

    def scan_directory(self, directory: Path) -> Iterator[Path]:
        """
        Scan directory recursively for image files.

        Args:
            directory: Directory path to scan

        Yields:
            Path objects for each image file found

        Raises:
            FileNotFoundError: If directory doesn't exist
            PermissionError: If directory is not accessible
        """
        if not directory.exists():
            raise FileNotFoundError(f"Directory does not exist: {directory}")

        if not directory.is_dir():
            raise NotADirectoryError(f"Path is not a directory: {directory}")

        self.logger.info("Starting directory scan", directory=str(directory))

        try:
            yield from self._scan_recursive(directory)
        except PermissionError as e:
            self.logger.error(
                "Permission denied accessing directory",
                directory=str(directory),
                error=str(e),
            )
            raise

        self.logger.info(
            "Directory scan completed",
            failed_files=len(self.failed_files),
            skipped_files=len(self.skipped_files),
        )

    def _scan_recursive(self, directory: Path) -> Iterator[Path]:
        """
        Recursively scan directory for image files.

        Args:
            directory: Directory to scan

        Yields:
            Path objects for each image file found
        """
        try:
            entries = list(directory.iterdir())
        except OSError as e:
            self.logger.warning(
                "Cannot access directory", directory=str(directory), error=str(e)
            )
            self.failed_files.append(str(directory))
            return

        for entry in entries:
            try:
                if entry.is_file():
                    if is_image_file(entry):
                        yield entry
                    else:
                        self.skipped_files.append(str(entry))

                elif entry.is_dir():
                    # Skip hidden directories and common system directories
                    if not entry.name.startswith(".") and entry.name not in {
                        "__pycache__",
                        "node_modules",
                        ".git",
                        ".svn",
                        ".hg",
                    }:
                        yield from self._scan_recursive(entry)

            except OSError as e:
                self.logger.warning(
                    "Cannot access file/directory", path=str(entry), error=str(e)
                )
                self.failed_files.append(str(entry))
                continue

    def count_images(self, directory: Path) -> int:
        """
        Count total number of image files in directory (for progress calculation).

        Args:
            directory: Directory path to count

        Returns:
            Total number of image files found
        """
        count = 0
        try:
            for _ in self.scan_directory(directory):
                count += 1
        except Exception as e:
            self.logger.error(
                "Error counting images", directory=str(directory), error=str(e)
            )

        return count

    def get_failed_files(self) -> List[str]:
        """
        Get list of files/directories that couldn't be accessed.

        Returns:
            List of failed file paths
        """
        return self.failed_files.copy()

    def get_skipped_files(self) -> List[str]:
        """
        Get list of files that were skipped (not image files).

        Returns:
            List of skipped file paths
        """
        return self.skipped_files.copy()

    def reset_counters(self) -> None:
        """Reset failed and skipped file counters."""
        self.failed_files.clear()
        self.skipped_files.clear()


def find_image_files(directory: Path, logger: structlog.BoundLogger) -> List[Path]:
    """
    Convenience function to find all image files in a directory.

    Args:
        directory: Directory to scan
        logger: Logger instance

    Returns:
        List of image file paths
    """
    scanner = DirectoryScanner(logger)
    return list(scanner.scan_directory(directory))
