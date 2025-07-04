#!/usr/bin/env python3
"""
Basic test script to verify dimensions CLI package structure and functionality.
Run this after installing dependencies to verify the package works correctly.
"""

import sys
import tempfile
import os
from pathlib import Path

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        # Add src to path for testing
        src_path = Path(__file__).parent / "src"
        sys.path.insert(0, str(src_path))
        
        # Test basic imports
        from dimensions import __version__
        print(f"✓ Package version: {__version__}")
        
        from dimensions.utils import format_file_size, is_image_file
        print("✓ Utils module imported")
        
        from dimensions.scanner import DirectoryScanner
        print("✓ Scanner module imported")
        
        from dimensions.processor import ImageProcessor
        print("✓ Processor module imported")
        
        from dimensions.formatter import OutputFormatter
        print("✓ Formatter module imported")
        
        from dimensions.organizer import FileOrganizer
        print("✓ Organizer module imported")
        
        from dimensions.cli import main
        print("✓ CLI module imported")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_utilities():
    """Test utility functions."""
    print("\nTesting utility functions...")
    
    try:
        from dimensions.utils import format_file_size, is_image_file, safe_filename
        
        # Test file size formatting
        assert format_file_size(0) == "0 B"
        assert format_file_size(1024) == "1.0 KB"
        assert format_file_size(1024 * 1024) == "1.0 MB"
        print("✓ File size formatting works")
        
        # Test image file detection
        assert is_image_file(Path("test.jpg")) == True
        assert is_image_file(Path("test.png")) == True
        assert is_image_file(Path("test.txt")) == False
        print("✓ Image file detection works")
        
        # Test safe filename
        assert safe_filename("1920×1080") == "1920x1080"
        assert safe_filename("test:file/name") == "test-file-name"
        print("✓ Safe filename generation works")
        
        return True
        
    except Exception as e:
        print(f"✗ Utility test failed: {e}")
        return False

def test_cli_help():
    """Test CLI help functionality."""
    print("\nTesting CLI help...")
    
    try:
        from dimensions.cli import main
        from click.testing import CliRunner
        
        runner = CliRunner()
        result = runner.invoke(main, ['--help'])
        
        if result.exit_code == 0 and "Analyze image dimensions" in result.output:
            print("✓ CLI help works")
            return True
        else:
            print(f"✗ CLI help failed: exit_code={result.exit_code}")
            return False
            
    except Exception as e:
        print(f"✗ CLI test failed: {e}")
        return False

def create_test_images():
    """Create some test image files for testing."""
    print("\nCreating test images...")
    
    try:
        from PIL import Image
        
        # Create temporary directory
        test_dir = Path(tempfile.mkdtemp(prefix="dimensions_test_"))
        print(f"Test directory: {test_dir}")
        
        # Create test images
        for i, (width, height) in enumerate([(100, 100), (200, 150), (100, 100)]):
            img = Image.new('RGB', (width, height), color='red')
            img_path = test_dir / f"test_image_{i}.png"
            img.save(img_path)
            print(f"✓ Created {img_path}")
        
        return test_dir
        
    except Exception as e:
        print(f"✗ Test image creation failed: {e}")
        return None

def test_basic_analysis(test_dir):
    """Test basic dimension analysis."""
    if not test_dir:
        return False
        
    print(f"\nTesting basic analysis on {test_dir}...")
    
    try:
        from dimensions.scanner import DirectoryScanner
        from dimensions.processor import ImageProcessor
        from dimensions.utils import setup_logging
        
        logger = setup_logging("ERROR")  # Quiet logging for tests
        
        # Test scanner
        scanner = DirectoryScanner(logger)
        image_files = list(scanner.scan_directory(test_dir))
        print(f"✓ Found {len(image_files)} image files")
        
        # Test processor
        processor = ImageProcessor(logger)
        results = processor.process_images(image_files)
        print(f"✓ Processed images, found {len(results)} unique dimensions")
        
        # Check results
        if len(results) > 0:
            for dim_str, stats in results.items():
                print(f"  - {dim_str}: {stats.count} images")
        
        return True
        
    except Exception as e:
        print(f"✗ Basic analysis failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Dimensions CLI Package Tests")
    print("=" * 40)
    
    success = True
    
    # Test imports
    success &= test_imports()
    
    # Test utilities (no dependencies needed)
    success &= test_utilities()
    
    # Test CLI help (requires Click)
    try:
        success &= test_cli_help()
    except ImportError:
        print("⚠ Skipping CLI test (Click not available)")
    
    # Test image processing (requires Pillow)
    try:
        test_dir = create_test_images()
        success &= test_basic_analysis(test_dir)
        
        # Cleanup
        if test_dir and test_dir.exists():
            import shutil
            shutil.rmtree(test_dir)
            print(f"✓ Cleaned up {test_dir}")
            
    except ImportError:
        print("⚠ Skipping image tests (Pillow not available)")
    
    print("\n" + "=" * 40)
    if success:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())