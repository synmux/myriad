"""YouTube API client wrapper for subscription management."""

import logging
import random
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from googleapiclient.errors import HttpError

from .utils import APIError


class YouTubeClient:
    """Wrapper for YouTube Data API v3 operations."""

    def __init__(self, service):
        """Initialize YouTube client with authenticated service.

        Args:
            service: Authenticated YouTube service object from Google API client
        """
        self.service = service
        self.logger = logging.getLogger(__name__)

    def get_subscriptions(self) -> List[Dict[str, Any]]:
        """Fetch all user subscriptions with pagination.

        Returns:
            List of subscription dictionaries containing channel information

        Raises:
            APIError: If API request fails or rate limits are exceeded
        """
        subscriptions = []
        page_token = None

        try:
            while True:
                batch = self._paginate_subscriptions_with_retry(page_token)
                subscriptions.extend(batch.get("items", []))

                page_token = batch.get("nextPageToken")
                if not page_token:
                    break

                # Small delay to avoid hitting rate limits
                time.sleep(0.1)

        except HttpError as e:
            self._handle_api_error(e, "fetching subscriptions")

        self.logger.info(f"Retrieved {len(subscriptions)} subscriptions")
        return subscriptions

    def unsubscribe_from_channel(self, subscription_id: str) -> bool:
        """Unsubscribe from a channel by subscription ID.

        Args:
            subscription_id: The YouTube subscription ID to remove

        Returns:
            True if unsubscription was successful, False otherwise

        Raises:
            APIError: If API request fails with non-recoverable error
        """
        return self._unsubscribe_with_retry(subscription_id)

    def get_channel_last_video_date(
        self, channel_id: str, wait_for_quota: bool = True
    ) -> Optional[datetime]:
        """Get the date of the most recent video posted by a channel.

        Args:
            channel_id: The YouTube channel ID
            wait_for_quota: Whether to wait for quota reset if exceeded

        Returns:
            datetime of the most recent video, or None if no videos found

        Raises:
            APIError: If API request fails
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Use search API to get the most recent video from the channel
                request = self.service.search().list(
                    part="snippet",
                    channelId=channel_id,
                    order="date",
                    maxResults=1,
                    type="video",
                )

                response = request.execute()

                items = response.get("items", [])
                if items:
                    # Get the publish date of the most recent video
                    published_at = items[0]["snippet"]["publishedAt"]
                    # Parse ISO 8601 date string
                    return datetime.fromisoformat(published_at.replace("Z", "+00:00"))

                return None

            except HttpError as e:
                if e.resp.status == 404:
                    # Channel not found or no videos
                    return None

                # Check if it's a quota error and we should wait
                if e.resp.status == 403 and wait_for_quota:
                    error_content = str(e.content)
                    if "quotaExceeded" in error_content:
                        if attempt < max_retries - 1:
                            # Short retry for temporary quota issues
                            wait_time = self._calculate_backoff_delay(attempt)
                            self.logger.warning(
                                f"Quota exceeded for channel {channel_id}, waiting {wait_time:.1f}s before retry"
                            )
                            time.sleep(wait_time)
                            continue

                # If not retryable or last attempt, raise error
                self._handle_api_error(e, f"fetching videos for channel {channel_id}")

    def _paginate_subscriptions(
        self, page_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """Handle pagination for subscription listing.

        Args:
            page_token: Token for next page of results

        Returns:
            API response containing subscription items and pagination info

        Raises:
            HttpError: If API request fails
        """
        request_params = {
            "part": "snippet,contentDetails,subscriberSnippet",
            "mine": True,
            "maxResults": 50,  # Maximum allowed by API
        }

        if page_token:
            request_params["pageToken"] = page_token

        return self.service.subscriptions().list(**request_params).execute()

    def _paginate_subscriptions_with_retry(
        self, page_token: Optional[str] = None, max_retries: int = 3
    ) -> Dict[str, Any]:
        """Handle pagination with retry logic for transient errors.

        Args:
            page_token: Token for next page of results
            max_retries: Maximum number of retry attempts

        Returns:
            API response containing subscription items and pagination info

        Raises:
            HttpError: If API request fails after all retries
        """
        for attempt in range(max_retries + 1):
            try:
                return self._paginate_subscriptions(page_token)
            except HttpError as e:
                if attempt == max_retries:
                    # Last attempt failed, re-raise the error
                    raise

                if self._is_retryable_error(e):
                    delay = self._calculate_backoff_delay(attempt)
                    self.logger.warning(
                        f"Retryable error on attempt {attempt + 1}/{max_retries + 1}: {e}. "
                        f"Retrying in {delay:.1f} seconds..."
                    )
                    time.sleep(delay)
                else:
                    # Non-retryable error, re-raise immediately
                    raise

    def _unsubscribe_with_retry(
        self, subscription_id: str, max_retries: int = 3
    ) -> bool:
        """Unsubscribe with retry logic for transient errors.

        Args:
            subscription_id: The YouTube subscription ID to remove
            max_retries: Maximum number of retry attempts

        Returns:
            True if unsubscription was successful, False otherwise
        """
        for attempt in range(max_retries + 1):
            try:
                self.service.subscriptions().delete(id=subscription_id).execute()
                self.logger.info(
                    f"Successfully unsubscribed from subscription {subscription_id}"
                )
                return True

            except HttpError as e:
                # Handle non-retryable errors immediately
                if e.resp.status == 404:
                    self.logger.warning(
                        f"Subscription {subscription_id} not found (may already be unsubscribed)"
                    )
                    return False
                elif e.resp.status == 403:
                    self.logger.error(
                        f"Permission denied for subscription {subscription_id}"
                    )
                    return False

                # Handle retryable errors
                if attempt == max_retries:
                    # Last attempt failed
                    if e.resp.status >= 500:
                        self.logger.error(
                            f"Server error while unsubscribing from {subscription_id} after {max_retries + 1} attempts: {e}"
                        )
                        return False
                    elif e.resp.status == 429:
                        self.logger.error(
                            f"Rate limit exceeded while unsubscribing from {subscription_id} after {max_retries + 1} attempts"
                        )
                        return False
                    else:
                        self.logger.error(
                            f"API error while unsubscribing from {subscription_id} after {max_retries + 1} attempts: {e}"
                        )
                        return False

                if self._is_retryable_error(e):
                    delay = self._calculate_backoff_delay(attempt)
                    self.logger.warning(
                        f"Retryable error unsubscribing from {subscription_id} on attempt {attempt + 1}/{max_retries + 1}: {e}. "
                        f"Retrying in {delay:.1f} seconds..."
                    )
                    time.sleep(delay)
                else:
                    # Non-retryable error
                    self.logger.error(
                        f"Non-retryable API error while unsubscribing from {subscription_id}: {e}"
                    )
                    return False

        return False

    def _is_retryable_error(self, error: HttpError) -> bool:
        """Check if an HTTP error is retryable.

        Args:
            error: The HttpError to check

        Returns:
            True if the error is retryable, False otherwise
        """
        status_code = error.resp.status

        # Server errors (5xx) are generally retryable
        if status_code >= 500:
            return True

        # Rate limiting (429) is retryable
        if status_code == 429:
            return True

        # Some 403 errors might be temporary quota issues
        if status_code == 403:
            error_details = getattr(error, "error_details", [])
            for detail in error_details:
                if "quotaExceeded" in str(detail) or "rateLimitExceeded" in str(detail):
                    return True

        return False

    def _calculate_backoff_delay(self, attempt: int) -> float:
        """Calculate exponential backoff delay with jitter.

        Args:
            attempt: The current attempt number (0-based)

        Returns:
            Delay in seconds
        """
        # Exponential backoff: 1s, 2s, 4s, 8s, etc.
        base_delay = 2**attempt

        # Add jitter to avoid thundering herd
        jitter = random.uniform(0.1, 0.5)

        # Cap at 30 seconds
        return min(base_delay + jitter, 30.0)

    def _get_quota_reset_time(self) -> datetime:
        """Calculate when YouTube API quota will reset.

        YouTube quotas reset daily at midnight Pacific Time (UTC-8 or UTC-7 during DST).

        Returns:
            datetime: The next quota reset time in UTC
        """
        try:
            # Try to use zoneinfo for proper timezone handling (Python 3.9+)
            from zoneinfo import ZoneInfo

            pacific = ZoneInfo("America/Los_Angeles")
        except ImportError:
            # Fallback: Use a simple approximation
            # This won't handle DST transitions perfectly but is close enough
            # PST = UTC-8, PDT = UTC-7
            # Rough DST: Second Sunday in March to first Sunday in November
            now = datetime.now(timezone.utc)
            month = now.month
            if 3 < month < 11:  # Approximate DST period
                pacific = timezone(timedelta(hours=-7))  # PDT
            else:
                pacific = timezone(timedelta(hours=-8))  # PST

        # Get current time in Pacific timezone
        now_utc = datetime.now(timezone.utc)
        now_pacific = now_utc.astimezone(pacific)

        # Calculate next midnight Pacific Time
        next_midnight_pacific = now_pacific.replace(
            hour=0, minute=0, second=0, microsecond=0
        ) + timedelta(days=1)

        # Convert back to UTC
        return next_midnight_pacific.astimezone(timezone.utc)

    def _handle_api_error(self, error: HttpError, operation: str) -> None:
        """Handle YouTube API errors with appropriate retry logic.

        Args:
            error: The HttpError from the API
            operation: Description of the operation that failed

        Raises:
            APIError: Always raises with appropriate error message
        """
        status_code = error.resp.status

        if status_code == 403:
            # Check if it's a quota exceeded error
            error_details = getattr(error, "error_details", [])
            if error_details and any(
                "quotaExceeded" in str(detail) for detail in error_details
            ):
                raise APIError(
                    f"YouTube API quota exceeded while {operation}. Please try again later."
                )
            else:
                raise APIError(
                    f"Permission denied while {operation}. Check your API credentials and scopes."
                )

        elif status_code == 429:
            raise APIError(
                f"Rate limit exceeded while {operation}. Please wait and try again."
            )

        elif status_code >= 500:
            raise APIError(
                f"YouTube API server error while {operation}. Please try again later."
            )

        else:
            raise APIError(f"API error while {operation}: {error}")
