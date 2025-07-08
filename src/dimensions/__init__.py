"""
Dimensions - A powerful Python CLI tool for analyzing image dimensions in directories.

This package provides fast scanning, beautiful terminal output, and comprehensive
statistics about image sizes in your collections.
"""

__version__ = "0.1.0"
__author__ = "Dimensions Team"
__description__ = "A CLI tool for analyzing image dimensions in directories"

from .formatter import OutputFormatter
from .organizer import FileOrganizer
from .processor import ImageProcessor
from .scanner import DirectoryScanner

__all__ = [
    "DirectoryScanner",
    "ImageProcessor",
    "OutputFormatter",
    "FileOrganizer",
    "__version__",
]
