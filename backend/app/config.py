"""Application configuration."""
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """Application settings."""
    
    # API Settings
    API_TITLE: str = "File Compressor API"
    API_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    # CORS Settings
    ALLOWED_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # File Settings
    MAX_FILE_SIZE: int = 500 * 1024 * 1024  # 500MB
    UPLOAD_DIR: Path = Path("uploads")
    TEMP_DIR: Path = Path("temp")
    COMPRESSED_DIR: Path = Path("compressed")
    
    # Supported file types
    SUPPORTED_IMAGE_FORMATS: set[str] = {"jpg", "jpeg", "png", "gif", "bmp", "webp", "tiff"}
    SUPPORTED_VIDEO_FORMATS: set[str] = {"mp4", "avi", "mov", "mkv", "flv", "wmv", "webm"}
    SUPPORTED_AUDIO_FORMATS: set[str] = {"mp3", "wav", "flac", "aac", "ogg", "m4a"}
    SUPPORTED_DOCUMENT_FORMATS: set[str] = {"pdf", "docx"}
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Create necessary directories
settings.UPLOAD_DIR.mkdir(exist_ok=True)
settings.TEMP_DIR.mkdir(exist_ok=True)
settings.COMPRESSED_DIR.mkdir(exist_ok=True)
