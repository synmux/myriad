"""Ollama client for managing models and performing image classification."""

import asyncio
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import aiohttp
import requests
import structlog

logger = structlog.get_logger(__name__)


class OllamaClient:
    """Client for interacting with Ollama API."""

    def __init__(self, base_url: str = "http://localhost:11434"):
        """Initialize Ollama client.

        Args:
            base_url: Base URL for Ollama API
        """
        self.base_url = base_url.rstrip("/")
        self.session = None

    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()

    def check_connection(self) -> bool:
        """Check if Ollama server is available.

        Returns:
            True if server is reachable
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error("Failed to connect to Ollama", error=str(e))
            return False

    def list_models(self) -> List[Dict[str, Any]]:
        """List available models.

        Returns:
            List of model information dictionaries
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            response.raise_for_status()

            data = response.json()
            models = data.get("models", [])

            logger.info("Listed models", count=len(models))
            return models
        except Exception as e:
            logger.error("Failed to list models", error=str(e))
            return []

    def has_model(self, model_name: str) -> bool:
        """Check if a specific model is available.

        Args:
            model_name: Name of the model to check

        Returns:
            True if model is available
        """
        models = self.list_models()
        return any(model["name"] == model_name for model in models)

    def download_model(self, model_name: str) -> bool:
        """Download a model.

        Args:
            model_name: Name of the model to download

        Returns:
            True if download was successful
        """
        try:
            logger.info("Starting model download", model=model_name)

            response = requests.post(
                f"{self.base_url}/api/pull",
                json={"name": model_name},
                stream=True,
                timeout=300,
            )
            response.raise_for_status()

            for line in response.iter_lines(decode_unicode=True):
                if line:
                    try:
                        data = json.loads(line)
                        if "status" in data:
                            logger.info(
                                "Download progress",
                                model=model_name,
                                status=data["status"],
                            )
                        if data.get("error"):
                            logger.error(
                                "Download error", model=model_name, error=data["error"]
                            )
                            return False
                    except json.JSONDecodeError:
                        continue

            logger.info("Model download completed", model=model_name)
            return True

        except Exception as e:
            logger.error("Failed to download model", model=model_name, error=str(e))
            return False

    def download_model_variants(self, model_pattern: str) -> List[str]:
        """Download all variants of a model (e.g., qwen2.5vl:*).

        Args:
            model_pattern: Pattern like "qwen2.5vl:*"

        Returns:
            List of successfully downloaded model names
        """
        if not model_pattern.endswith(":*"):
            logger.warning("Model pattern should end with ':*'", pattern=model_pattern)
            return []

        base_name = model_pattern[:-2]

        try:
            response = requests.get("https://ollama.com/api/tags", timeout=10)
            response.raise_for_status()

            available_models = response.json().get("models", [])
            matching_models = [
                model["name"]
                for model in available_models
                if model["name"].startswith(base_name + ":")
            ]

            logger.info(
                "Found matching models",
                pattern=model_pattern,
                count=len(matching_models),
            )

            downloaded = []
            for model_name in matching_models:
                if self.download_model(model_name):
                    downloaded.append(model_name)

            return downloaded

        except Exception as e:
            logger.error(
                "Failed to download model variants", pattern=model_pattern, error=str(e)
            )
            return []

    async def classify_image(
        self, image_base64: str, model_name: str = "qwen2.5vl:7b"
    ) -> Optional[str]:
        """Classify an image using a vision model.

        Args:
            image_base64: Base64 encoded image
            model_name: Name of the vision model to use

        Returns:
            Classification result or None if failed
        """
        if not self.session:
            raise RuntimeError(
                "Client not initialized. Use 'async with' context manager."
            )

        prompt = """Look at this image and determine if it is a screenshot or not.

A screenshot is an image that shows:
- Computer desktop, windows, or applications
- Mobile phone interface or app screens
- Web browser content
- Terminal or command line interface
- Any other digital interface capture

Respond with exactly one word: "screenshot" or "other"."""

        payload = {
            "model": model_name,
            "prompt": prompt,
            "images": [image_base64],
            "stream": False,
        }

        try:
            async with self.session.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=60),
            ) as response:
                response.raise_for_status()

                data = await response.json()
                result = data.get("response", "").strip().lower()

                if "screenshot" in result:
                    return "screenshot"
                elif "other" in result:
                    return "other"
                else:
                    logger.warning(
                        "Unexpected classification result",
                        result=result,
                        model=model_name,
                    )
                    return None

        except Exception as e:
            logger.error("Failed to classify image", model=model_name, error=str(e))
            return None

    async def classify_images_batch(
        self,
        image_data: List[tuple],
        model_name: str = "qwen2.5vl:7b",
        batch_size: int = 5,
    ) -> List[tuple]:
        """Classify multiple images in batches.

        Args:
            image_data: List of (file_path, image_base64) tuples
            model_name: Name of the vision model to use
            batch_size: Number of images to process concurrently

        Returns:
            List of (file_path, classification) tuples
        """
        results = []

        for i in range(0, len(image_data), batch_size):
            batch = image_data[i : i + batch_size]

            tasks = [
                self.classify_image(image_base64, model_name)
                for file_path, image_base64 in batch
            ]

            batch_results = await asyncio.gather(*tasks, return_exceptions=True)

            for j, (file_path, _) in enumerate(batch):
                result = batch_results[j]
                if isinstance(result, Exception):
                    logger.error(
                        "Classification failed",
                        file_path=str(file_path),
                        error=str(result),
                    )
                    classification = None
                else:
                    classification = result

                results.append((file_path, classification))

        return results

    def get_model_info(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a model.

        Args:
            model_name: Name of the model

        Returns:
            Model information dictionary or None if not found
        """
        models = self.list_models()
        for model in models:
            if model["name"] == model_name:
                return model
        return None

    def ensure_model_available(self, model_name: str) -> bool:
        """Ensure a model is available, downloading if necessary.

        Args:
            model_name: Name of the model

        Returns:
            True if model is available
        """
        if self.has_model(model_name):
            logger.info("Model already available", model=model_name)
            return True

        logger.info("Model not found, downloading", model=model_name)
        return self.download_model(model_name)
