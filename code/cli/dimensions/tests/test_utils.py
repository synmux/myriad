"""
Tests for the utilities module.
"""

import pytest
import tempfile
import shutil
from pathlib import Path

from dimensions.utils import (
    format_file_size, 
    get_file_size, 
    truncate_file_list, 
    ensure_directory,
    safe_filename,
    is_image_file,
    setup_logging
)


class TestFormatFileSize:
    """Test cases for format_file_size function."""
    
    def test_format_zero_bytes(self):
        """Test formatting zero bytes."""
        assert format_file_size(0) == "0 B"
    
    def test_format_bytes(self):
        """Test formatting bytes (less than 1024)."""
        assert format_file_size(100) == "100 B"
        assert format_file_size(1023) == "1023 B"
    
    def test_format_kilobytes(self):
        """Test formatting kilobytes."""
        assert format_file_size(1024) == "1.0 KB"
        assert format_file_size(1536) == "1.5 KB"  # 1.5 * 1024
        assert format_file_size(10240) == "10.0 KB"
    
    def test_format_megabytes(self):
        """Test formatting megabytes."""
        assert format_file_size(1024 * 1024) == "1.0 MB"
        assert format_file_size(1024 * 1024 * 2) == "2.0 MB"
        assert format_file_size(int(1024 * 1024 * 1.5)) == "1.5 MB"
    
    def test_format_gigabytes(self):
        """Test formatting gigabytes."""
        assert format_file_size(1024 * 1024 * 1024) == "1.0 GB"
        assert format_file_size(1024 * 1024 * 1024 * 2) == "2.0 GB"
    
    def test_format_terabytes(self):
        """Test formatting terabytes."""
        assert format_file_size(1024 * 1024 * 1024 * 1024) == "1.0 TB"


class TestGetFileSize:
    """Test cases for get_file_size function."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_file = self.temp_dir / "test_file.txt"
    
    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_get_existing_file_size(self):
        """Test getting size of an existing file."""
        # Create a file with known content
        content = "Hello, World!"
        self.test_file.write_text(content)
        
        size = get_file_size(self.test_file)
        assert size == len(content.encode('utf-8'))
    
    def test_get_nonexistent_file_size(self):
        """Test getting size of non-existent file returns 0."""
        nonexistent_file = self.temp_dir / "nonexistent.txt"
        size = get_file_size(nonexistent_file)
        assert size == 0
    
    def test_get_empty_file_size(self):
        """Test getting size of empty file."""
        self.test_file.touch()
        size = get_file_size(self.test_file)
        assert size == 0


class TestTruncateFileList:
    """Test cases for truncate_file_list function."""
    
    def test_empty_list(self):
        """Test truncating empty list."""
        result = truncate_file_list([])
        assert result == "No files"
    
    def test_list_shorter_than_max(self):
        """Test list shorter than max length."""
        files = ["/path/to/file1.jpg", "/path/to/file2.png"]
        result = truncate_file_list(files, max_length=5)
        assert result == "file1.jpg, file2.png"
    
    def test_list_equal_to_max(self):
        """Test list equal to max length."""
        files = ["/path/to/file1.jpg", "/path/to/file2.png", "/path/to/file3.gif"]
        result = truncate_file_list(files, max_length=3)
        assert result == "file1.jpg, file2.png, file3.gif"
    
    def test_list_longer_than_max(self):
        """Test list longer than max length."""
        files = [
            "/path/to/file1.jpg", 
            "/path/to/file2.png", 
            "/path/to/file3.gif",
            "/path/to/file4.jpeg",
            "/path/to/file5.webp"
        ]
        result = truncate_file_list(files, max_length=3)
        assert result == "file1.jpg, file2.png, file3.gif (+2)"
    
    def test_default_max_length(self):
        """Test default max length of 3."""
        files = [f"/path/to/file{i}.jpg" for i in range(1, 6)]
        result = truncate_file_list(files)
        assert result == "file1.jpg, file2.jpg, file3.jpg (+2)"


class TestEnsureDirectory:
    """Test cases for ensure_directory function."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_create_new_directory(self):
        """Test creating a new directory."""
        new_dir = self.temp_dir / "new_directory"
        assert not new_dir.exists()
        
        ensure_directory(new_dir)
        assert new_dir.exists()
        assert new_dir.is_dir()
    
    def test_create_nested_directories(self):
        """Test creating nested directories."""
        nested_dir = self.temp_dir / "level1" / "level2" / "level3"
        assert not nested_dir.exists()
        
        ensure_directory(nested_dir)
        assert nested_dir.exists()
        assert nested_dir.is_dir()
    
    def test_ensure_existing_directory(self):
        """Test ensuring an existing directory doesn't raise an error."""
        existing_dir = self.temp_dir / "existing"
        existing_dir.mkdir()
        assert existing_dir.exists()
        
        # Should not raise an error
        ensure_directory(existing_dir)
        assert existing_dir.exists()


class TestSafeFilename:
    """Test cases for safe_filename function."""
    
    def test_replace_multiplication_sign(self):
        """Test replacing multiplication sign with 'x'."""
        assert safe_filename("1920×1080") == "1920x1080"
    
    def test_replace_colon(self):
        """Test replacing colon with dash."""
        assert safe_filename("time:stamp") == "time-stamp"
    
    def test_replace_forward_slash(self):
        """Test replacing forward slash with dash."""
        assert safe_filename("width/height") == "width-height"
    
    def test_combined_replacements(self):
        """Test multiple character replacements."""
        assert safe_filename("1920×1080:test/file") == "1920x1080-test-file"
    
    def test_no_replacements_needed(self):
        """Test string that doesn't need replacements."""
        assert safe_filename("1920x1080") == "1920x1080"


class TestIsImageFile:
    """Test cases for is_image_file function."""
    
    def test_supported_extensions(self):
        """Test that supported extensions return True."""
        supported = [
            'image.jpg', 'image.jpeg', 'image.png', 'image.gif', 
            'image.bmp', 'image.tiff', 'image.tif', 'image.webp',
            'image.heic', 'image.heif', 'image.heics', 'image.heifs', 'image.hif'
        ]
        
        for filename in supported:
            assert is_image_file(Path(filename)), f"{filename} should be recognized as image"
    
    def test_unsupported_extensions(self):
        """Test that unsupported extensions return False."""
        unsupported = [
            'document.txt', 'data.csv', 'video.mp4', 'audio.mp3',
            'archive.zip', 'code.py', 'style.css'
        ]
        
        for filename in unsupported:
            assert not is_image_file(Path(filename)), f"{filename} should not be recognized as image"
    
    def test_case_insensitive(self):
        """Test that extension matching is case-insensitive."""
        assert is_image_file(Path("image.JPG"))
        assert is_image_file(Path("image.PNG"))
        assert is_image_file(Path("image.JPEG"))
        assert is_image_file(Path("image.GIF"))
    
    def test_no_extension(self):
        """Test file with no extension."""
        assert not is_image_file(Path("filename_without_extension"))


class TestSetupLogging:
    """Test cases for setup_logging function."""
    
    def test_setup_logging_returns_logger(self):
        """Test that setup_logging returns a logger."""
        logger = setup_logging("INFO")
        assert logger is not None
        # Can't easily test the actual logging without mocking, 
        # but we can ensure it returns something
    
    def test_different_log_levels(self):
        """Test setting up logging with different levels."""
        levels = ["DEBUG", "INFO", "WARNING", "ERROR"]
        
        for level in levels:
            logger = setup_logging(level)
            assert logger is not None