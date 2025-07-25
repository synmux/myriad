"""CSV file handling for YouTube subscriptions data."""

import csv
import os
from typing import Any, Dict, List

from .utils import FileError, ensure_directory_exists, validate_csv_format


class SubscriptionCSVHandler:
    """Handles CSV file operations for YouTube subscriptions."""

    def __init__(self, filename: str):
        """Initialize CSV handler with filename.

        Args:
            filename: Path to the CSV file
        """
        self.filename = filename
        self.fieldnames = [
            "channel_name",
            "channel_id",
            "description",
            "subscription_id",
            "published_at",
            "thumbnail_url",
            "video_count",
            "new_video_count",
            "unsubscribe",
        ]

    def write_subscriptions(self, subscriptions: List[Dict[str, Any]]) -> None:
        """Write subscriptions data to CSV file.

        Args:
            subscriptions: List of subscription data from YouTube API

        Raises:
            FileError: If file cannot be written
        """
        if not subscriptions:
            raise FileError("No subscriptions data provided to write")

        # Ensure directory exists
        ensure_directory_exists(self.filename)

        try:
            with open(self.filename, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                writer.writeheader()

                for subscription in subscriptions:
                    row = self._format_subscription_row(subscription)
                    writer.writerow(row)

        except (IOError, csv.Error) as e:
            raise FileError(f"Error writing to CSV file {self.filename}: {e}") from e

    def read_unsubscribe_list(self) -> List[Dict[str, str]]:
        """Read CSV and return channels marked for unsubscription.

        Returns:
            List of subscription data for channels marked for unsubscription

        Raises:
            FileError: If file cannot be read or has invalid format
        """
        # Validate file format first
        validate_csv_format(self.filename)

        unsubscribe_list = []
        total_rows = 0
        marked_rows = 0

        try:
            with open(self.filename, "r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)

                for row_num, row in enumerate(reader, start=2):  # Start at 2 for header
                    total_rows += 1

                    # Check if unsubscribe field has any non-empty value
                    unsubscribe_value = row.get("unsubscribe", "").strip()

                    if unsubscribe_value:
                        marked_rows += 1

                        # Validate required fields are present
                        subscription_id = row.get("subscription_id", "").strip()
                        channel_name = row.get("channel_name", "").strip()

                        if not subscription_id:
                            raise FileError(
                                f"Row {row_num}: Missing or empty subscription_id for channel marked for unsubscription.\n"
                                f"Channel name: '{channel_name}'\n"
                                f"Each channel marked for unsubscription must have a valid subscription_id."
                            )

                        if not channel_name:
                            raise FileError(
                                f"Row {row_num}: Missing or empty channel_name for channel marked for unsubscription.\n"
                                f"Subscription ID: '{subscription_id}'\n"
                                f"Each channel marked for unsubscription must have a channel name."
                            )

                        # Validate subscription ID format (YouTube subscription IDs start with UC)
                        if (
                            not subscription_id.startswith("UC")
                            or len(subscription_id) != 24
                        ):
                            raise FileError(
                                f"Row {row_num}: Invalid subscription_id format: '{subscription_id}'\n"
                                f"Channel name: '{channel_name}'\n"
                                f"YouTube subscription IDs should start with 'UC' and be 24 characters long."
                            )

                        unsubscribe_list.append(
                            {
                                "channel_name": channel_name,
                                "description": row.get("description", "").strip(),
                                "subscription_id": subscription_id,
                                "unsubscribe": unsubscribe_value,
                            }
                        )

        except csv.Error as e:
            raise FileError(
                f"CSV parsing error in file {self.filename}: {e}\n"
                f"This usually indicates malformed CSV data.\n"
                f"Please ensure the file is properly formatted with correct delimiters and quoting."
            ) from e
        except UnicodeDecodeError as e:
            raise FileError(
                f"Text encoding error reading file {self.filename}: {e}\n"
                f"The file may contain invalid UTF-8 characters.\n"
                f"Try saving the file with UTF-8 encoding."
            ) from e
        except IOError as e:
            raise FileError(
                f"File access error for {self.filename}: {e}\n"
                f"Please check that:\n"
                f"1. The file exists and is readable\n"
                f"2. You have permission to access the file\n"
                f"3. The file is not open in another application"
            ) from e

        if total_rows == 0:
            raise FileError(
                f"CSV file {self.filename} appears to be empty (no data rows found).\n"
                f"Please ensure the file contains subscription data."
            )

        return unsubscribe_list

    def _format_subscription_row(self, subscription: Dict[str, Any]) -> Dict[str, str]:
        """Format subscription data for CSV row.

        Args:
            subscription: YouTube API subscription resource

        Returns:
            Dict with CSV row data

        Raises:
            FileError: If subscription data is invalid
        """
        try:
            # Extract data from YouTube API response format
            snippet = subscription.get("snippet", {})
            content_details = subscription.get("contentDetails", {})

            # Basic fields from snippet
            channel_name = snippet.get("title", "").strip()
            description = snippet.get("description", "").strip()
            subscription_id = subscription.get("id", "").strip()
            published_at = snippet.get("publishedAt", "").strip()

            # Channel ID from resourceId
            resource_id = snippet.get("resourceId", {})
            channel_id = resource_id.get("channelId", "").strip()

            # Thumbnail URL (prefer high quality)
            thumbnails = snippet.get("thumbnails", {})
            thumbnail_url = ""
            if "high" in thumbnails:
                thumbnail_url = thumbnails["high"].get("url", "")
            elif "medium" in thumbnails:
                thumbnail_url = thumbnails["medium"].get("url", "")
            elif "default" in thumbnails:
                thumbnail_url = thumbnails["default"].get("url", "")

            # Content details
            video_count = str(content_details.get("totalItemCount", ""))
            new_video_count = str(content_details.get("newItemCount", ""))

            # Validate required fields
            if not channel_name:
                raise FileError("Subscription missing channel name")
            if not subscription_id:
                raise FileError("Subscription missing subscription ID")

            # Clean multi-line descriptions by replacing newlines with spaces
            description = " ".join(description.splitlines())

            return {
                "channel_name": channel_name,
                "channel_id": channel_id,
                "description": description,
                "subscription_id": subscription_id,
                "published_at": published_at,
                "thumbnail_url": thumbnail_url,
                "video_count": video_count,
                "new_video_count": new_video_count,
                "unsubscribe": "",  # Empty by default
            }

        except (KeyError, AttributeError) as e:
            raise FileError(f"Invalid subscription data format: {e}") from e

    def get_subscription_count(self) -> int:
        """Get the number of subscriptions in the CSV file.

        Returns:
            Number of subscription rows in the file

        Raises:
            FileError: If file cannot be read
        """
        if not os.path.exists(self.filename):
            return 0

        try:
            with open(self.filename, "r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                return sum(1 for _ in reader)
        except (IOError, csv.Error, UnicodeDecodeError) as e:
            raise FileError(
                f"Error counting subscriptions in {self.filename}: {e}"
            ) from e

    def file_exists(self) -> bool:
        """Check if the CSV file exists.

        Returns:
            True if file exists, False otherwise
        """
        return os.path.exists(self.filename)
