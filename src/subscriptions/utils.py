"""Utility functions for the YouTube subscriptions tool."""

import csv
import os
from datetime import datetime
from typing import Optional


class YouTubeSubscriptionsError(Exception):
    """Base exception for YouTube subscriptions tool."""

    pass


class AuthenticationError(YouTubeSubscriptionsError):
    """Authentication-related errors."""

    pass


class APIError(YouTubeSubscriptionsError):
    """YouTube API-related errors."""

    pass


class FileError(YouTubeSubscriptionsError):
    """File operation errors."""

    pass


def generate_default_filename() -> str:
    """Generate default filename with timestamp.

    Returns:
        str: Filename in format 'subscriptions-YYMMdd-HHmmss.csv'
    """
    timestamp = datetime.now().strftime("%y%m%d-%H%M%S")
    return f"subscriptions-{timestamp}.csv"


def validate_csv_format(filename: str) -> bool:
    """Validate CSV file has required columns.

    Args:
        filename: Path to the CSV file to validate

    Returns:
        bool: True if CSV has valid format

    Raises:
        FileError: If file doesn't exist or has invalid format
    """
    required_columns = {
        "channel_name",
        "channel_id",
        "description",
        "subscription_id",
        "published_at",
        "thumbnail_url",
        "video_count",
        "new_video_count",
        "last_video_date",
        "unsubscribe",
    }

    if not os.path.exists(filename):
        raise FileError(
            f"CSV file not found: {filename}\n"
            f"Please ensure:\n"
            f"1. The file path is correct\n"
            f"2. The file exists in the specified location\n"
            f"3. You have permission to read the file"
        )

    # Check if file is readable
    if not os.access(filename, os.R_OK):
        raise FileError(
            f"Cannot read CSV file: {filename}\n"
            f"Permission denied. Please check file permissions."
        )

    # Check file size
    try:
        file_size = os.path.getsize(filename)
        if file_size == 0:
            raise FileError(
                f"CSV file is empty: {filename}\n"
                f"Please ensure the file contains subscription data with proper headers."
            )
        elif file_size > 50 * 1024 * 1024:  # 50MB limit
            raise FileError(
                f"CSV file is too large: {filename} ({file_size / 1024 / 1024:.1f}MB)\n"
                f"Maximum supported file size is 50MB."
            )
    except OSError as e:
        raise FileError(f"Cannot access file {filename}: {e}") from e

    try:
        with open(filename, "r", encoding="utf-8") as file:
            # Try to read first few lines to detect issues early
            first_line = file.readline().strip()
            if not first_line:
                raise FileError(
                    f"CSV file appears to be empty: {filename}\n"
                    f"Please ensure the file contains a header row and data."
                )

            # Reset file pointer and create reader
            file.seek(0)
            reader = csv.DictReader(file)

            # Check if file has headers
            if reader.fieldnames is None:
                raise FileError(
                    f"CSV file has no headers: {filename}\n"
                    f"The first row should contain column headers: {', '.join(sorted(required_columns))}"
                )

            # Convert fieldnames to set for comparison, handling None values
            file_columns = set(col for col in reader.fieldnames if col is not None)

            # Check for empty column names
            if None in reader.fieldnames or "" in reader.fieldnames:
                raise FileError(
                    f"CSV file has empty column names: {filename}\n"
                    f"All columns must have names. Found columns: {reader.fieldnames}"
                )

            # Check if all required columns are present
            missing_columns = required_columns - file_columns
            if missing_columns:
                extra_columns = file_columns - required_columns
                error_msg = (
                    f"CSV file missing required columns: {', '.join(sorted(missing_columns))}\n"
                    f"Required columns: {', '.join(sorted(required_columns))}\n"
                    f"Found columns: {', '.join(sorted(file_columns))}"
                )
                if extra_columns:
                    error_msg += f"\nExtra columns (will be ignored): {', '.join(sorted(extra_columns))}"

                raise FileError(error_msg)

            # Try to read first data row to validate CSV structure
            try:
                first_row = next(reader, None)
                if first_row is None:
                    raise FileError(
                        f"CSV file has headers but no data rows: {filename}\n"
                        f"Please ensure the file contains subscription data."
                    )
            except csv.Error as e:
                raise FileError(
                    f"CSV structure error in {filename}: {e}\n"
                    f"The file may have malformed data in the first row."
                ) from e

            return True

    except UnicodeDecodeError as e:
        raise FileError(
            f"Text encoding error reading {filename}: {e}\n"
            f"The file may not be saved in UTF-8 encoding.\n"
            f"Please save the file with UTF-8 encoding and try again."
        ) from e
    except csv.Error as e:
        raise FileError(
            f"CSV format error in {filename}: {e}\n"
            f"This usually indicates:\n"
            f"1. Malformed CSV data (unmatched quotes, incorrect delimiters)\n"
            f"2. Binary data in a text file\n"
            f"3. Corrupted file\n"
            f"Please check the file format and try again."
        ) from e
    except IOError as e:
        raise FileError(
            f"File access error for {filename}: {e}\n"
            f"Please ensure:\n"
            f"1. The file is not open in another application\n"
            f"2. You have permission to read the file\n"
            f"3. The file is not corrupted"
        ) from e


def format_error_message(error: Exception, context: Optional[str] = None) -> str:
    """Format error messages for user-friendly display.

    Args:
        error: The exception that occurred
        context: Optional context about where the error occurred

    Returns:
        str: Formatted error message
    """
    error_type = type(error).__name__
    error_msg = str(error)

    if context:
        return f"Error in {context}: {error_msg}"
    else:
        return f"{error_type}: {error_msg}"


def ensure_directory_exists(filepath: str) -> None:
    """Ensure the directory for a file path exists.

    Args:
        filepath: Path to a file

    Raises:
        FileError: If directory cannot be created
    """
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        try:
            os.makedirs(directory, exist_ok=True)
        except OSError as e:
            raise FileError(f"Cannot create directory {directory}: {e}") from e
