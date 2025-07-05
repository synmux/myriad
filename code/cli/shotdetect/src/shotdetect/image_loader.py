"""Image loading utilities with support for HEIC and DNG formats."""

import base64
import io
import logging
from pathlib import Path
from typing import List, Optional, Tuple, Union

import pillow_heif
import rawpy
import structlog
from PIL import Image

logger = structlog.get_logger(__name__)

pillow_heif.register_heif_opener()


class ImageLoader:
    """Loads images from various formats including HEIC and DNG."""

    SUPPORTED_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".webp",
        ".tiff",
        ".tif",
        ".heic",
        ".heif",
        ".dng",
        ".nef",
        ".cr2",
        ".cr3",
        ".arw",
        ".orf",
        ".rw2",
    }

    RAW_EXTENSIONS = {".dng", ".nef", ".cr2", ".cr3", ".arw", ".orf", ".rw2"}
    HEIC_EXTENSIONS = {".heic", ".heif"}

    def __init__(self, max_size: Tuple[int, int] = (2048, 2048)):
        """Initialize image loader.

        Args:
            max_size: Maximum image dimensions for resizing large images
        """
        self.max_size = max_size

    def is_supported(self, file_path: Union[str, Path]) -> bool:
        """Check if file format is supported.

        Args:
            file_path: Path to the image file

        Returns:
            True if the file format is supported
        """
        path = Path(file_path)
        return path.suffix.lower() in self.SUPPORTED_EXTENSIONS

    def load_image(self, file_path: Union[str, Path]) -> Optional[Image.Image]:
        """Load an image from file.

        Args:
            file_path: Path to the image file

        Returns:
            PIL Image object or None if loading failed
        """
        path = Path(file_path)

        if not path.exists():
            logger.warning("File not found", file_path=str(path))
            return None

        if not self.is_supported(path):
            logger.warning(
                "Unsupported file format", file_path=str(path), extension=path.suffix
            )
            return None

        try:
            if path.suffix.lower() in self.RAW_EXTENSIONS:
                return self._load_raw_image(path)
            elif path.suffix.lower() in self.HEIC_EXTENSIONS:
                return self._load_heic_image(path)
            else:
                return self._load_standard_image(path)
        except Exception as e:
            logger.error("Failed to load image", file_path=str(path), error=str(e))
            return None

    def _load_standard_image(self, file_path: Path) -> Optional[Image.Image]:
        """Load standard image formats using PIL."""
        try:
            with Image.open(file_path) as img:
                img = img.convert("RGB")
                if img.size[0] > self.max_size[0] or img.size[1] > self.max_size[1]:
                    img.thumbnail(self.max_size, Image.Resampling.LANCZOS)
                return img.copy()
        except Exception as e:
            logger.error(
                "Failed to load standard image", file_path=str(file_path), error=str(e)
            )
            return None

    def _load_heic_image(self, file_path: Path) -> Optional[Image.Image]:
        """Load HEIC/HEIF image using pillow-heif."""
        try:
            with Image.open(file_path) as img:
                img = img.convert("RGB")
                if img.size[0] > self.max_size[0] or img.size[1] > self.max_size[1]:
                    img.thumbnail(self.max_size, Image.Resampling.LANCZOS)
                return img.copy()
        except Exception as e:
            logger.error(
                "Failed to load HEIC image", file_path=str(file_path), error=str(e)
            )
            return None

    def _load_raw_image(self, file_path: Path) -> Optional[Image.Image]:
        """Load RAW image using rawpy."""
        try:
            with rawpy.imread(str(file_path)) as raw:
                rgb_array = raw.postprocess(
                    use_camera_wb=True,
                    half_size=False,
                    no_auto_bright=True,
                    output_color=rawpy.ColorSpace.sRGB,
                    output_bps=8,
                )

                img = Image.fromarray(rgb_array)
                if img.size[0] > self.max_size[0] or img.size[1] > self.max_size[1]:
                    img.thumbnail(self.max_size, Image.Resampling.LANCZOS)
                return img
        except Exception as e:
            logger.error(
                "Failed to load RAW image", file_path=str(file_path), error=str(e)
            )
            return None

    def image_to_base64(
        self, image: Image.Image, format: str = "JPEG", quality: int = 85
    ) -> str:
        """Convert PIL Image to base64 string.

        Args:
            image: PIL Image object
            format: Output format (JPEG, PNG, etc.)
            quality: JPEG quality (1-100)

        Returns:
            Base64 encoded image string
        """
        buffer = io.BytesIO()

        if format.upper() == "JPEG":
            image.save(buffer, format=format, quality=quality, optimize=True)
        else:
            image.save(buffer, format=format)

        buffer.seek(0)
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

    def scan_directory(
        self, directory: Union[str, Path], recursive: bool = True
    ) -> List[Path]:
        """Scan directory for supported image files.

        Args:
            directory: Directory to scan
            recursive: Whether to scan subdirectories

        Returns:
            List of image file paths
        """
        dir_path = Path(directory)

        if not dir_path.exists() or not dir_path.is_dir():
            logger.error("Directory does not exist", directory=str(dir_path))
            return []

        pattern = "**/*" if recursive else "*"
        image_files = []

        for file_path in dir_path.glob(pattern):
            if file_path.is_file() and self.is_supported(file_path):
                image_files.append(file_path)

        logger.info(
            "Scanned directory",
            directory=str(dir_path),
            files_found=len(image_files),
            recursive=recursive,
        )

        return sorted(image_files)

    def get_image_info(self, file_path: Union[str, Path]) -> dict:
        """Get basic information about an image file.

        Args:
            file_path: Path to the image file

        Returns:
            Dictionary with image information
        """
        path = Path(file_path)

        info = {
            "path": str(path),
            "name": path.name,
            "extension": path.suffix.lower(),
            "size_bytes": path.stat().st_size if path.exists() else 0,
            "supported": self.is_supported(path),
            "format_type": "unknown",
        }

        if path.suffix.lower() in self.RAW_EXTENSIONS:
            info["format_type"] = "raw"
        elif path.suffix.lower() in self.HEIC_EXTENSIONS:
            info["format_type"] = "heic"
        elif path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
            info["format_type"] = "standard"

        return info
