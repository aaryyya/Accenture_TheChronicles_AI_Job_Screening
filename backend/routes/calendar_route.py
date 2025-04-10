from fastapi import APIRouter, HTTPException, Response, status
from pydantic import BaseModel
from services.calendar_service import schedule_interview, get_calendar_service
import os
import logging

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

class InterviewRequest(BaseModel):
    candidate_email: str
    interviewer_email: str
    start_time: str
    end_time: str

@router.get("/auth-status")
async def check_auth_status():
    """Check if we have valid authentication for Google Calendar"""
    try:
        # Use the base directory from the calendar service
        from services.calendar_service import TOKEN_FILE
        
        if os.path.exists(TOKEN_FILE):
            logger.info(f"Auth status check: Token file found at {TOKEN_FILE}")
            return {
                "authenticated": True, 
                "message": "Calendar authentication is ready",
                "token_path": TOKEN_FILE
            }
        else:
            logger.warning(f"Auth status check: Token file not found at {TOKEN_FILE}")
            return {
                "authenticated": False, 
                "message": "Authentication required. Please use the /auth endpoint.",
                "token_path": TOKEN_FILE
            }
    except Exception as e:
        logger.error(f"Error checking auth status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking authentication status: {str(e)}"
        )

@router.post("/schedule-interview/")
async def schedule(request: InterviewRequest):
    try:
        # Check if we have valid authentication
        from services.calendar_service import TOKEN_FILE
        
        if not os.path.exists(TOKEN_FILE):
            logger.warning(f"Schedule interview: Token file not found at {TOKEN_FILE}")
            return Response(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                content="Calendar authentication required. Please authenticate first using the /auth endpoint."
            )
            
        logger.info(f"Scheduling interview for {request.candidate_email} with {request.interviewer_email}")
        link = schedule_interview(
            request.candidate_email,
            request.interviewer_email,
            request.start_time,
            request.end_time
        )
        logger.info(f"Interview scheduled successfully, calendar link: {link}")
        return {"calendar_link": link}
    except Exception as e:
        logger.error(f"Error scheduling interview: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error scheduling interview: {str(e)}"
        )

@router.get("/auth")
async def authenticate():
    """Force authentication flow. This will create the token.pickle file."""
    try:
        # This will trigger the authentication flow if needed
        logger.info("Starting Google Calendar authentication flow")
        service = get_calendar_service()
        logger.info("Authentication completed successfully")
        return {"status": "success", "message": "Authentication completed successfully"}
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication error: {str(e)}"
        )
