"""OAuth2 authentication module for YouTube API access."""

import json
import os
from pathlib import Path
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class AuthenticationError(Exception):
    """Authentication-related errors."""

    pass


class YouTubeAuthenticator:
    """Handles OAuth2 authentication flow for YouTube API access."""

    def __init__(
        self,
        credentials_file: str = "client_secrets.json",
        token_file: str = "token.json",
    ):
        """Initialize the authenticator.

        Args:
            credentials_file: Path to the OAuth2 client secrets file
            token_file: Path to store the access token
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.scopes = ["https://www.googleapis.com/auth/youtube"]

    def get_authenticated_service(self):
        """Returns authenticated YouTube service object.

        Returns:
            googleapiclient.discovery.Resource: Authenticated YouTube API service

        Raises:
            AuthenticationError: If authentication fails
        """
        try:
            credentials = self._get_valid_credentials()
            service = build("youtube", "v3", credentials=credentials)
            return service
        except Exception as e:
            raise AuthenticationError(f"Failed to authenticate: {str(e)}") from e

    def _get_valid_credentials(self) -> Credentials:
        """Get valid credentials, refreshing or re-authenticating as needed.

        Returns:
            google.oauth2.credentials.Credentials: Valid credentials

        Raises:
            AuthenticationError: If credentials cannot be obtained
        """
        credentials = self._load_credentials()

        if credentials and credentials.valid:
            return credentials

        if credentials and credentials.expired and credentials.refresh_token:
            try:
                credentials.refresh(Request())
                self._save_credentials(credentials)
                return credentials
            except Exception as e:
                # If refresh fails, we'll need to re-authenticate
                print(f"Token refresh failed: {e}")

        # Need to run OAuth flow
        credentials = self._run_oauth_flow()
        self._save_credentials(credentials)
        return credentials

    def _load_credentials(self) -> Optional[Credentials]:
        """Load existing credentials from token file.

        Returns:
            google.oauth2.credentials.Credentials or None: Loaded credentials if available
        """
        if not os.path.exists(self.token_file):
            return None

        try:
            return Credentials.from_authorized_user_file(self.token_file, self.scopes)
        except Exception as e:
            print(f"Warning: Could not load existing credentials: {e}")
            return None

    def _save_credentials(self, credentials: Credentials) -> None:
        """Save credentials to token file.

        Args:
            credentials: The credentials to save

        Raises:
            AuthenticationError: If credentials cannot be saved
        """
        try:
            # Ensure the directory exists
            token_path = Path(self.token_file)
            token_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.token_file, "w") as token:
                token.write(credentials.to_json())
        except Exception as e:
            raise AuthenticationError(f"Failed to save credentials: {str(e)}") from e

    def _run_oauth_flow(self) -> Credentials:
        """Run OAuth2 flow for new credentials.

        Returns:
            google.oauth2.credentials.Credentials: New credentials from OAuth flow

        Raises:
            AuthenticationError: If OAuth flow fails
        """
        if not os.path.exists(self.credentials_file):
            raise AuthenticationError(
                f"Client secrets file not found: {self.credentials_file}\n\n"
                "To set up authentication:\n"
                "1. Go to https://console.cloud.google.com/\n"
                "2. Select your project or create a new one\n"
                "3. Enable the YouTube Data API v3:\n"
                "   - Go to 'APIs & Services' > 'Library'\n"
                "   - Search for 'YouTube Data API v3'\n"
                "   - Click 'Enable'\n"
                "4. Create OAuth2 credentials:\n"
                "   - Go to 'APIs & Services' > 'Credentials'\n"
                "   - Click 'Create Credentials' > 'OAuth client ID'\n"
                "   - Choose 'Desktop application'\n"
                "   - Download the JSON file\n"
                "5. Save the downloaded file as 'client_secrets.json' in the current directory\n\n"
                "For more help, see: https://developers.google.com/youtube/v3/quickstart/python"
            )

        # Validate the client secrets file format
        try:
            with open(self.credentials_file, "r") as f:
                import json

                secrets_data = json.load(f)

            if "installed" not in secrets_data and "web" not in secrets_data:
                raise AuthenticationError(
                    f"Invalid client secrets file format: {self.credentials_file}\n"
                    "The file should contain either 'installed' or 'web' credentials.\n"
                    "Please download a new client secrets file from the Google Cloud Console."
                )

        except json.JSONDecodeError as e:
            raise AuthenticationError(
                f"Invalid JSON in client secrets file: {self.credentials_file}\n"
                f"JSON error: {e}\n"
                "Please download a new client secrets file from the Google Cloud Console."
            ) from e
        except IOError as e:
            raise AuthenticationError(
                f"Cannot read client secrets file: {self.credentials_file}\n"
                f"Error: {e}"
            ) from e

        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                self.credentials_file, self.scopes
            )

            print("Opening browser for authentication...")
            print(
                "If the browser doesn't open automatically, copy and paste the URL from the console."
            )

            credentials = flow.run_local_server(port=0)
            return credentials

        except Exception as e:
            error_msg = str(e).lower()

            if "invalid_client" in error_msg:
                raise AuthenticationError(
                    f"Invalid client credentials in {self.credentials_file}\n"
                    "This usually means:\n"
                    "1. The client secrets file is corrupted or invalid\n"
                    "2. The OAuth2 client has been deleted or disabled\n"
                    "3. The client ID/secret don't match\n\n"
                    "Please create new OAuth2 credentials in the Google Cloud Console."
                ) from e
            elif "redirect_uri_mismatch" in error_msg:
                raise AuthenticationError(
                    "OAuth2 redirect URI mismatch.\n"
                    "This usually happens with web application credentials.\n"
                    "Please ensure you're using 'Desktop application' credentials."
                ) from e
            elif "access_denied" in error_msg:
                raise AuthenticationError(
                    "Authentication was denied or cancelled.\n"
                    "Please complete the authorization process in your browser."
                ) from e
            elif "network" in error_msg or "connection" in error_msg:
                raise AuthenticationError(
                    f"Network error during authentication: {e}\n"
                    "Please check your internet connection and try again."
                ) from e
            else:
                raise AuthenticationError(
                    f"OAuth2 flow failed: {str(e)}\n\n"
                    "Troubleshooting steps:\n"
                    "1. Ensure your client_secrets.json file is valid\n"
                    "2. Check your internet connectivity\n"
                    "3. Complete the authorization in your browser\n"
                    "4. Make sure you're using 'Desktop application' credentials\n"
                    "5. Try creating new OAuth2 credentials if the problem persists"
                ) from e
