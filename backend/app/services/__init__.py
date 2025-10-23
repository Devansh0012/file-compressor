"""Compression services package."""
from .image_compressor import ImageCompressor
from .video_compressor import VideoCompressor
from .audio_compressor import AudioCompressor
from .document_compressor import DocumentCompressor

__all__ = ['ImageCompressor', 'VideoCompressor', 'AudioCompressor', 'DocumentCompressor']
