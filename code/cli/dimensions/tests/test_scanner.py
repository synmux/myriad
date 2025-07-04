"""
Tests for the directory scanner module.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock

from dimensions.scanner import DirectoryScanner, find_image_files
from dimensions.utils import setup_logging


class TestDirectoryScanner:
    """Test cases for DirectoryScanner class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.logger = setup_logging("ERROR")  # Use ERROR level to reduce test output
        self.scanner = DirectoryScanner(self.logger)
        
        # Create temporary directory structure
        self.temp_dir = Path(tempfile.mkdtemp())
        
        # Create subdirectories
        (self.temp_dir / "subdir1").mkdir()
        (self.temp_dir / "subdir2").mkdir()
        (self.temp_dir / ".hidden").mkdir()
        
        # Create test files
        self.image_files = [
            self.temp_dir / "image1.jpg",
            self.temp_dir / "image2.png", 
            self.temp_dir / "subdir1" / "image3.gif",
            self.temp_dir / "subdir2" / "image4.jpeg",
            self.temp_dir / "subdir1" / "image5.webp",
        ]
        
        self.non_image_files = [
            self.temp_dir / "document.txt",
            self.temp_dir / "data.csv",
            self.temp_dir / "subdir1" / "readme.md",
        ]
        
        # Create all files
        for file_path in self.image_files + self.non_image_files:
            file_path.touch()
    
    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_scan_directory_finds_all_images(self):
        """Test that scanner finds all image files recursively."""
        found_files = list(self.scanner.scan_directory(self.temp_dir))
        found_paths = set(found_files)
        expected_paths = set(self.image_files)
        
        assert found_paths == expected_paths
        assert len(found_files) == len(self.image_files)
    
    def test_scan_directory_skips_non_images(self):
        """Test that scanner skips non-image files."""
        found_files = list(self.scanner.scan_directory(self.temp_dir))
        found_paths = set(found_files)
        
        for non_image in self.non_image_files:
            assert non_image not in found_paths
    
    def test_scan_directory_skips_hidden_directories(self):
        """Test that scanner skips hidden directories."""
        # Create image in hidden directory
        hidden_image = self.temp_dir / ".hidden" / "hidden_image.jpg"
        hidden_image.touch()
        
        found_files = list(self.scanner.scan_directory(self.temp_dir))
        found_paths = set(found_files)
        
        assert hidden_image not in found_paths
    
    def test_scan_nonexistent_directory_raises_error(self):
        """Test that scanning non-existent directory raises FileNotFoundError."""
        nonexistent = Path("/this/path/does/not/exist")
        
        with pytest.raises(FileNotFoundError):
            list(self.scanner.scan_directory(nonexistent))
    
    def test_scan_file_instead_of_directory_raises_error(self):
        """Test that scanning a file instead of directory raises NotADirectoryError."""
        file_path = self.temp_dir / "test_file.txt"
        file_path.touch()
        
        with pytest.raises(NotADirectoryError):
            list(self.scanner.scan_directory(file_path))
    
    def test_count_images(self):
        """Test counting images in directory."""
        count = self.scanner.count_images(self.temp_dir)
        assert count == len(self.image_files)
    
    def test_reset_counters(self):
        """Test resetting failed and skipped file counters."""
        # Add some fake failures
        self.scanner.failed_files.append("fake_failure.jpg")
        self.scanner.skipped_files.append("fake_skip.txt")
        
        assert len(self.scanner.failed_files) > 0
        assert len(self.scanner.skipped_files) > 0
        
        self.scanner.reset_counters()
        
        assert len(self.scanner.failed_files) == 0
        assert len(self.scanner.skipped_files) == 0
    
    def test_get_failed_files_returns_copy(self):
        """Test that get_failed_files returns a copy, not the original list."""
        self.scanner.failed_files.append("test_failure.jpg")
        
        failed_copy = self.scanner.get_failed_files()
        failed_copy.append("modified_copy.jpg")
        
        # Original list should not be modified
        assert len(self.scanner.failed_files) == 1
        assert len(failed_copy) == 2
    
    def test_get_skipped_files_returns_copy(self):
        """Test that get_skipped_files returns a copy, not the original list."""
        self.scanner.skipped_files.append("test_skip.txt")
        
        skipped_copy = self.scanner.get_skipped_files()
        skipped_copy.append("modified_copy.txt")
        
        # Original list should not be modified
        assert len(self.scanner.skipped_files) == 1
        assert len(skipped_copy) == 2


class TestFindImageFiles:
    """Test cases for find_image_files convenience function."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.logger = setup_logging("ERROR")
        self.temp_dir = Path(tempfile.mkdtemp())
        
        # Create test images
        self.image_files = [
            self.temp_dir / "image1.jpg",
            self.temp_dir / "image2.png",
        ]
        
        for file_path in self.image_files:
            file_path.touch()
    
    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_find_image_files_convenience_function(self):
        """Test the convenience function works correctly."""
        found_files = find_image_files(self.temp_dir, self.logger)
        found_paths = set(found_files)
        expected_paths = set(self.image_files)
        
        assert found_paths == expected_paths


class TestErrorHandling:
    """Test error handling scenarios."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.logger = setup_logging("ERROR")
        self.scanner = DirectoryScanner(self.logger)
    
    def test_permission_error_handling(self):
        """Test handling of permission errors during directory access."""
        # Create a mock that raises PermissionError
        mock_directory = Mock()
        mock_directory.exists.return_value = True
        mock_directory.is_dir.return_value = True
        mock_directory.iterdir.side_effect = PermissionError("Access denied")
        
        # This should not raise an exception, but should log the error
        result = list(self.scanner._scan_recursive(mock_directory))
        assert result == []
        assert len(self.scanner.failed_files) == 1


def test_image_file_extensions():
    """Test that all expected image file extensions are supported."""
    from dimensions.utils import is_image_file
    
    # Test supported extensions
    supported_extensions = [
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif',
        '.webp', '.heic', '.heif', '.heics', '.heifs', '.hif'
    ]
    
    for ext in supported_extensions:
        test_path = Path(f"test_image{ext}")
        assert is_image_file(test_path), f"Extension {ext} should be supported"
        
        # Test uppercase versions
        test_path_upper = Path(f"test_image{ext.upper()}")
        assert is_image_file(test_path_upper), f"Extension {ext.upper()} should be supported"
    
    # Test unsupported extensions
    unsupported_extensions = ['.txt', '.doc', '.pdf', '.mp4', '.avi']
    
    for ext in unsupported_extensions:
        test_path = Path(f"test_file{ext}")
        assert not is_image_file(test_path), f"Extension {ext} should not be supported"