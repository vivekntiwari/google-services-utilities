"""
Google Photos Authentication Handler

Handles OAuth2 authentication for Google Photos Library API.
Similar to DriveAuthHandler but uses Photos API scopes.
"""

import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class PhotosAuthHandler:
    """Handles authentication for Google Photos API"""
    
    # Scopes for Google Photos API - read-only access
    SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']
    
    def __init__(self, credentials_file='photos_credentials.json', token_file='photos_token.json'):
        """
        Initialize the authentication handler.
        
        Args:
            credentials_file: Path to OAuth credentials JSON file
            token_file: Path to store/load authentication token
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.creds = None
    
    def authenticate(self):
        """
        Authenticate with Google Photos API using OAuth2.
        
        Returns:
            Authenticated Google Photos API service object
            
        Raises:
            FileNotFoundError: If credentials file is not found
        """
        # Check if credentials file exists
        if not os.path.exists(self.credentials_file):
            raise FileNotFoundError(
                f"Credentials file '{self.credentials_file}' not found.\n"
                f"Please download OAuth credentials from Google Cloud Console:\n"
                f"1. Go to https://console.cloud.google.com/\n"
                f"2. Enable Google Photos Library API\n"
                f"3. Create OAuth 2.0 credentials\n"
                f"4. Download and save as '{self.credentials_file}'"
            )
        
        # Load existing token if available
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                self.creds = pickle.load(token)
        
        # If no valid credentials, authenticate
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                # Refresh expired token
                print("🔄 Refreshing authentication token...")
                self.creds.refresh(Request())
            else:
                # Run OAuth flow
                print("🔐 Starting OAuth authentication...")
                print("   A browser window will open for authentication.")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            # Save credentials for future use
            with open(self.token_file, 'wb') as token:
                pickle.dump(self.creds, token)
            print("✅ Authentication successful!")
        
        # Build and return the service
        service = build('photoslibrary', 'v1', credentials=self.creds, static_discovery=False)
        return service
    
    def revoke_credentials(self):
        """Revoke and delete stored credentials"""
        if os.path.exists(self.token_file):
            os.remove(self.token_file)
            print(f"🗑️  Deleted token file: {self.token_file}")
        else:
            print("No token file to delete")
