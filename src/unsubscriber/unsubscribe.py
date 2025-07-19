"""
Core unsubscription logic with reduced cyclomatic complexity
"""

import structlog
import webbrowser
from typing import Tuple, List, Optional, Dict

import requests
from bs4 import BeautifulSoup

from .config import (
    HTTP_TIMEOUT, USER_AGENT, SUCCESS_INDICATORS,
    LABEL_PENDING, LABEL_UNSUBSCRIBED
)
from .utils import (
    extract_headers, parse_list_unsubscribe,
    parse_mailto_link, create_unsubscribe_email,
    check_success_indicators
)
from .gmail_service import GmailService

logger = structlog.get_logger()


class UnsubscribeHandler:
    """Handles different unsubscription methods"""
    
    def __init__(self, gmail_service: GmailService):
        self.gmail_service = gmail_service
    
    def process_email(self, msg_id: str, dry_run: bool = False, 
                     open_browser: bool = True) -> bool:
        """Process a single email for unsubscription"""
        message = self.gmail_service.get_email_details(msg_id)
        if not message:
            return False
        
        headers = extract_headers(message)
        if not self._log_email_info(headers):
            return False
        
        list_unsubscribe = headers.get('List-Unsubscribe')
        if not list_unsubscribe:
            logger.warning("no_unsubscribe_header", msg_id=msg_id)
            return False
        
        mailto_links, http_links = parse_list_unsubscribe(list_unsubscribe)
        
        if dry_run:
            self._log_dry_run_info(mailto_links, http_links)
            return True
        
        # Try unsubscription methods
        success = self._attempt_unsubscribe(
            headers, mailto_links, http_links, open_browser
        )
        
        if success:
            self._update_labels(msg_id)
        
        return success
    
    def _log_email_info(self, headers: Dict) -> bool:
        """Log email information"""
        subject = headers.get('Subject', 'No Subject')
        from_addr = headers.get('From', 'Unknown')
        logger.info("processing_email", subject=subject, from_addr=from_addr)
        return True
    
    def _log_dry_run_info(self, mailto_links: List[str], http_links: List[str]):
        """Log dry run information"""
        logger.info("dry_run_unsubscribe", mailto_links=mailto_links, http_links=http_links)
    
    def _attempt_unsubscribe(self, headers: Dict, mailto_links: List[str], 
                           http_links: List[str], open_browser: bool) -> bool:
        """Attempt unsubscription using available methods"""
        has_one_click = 'List-Unsubscribe-Post' in headers
        
        # Try HTTP method first
        if http_links:
            success = self._try_http_unsubscribe(
                http_links, has_one_click, open_browser
            )
            if success:
                return True
        
        # Fall back to email method
        if mailto_links:
            return self._try_email_unsubscribe(mailto_links)
        
        return False
    
    def _try_http_unsubscribe(self, http_links: List[str], 
                            has_one_click: bool, open_browser: bool) -> bool:
        """Try HTTP unsubscription methods"""
        for link in http_links:
            if has_one_click:
                success, needs_browser = self._http_unsubscribe(link, use_post=True)
                if success:
                    return True
                if needs_browser and open_browser:
                    self._open_browser(link)
                    return True
            
            success, needs_browser = self._http_unsubscribe(link, use_post=False)
            if success:
                return True
            if needs_browser and open_browser:
                self._open_browser(link)
                return True
        
        return False
    
    def _try_email_unsubscribe(self, mailto_links: List[str]) -> bool:
        """Try email unsubscription"""
        for link in mailto_links:
            if self._email_unsubscribe(link):
                return True
        return False
    
    def _http_unsubscribe(self, http_link: str, use_post: bool = False) -> Tuple[bool, bool]:
        """Send HTTP unsubscribe request"""
        try:
            response = self._make_http_request(http_link, use_post)
            return self._process_http_response(response, http_link)
        except requests.RequestException as e:
            logger.error("http_request_error", error=str(e), url=http_link)
            return False, False
    
    def _make_http_request(self, url: str, use_post: bool) -> requests.Response:
        """Make HTTP request with appropriate method"""
        headers = {'User-Agent': USER_AGENT}
        
        if use_post:
            return requests.post(
                url,
                headers=headers,
                data={'List-Unsubscribe': 'One-Click'},
                timeout=HTTP_TIMEOUT,
                allow_redirects=True
            )
        else:
            return requests.get(
                url,
                headers=headers,
                timeout=HTTP_TIMEOUT,
                allow_redirects=True
            )
    
    def _process_http_response(self, response: requests.Response, 
                             url: str) -> Tuple[bool, bool]:
        """Process HTTP response and determine success"""
        if response.status_code not in [200, 201, 202, 204]:
            logger.warning("http_unsubscribe_failed", status_code=response.status_code, url=url)
            return False, False
        
        # Check for success indicators
        if check_success_indicators(response.text, SUCCESS_INDICATORS):
            logger.info("http_unsubscribe_success", url=url)
            return True, False
        
        # Check if browser interaction needed
        if self._needs_browser_interaction(response.text):
            logger.info("browser_interaction_required", url=url)
            return False, True
        
        # Assume success for 2xx response
        logger.info("http_request_completed", url=url)
        return True, False
    
    def _needs_browser_interaction(self, html_content: str) -> bool:
        """Check if page requires browser interaction"""
        soup = BeautifulSoup(html_content, 'html.parser')
        forms = soup.find_all('form')
        buttons = soup.find_all(['button', 'input'], type=['submit', 'button'])
        return bool(forms or buttons)
    
    def _email_unsubscribe(self, mailto_link: str) -> bool:
        """Send unsubscribe email"""
        try:
            to_address, subject = parse_mailto_link(mailto_link)
            message = create_unsubscribe_email(to_address, subject)
            
            result = self.gmail_service.send_message(message)
            if result:
                logger.info("email_unsubscribe_sent", to_address=to_address)
                return True
            return False
            
        except Exception as e:
            logger.error("email_unsubscribe_error", error=str(e), mailto_link=mailto_link)
            return False
    
    def _open_browser(self, url: str):
        """Open URL in browser"""
        logger.info("opening_browser", url=url)
        webbrowser.open(url)
    
    def _update_labels(self, msg_id: str):
        """Update email labels after successful unsubscription"""
        self.gmail_service.remove_label_from_message(msg_id, LABEL_PENDING)
        self.gmail_service.add_label_to_message(msg_id, LABEL_UNSUBSCRIBED)
        logger.info("labels_updated", msg_id=msg_id)