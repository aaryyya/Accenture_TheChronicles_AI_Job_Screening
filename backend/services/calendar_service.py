import os
import pickle
import logging
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API scopes
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

# Get absolute paths to the credential files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDENTIALS_FILE = os.path.join(BASE_DIR, 'credentials.json')
TOKEN_FILE = os.path.join(BASE_DIR, 'token.pickle')

def get_calendar_service():
    """Get authenticated Google Calendar service using OAuth2"""
    creds = None
    
    try:
        logger.info(f"Looking for token file at: {TOKEN_FILE}")
        # Look for existing token
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
            logger.info("Token file found and loaded")
        else:
            logger.warning(f"Token file not found at {TOKEN_FILE}")
        
        # If credentials don't exist or are invalid, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logger.info("Refreshing expired credentials")
                try:
                    creds.refresh(Request())
                except RefreshError as e:
                    logger.error(f"Error refreshing token: {e}")
                    creds = None
            
            # If refresh failed or we don't have credentials, start OAuth flow
            if not creds:
                logger.info(f"Starting new OAuth flow with credentials file: {CREDENTIALS_FILE}")
                if not os.path.exists(CREDENTIALS_FILE):
                    logger.error(f"Credentials file not found at {CREDENTIALS_FILE}")
                    raise FileNotFoundError(f"Credentials file not found at {CREDENTIALS_FILE}")
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, SCOPES)
                # This will print a URL that the user needs to visit
                logger.info("Starting local server for OAuth callback")
                creds = flow.run_local_server(port=0)
                logger.info("Authentication successful!")
            
            # Save the credentials for future use
            logger.info(f"Saving new token to {TOKEN_FILE}")
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)
        
        # Build and return the service
        logger.info("Building Google Calendar service")
        return build('calendar', 'v3', credentials=creds)
        
    except Exception as e:
        logger.error(f"Error in authentication: {e}")
        raise

def schedule_interview(candidate_email: str, interviewer_email: str, start_time: str, end_time: str) -> str:
    """Schedule an interview on Google Calendar and return the event link"""
    try:
        logger.info(f"Scheduling interview for {candidate_email} with {interviewer_email}")
        service = get_calendar_service()

        event = {
            'summary': f'Interview with {candidate_email}',
            'start': {'dateTime': start_time, 'timeZone': 'UTC'},
            'end': {'dateTime': end_time, 'timeZone': 'UTC'},
            'attendees': [
                {'email': candidate_email},
                {'email': interviewer_email},
            ],
        }

        logger.info("Creating calendar event")
        created_event = service.events().insert(calendarId='primary', body=event).execute()
        logger.info(f"Event created successfully: {created_event.get('htmlLink')}")
        return created_event['htmlLink']
    except Exception as e:
        logger.error(f"Error scheduling interview: {e}")
        raise
