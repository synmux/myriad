"""
Utility functions for the dimensions CLI tool.
"""

import os
import structlog
from pathlib import Path
from typing import List


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in bytes to human-readable string.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Human-readable size string (e.g., "1.2 GB", "456.7 MB")
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    size = float(size_bytes)
    i = 0
    
    while size >= 1024.0 and i < len(size_names) - 1:
        size /= 1024.0
        i += 1
    
    if i == 0:
        return f"{int(size)} {size_names[i]}"
    else:
        return f"{size:.1f} {size_names[i]}"


def setup_logging(level: str = "INFO") -> structlog.BoundLogger:
    """
    Set up structured logging for the application.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        
    Returns:
        Configured structlog logger
    """
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.ConsoleRenderer(colors=True)
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(structlog.stdlib, level.upper(), structlog.stdlib.INFO)
        ),
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    return structlog.get_logger()


def get_file_size(file_path: Path) -> int:
    """
    Get file size in bytes, handling errors gracefully.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File size in bytes, or 0 if error
    """
    try:
        return file_path.stat().st_size
    except (OSError, IOError):
        return 0


def truncate_file_list(files: List[str], max_length: int = 3) -> str:
    """
    Truncate a list of filenames for display.
    
    Args:
        files: List of file paths
        max_length: Maximum number of files to show
        
    Returns:
        Formatted string showing files with count if truncated
    """
    if not files:
        return "No files"
    
    filenames = [os.path.basename(f) for f in files]
    
    if len(filenames) <= max_length:
        return ", ".join(filenames)
    else:
        displayed = filenames[:max_length]
        remaining = len(filenames) - max_length
        return f"{', '.join(displayed)} (+{remaining})"


def ensure_directory(path: Path) -> None:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Directory path to create
        
    Raises:
        OSError: If directory cannot be created
    """
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise OSError(f"Cannot create directory {path}: {e}")


def safe_filename(dimensions: str) -> str:
    """
    Create a safe filename from dimensions string.
    
    Args:
        dimensions: Dimensions string like "1920×1080"
        
    Returns:
        Safe filename string like "1920x1080"
    """
    return dimensions.replace("×", "x").replace(":", "-").replace("/", "-")


SUPPORTED_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', 
    '.webp', '.heic', '.heif', '.heics', '.heifs', '.hif'
}


def is_image_file(file_path: Path) -> bool:
    """
    Check if a file is a supported image format.
    
    Args:
        file_path: Path to check
        
    Returns:
        True if file has supported image extension
    """
    return file_path.suffix.lower() in SUPPORTED_EXTENSIONS