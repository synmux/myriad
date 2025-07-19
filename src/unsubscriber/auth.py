"""
Gmail authentication module
"""

import os
import pickle
import structlog
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from .config import GMAIL_SCOPES, DEFAULT_CREDENTIALS_FILE, DEFAULT_TOKEN_FILE

logger = structlog.get_logger()


class GmailAuthenticator:
    """Handles Gmail API authentication"""
    
    def __init__(self, credentials_file: str = DEFAULT_CREDENTIALS_FILE):
        self.credentials_file = credentials_file
        self.token_file = DEFAULT_TOKEN_FILE
        self.creds = None
        self.service = None
    
    def authenticate(self):
        """Authenticate with Gmail API and return service object"""
        self.creds = self._get_credentials()
        self.service = build('gmail', 'v1', credentials=self.creds, cache_discovery=False)
        logger.info("gmail_auth_success", status="authenticated")
        return self.service
    
    def create_service(self):
        """Create a new service instance using existing credentials"""
        if not self.creds:
            self.creds = self._get_credentials()
        return build('gmail', 'v1', credentials=self.creds, cache_discovery=False)
    
    def get_credentials(self):
        """Get the current credentials object"""
        if not self.creds:
            self.creds = self._get_credentials()
        return self.creds
    
    def _get_credentials(self) -> Credentials:
        """Get or refresh credentials"""
        creds = self._load_token()
        
        if not creds or not creds.valid:
            creds = self._refresh_or_authorize(creds)
            self._save_token(creds)
        
        return creds
    
    def _load_token(self) -> Optional[Credentials]:
        """Load saved token from file"""
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                return pickle.load(token)
        return None
    
    def _save_token(self, creds: Credentials):
        """Save credentials to token file"""
        with open(self.token_file, 'wb') as token:
            pickle.dump(creds, token)
    
    def _refresh_or_authorize(self, creds: Optional[Credentials]) -> Credentials:
        """Refresh expired credentials or authorize new ones"""
        if creds and creds.expired and creds.refresh_token:
            return self._refresh_token(creds)
        else:
            return self._authorize_new()
    
    def _refresh_token(self, creds: Credentials) -> Credentials:
        """Refresh expired token"""
        creds.refresh(Request())
        return creds
    
    def _authorize_new(self) -> Credentials:
        """Authorize new credentials via OAuth flow"""
        if not os.path.exists(self.credentials_file):
            raise FileNotFoundError(
                f"Credentials file '{self.credentials_file}' not found. "
                "Please download it from Google Cloud Console."
            )
        
        flow = InstalledAppFlow.from_client_secrets_file(
            self.credentials_file, GMAIL_SCOPES
        )
        creds = flow.run_local_server(port=0)
        return creds