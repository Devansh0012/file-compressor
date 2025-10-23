"""Compression API routes."""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pathlib import Path
import json
from typing import Optional

from app.models import CompressionRequest, CompressionResponse, FileType
from app.utils.file_handler import FileHandler
from app.services import ImageCompressor, VideoCompressor, AudioCompressor, DocumentCompressor
from app.config import settings

router = APIRouter(prefix="/compress", tags=["compression"])


@router.post("/", response_model=CompressionResponse)
async def compress_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    compression_data: str = Form(...)
):
    """
    Compress a file based on the specified strategy.
    
    Args:
        file: The file to compress
        compression_data: JSON string containing compression parameters
    
    Returns:
        CompressionResponse with compression details
    """
    try:
        # Parse compression request
        request_data = json.loads(compression_data)
        compression_request = CompressionRequest(**request_data)
        
        # Read file content
        content = await file.read()
        
        # Validate file size
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size is {settings.MAX_FILE_SIZE / (1024*1024)}MB"
            )
        
        # Determine file type
        try:
            file_type, mime_type = FileHandler.get_file_type(file.filename, content)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
        # Generate unique filenames
        input_filename = FileHandler.generate_unique_filename(file.filename)
        output_filename = f"compressed_{input_filename}"
        
        # Save uploaded file
        input_path = FileHandler.save_uploaded_file(
            content,
            input_filename,
            settings.UPLOAD_DIR
        )
        output_path = settings.COMPRESSED_DIR / output_filename
        
        # Get original size
        original_size = FileHandler.get_file_size(input_path)
        
        # Compress based on file type
        try:
            if file_type == FileType.IMAGE:
                compressor = ImageCompressor(input_path, output_path)
            elif file_type == FileType.VIDEO:
                compressor = VideoCompressor(input_path, output_path)
            elif file_type == FileType.AUDIO:
                compressor = AudioCompressor(input_path, output_path)
            elif file_type == FileType.DOCUMENT:
                compressor = DocumentCompressor(input_path, output_path)
            else:
                raise HTTPException(status_code=400, detail="Unsupported file type")
            
            # Perform compression
            compressed_path = compressor.compress(compression_request)
            compressed_size = FileHandler.get_file_size(compressed_path)
            
            # Calculate reduction percentage
            reduction = ((original_size - compressed_size) / original_size) * 100
            
            # Schedule cleanup of input file
            background_tasks.add_task(FileHandler.cleanup_file, input_path)
            
            return CompressionResponse(
                success=True,
                original_size=original_size,
                compressed_size=compressed_size,
                reduction_percentage=round(reduction, 2),
                filename=output_filename,
                download_url=f"/api/compress/download/{output_filename}",
                message="File compressed successfully"
            )
            
        except Exception as e:
            # Cleanup files on error
            FileHandler.cleanup_file(input_path)
            FileHandler.cleanup_file(output_path)
            raise HTTPException(status_code=500, detail=f"Compression failed: {str(e)}")
    
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid compression data format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{filename}")
async def download_file(filename: str, background_tasks: BackgroundTasks):
    """
    Download a compressed file.
    
    Args:
        filename: Name of the file to download
    
    Returns:
        FileResponse with the compressed file
    """
    file_path = settings.COMPRESSED_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Schedule file cleanup after download
    background_tasks.add_task(FileHandler.cleanup_file, file_path)
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )


@router.get("/info")
async def get_info():
    """Get information about supported formats and limits."""
    return {
        "max_file_size_mb": settings.MAX_FILE_SIZE / (1024 * 1024),
        "supported_formats": {
            "images": list(settings.SUPPORTED_IMAGE_FORMATS),
            "videos": list(settings.SUPPORTED_VIDEO_FORMATS),
            "audio": list(settings.SUPPORTED_AUDIO_FORMATS),
            "documents": list(settings.SUPPORTED_DOCUMENT_FORMATS)
        },
        "compression_strategies": ["quality", "target_size", "percentage"]
    }
