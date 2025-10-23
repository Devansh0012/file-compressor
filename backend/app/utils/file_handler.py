"""File handling utilities."""
import os
import uuid
from pathlib import Path
from typing import Tuple
try:
    import magic
except ImportError:
    magic = None
from app.models import FileType
from app.config import settings


class FileHandler:
    """Handles file operations and validation."""
    
    @staticmethod
    def get_file_type(filename: str, content: bytes) -> Tuple[FileType, str]:
        """Determine file type from content and extension."""
        extension = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        
        # Try to get MIME type if magic is available
        mime = 'application/octet-stream'
        if magic is not None:
            try:
                mime = magic.from_buffer(content, mime=True)
            except:
                pass
        
        # Determine file type primarily by extension
        if extension in settings.SUPPORTED_IMAGE_FORMATS:
            return FileType.IMAGE, mime if mime.startswith('image/') else f'image/{extension}'
        elif extension in settings.SUPPORTED_VIDEO_FORMATS:
            return FileType.VIDEO, mime if mime.startswith('video/') else f'video/{extension}'
        elif extension in settings.SUPPORTED_AUDIO_FORMATS:
            return FileType.AUDIO, mime if mime.startswith('audio/') else f'audio/{extension}'
        elif extension in settings.SUPPORTED_DOCUMENT_FORMATS:
            return FileType.DOCUMENT, mime if 'pdf' in mime or 'word' in mime else f'application/{extension}'
        else:
            raise ValueError(f"Unsupported file type: {extension}")
    
    @staticmethod
    def generate_unique_filename(original_filename: str) -> str:
        """Generate a unique filename while preserving extension."""
        name, ext = os.path.splitext(original_filename)
        unique_id = str(uuid.uuid4())[:8]
        return f"{name}_{unique_id}{ext}"
    
    @staticmethod
    def save_uploaded_file(content: bytes, filename: str, directory: Path) -> Path:
        """Save uploaded file to specified directory."""
        filepath = directory / filename
        with open(filepath, 'wb') as f:
            f.write(content)
        return filepath
    
    @staticmethod
    def get_file_size(filepath: Path) -> int:
        """Get file size in bytes."""
        return filepath.stat().st_size
    
    @staticmethod
    def cleanup_file(filepath: Path) -> None:
        """Remove file if it exists."""
        if filepath.exists():
            filepath.unlink()
