"""
Command-line interface for the dimensions analysis tool.
"""

import sys
import time
from pathlib import Path
from typing import Optional

import click
from tqdm import tqdm
import structlog

from . import __version__
from .scanner import DirectoryScanner
from .processor import ImageProcessor
from .formatter import OutputFormatter
from .organizer import FileOrganizer, OperationType, validate_operation_type, check_target_directory_writable
from .utils import setup_logging


@click.command()
@click.argument('path', type=click.Path(exists=True, path_type=Path), default=Path.cwd())
@click.option('--format', 'output_format', 
              type=click.Choice(['text', 'json', 'yaml']), 
              default='text',
              help='Output format')
@click.option('--sort', 'sort_by',
              type=click.Choice(['count', 'dimensions']),
              default='count', 
              help='Sort results by count (descending) or dimensions')
@click.option('--min-count', 
              type=int, 
              default=1,
              help='Only show dimensions with at least N images')
@click.option('--max-results',
              type=int,
              help='Limit number of results shown')
@click.option('--threads',
              type=int,
              default=1,
              help='Number of processing threads (default: 1)')
@click.option('--log-level',
              type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR']),
              default='INFO',
              help='Logging level')
@click.option('--output', '-o',
              type=click.Path(path_type=Path),
              help='Save output to file')
@click.option('--no-progress',
              is_flag=True,
              help='Disable progress bars')
@click.option('--move',
              type=click.Path(path_type=Path),
              help='Move images to directories by dimensions')
@click.option('--copy', 
              type=click.Path(path_type=Path),
              help='Copy images to directories by dimensions')
@click.option('--symlink',
              type=click.Path(path_type=Path),
              help='Create symlinks to images by dimensions')
@click.option('--dry-run',
              is_flag=True,
              help='Preview operations without executing them')
@click.version_option(version=__version__)
def main(path: Path,
         output_format: str,
         sort_by: str,
         min_count: int,
         max_results: Optional[int],
         threads: int,
         log_level: str,
         output: Optional[Path],
         no_progress: bool,
         move: Optional[Path],
         copy: Optional[Path],
         symlink: Optional[Path],
         dry_run: bool) -> None:
    """
    Analyze image dimensions in a directory.
    
    PATH: Directory to analyze (default: current directory)
    """
    # Validate mutually exclusive file operations
    file_operations = [move, copy, symlink]
    active_operations = [op for op in file_operations if op is not None]
    
    if len(active_operations) > 1:
        click.echo("Error: Only one of --move, --copy, or --symlink can be specified", err=True)
        sys.exit(1)
    
    # Determine operation type and target directory
    operation_type = None
    target_directory = None
    
    if move:
        operation_type = OperationType.MOVE
        target_directory = move
    elif copy:
        operation_type = OperationType.COPY
        target_directory = copy
    elif symlink:
        operation_type = OperationType.SYMLINK
        target_directory = symlink
    
    # Validate dry-run usage
    if dry_run and operation_type is None:
        click.echo("Error: --dry-run can only be used with --move, --copy, or --symlink", err=True)
        sys.exit(1)
    
    # Validate target directory writability for non-dry-run operations
    if operation_type and not dry_run:
        if not check_target_directory_writable(target_directory):
            click.echo(f"Error: Cannot write to target directory: {target_directory}", err=True)
            sys.exit(1)
    
    # Set up logging
    logger = setup_logging(log_level)
    
    # Validate threads parameter
    if threads < 1:
        click.echo("Error: Number of threads must be at least 1", err=True)
        sys.exit(1)
    
    try:
        # Initialize components
        scanner = DirectoryScanner(logger)
        processor = ImageProcessor(logger)
        formatter = OutputFormatter(logger)
        organizer = FileOrganizer(logger) if operation_type else None
        
        # Start timing
        start_time = time.time()
        
        # Phase 1: Scan for image files
        logger.info("Starting image dimension analysis", directory=str(path))
        
        if not no_progress:
            click.echo("Scanning for image files...", err=True)
        
        image_files = list(scanner.scan_directory(path))
        
        if not image_files:
            click.echo("No image files found in the specified directory.", err=True)
            sys.exit(0)
        
        logger.info("Found image files", count=len(image_files))
        
        # Phase 2: Process images with progress bar
        if not no_progress:
            click.echo(f"Processing {len(image_files)} image files...", err=True)
            
            # Use tqdm for progress tracking
            with tqdm(total=len(image_files), 
                     desc="Processing images",
                     unit="images",
                     file=sys.stderr) as pbar:
                
                # Process all files with progress updates
                results = processor.process_images(image_files, threads)
                
                # Update progress bar to completion
                pbar.update(len(image_files))
                pbar.set_postfix(
                    failed=len(processor.get_failed_files()),
                    dimensions=len(results)
                )
        else:
            # Process without progress bar
            results = processor.process_images(image_files, threads)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Phase 3: File operations (if requested)
        if operation_type:
            if not no_progress:
                click.echo(f"\n{operation_type.value.title()}ing files by dimensions...", err=True)
            
            organizer.organize_files(results, target_directory, operation_type, dry_run)
            
            # Show organization statistics
            stats = organizer.get_statistics()
            if dry_run:
                logger.info("Dry run completed - no files were actually moved/copied/linked")
            else:
                logger.info("File organization statistics", **stats)
                
                failed_ops = organizer.get_failed_operations()
                if failed_ops:
                    logger.warning("Some file operations failed", count=len(failed_ops))
        
        # Phase 4: Output results
        formatter.format_results(
            results=results,
            format_type=output_format,
            sort_by=sort_by,
            min_count=min_count,
            max_results=max_results,
            output_file=output
        )
        
        # Show processing summary (only for text format or if writing to file)
        if output_format == 'text' or output:
            formatter.show_progress_summary(
                total_processed=len(processor.get_processed_files()),
                total_failed=len(processor.get_failed_files()),
                processing_time=processing_time
            )
        
        # Log final statistics
        logger.info("Analysis completed successfully",
                   processed_images=len(processor.get_processed_files()),
                   failed_images=len(processor.get_failed_files()),
                   unique_dimensions=len(results),
                   processing_time=processing_time)
        
    except KeyboardInterrupt:
        click.echo("\nOperation cancelled by user.", err=True)
        sys.exit(1)
    except Exception as e:
        logger.error("Unexpected error during processing", error=str(e))
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()