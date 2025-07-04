"""
File organization functionality for arranging images by dimensions.
"""

import shutil
from enum import Enum
from pathlib import Path
from typing import Dict, List

import structlog

from .processor import DimensionStats
from .utils import ensure_directory, safe_filename


class OperationType(Enum):
    """Types of file operations."""

    MOVE = "move"
    COPY = "copy"
    SYMLINK = "symlink"


class FileOrganizer:
    """Organizes image files by dimensions using move, copy, or symlink operations."""

    def __init__(self, logger: structlog.BoundLogger):
        """
        Initialize the file organizer.

        Args:
            logger: Structured logger instance
        """
        self.logger = logger
        self.success_count: int = 0
        self.failure_count: int = 0
        self.failed_operations: List[Dict] = []

    def organize_files(
        self,
        results: Dict[str, DimensionStats],
        target_directory: Path,
        operation: OperationType,
        dry_run: bool = False,
    ) -> None:
        """
        Organize files by dimensions into subdirectories.

        Args:
            results: Dictionary of dimension statistics
            target_directory: Base directory for organized files
            operation: Type of operation (move, copy, symlink)
            dry_run: If True, preview operations without executing
        """
        self.logger.info(
            "Starting file organization",
            operation=operation.value,
            target_directory=str(target_directory),
            dry_run=dry_run,
            dimensions_count=len(results),
        )

        if dry_run:
            self._preview_operations(results, target_directory, operation)
        else:
            self._execute_operations(results, target_directory, operation)

        self.logger.info(
            "File organization completed",
            success_count=self.success_count,
            failure_count=self.failure_count,
        )

    def _preview_operations(
        self,
        results: Dict[str, DimensionStats],
        target_directory: Path,
        operation: OperationType,
    ) -> None:
        """
        Preview operations without executing them.

        Args:
            results: Dictionary of dimension statistics
            target_directory: Base directory for organized files
            operation: Type of operation
        """
        self.logger.info("[DRY RUN] Previewing file operations")

        total_files = 0
        for dimension_str, stats in results.items():
            safe_dim = safe_filename(dimension_str)
            dimension_dir = target_directory / safe_dim

            total_files += len(stats.files)

            self.logger.info(f"[DRY RUN] Would create directory: {dimension_dir}")
            self.logger.info(
                f"[DRY RUN] Would {operation.value} {len(stats.files)} files to {dimension_dir}"
            )

            # Show sample files
            sample_files = stats.files[:3]
            for file_path in sample_files:
                source = Path(file_path)
                target = dimension_dir / source.name
                self.logger.info(f"[DRY RUN] {source} -> {target}")

            if len(stats.files) > 3:
                self.logger.info(f"[DRY RUN] ... and {len(stats.files) - 3} more files")

        self.logger.info(f"[DRY RUN] Total files to {operation.value}: {total_files}")

    def _execute_operations(
        self,
        results: Dict[str, DimensionStats],
        target_directory: Path,
        operation: OperationType,
    ) -> None:
        """
        Execute file operations.

        Args:
            results: Dictionary of dimension statistics
            target_directory: Base directory for organized files
            operation: Type of operation
        """
        self.success_count = 0
        self.failure_count = 0
        self.failed_operations.clear()

        # Ensure target directory exists
        try:
            ensure_directory(target_directory)
        except OSError as e:
            self.logger.error(
                "Cannot create target directory",
                directory=str(target_directory),
                error=str(e),
            )
            return

        for dimension_str, stats in results.items():
            safe_dim = safe_filename(dimension_str)
            dimension_dir = target_directory / safe_dim

            # Create dimension subdirectory
            try:
                ensure_directory(dimension_dir)
                self.logger.info(
                    "Created dimension directory", directory=str(dimension_dir)
                )
            except OSError as e:
                self.logger.error(
                    "Cannot create dimension directory",
                    directory=str(dimension_dir),
                    error=str(e),
                )
                self.failure_count += len(stats.files)
                continue

            # Process files in this dimension
            for file_path in stats.files:
                self._process_single_file(Path(file_path), dimension_dir, operation)

    def _process_single_file(
        self, source_path: Path, target_dir: Path, operation: OperationType
    ) -> None:
        """
        Process a single file operation.

        Args:
            source_path: Source file path
            target_dir: Target directory
            operation: Type of operation
        """
        target_path = target_dir / source_path.name

        # Handle filename conflicts
        if target_path.exists():
            target_path = self._resolve_filename_conflict(target_path)

        try:
            if operation == OperationType.MOVE:
                shutil.move(str(source_path), str(target_path))
            elif operation == OperationType.COPY:
                shutil.copy2(str(source_path), str(target_path))
            elif operation == OperationType.SYMLINK:
                # Create relative symlink if possible
                try:
                    relative_source = source_path.resolve().relative_to(
                        target_path.parent.resolve()
                    )
                    target_path.symlink_to(relative_source)
                except ValueError:
                    # Use absolute path if relative doesn't work
                    target_path.symlink_to(source_path.resolve())

            self.success_count += 1
            self.logger.debug(
                f"Successfully {operation.value}d file",
                source=str(source_path),
                target=str(target_path),
            )

        except Exception as e:
            self.failure_count += 1
            error_info = {
                "source": str(source_path),
                "target": str(target_path),
                "operation": operation.value,
                "error": str(e),
            }
            self.failed_operations.append(error_info)
            self.logger.warning(
                f"Failed to {operation.value} file",
                source=str(source_path),
                target=str(target_path),
                error=str(e),
            )

    def _resolve_filename_conflict(self, target_path: Path) -> Path:
        """
        Resolve filename conflicts by adding a suffix.

        Args:
            target_path: Original target path

        Returns:
            New target path that doesn't conflict
        """
        base_name = target_path.stem
        extension = target_path.suffix
        parent = target_path.parent

        counter = 1
        while True:
            new_name = f"{base_name}_{counter}{extension}"
            new_path = parent / new_name
            if not new_path.exists():
                return new_path
            counter += 1

    def get_failed_operations(self) -> List[Dict]:
        """
        Get list of failed operations.

        Returns:
            List of dictionaries containing failure information
        """
        return self.failed_operations.copy()

    def get_statistics(self) -> Dict:
        """
        Get organization statistics.

        Returns:
            Dictionary with success/failure counts
        """
        return {
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "total_operations": self.success_count + self.failure_count,
        }

    def reset_counters(self) -> None:
        """Reset success and failure counters."""
        self.success_count = 0
        self.failure_count = 0
        self.failed_operations.clear()


def validate_operation_type(operation_str: str) -> OperationType:
    """
    Validate and convert operation string to OperationType.

    Args:
        operation_str: Operation string ("move", "copy", "symlink")

    Returns:
        OperationType enum value

    Raises:
        ValueError: If operation string is invalid
    """
    try:
        return OperationType(operation_str)
    except ValueError as e:
        valid_operations = [op.value for op in OperationType]
        raise ValueError(
            f"Invalid operation: {operation_str}. Must be one of: {valid_operations}"
        ) from e


def check_target_directory_writable(target_dir: Path) -> bool:
    """
    Check if target directory is writable.

    Args:
        target_dir: Directory to check

    Returns:
        True if directory is writable, False otherwise
    """
    try:
        if not target_dir.exists():
            target_dir.mkdir(parents=True, exist_ok=True)

        # Test write permissions by creating a temporary file
        test_file = target_dir / ".dimensions_write_test"
        test_file.touch()
        test_file.unlink()
        return True

    except OSError:
        return False
