"""Audio compression service."""
from pathlib import Path
import ffmpeg
from app.models import CompressionStrategy, CompressionRequest


class AudioCompressor:
    """Handles audio compression using FFmpeg."""
    
    def __init__(self, input_path: Path, output_path: Path):
        self.input_path = input_path
        self.output_path = output_path
        self.original_size = input_path.stat().st_size
    
    def compress(self, request: CompressionRequest) -> Path:
        """Compress audio based on strategy."""
        if request.strategy == CompressionStrategy.QUALITY:
            return self._compress_by_quality(request.quality)
        elif request.strategy == CompressionStrategy.TARGET_SIZE:
            return self._compress_to_target_size(request.target_size_mb)
        elif request.strategy == CompressionStrategy.PERCENTAGE:
            return self._compress_by_percentage(request.reduction_percentage)
        
        raise ValueError(f"Unknown compression strategy: {request.strategy}")
    
    def _compress_by_quality(self, quality: int) -> Path:
        """Compress audio with specified quality."""
        # Map quality (1-100) to bitrate (32k-320k)
        bitrate = int(32 + (quality / 100) * 288)
        bitrate = f"{bitrate}k"
        
        try:
            (
                ffmpeg
                .input(str(self.input_path))
                .output(
                    str(self.output_path),
                    acodec='libmp3lame',
                    audio_bitrate=bitrate
                )
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
        except ffmpeg.Error as e:
            raise RuntimeError(f"FFmpeg error: {e.stderr.decode()}")
        
        return self.output_path
    
    def _compress_to_target_size(self, target_size_mb: float) -> Path:
        """Compress audio to target file size."""
        target_size_bytes = int(target_size_mb * 1024 * 1024)
        
        # Get audio duration
        probe = ffmpeg.probe(str(self.input_path))
        duration = float(probe['format']['duration'])
        
        # Calculate target bitrate
        target_bitrate = int((target_size_bytes * 8) / duration)
        
        # Ensure bitrate is within reasonable range
        if target_bitrate < 32000:  # Minimum 32kbps
            target_bitrate = 32000
        elif target_bitrate > 320000:  # Maximum 320kbps
            target_bitrate = 320000
        
        bitrate = f"{target_bitrate // 1000}k"
        
        try:
            (
                ffmpeg
                .input(str(self.input_path))
                .output(
                    str(self.output_path),
                    acodec='libmp3lame',
                    audio_bitrate=bitrate
                )
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
        except ffmpeg.Error as e:
            raise RuntimeError(f"FFmpeg error: {e.stderr.decode()}")
        
        return self.output_path
    
    def _compress_by_percentage(self, reduction_percentage: int) -> Path:
        """Compress audio by reduction percentage."""
        target_size = self.original_size * (100 - reduction_percentage) / 100
        return self._compress_to_target_size(target_size / (1024 * 1024))
