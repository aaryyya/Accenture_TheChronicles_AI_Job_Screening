# backend/routes/upload_routes.py
from fastapi import APIRouter, UploadFile, File
from typing import List

router = APIRouter()

@router.post("/upload-cvfolder")
async def upload_cvfolder(files: List[UploadFile] = File(...)):
    """
    Accept multiple uploaded files and process them.
    """
    # For demonstration, just collect file names and count them
    file_names = [file.filename for file in files]
    file_count = len(files)

    # Print them on the server console/log, or do any processing you want
    print("Received files:")
    for name in file_names:
        print(name)
    print(f"Total files: {file_count}")

    # Return a response to the client
    return {
        "message": "Files received successfully",
        "file_count": file_count,
        "files": file_names
    }
