"""
Google Drive Authentication Handler

Handles OAuth 2.0 authentication flow for Google Drive API.
Manages token storage and refresh.
"""

import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

class DriveAuthHandler:
    """Handles Google Drive API authentication"""
    
    def __init__(self, credentials_file='credentials.json', token_file='token.json'):
        """
        Initialize the authentication handler.
        
        Args:
            credentials_file: Path to OAuth 2.0 credentials JSON file
            token_file: Path to store/load user access token
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.creds = None
        
    def authenticate(self):
        """
        Authenticate with Google Drive API.
        
        Returns:
            Google Drive API service object
            
        Raises:
            FileNotFoundError: If credentials.json is not found
        """
        # Check if credentials file exists
        if not os.path.exists(self.credentials_file):
            raise FileNotFoundError(
                f"Credentials file '{self.credentials_file}' not found.\n"
                "Please download OAuth 2.0 credentials from Google Cloud Console.\n"
                "See README.md for setup instructions."
            )
        
        # Load existing token if available
        if os.path.exists(self.token_file):
            self.creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
        
        # If no valid credentials, let user log in
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                print("Refreshing access token...")
                self.creds.refresh(Request())
            else:
                print("Opening browser for authentication...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(self.token_file, 'w') as token:
                token.write(self.creds.to_json())
            print(f"Authentication successful! Token saved to {self.token_file}")
        
        # Build and return the service
        service = build('drive', 'v3', credentials=self.creds)
        return service
    
    def revoke_credentials(self):
        """Revoke and delete stored credentials"""
        if os.path.exists(self.token_file):
            os.remove(self.token_file)
            print(f"Deleted {self.token_file}")
        print("Credentials revoked. Run the app again to re-authenticate.")
