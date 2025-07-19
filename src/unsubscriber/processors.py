"""
Email processing with threading support
"""

import structlog
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import ssl
import httplib2
from http.client import IncompleteRead

from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn, MofNCompleteColumn
from rich.table import Table
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google_auth_httplib2

from .gmail_service import GmailService
from .unsubscribe import UnsubscribeHandler
from .utils import extract_headers
from .config import DEFAULT_THREAD_COUNT, DEFAULT_DELAY_SECONDS, console

logger = structlog.get_logger()


@dataclass
class ProcessResult:
    """Result of processing a single email"""
    msg_id: str
    subject: str
    from_addr: str
    success: bool
    error: Optional[str] = None


class EmailProcessor:
    """Processes emails with threading support"""
    
    def __init__(self, gmail_service: GmailService, thread_count: int = DEFAULT_THREAD_COUNT, credentials=None):
        self.gmail_service = gmail_service
        self.thread_count = thread_count
        # Store the credentials for thread safety
        self.credentials = credentials
        
        # Try to extract credentials from service if not provided
        if not self.credentials and hasattr(gmail_service.service, '_http'):
            if hasattr(gmail_service.service._http, 'credentials'):
                self.credentials = gmail_service.service._http.credentials
    
    def process_batch(self, emails: List[Dict], dry_run: bool = False,
                     open_browser: bool = True, delay: int = DEFAULT_DELAY_SECONDS) -> Tuple[int, int]:
        """Process a batch of emails with threading"""
        total = len(emails)
        results = []
        
        # Create Rich progress bar with multiple columns
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            TextColumn("•"),
            TaskProgressColumn(),
            TextColumn("•"),
            TimeRemainingColumn(),
            console=console,
            refresh_per_second=4
        ) as progress:
            
            # Add main task
            main_task = progress.add_task(
                f"[green]Processing {total} emails with {self.thread_count} threads...", 
                total=total
            )
            
            # Add status tracking
            success_counter = 0
            failed_counter = 0
            
            with ThreadPoolExecutor(max_workers=self.thread_count) as executor:
                # Submit all tasks
                future_to_email = {
                    executor.submit(
                        self._process_single_email_safe, 
                        email['id'], 
                        dry_run, 
                        open_browser,
                        delay
                    ): email for email in emails
                }
                
                # Process completed tasks
                for future in as_completed(future_to_email):
                    result = future.result()
                    results.append(result)
                    
                    # Update counters
                    if result.success:
                        success_counter += 1
                        status_icon = "[green]✓[/green]"
                    else:
                        failed_counter += 1
                        status_icon = "[red]✗[/red]"
                    
                    # Update progress bar with current email info
                    progress.update(
                        main_task, 
                        advance=1,
                        description=f"[green]Processing emails... {status_icon} {result.subject[:40]}... ([green]{success_counter}[/green] ✓ / [red]{failed_counter}[/red] ✗)"
                    )
                    
                    # Log result with structured logging
                    if result.success:
                        logger.info("email_processed", 
                                  msg_id=result.msg_id, 
                                  subject=result.subject[:50],
                                  status="success")
                    else:
                        logger.warning("email_process_failed",
                                     msg_id=result.msg_id,
                                     subject=result.subject[:50],
                                     error=result.error)
        
        # Count successes and failures
        success_count = sum(1 for r in results if r.success)
        failed_count = total - success_count
        
        self._print_summary(results, success_count, failed_count)
        
        return success_count, failed_count
    
    def _create_thread_local_service(self):
        """Create a new service instance for the current thread"""
        try:
            # Create a new HTTP object with custom SSL context
            http = httplib2.Http(timeout=30)
            
            # Use google_auth_httplib2 to create an authorized HTTP object
            if self.credentials:
                authorized_http = google_auth_httplib2.AuthorizedHttp(
                    self.credentials, 
                    http=http
                )
                # Build a new service instance with the authorized HTTP
                service = build('gmail', 'v1', http=authorized_http, cache_discovery=False)
            else:
                # Fallback to regular service if no credentials
                service = build('gmail', 'v1', http=http, cache_discovery=False)
            
            return service
        except Exception as e:
            logger.error("service_creation_error", error=str(e))
            raise
    
    def _process_single_email_safe(self, msg_id: str, dry_run: bool, 
                                 open_browser: bool, delay: int) -> ProcessResult:
        """Process a single email with retry logic for SSL errors"""
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                return self._process_single_email(msg_id, dry_run, open_browser, delay)
            except (ssl.SSLError, HttpError, ConnectionError, IncompleteRead) as e:
                error_str = str(e)
                if attempt < max_retries - 1 and any(err in error_str for err in [
                    'DECRYPTION_FAILED', 'BAD_RECORD_MAC', 'UNEXPECTED_RECORD',
                    'MIXED_HANDSHAKE', 'IncompleteRead', 'SSL'
                ]):
                    logger.warning("ssl_error_retry", 
                                 msg_id=msg_id, 
                                 attempt=attempt + 1,
                                 error=error_str)
                    time.sleep(retry_delay * (attempt + 1))
                    continue
                else:
                    # Final attempt failed
                    logger.error("email_processing_error", msg_id=msg_id, error=error_str)
                    return ProcessResult(
                        msg_id=msg_id,
                        subject="Error",
                        from_addr="Unknown",
                        success=False,
                        error=error_str
                    )
            except Exception as e:
                logger.error("email_processing_error", msg_id=msg_id, error=str(e))
                return ProcessResult(
                    msg_id=msg_id,
                    subject="Error",
                    from_addr="Unknown",
                    success=False,
                    error=str(e)
                )
    
    def _process_single_email(self, msg_id: str, dry_run: bool, 
                            open_browser: bool, delay: int) -> ProcessResult:
        """Process a single email and return result"""
        # Create thread-local service instance
        service = self._create_thread_local_service()
        thread_gmail_service = GmailService(service)
        thread_unsubscribe_handler = UnsubscribeHandler(thread_gmail_service)
        
        # Get email details for logging
        message = thread_gmail_service.get_email_details(msg_id)
        headers = extract_headers(message) if message else {}
        subject = headers.get('Subject', 'No Subject')
        from_addr = headers.get('From', 'Unknown')
        
        # Process the email
        success = thread_unsubscribe_handler.process_email(
            msg_id, dry_run=dry_run, open_browser=open_browser
        )
        
        # Delay between requests to avoid rate limiting
        if not dry_run and delay > 0:
            time.sleep(delay)
        
        return ProcessResult(
            msg_id=msg_id,
            subject=subject,
            from_addr=from_addr,
            success=success
        )
    
    def _print_summary(self, results: List[ProcessResult], 
                      success_count: int, failed_count: int):
        """Print processing summary using rich formatting"""
        summary_text = Text()
        summary_text.append("Processing Summary\n\n", style="bold cyan")
        summary_text.append(f"✅ Successfully unsubscribed: {success_count}\n", style="green")
        summary_text.append(f"❌ Failed: {failed_count}\n", style="red")
        
        if failed_count > 0:
            summary_text.append("\n⚠️  Failed emails:\n", style="yellow")
            for result in results:
                if not result.success:
                    error_msg = f" - Error: {result.error}" if result.error else ""
                    summary_text.append(
                        f"  • {result.subject[:50]}... from {result.from_addr[:30]}...{error_msg}\n",
                        style="dim"
                    )
        
        console.print("\n")
        console.print(Panel(summary_text, title="Results", expand=False))