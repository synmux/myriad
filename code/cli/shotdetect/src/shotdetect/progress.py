"""Progress tracking and logging utilities."""

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import structlog
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
)
from rich.table import Table
from rich.text import Text

logger = structlog.get_logger(__name__)


class ProgressTracker:
    """Tracks and displays progress for image classification."""

    def __init__(self, json_output: bool = False, quiet: bool = False):
        """Initialize progress tracker.

        Args:
            json_output: If True, output JSON instead of rich formatting
            quiet: If True, minimize output
        """
        self.json_output = json_output
        self.quiet = quiet
        self.console = Console() if not json_output else None
        self.start_time = None
        self.stats = {
            "total_files": 0,
            "processed_files": 0,
            "screenshots": 0,
            "other": 0,
            "errors": 0,
            "start_time": None,
            "end_time": None,
        }

    def start_processing(self, total_files: int, directory: str, model: str):
        """Start processing with initial setup.

        Args:
            total_files: Total number of files to process
            directory: Directory being processed
            model: Model being used
        """
        self.start_time = time.time()
        self.stats["total_files"] = total_files
        self.stats["start_time"] = self.start_time

        if self.json_output:
            self._output_json(
                {
                    "event": "processing_started",
                    "total_files": total_files,
                    "directory": directory,
                    "model": model,
                    "timestamp": self.start_time,
                }
            )
        elif not self.quiet:
            self.console.print(
                Panel(
                    f"[bold]Starting Classification[/bold]\n"
                    f"Directory: {directory}\n"
                    f"Model: {model}\n"
                    f"Total files: {total_files:,}",
                    title="shotdetect",
                    expand=False,
                )
            )

    def create_progress_bar(self, description: str = "Processing") -> tuple:
        """Create a progress bar for file processing.

        Args:
            description: Description for the progress bar

        Returns:
            Tuple of (progress_context, task_id) or (None, None) for JSON output
        """
        if self.json_output or self.quiet:
            return None, None

        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            TimeRemainingColumn(),
            console=self.console,
            expand=True,
        )

        return progress, progress.add_task(description, total=self.stats["total_files"])

    def update_progress(
        self, progress: Optional[Progress], task_id: Optional[TaskID], advance: int = 1
    ):
        """Update progress bar.

        Args:
            progress: Progress context manager
            task_id: Task ID from progress bar
            advance: Number of steps to advance
        """
        if progress and task_id:
            progress.update(task_id, advance=advance)

    def log_classification(
        self, file_path: str, classification: str, error: Optional[str] = None
    ):
        """Log a classification result.

        Args:
            file_path: Path to the classified file
            classification: Classification result
            error: Error message if classification failed
        """
        self.stats["processed_files"] += 1

        if classification == "screenshot":
            self.stats["screenshots"] += 1
        elif classification == "other":
            self.stats["other"] += 1
        elif classification is None:
            self.stats["errors"] += 1

        if self.json_output:
            self._output_json(
                {
                    "event": "file_classified",
                    "file_path": file_path,
                    "classification": classification,
                    "error": error,
                    "timestamp": time.time(),
                }
            )
        else:
            # Real-time logging is handled by structlog
            pass

    def log_file_operation(
        self, operation: str, source: str, destination: str, classification: str
    ):
        """Log a file operation (copy/move).

        Args:
            operation: Operation type (copy/move)
            source: Source file path
            destination: Destination file path
            classification: File classification
        """
        if self.json_output:
            self._output_json(
                {
                    "event": "file_operation",
                    "operation": operation,
                    "source": source,
                    "destination": destination,
                    "classification": classification,
                    "timestamp": time.time(),
                }
            )

    def finish_processing(self):
        """Finish processing and show final statistics."""
        self.stats["end_time"] = time.time()
        duration = self.stats["end_time"] - self.stats["start_time"]

        if self.json_output:
            self._output_json(
                {
                    "event": "processing_completed",
                    "stats": self.stats,
                    "duration_seconds": duration,
                    "timestamp": self.stats["end_time"],
                }
            )
        elif not self.quiet:
            self._show_final_stats(duration)

    def _show_final_stats(self, duration: float):
        """Show final statistics in rich format.

        Args:
            duration: Processing duration in seconds
        """
        table = Table(title="Classification Results")

        table.add_column("Metric", style="cyan")
        table.add_column("Count", style="green")
        table.add_column("Percentage", style="yellow")

        total = self.stats["processed_files"]

        table.add_row("Total Files", f"{total:,}", "100.0%")
        table.add_row(
            "Screenshots",
            f"{self.stats['screenshots']:,}",
            f"{self.stats['screenshots']/total*100:.1f}%" if total > 0 else "0.0%",
        )
        table.add_row(
            "Other Images",
            f"{self.stats['other']:,}",
            f"{self.stats['other']/total*100:.1f}%" if total > 0 else "0.0%",
        )
        table.add_row(
            "Errors",
            f"{self.stats['errors']:,}",
            f"{self.stats['errors']/total*100:.1f}%" if total > 0 else "0.0%",
        )

        self.console.print(table)

        self.console.print(
            Panel(
                (
                    f"[bold]Processing Complete[/bold]\n"
                    f"Duration: {duration:.1f} seconds\n"
                    f"Rate: {total/duration:.1f} files/second"
                    if duration > 0
                    else "Rate: N/A"
                ),
                title="Summary",
                expand=False,
            )
        )

    def _output_json(self, data: Dict[str, Any]):
        """Output JSON data to stdout.

        Args:
            data: Data to output as JSON
        """
        print(json.dumps(data, default=str))

    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics.

        Returns:
            Dictionary of current statistics
        """
        return self.stats.copy()

    def show_model_info(self, model_info: Dict[str, Any]):
        """Show model information.

        Args:
            model_info: Model information dictionary
        """
        if self.json_output:
            self._output_json(
                {
                    "event": "model_info",
                    "model_info": model_info,
                    "timestamp": time.time(),
                }
            )
        elif not self.quiet:
            self.console.print(
                Panel(
                    f"[bold]Model Information[/bold]\n"
                    f"Name: {model_info.get('name', 'Unknown')}\n"
                    f"Size: {model_info.get('size', 'Unknown')}\n"
                    f"Modified: {model_info.get('modified_at', 'Unknown')}",
                    title="Model Details",
                    expand=False,
                )
            )

    def show_scan_results(self, file_count: int, supported_count: int, directory: str):
        """Show directory scan results.

        Args:
            file_count: Total files found
            supported_count: Supported files found
            directory: Directory scanned
        """
        if self.json_output:
            self._output_json(
                {
                    "event": "scan_completed",
                    "total_files": file_count,
                    "supported_files": supported_count,
                    "directory": directory,
                    "timestamp": time.time(),
                }
            )
        elif not self.quiet:
            self.console.print(
                Panel(
                    f"[bold]Directory Scan Complete[/bold]\n"
                    f"Directory: {directory}\n"
                    f"Total files: {file_count:,}\n"
                    f"Supported images: {supported_count:,}",
                    title="Scan Results",
                    expand=False,
                )
            )

    def show_error(self, error_msg: str, error_type: str = "error"):
        """Show error message.

        Args:
            error_msg: Error message
            error_type: Type of error
        """
        if self.json_output:
            self._output_json(
                {
                    "event": "error",
                    "error_type": error_type,
                    "error_message": error_msg,
                    "timestamp": time.time(),
                }
            )
        else:
            self.console.print(f"[bold red]Error:[/bold red] {error_msg}")

    def show_warning(self, warning_msg: str):
        """Show warning message.

        Args:
            warning_msg: Warning message
        """
        if self.json_output:
            self._output_json(
                {
                    "event": "warning",
                    "warning_message": warning_msg,
                    "timestamp": time.time(),
                }
            )
        else:
            self.console.print(f"[bold yellow]Warning:[/bold yellow] {warning_msg}")

    def show_dry_run_summary(self, summary: Dict[str, Any]):
        """Show dry run summary.

        Args:
            summary: Summary of what would be done
        """
        if self.json_output:
            self._output_json(
                {
                    "event": "dry_run_summary",
                    "summary": summary,
                    "timestamp": time.time(),
                }
            )
        elif not self.quiet:
            self.console.print(
                Panel(
                    f"[bold]Dry Run Summary[/bold]\n"
                    f"Operation: {summary.get('operation', 'unknown')}\n"
                    f"Screenshots: {summary.get('screenshots', 0):,}\n"
                    f"Other images: {summary.get('other', 0):,}\n"
                    f"Errors: {summary.get('errors', 0):,}",
                    title="Would Perform",
                    expand=False,
                )
            )
