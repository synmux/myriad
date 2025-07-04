"""
Output formatting functionality for displaying dimension analysis results.
"""

import sys
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List, Optional
import structlog

import orjson
import yaml
from rich.console import Console
from rich.table import Table
from rich.text import Text

from .processor import DimensionStats
from .utils import format_file_size, truncate_file_list


class OutputFormatter:
    """Formats and outputs dimension analysis results."""
    
    def __init__(self, logger: structlog.BoundLogger):
        """
        Initialize the output formatter.
        
        Args:
            logger: Structured logger instance
        """
        self.logger = logger
        self.console = Console(file=sys.stderr)  # Rich output goes to stderr
    
    def format_results(self,
                      results: Dict[str, DimensionStats],
                      format_type: str = "text",
                      sort_by: str = "count",
                      min_count: int = 1,
                      max_results: Optional[int] = None,
                      output_file: Optional[Path] = None) -> None:
        """
        Format and output results in the specified format.
        
        Args:
            results: Dictionary of dimension statistics
            format_type: Output format ('text', 'json', 'yaml')
            sort_by: Sort criteria ('count' or 'dimensions')
            min_count: Minimum count to include
            max_results: Maximum number of results to show
            output_file: Optional file to save output
        """
        # Filter and sort results
        filtered_results = self._filter_and_sort_results(
            results, sort_by, min_count, max_results
        )
        
        # Generate summary statistics
        summary = self._generate_summary(results, filtered_results)
        
        # Format based on type
        if format_type == "text":
            self._output_text_format(filtered_results, summary, output_file)
        elif format_type == "json":
            self._output_json_format(filtered_results, summary, output_file)
        elif format_type == "yaml":
            self._output_yaml_format(filtered_results, summary, output_file)
        else:
            raise ValueError(f"Unsupported format type: {format_type}")
    
    def _filter_and_sort_results(self,
                                results: Dict[str, DimensionStats],
                                sort_by: str,
                                min_count: int,
                                max_results: Optional[int]) -> List[DimensionStats]:
        """
        Filter and sort dimension statistics.
        
        Args:
            results: Raw results dictionary
            sort_by: Sort criteria ('count' or 'dimensions')
            min_count: Minimum count filter
            max_results: Maximum results limit
            
        Returns:
            Filtered and sorted list of DimensionStats
        """
        # Filter by minimum count
        filtered = [stats for stats in results.values() if stats.count >= min_count]
        
        # Sort based on criteria
        if sort_by == "count":
            filtered.sort(key=lambda x: x.count, reverse=True)
        elif sort_by == "dimensions":
            filtered.sort(key=lambda x: (x.width, x.height))
        else:
            raise ValueError(f"Unsupported sort criteria: {sort_by}")
        
        # Limit results
        if max_results is not None:
            filtered = filtered[:max_results]
        
        return filtered
    
    def _generate_summary(self,
                         all_results: Dict[str, DimensionStats],
                         filtered_results: List[DimensionStats]) -> Dict:
        """
        Generate summary statistics.
        
        Args:
            all_results: All dimension statistics
            filtered_results: Filtered results being displayed
            
        Returns:
            Summary statistics dictionary
        """
        total_images = sum(stats.count for stats in all_results.values())
        total_size = sum(stats.total_size for stats in all_results.values())
        unique_dimensions = len(all_results)
        
        # Find most common dimension
        most_common = None
        if all_results:
            most_common = max(all_results.values(), key=lambda x: x.count)
        
        return {
            "total_images": total_images,
            "unique_dimensions": unique_dimensions,
            "total_size_bytes": total_size,
            "total_size": format_file_size(total_size),
            "most_common_dimension": most_common.dimensions_str if most_common else "None",
            "most_common_count": most_common.count if most_common else 0,
            "displayed_results": len(filtered_results)
        }
    
    def _output_text_format(self,
                           results: List[DimensionStats],
                           summary: Dict,
                           output_file: Optional[Path]) -> None:
        """
        Output results in rich text format.
        
        Args:
            results: Filtered dimension statistics
            summary: Summary statistics
            output_file: Optional output file
        """
        output_console = Console(file=open(output_file, 'w', encoding='utf-8')) if output_file else Console()
        
        # Summary table
        summary_table = Table(title="Summary Statistics", show_header=True)
        summary_table.add_column("Metric", style="cyan", width=20)
        summary_table.add_column("Value", style="white")
        
        summary_table.add_row("Total Images", f"{summary['total_images']:,}")
        summary_table.add_row("Unique Dimensions", f"{summary['unique_dimensions']:,}")
        summary_table.add_row("Total Size", summary['total_size'])
        summary_table.add_row("Most Common", 
                             f"{summary['most_common_dimension']} ({summary['most_common_count']:,} images)")
        
        output_console.print(summary_table)
        output_console.print()
        
        # Results table
        if results:
            results_table = Table(
                title=f"Image Dimensions Analysis - {summary['total_images']:,} images",
                show_header=True
            )
            results_table.add_column("Dimensions", style="yellow", width=15)
            results_table.add_column("Count", style="green", justify="right", width=7)
            results_table.add_column("Percentage", style="blue", justify="right", width=12)
            results_table.add_column("Total Size", style="magenta", justify="right", width=12)
            results_table.add_column("Sample Files", style="white", width=40)
            
            for stats in results:
                percentage = (stats.count / summary['total_images']) * 100
                sample_files = truncate_file_list(stats.files, 3)
                
                results_table.add_row(
                    stats.dimensions_str,
                    f"{stats.count:,}",
                    f"{percentage:.1f}%",
                    stats.formatted_size,
                    sample_files
                )
            
            output_console.print(results_table)
        else:
            output_console.print("[yellow]No results match the specified criteria.[/yellow]")
        
        if output_file:
            output_console.file.close()
    
    def _output_json_format(self,
                           results: List[DimensionStats],
                           summary: Dict,
                           output_file: Optional[Path]) -> None:
        """
        Output results in JSON format.
        
        Args:
            results: Filtered dimension statistics
            summary: Summary statistics
            output_file: Optional output file
        """
        # Convert results to JSON-serializable format
        dimensions_data = []
        for stats in results:
            percentage = (stats.count / summary['total_images']) * 100 if summary['total_images'] > 0 else 0
            
            dimensions_data.append({
                "width": stats.width,
                "height": stats.height,
                "dimensions": stats.dimensions_str,
                "count": stats.count,
                "percentage": round(percentage, 1),
                "total_size_bytes": stats.total_size,
                "total_size": stats.formatted_size,
                "sample_files": stats.files[:5]  # Limit to 5 samples for JSON
            })
        
        output_data = {
            "summary": summary,
            "dimensions": dimensions_data
        }
        
        # Output JSON
        json_bytes = orjson.dumps(output_data, option=orjson.OPT_INDENT_2)
        json_str = json_bytes.decode('utf-8')
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(json_str)
        else:
            print(json_str)
    
    def _output_yaml_format(self,
                           results: List[DimensionStats],
                           summary: Dict,
                           output_file: Optional[Path]) -> None:
        """
        Output results in YAML format.
        
        Args:
            results: Filtered dimension statistics
            summary: Summary statistics
            output_file: Optional output file
        """
        # Convert results to YAML-serializable format
        dimensions_data = []
        for stats in results:
            percentage = (stats.count / summary['total_images']) * 100 if summary['total_images'] > 0 else 0
            
            dimensions_data.append({
                "width": stats.width,
                "height": stats.height,
                "dimensions": stats.dimensions_str,
                "count": stats.count,
                "percentage": round(percentage, 1),
                "total_size_bytes": stats.total_size,
                "total_size": stats.formatted_size,
                "sample_files": stats.files[:5]  # Limit to 5 samples for YAML
            })
        
        output_data = {
            "summary": summary,
            "dimensions": dimensions_data
        }
        
        # Output YAML
        yaml_str = yaml.dump(output_data, default_flow_style=False, sort_keys=False, allow_unicode=True)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(yaml_str)
        else:
            print(yaml_str)
    
    def show_progress_summary(self, 
                            total_processed: int,
                            total_failed: int,
                            processing_time: float) -> None:
        """
        Show processing summary to stderr.
        
        Args:
            total_processed: Number of successfully processed files
            total_failed: Number of failed files
            processing_time: Total processing time in seconds
        """
        self.console.print(f"\n[green]Processing completed![/green]")
        self.console.print(f"  Processed: {total_processed:,} images")
        if total_failed > 0:
            self.console.print(f"  [yellow]Failed: {total_failed:,} images[/yellow]")
        self.console.print(f"  Time: {processing_time:.2f} seconds")
        if total_processed > 0:
            rate = total_processed / processing_time
            self.console.print(f"  Rate: {rate:.1f} images/second")
        self.console.print()