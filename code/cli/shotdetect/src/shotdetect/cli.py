"""Command line interface for shotdetect."""

import asyncio
import sys
from pathlib import Path
from typing import Optional

import click
import structlog

from .classifier import ImageClassifier
from .file_handler import FileHandler
from .ollama_client import OllamaClient
from .progress import ProgressTracker

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)


@click.command()
@click.argument(
    "image_directory",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
)
@click.option(
    "--model",
    default="qwen2.5vl:3b",
    help="Ollama model to use for classification (default: qwen2.5vl:7b)",
)
@click.option(
    "--move",
    type=click.Path(path_type=Path),
    help="Move screenshots to DIR/screenshots and other to DIR/other",
)
@click.option(
    "--copy",
    type=click.Path(path_type=Path),
    help="Copy screenshots to DIR/screenshots and other to DIR/other",
)
@click.option(
    "--dry-run", is_flag=True, help="Show what would be done without actually doing it"
)
@click.option("--json", "json_output", is_flag=True, help="Output JSON for scripting")
@click.option(
    "--batch-size",
    default=5,
    type=int,
    help="Number of images to process in parallel (default: 5)",
)
@click.option(
    "--download-models",
    is_flag=True,
    help="Download all variants of the specified model (e.g., qwen2.5vl:*)",
)
@click.option(
    "--recursive/--no-recursive",
    default=True,
    help="Recursively scan subdirectories (default: recursive)",
)
@click.option("--quiet", is_flag=True, help="Minimize output (except for JSON mode)")
@click.option(
    "--max-image-size",
    default="1024x1024",
    help="Maximum image size for processing (default: 1024x1024)",
)
def main(
    image_directory: Path,
    model: str,
    move: Optional[Path],
    copy: Optional[Path],
    dry_run: bool,
    json_output: bool,
    batch_size: int,
    download_models: bool,
    recursive: bool,
    quiet: bool,
    max_image_size: str,
):
    """Classify images as screenshots or other content using Ollama vision models.

    IMAGE_DIRECTORY is the directory containing images to classify.
    """
    # Parse max image size
    try:
        width, height = map(int, max_image_size.split("x"))
        max_size = (width, height)
    except ValueError:
        click.echo(
            f"Error: Invalid max-image-size format. Use WIDTHxHEIGHT (e.g., 1024x1024)",
            err=True,
        )
        sys.exit(1)

    # Validate arguments
    if move and copy:
        click.echo("Error: Cannot specify both --move and --copy", err=True)
        sys.exit(1)

    if download_models:
        if not model.endswith(":*"):
            model = model + ":*"

    # Initialize progress tracker
    progress_tracker = ProgressTracker(json_output=json_output, quiet=quiet)

    try:
        asyncio.run(
            _run_classification(
                image_directory=image_directory,
                model=model,
                move_dir=move,
                copy_dir=copy,
                dry_run=dry_run,
                batch_size=batch_size,
                download_models=download_models,
                recursive=recursive,
                max_size=max_size,
                progress_tracker=progress_tracker,
            )
        )
    except KeyboardInterrupt:
        progress_tracker.show_error("Classification interrupted by user")
        sys.exit(1)
    except Exception as e:
        progress_tracker.show_error(f"Classification failed: {str(e)}")
        logger.exception("Classification failed")
        sys.exit(1)


async def _run_classification(
    image_directory: Path,
    model: str,
    move_dir: Optional[Path],
    copy_dir: Optional[Path],
    dry_run: bool,
    batch_size: int,
    download_models: bool,
    recursive: bool,
    max_size: tuple,
    progress_tracker: ProgressTracker,
):
    """Run the classification process."""

    # Initialize components
    classifier = ImageClassifier(
        model_name=model if not download_models else model.replace(":*", ":7b"),
        batch_size=batch_size,
        max_image_size=max_size,
    )

    # Check Ollama connection
    if not classifier.ollama_client.check_connection():
        progress_tracker.show_error(
            "Cannot connect to Ollama server. Make sure Ollama is running."
        )
        sys.exit(1)

    # Handle model downloads
    if download_models:
        progress_tracker.show_warning(f"Downloading all variants of {model}")
        downloaded = classifier.ollama_client.download_model_variants(model)
        if not downloaded:
            progress_tracker.show_error(f"No models downloaded for pattern {model}")
            sys.exit(1)

        # Use the first downloaded model
        classifier.model_name = downloaded[0]
        model = downloaded[0]
    else:
        # Ensure single model is available
        if not classifier.download_model_if_needed():
            progress_tracker.show_error(f"Failed to download model {model}")
            sys.exit(1)

    # Show model info
    model_info = classifier.get_model_info()
    if model_info:
        progress_tracker.show_model_info(model_info)

    # Scan directory for images
    image_files = classifier.image_loader.scan_directory(image_directory, recursive)
    supported_files = [
        f for f in image_files if classifier.image_loader.is_supported(f)
    ]

    progress_tracker.show_scan_results(
        file_count=len(image_files),
        supported_count=len(supported_files),
        directory=str(image_directory),
    )

    if not supported_files:
        progress_tracker.show_error("No supported image files found")
        sys.exit(1)

    # Start classification
    progress_tracker.start_processing(
        total_files=len(supported_files), directory=str(image_directory), model=model
    )

    progress, task_id = progress_tracker.create_progress_bar("Classifying images")

    def progress_callback(processed: int, total: int):
        progress_tracker.update_progress(progress, task_id, advance=1)

    try:
        if progress:
            with progress:
                results = await classifier.classify_directory(
                    directory=image_directory,
                    recursive=recursive,
                    progress_callback=progress_callback,
                )
        else:
            results = await classifier.classify_directory(
                directory=image_directory,
                recursive=recursive,
                progress_callback=progress_callback,
            )
    except Exception as e:
        progress_tracker.show_error(f"Classification failed: {str(e)}")
        raise

    # Log individual results
    for result in results:
        progress_tracker.log_classification(
            file_path=result["file_path"],
            classification=result["classification"],
            error=result["error"],
        )

    # Handle file operations
    target_dir = move_dir or copy_dir
    if target_dir:
        file_handler = FileHandler(dry_run=dry_run)

        if not file_handler.validate_target_directory(target_dir):
            progress_tracker.show_error(f"Invalid target directory: {target_dir}")
            sys.exit(1)

        operation = "move" if move_dir else "copy"

        # Show space estimate
        if not dry_run:
            space_info = file_handler.estimate_space_needed(results)
            if not progress_tracker.json_output and not progress_tracker.quiet:
                progress_tracker.console.print(
                    f"Estimated space needed: {space_info['total_mb']:.1f} MB"
                )

        # Perform file operations
        summary = file_handler.organize_files(results, target_dir, operation)

        # Log file operations
        for result in results:
            if result["classification"] in ["screenshot", "other"]:
                source_path = result["file_path"]
                dest_subdir = (
                    "screenshots"
                    if result["classification"] == "screenshot"
                    else "other"
                )
                dest_path = target_dir / dest_subdir / Path(source_path).name

                progress_tracker.log_file_operation(
                    operation=operation,
                    source=source_path,
                    destination=str(dest_path),
                    classification=result["classification"],
                )

        if dry_run:
            operation_summary = file_handler.get_operation_summary(results)
            progress_tracker.show_dry_run_summary(operation_summary)

    # Finish and show final stats
    progress_tracker.finish_processing()


@click.group()
def cli():
    """shotdetect: Image classification tool for detecting screenshots."""
    pass


@cli.command()
@click.option(
    "--model",
    default="qwen2.5vl:7b",
    help="Model to download (supports wildcards like qwen2.5vl:*)",
)
def download(model: str):
    """Download Ollama models for image classification."""
    client = OllamaClient()

    if not client.check_connection():
        click.echo("Error: Cannot connect to Ollama server", err=True)
        sys.exit(1)

    if model.endswith(":*"):
        click.echo(f"Downloading all variants of {model}")
        downloaded = client.download_model_variants(model)
        if downloaded:
            click.echo(f"Successfully downloaded {len(downloaded)} models:")
            for model_name in downloaded:
                click.echo(f"  - {model_name}")
        else:
            click.echo("No models were downloaded", err=True)
            sys.exit(1)
    else:
        click.echo(f"Downloading model {model}")
        if client.download_model(model):
            click.echo(f"Successfully downloaded {model}")
        else:
            click.echo(f"Failed to download {model}", err=True)
            sys.exit(1)


@cli.command()
def models():
    """List available Ollama models."""
    client = OllamaClient()

    if not client.check_connection():
        click.echo("Error: Cannot connect to Ollama server", err=True)
        sys.exit(1)

    available_models = client.list_models()

    if not available_models:
        click.echo("No models available")
        return

    click.echo("Available models:")
    for model in available_models:
        size = model.get("size", 0)
        size_mb = size / (1024 * 1024) if size else 0
        click.echo(f"  {model['name']} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    # For direct execution, use the main command
    main()
