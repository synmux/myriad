"""
Image processing functionality for extracting dimensions from image files.
"""

import concurrent.futures
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

import pillow_heif
import rawpy
import structlog

# Import Pillow and HEIC support
from PIL import Image, ImageFile

from .utils import format_file_size, get_file_size

# Enable loading of truncated images and register HEIF opener
ImageFile.LOAD_TRUNCATED_IMAGES = True
pillow_heif.register_heif_opener()

# Disable PIL's MAX_IMAGE_PIXELS limit to handle large images
# This allows processing of very large images that would otherwise be rejected
# as potential decompression bomb attacks
Image.MAX_IMAGE_PIXELS = None


@dataclass
class ImageInfo:
    """Information about a single image file."""

    path: str
    width: int
    height: int
    file_size: int
    dimensions_str: str

    def __post_init__(self):
        """Generate dimensions string after initialization."""
        if not self.dimensions_str:
            self.dimensions_str = f"{self.width}×{self.height}"


@dataclass
class DimensionStats:
    """Statistics for a specific dimension."""

    width: int
    height: int
    count: int
    total_size: int
    files: List[str]

    @property
    def dimensions_str(self) -> str:
        """Get dimensions as formatted string."""
        return f"{self.width}×{self.height}"

    @property
    def formatted_size(self) -> str:
        """Get total size as formatted string."""
        return format_file_size(self.total_size)


class ImageProcessor:
    """Processes image files to extract dimension information."""

    def __init__(self, logger: structlog.BoundLogger):
        """
        Initialize the image processor.

        Args:
            logger: Structured logger instance
        """
        self.logger = logger
        self.failed_files: List[str] = []
        self.processed_files: List[ImageInfo] = []
        self._dimension_cache: Dict[str, Tuple[int, int]] = {}
        self._progress_lock = threading.Lock()

    def process_images(
        self,
        image_paths: List[Path],
        max_workers: int = 1,
        progress_callback: Optional[Callable[[int], None]] = None,
    ) -> Dict[str, DimensionStats]:
        """
        Process multiple image files to extract dimensions.

        Args:
            image_paths: List of image file paths
            max_workers: Number of worker threads (1 for single-threaded)
            progress_callback: Optional callback function called after each processed image

        Returns:
            Dictionary mapping dimension strings to DimensionStats
        """
        self.logger.info(
            "Starting image processing",
            total_images=len(image_paths),
            workers=max_workers,
        )

        # Process images
        if max_workers == 1:
            # Single-threaded processing
            for path in image_paths:
                self._process_single_image(path)
                if progress_callback:
                    progress_callback(1)
        else:
            # Multi-threaded processing
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=max_workers
            ) as executor:
                futures = [
                    executor.submit(
                        self._process_single_image_with_callback,
                        path,
                        progress_callback,
                    )
                    for path in image_paths
                ]

                for future in concurrent.futures.as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        self.logger.error("Thread processing error", error=str(e))

        # Aggregate results
        results = self._aggregate_results()

        self.logger.info(
            "Image processing completed",
            processed=len(self.processed_files),
            failed=len(self.failed_files),
            unique_dimensions=len(results),
        )

        return results

    def _process_single_image_with_callback(
        self, image_path: Path, progress_callback: Optional[Callable[[int], None]]
    ) -> Optional[ImageInfo]:
        """
        Process a single image with progress callback (for multithreading).

        Args:
            image_path: Path to the image file
            progress_callback: Optional callback function for progress updates

        Returns:
            ImageInfo object if successful, None otherwise
        """
        result = self._process_single_image(image_path)
        if progress_callback:
            progress_callback(1)
        return result

    def _create_and_store_image_info(
        self, path_str: str, width: int, height: int, file_size: int
    ) -> ImageInfo:
        """
        Create ImageInfo object and store it in processed files list.

        Args:
            path_str: Path as string
            width: Image width in pixels
            height: Image height in pixels
            file_size: File size in bytes

        Returns:
            Created ImageInfo object
        """
        info = ImageInfo(
            path=path_str,
            width=width,
            height=height,
            file_size=file_size,
            dimensions_str="",
        )
        with self._progress_lock:
            self.processed_files.append(info)
        return info

    def _process_single_image(self, image_path: Path) -> Optional[ImageInfo]:
        """
        Process a single image file to extract dimensions.

        Args:
            image_path: Path to the image file

        Returns:
            ImageInfo object if successful, None otherwise
        """
        try:
            # Check cache first
            path_str = str(image_path)
            if path_str in self._dimension_cache:
                width, height = self._dimension_cache[path_str]
                file_size = get_file_size(image_path)
                return self._create_and_store_image_info(
                    path_str, width, height, file_size
                )

            # Handle DNG files (RAW format) using rawpy
            if image_path.suffix.lower() == ".dng":
                with rawpy.imread(str(image_path)) as raw:
                    # Get RAW image dimensions from the RAW file
                    width, height = raw.sizes.raw_width, raw.sizes.raw_height
                    file_size = get_file_size(image_path)

                    # Cache the result
                    self._dimension_cache[path_str] = (width, height)

                    return self._create_and_store_image_info(
                        path_str, width, height, file_size
                    )
            else:
                # Open and get dimensions for regular image files
                with Image.open(image_path) as img:
                    width, height = img.size
                    file_size = get_file_size(image_path)

                    # Cache the result
                    self._dimension_cache[path_str] = (width, height)

                    return self._create_and_store_image_info(
                        path_str, width, height, file_size
                    )

        except Exception as e:
            self.logger.warning(
                "Failed to process image", file=str(image_path), error=str(e)
            )
            with self._progress_lock:
                self.failed_files.append(str(image_path))
            return None

    def _aggregate_results(self) -> Dict[str, DimensionStats]:
        """
        Aggregate processed image results by dimensions.

        Returns:
            Dictionary mapping dimension strings to DimensionStats
        """
        dimension_map: Dict[str, DimensionStats] = {}

        for info in self.processed_files:
            dim_str = info.dimensions_str

            if dim_str not in dimension_map:
                dimension_map[dim_str] = DimensionStats(
                    width=info.width,
                    height=info.height,
                    count=0,
                    total_size=0,
                    files=[],
                )

            stats = dimension_map[dim_str]
            stats.count += 1
            stats.total_size += info.file_size
            stats.files.append(info.path)

        return dimension_map

    def get_failed_files(self) -> List[str]:
        """
        Get list of files that failed to process.

        Returns:
            List of failed file paths
        """
        return self.failed_files.copy()

    def get_processed_files(self) -> List[ImageInfo]:
        """
        Get list of successfully processed files.

        Returns:
            List of ImageInfo objects
        """
        return self.processed_files.copy()

    def clear_cache(self) -> None:
        """Clear the dimension cache."""
        self._dimension_cache.clear()

    def reset_counters(self) -> None:
        """Reset failed and processed file lists."""
        self.failed_files.clear()
        self.processed_files.clear()


def get_image_dimensions(image_path: Path) -> Optional[Tuple[int, int]]:
    """
    Get dimensions of a single image file.

    Args:
        image_path: Path to the image file

    Returns:
        Tuple of (width, height) or None if failed
    """
    try:
        # Handle DNG files (RAW format) using rawpy
        if image_path.suffix.lower() == ".dng":
            with rawpy.imread(str(image_path)) as raw:
                return (raw.sizes.raw_width, raw.sizes.raw_height)
        else:
            # Handle regular image files using PIL
            with Image.open(image_path) as img:
                return img.size
    except Exception:
        return None
