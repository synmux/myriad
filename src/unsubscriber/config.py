"""
Configuration constants for Gmail Unsubscriber
"""

import structlog
from rich.console import Console

# Gmail API scope
GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# Default values
DEFAULT_CREDENTIALS_FILE = 'credentials.json'
DEFAULT_TOKEN_FILE = 'token.pickle'
DEFAULT_THREAD_COUNT = 4
DEFAULT_DELAY_SECONDS = 2
DEFAULT_MAX_RESULTS = 100

# Labels
LABEL_PENDING = 'pending-unsubscribe'
LABEL_UNSUBSCRIBED = 'unsubscribed'

# HTTP Request settings
HTTP_TIMEOUT = 10
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

# Success indicators for HTTP unsubscribe
SUCCESS_INDICATORS = ['unsubscribed', 'success', 'confirmed', 'removed']

# Rich console instance (shared across modules)
console = Console()

# Configure structlog
def configure_logging(verbose: bool = False):
    """Configure structlog based on verbosity"""
    if verbose:
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.dev.ConsoleRenderer()
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        # Silent mode - only critical errors
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.processors.format_exc_info,
                structlog.processors.JSONRenderer()
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )