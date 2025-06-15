# utils.py
import re
import cloudinary
import cloudinary.uploader
from fastapi import HTTPException, UploadFile
from ..config import settings
import os
from pathlib import Path

def sanitize_filename(name: str) -> str:
    return re.sub(r'[^a-zA-Z0-9_-]', '', name)[:50]

async def upload_to_cloud(file: UploadFile, identifier: str) -> str:
    """Upload file to Cloudinary with enhanced error handling"""
    # Configure Cloudinary if credentials exist
    if all([
        settings.CLOUDINARY_CLOUD_NAME,
        settings.CLOUDINARY_API_KEY,
        settings.CLOUDINARY_API_SECRET
    ]):
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
            secure=True
        )
        
        try:
            # Read file content
            file_content = await file.read()
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                file_content,
                folder=settings.CLOUDINARY_FOLDER,
                public_id=identifier,
                overwrite=True,
                resource_type="image"
            )
            return result.get('secure_url', '')
        except cloudinary.exceptions.Error as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Cloudinary upload failed: {str(e)}"
            )
        finally:
            await file.seek(0)  # Reset file pointer
    
    # Fallback to local storage
    return await save_file_locally(file, identifier)

async def save_file_locally(file: UploadFile, identifier: str) -> str:
    """Save file to local storage as fallback"""
    try:
        upload_dir = Path("static/uploads")
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_path = upload_dir / f"{identifier}.jpg"
        
        # Save file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return f"/uploads/{identifier}.jpg"
    except IOError as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Local file save failed: {str(e)}"
        )