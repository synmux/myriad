"""
AI-related utilities and functions for myriad.

This module contains functions for AI operations that will be implemented
as needed throughout the application development.
"""

import os
from enum import Enum
from typing import Any, Dict, Optional

from openai import OpenAI


class BackoffType(Enum):
    """Supported backoff types for request retries."""

    CONSTANT = "constant"
    LINEAR = "linear"
    EXPONENTIAL = "exponential"


class AIGatewayConfig:
    """Configuration class for AI Gateway headers."""

    def __init__(
        self,
        enable_caching: bool = False,
        cache_ttl: Optional[int] = None,
        cache_key: Optional[str] = None,
        skip_cache: Optional[bool] = None,
        collect_log: Optional[bool] = None,
        custom_cost: Optional[float] = None,
        event_id: Optional[str] = None,
        max_attempts: Optional[int] = None,
        retry_delay: Optional[int] = None,
        backoff_type: Optional[BackoffType] = None,
        request_timeout: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize AI Gateway configuration.

        Args:
            enable_caching (bool): Whether to enable caching for requests
            cache_ttl (Optional[int]): Cache time-to-live in seconds (max 1 month)
            cache_key (Optional[str]): Custom cache key for precise cacheability control
            skip_cache (Optional[bool]): Explicitly bypass caching (overrides enable_caching)
            collect_log (Optional[bool]): Whether to collect logs for this request
            custom_cost (Optional[float]): Custom cost value for the request
            event_id (Optional[str]): Unique identifier for event tracing
            max_attempts (Optional[int]): Maximum retry attempts (max 5)
            retry_delay (Optional[int]): Retry delay in milliseconds (max 5000)
            backoff_type (Optional[BackoffType]): Backoff strategy for retries
            request_timeout (Optional[int]): Request timeout in milliseconds
            metadata (Optional[Dict[str, Any]]): Custom metadata (max 5 entries)
        """
        self.enable_caching = enable_caching
        self.cache_ttl = cache_ttl
        self.cache_key = cache_key
        self.skip_cache = skip_cache
        self.collect_log = collect_log
        self.custom_cost = custom_cost
        self.event_id = event_id
        self.max_attempts = max_attempts
        self.retry_delay = retry_delay
        self.backoff_type = backoff_type
        self.request_timeout = request_timeout
        self.metadata = metadata or {}

    def to_headers(self) -> Dict[str, str]:
        """Convert configuration to HTTP headers."""
        headers: Dict[str, str] = {}

        # Caching headers
        if self.skip_cache is True or (
            self.skip_cache is None and not self.enable_caching
        ):
            headers["cf-aig-skip-cache"] = "true"

        if self.cache_ttl is not None:
            headers["cf-aig-cache-ttl"] = str(self.cache_ttl)

        if self.cache_key is not None:
            headers["cf-aig-cache-key"] = self.cache_key

        # Logging headers
        if self.collect_log is not None:
            headers["cf-aig-collect-log"] = str(self.collect_log).lower()

        # Cost headers
        if self.custom_cost is not None:
            headers["cf-aig-custom-cost"] = str(self.custom_cost)

        # Event tracking headers
        if self.event_id is not None:
            headers["cf-aig-event-id"] = self.event_id

        # Retry headers
        if self.max_attempts is not None:
            if self.max_attempts > 5:
                raise ValueError("max_attempts cannot exceed 5")
            headers["cf-aig-max-attempts"] = str(self.max_attempts)

        if self.retry_delay is not None:
            if self.retry_delay > 5000:
                raise ValueError("retry_delay cannot exceed 5000 milliseconds")
            headers["cf-aig-retry-delay"] = str(self.retry_delay)

        if self.backoff_type is not None:
            headers["cf-aig-backoff"] = self.backoff_type.value

        # Request handling headers
        if self.request_timeout is not None:
            headers["cf-aig-request-timeout"] = str(self.request_timeout)

        # Metadata headers (max 5 entries)
        if self.metadata:
            if len(self.metadata) > 5:
                raise ValueError("metadata cannot have more than 5 entries")
            # Convert metadata dict to JSON string for the header
            import json

            headers["cf-aig-metadata"] = json.dumps(self.metadata)

        return headers


class AIService(Enum):
    """Supported AI service providers."""

    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    OPENROUTER = "openrouter"


def get_api_key(service: AIService) -> str:
    """
    Read environment variables and validate configuration.

    Args:
        service (AIService): The AI service provider to get the API key for

    Returns:
        str: The API key for the specified service

    Raises:
        ValueError: If the API key is not set in environment variables
    """
    api_key = os.getenv(f"{service.value.upper()}_API_KEY")

    if not api_key:
        raise ValueError(
            f"{service.value} API key is not set in environment variables."
        )

    return api_key


def get_openai_client(
    enable_caching: bool = False, gateway_config: Optional[AIGatewayConfig] = None
) -> OpenAI:
    """
    Create and return an OpenAI client instance configured to use OpenRouter via Cloudflare AI Gateway.

    Args:
        enable_caching (bool): Whether to enable caching for requests. If False, adds cf-aig-skip-cache header to bypass cache. Defaults to False.
        gateway_config (Optional[AIGatewayConfig]): Advanced AI Gateway configuration. If provided, overrides enable_caching parameter.

    Returns:
        OpenAI: Configured OpenAI client instance pointing to OpenRouter via Cloudflare AI Gateway

    Raises:
        ValueError: If no API key is provided and OPENROUTER_API_KEY env var is not set
        ValueError: If required Cloudflare AI Gateway environment variables are not set
        ValueError: If CLOUDFLARE_AI_GATEWAY_TOKEN environment variable is not set
        ValueError: If gateway_config has invalid values (e.g., max_attempts > 5, retry_delay > 5000ms, metadata > 5 entries)
    """

    api_key = get_api_key(AIService.OPENROUTER)

    # Get Cloudflare AI Gateway configuration
    account_id = "def50674a738cee409235f71819973cf"
    gateway_id = "ai-dave-io"
    gateway_token = os.getenv("CLOUDFLARE_AI_GATEWAY_TOKEN")

    if not account_id or not gateway_id:
        raise ValueError(
            "Cloudflare AI Gateway configuration is required. Set "
            "CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_GATEWAY_ID environment variables."
        )

    if not gateway_token:
        raise ValueError(
            "Cloudflare AI Gateway token is required. Set "
            "CLOUDFLARE_AI_GATEWAY_TOKEN environment variable."
        )

    # Configure OpenAI client to use OpenRouter via Cloudflare AI Gateway
    base_url = (
        f"https://gateway.ai.cloudflare.com/v1/{account_id}/{gateway_id}/openrouter"
    )

    # Set up default headers for authentication and configuration
    default_headers: dict[str, str] = {"cf-aig-authorization": gateway_token}

    # Apply gateway configuration if provided, otherwise use simple caching parameter
    if gateway_config is not None:
        gateway_headers = gateway_config.to_headers()
        default_headers.update(gateway_headers)
    elif not enable_caching:
        default_headers["cf-aig-skip-cache"] = "true"

    return OpenAI(api_key=api_key, base_url=base_url, default_headers=default_headers)
