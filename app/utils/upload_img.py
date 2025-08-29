import cloudinary
import cloudinary.uploader
import cloudinary.api
from fastapi import HTTPException, UploadFile
from typing import List, Optional
import logging
import os
from urllib.parse import urlparse

from app.configs.setting import setting

logger = logging.getLogger(__name__)


class CloudinaryService:
    def __init__(self):
        """Initialize Cloudinary with CLOUDINARY_URL"""
        if not setting.CLOUDINARY_URL:
            raise ValueError("CLOUDINARY_URL is not configured")
        
        # Parse CLOUDINARY_URL and configure
        # Format: cloudinary://api_key:api_secret@cloud_name
        parsed = urlparse(setting.CLOUDINARY_URL)
        
        cloudinary.config(
            cloud_name=parsed.hostname,
            api_key=parsed.username,
            api_secret=parsed.password,
            secure=True
        )
        
        logger.info("Cloudinary configured successfully")
    
    async def upload_image(
        self, 
        file: UploadFile, 
        folder: str = "demarthology",
        max_size_mb: int = 5
    ) -> dict:
        """
        Upload single image to Cloudinary
        
        Args:
            file: FastAPI UploadFile object
            folder: Cloudinary folder name
            max_size_mb: Maximum file size in MB
            
        Returns:
            dict: Contains url, public_id, and other metadata
        """
        try:
            # Validate file type
            if not file.content_type or not file.content_type.startswith('image/'):
                raise HTTPException(
                    status_code=400, 
                    detail="File must be an image"
                )
            
            # Read file content
            content = await file.read()
            
            # Validate file size
            if len(content) > max_size_mb * 1024 * 1024:
                raise HTTPException(
                    status_code=400,
                    detail=f"File size must be less than {max_size_mb}MB"
                )
            
            # Reset file pointer and upload
            await file.seek(0)
            
            result = cloudinary.uploader.upload(
                file.file,
                folder=folder,
                resource_type="image",
                transformation=[
                    {"quality": "auto:good"},
                    {"fetch_format": "auto"}
                ]
            )
            
            return {
                "url": result["secure_url"],
                "public_id": result["public_id"],
                "width": result.get("width"),
                "height": result.get("height"),
                "format": result.get("format"),
                "size": result.get("bytes")
            }
            
        except Exception as e:
            logger.error(f"Failed to upload image: {str(e)}")
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(
                status_code=500,
                detail="Failed to upload image"
            )
    
    async def upload_multiple_images(
        self, 
        files: List[UploadFile], 
        folder: str = "demarthology"
    ) -> List[dict]:
        """Upload multiple images"""
        results = []
        
        for file in files:
            try:
                result = await self.upload_image(file, folder)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to upload {file.filename}: {str(e)}")
                # Continue with other files
                continue
        
        return results
    
    def delete_image(self, public_id: str) -> bool:
        """Delete image from Cloudinary"""
        try:
            result = cloudinary.uploader.destroy(public_id)
            return result.get("result") == "ok"
        except Exception as e:
            logger.error(f"Failed to delete image {public_id}: {str(e)}")
            return False
    
    def get_image_url(self, public_id: str, transformation: Optional[dict] = None) -> str:
        """Get optimized image URL with transformations"""
        try:
            if transformation:
                return cloudinary.CloudinaryImage(public_id).build_url(**transformation)
            return cloudinary.CloudinaryImage(public_id).build_url()
        except Exception as e:
            logger.error(f"Failed to build URL for {public_id}: {str(e)}")
            return ""


# Create singleton instance
cloudinary_service = CloudinaryService()
