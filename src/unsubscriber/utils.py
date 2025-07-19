"""
Utility functions for Gmail Unsubscriber
"""

import re
import base64
from typing import Dict, List, Tuple
from urllib.parse import unquote
from email.mime.text import MIMEText


def extract_headers(message: Dict) -> Dict[str, str]:
    """Extract headers from email message"""
    headers = {}
    if 'payload' in message and 'headers' in message['payload']:
        for header in message['payload']['headers']:
            headers[header['name']] = header['value']
    return headers


def parse_list_unsubscribe(header_value: str) -> Tuple[List[str], List[str]]:
    """Parse List-Unsubscribe header to extract mailto and http links"""
    mailto_links = []
    http_links = []
    
    # Extract all URLs within angle brackets
    urls = re.findall(r'<([^>]+)>', header_value)
    
    for url in urls:
        if url.startswith('mailto:'):
            mailto_links.append(url)
        elif url.startswith(('http://', 'https://')):
            http_links.append(url)
    
    return mailto_links, http_links


def parse_mailto_link(mailto_link: str) -> Tuple[str, str]:
    """Parse mailto link and extract email and subject"""
    match = re.match(r'mailto:([^?]+)(?:\?(.*))?', mailto_link)
    if not match:
        raise ValueError(f"Invalid mailto link: {mailto_link}")
    
    to_address = match.group(1)
    params = match.group(2) or ''
    
    # Parse subject from params
    subject = 'unsubscribe'
    if 'subject=' in params:
        subject_match = re.search(r'subject=([^&]+)', params)
        if subject_match:
            subject = unquote(subject_match.group(1))
    
    return to_address, subject


def create_unsubscribe_email(to_address: str, subject: str) -> Dict:
    """Create unsubscribe email message"""
    message = MIMEText('Please unsubscribe me from this mailing list.')
    message['to'] = to_address
    message['from'] = 'me'
    message['subject'] = subject
    
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}


def check_success_indicators(content: str, indicators: List[str]) -> bool:
    """Check if content contains success indicators"""
    content_lower = content.lower()
    return any(indicator in content_lower for indicator in indicators)