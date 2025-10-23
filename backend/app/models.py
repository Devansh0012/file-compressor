"""Data models for the application."""
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional


class CompressionStrategy(str, Enum):
    """Compression strategy options."""
    TARGET_SIZE = "target_size"
    PERCENTAGE = "percentage"
    QUALITY = "quality"


class FileType(str, Enum):
    """Supported file types."""
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"


class CompressionRequest(BaseModel):
    """Compression request model."""
    strategy: CompressionStrategy
    target_size_mb: Optional[float] = Field(None, gt=0, description="Target size in MB")
    reduction_percentage: Optional[int] = Field(None, ge=1, le=99, description="Percentage to reduce")
    quality: Optional[int] = Field(None, ge=1, le=100, description="Quality level (1-100)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "strategy": "quality",
                "quality": 75
            }
        }


class FileInfo(BaseModel):
    """File information model."""
    filename: str
    size: int
    file_type: FileType
    mime_type: str


class CompressionResponse(BaseModel):
    """Compression response model."""
    success: bool
    original_size: int
    compressed_size: int
    reduction_percentage: float
    filename: str
    download_url: str
    message: Optional[str] = None
