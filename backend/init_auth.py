"""
Initialization script for Google Calendar authentication.
Run this script before starting the FastAPI server to authenticate with Google Calendar.
"""

import os
import logging
from services.calendar_service import get_calendar_service, TOKEN_FILE, CREDENTIALS_FILE

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_auth():
    """Initialize Google Calendar authentication"""
    print("=" * 80)
    print("Google Calendar Authentication Setup")
    print("=" * 80)
    
    # Check if credentials file exists
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"ERROR: Credentials file not found at {CREDENTIALS_FILE}")
        print("Please make sure you have a valid Google API credentials.json file.")
        return False
    
    print(f"Using credentials file: {CREDENTIALS_FILE}")
    print(f"Token will be saved to: {TOKEN_FILE}")
    print("\nA browser window will open. Please log in to your Google account and grant access.")
    print("If no browser opens, check the terminal for a URL to visit.")
    
    try:
        # This will trigger the OAuth2 flow and save the token
        service = get_calendar_service()
        
        if os.path.exists(TOKEN_FILE):
            print("\n✅ Authentication successful!")
            print(f"✅ Token saved to {TOKEN_FILE}")
            print("\nYou can now start the FastAPI server.")
            return True
        else:
            print("\n❌ Authentication failed: Token file was not created.")
            return False
    except Exception as e:
        print(f"\n❌ Authentication failed: {str(e)}")
        return False

if __name__ == "__main__":
    initialize_auth()
