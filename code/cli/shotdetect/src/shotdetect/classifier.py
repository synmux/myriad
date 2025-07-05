"""Image classification logic for screenshot detection."""

import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import structlog

from .image_loader import ImageLoader
from .ollama_client import OllamaClient

logger = structlog.get_logger(__name__)


class ImageClassifier:
    """Main classifier for detecting screenshots in images."""

    def __init__(
        self,
        model_name: str = "qwen2.5vl:7b",
        batch_size: int = 5,
        max_image_size: Tuple[int, int] = (1024, 1024),
    ):
        """Initialize image classifier.

        Args:
            model_name: Ollama model name to use
            batch_size: Number of images to process concurrently
            max_image_size: Maximum image dimensions for processing
        """
        self.model_name = model_name
        self.batch_size = batch_size
        self.image_loader = ImageLoader(max_size=max_image_size)
        self.ollama_client = OllamaClient()

    async def classify_directory(
        self,
        directory: Path,
        recursive: bool = True,
        progress_callback: Optional[callable] = None,
    ) -> List[Dict[str, Any]]:
        """Classify all images in a directory.

        Args:
            directory: Directory containing images
            recursive: Whether to scan subdirectories
            progress_callback: Optional callback for progress updates

        Returns:
            List of classification results
        """
        if not self.ollama_client.check_connection():
            raise RuntimeError("Cannot connect to Ollama server")

        if not self.ollama_client.ensure_model_available(self.model_name):
            raise RuntimeError(f"Model {self.model_name} is not available")

        image_files = self.image_loader.scan_directory(directory, recursive)

        if not image_files:
            logger.warning("No supported images found", directory=str(directory))
            return []

        logger.info(
            "Starting classification",
            directory=str(directory),
            total_files=len(image_files),
            model=self.model_name,
        )

        results = []

        async with self.ollama_client:
            for i in range(0, len(image_files), self.batch_size):
                batch_files = image_files[i : i + self.batch_size]

                batch_data = []
                for file_path in batch_files:
                    image = self.image_loader.load_image(file_path)
                    if image:
                        image_base64 = self.image_loader.image_to_base64(
                            image, "JPEG", 75
                        )
                        batch_data.append((file_path, image_base64))
                    else:
                        results.append(
                            {
                                "file_path": str(file_path),
                                "classification": None,
                                "error": "Failed to load image",
                            }
                        )

                if batch_data:
                    batch_results = await self.ollama_client.classify_images_batch(
                        batch_data, self.model_name, len(batch_data)
                    )

                    for file_path, classification in batch_results:
                        result = {
                            "file_path": str(file_path),
                            "classification": classification,
                            "error": (
                                None if classification else "Classification failed"
                            ),
                        }
                        results.append(result)

                        logger.info(
                            "Classified image",
                            file_path=str(file_path),
                            classification=classification,
                        )

                if progress_callback:
                    progress_callback(
                        min(i + self.batch_size, len(image_files)), len(image_files)
                    )

        screenshot_count = sum(
            1 for r in results if r["classification"] == "screenshot"
        )
        other_count = sum(1 for r in results if r["classification"] == "other")
        error_count = sum(1 for r in results if r["classification"] is None)

        logger.info(
            "Classification completed",
            total=len(results),
            screenshots=screenshot_count,
            other=other_count,
            errors=error_count,
        )

        return results

    async def classify_single_image(self, file_path: Path) -> Dict[str, Any]:
        """Classify a single image.

        Args:
            file_path: Path to the image file

        Returns:
            Classification result
        """
        if not self.ollama_client.check_connection():
            raise RuntimeError("Cannot connect to Ollama server")

        if not self.ollama_client.ensure_model_available(self.model_name):
            raise RuntimeError(f"Model {self.model_name} is not available")

        image = self.image_loader.load_image(file_path)
        if not image:
            return {
                "file_path": str(file_path),
                "classification": None,
                "error": "Failed to load image",
            }

        image_base64 = self.image_loader.image_to_base64(image, "JPEG", 75)

        async with self.ollama_client:
            classification = await self.ollama_client.classify_image(
                image_base64, self.model_name
            )

        return {
            "file_path": str(file_path),
            "classification": classification,
            "error": None if classification else "Classification failed",
        }

    def get_supported_extensions(self) -> set:
        """Get set of supported file extensions.

        Returns:
            Set of supported file extensions
        """
        return self.image_loader.SUPPORTED_EXTENSIONS

    def validate_model(self) -> bool:
        """Validate that the model is available and working.

        Returns:
            True if model is available and working
        """
        try:
            if not self.ollama_client.check_connection():
                logger.error("Cannot connect to Ollama server")
                return False

            if not self.ollama_client.has_model(self.model_name):
                logger.error("Model not available", model=self.model_name)
                return False

            return True

        except Exception as e:
            logger.error("Model validation failed", error=str(e))
            return False

    def download_model_if_needed(self) -> bool:
        """Download the model if it's not available.

        Returns:
            True if model is available after download attempt
        """
        return self.ollama_client.ensure_model_available(self.model_name)

    def get_model_info(self) -> Optional[Dict[str, Any]]:
        """Get information about the current model.

        Returns:
            Model information or None if not available
        """
        return self.ollama_client.get_model_info(self.model_name)
