"""Basic tests for the unsubscribe tool."""

from unittest.mock import Mock

import pytest

from unsubscribe.scanner import EmailScanner
from unsubscribe.utils import (
    clean_email_address,
    format_unsubscribe_action,
    is_valid_email,
    is_valid_url,
    truncate_string,
)


class TestUtils:
    """Test utility functions."""

    def test_is_valid_email(self):
        """Test email validation."""
        assert is_valid_email("test@example.com")
        assert is_valid_email("user.name+tag@domain.co.uk")
        assert not is_valid_email("invalid-email")
        assert not is_valid_email("@domain.com")
        assert not is_valid_email("user@")
        assert not is_valid_email("")

    def test_is_valid_url(self):
        """Test URL validation."""
        assert is_valid_url("https://example.com")
        assert is_valid_url("http://example.com/path")
        assert is_valid_url("https://sub.domain.com/path?param=value")
        assert not is_valid_url("ftp://example.com")
        assert not is_valid_url("invalid-url")
        assert not is_valid_url("://example.com")
        assert not is_valid_url("")

    def test_clean_email_address(self):
        """Test email address cleaning."""
        assert clean_email_address("test@example.com") == "test@example.com"
        assert clean_email_address("  test@example.com  ") == "test@example.com"
        assert clean_email_address('"test@example.com"') == "test@example.com"
        assert clean_email_address("John Doe <john@example.com>") == "john@example.com"
        assert clean_email_address("TEST@EXAMPLE.COM") == "test@example.com"
        assert clean_email_address("") == ""

    def test_format_unsubscribe_action(self):
        """Test unsubscribe action formatting."""
        assert (
            format_unsubscribe_action("test@example.com", "https://example.com")
            == "both (email: email, http: http, both: both)"
        )
        assert format_unsubscribe_action("test@example.com", "") == "email"
        assert format_unsubscribe_action("", "https://example.com") == "http"
        assert format_unsubscribe_action("", "") == "none"
        assert format_unsubscribe_action("invalid-email", "invalid-url") == "none"

    def test_truncate_string(self):
        """Test string truncation."""
        assert truncate_string("short", 10) == "short"
        assert truncate_string("this is a very long string", 10) == "this is..."
        assert truncate_string("exactly ten", 10) == "exactly ten"


class TestEmailScanner:
    """Test email scanner functionality."""

    def test_parse_unsubscribe_header(self):
        """Test parsing of List-Unsubscribe headers."""
        scanner = EmailScanner(Mock())

        # Test email only
        email, url = scanner._parse_unsubscribe_header(
            "<mailto:unsubscribe@example.com>"
        )
        assert email == "unsubscribe@example.com"
        assert url is None

        # Test URL only
        email, url = scanner._parse_unsubscribe_header(
            "<https://example.com/unsubscribe>"
        )
        assert email is None
        assert url == "https://example.com/unsubscribe"

        # Test both
        email, url = scanner._parse_unsubscribe_header(
            "<mailto:unsubscribe@example.com>, <https://example.com/unsubscribe>"
        )
        assert email == "unsubscribe@example.com"
        assert url == "https://example.com/unsubscribe"

        # Test empty
        email, url = scanner._parse_unsubscribe_header("")
        assert email is None
        assert url is None

    def test_extract_sender_info(self):
        """Test extraction of sender information."""
        scanner = EmailScanner(Mock())

        # Test with name and email
        email, name = scanner._extract_sender_info(
            {"from": "John Doe <john@example.com>"}
        )
        assert email == "john@example.com"
        assert name == "John Doe"

        # Test with quoted name
        email, name = scanner._extract_sender_info(
            {"from": '"John Doe" <john@example.com>'}
        )
        assert email == "john@example.com"
        assert name == "John Doe"

        # Test email only
        email, name = scanner._extract_sender_info({"from": "john@example.com"})
        assert email == "john@example.com"
        assert name == ""

        # Test empty
        email, name = scanner._extract_sender_info({})
        assert email == ""
        assert name == ""


if __name__ == "__main__":
    pytest.main([__file__])
