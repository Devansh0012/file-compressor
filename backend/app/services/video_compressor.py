"""Video compression service."""
from pathlib import Path
import ffmpeg
from app.models import CompressionStrategy, CompressionRequest


class VideoCompressor:
    """Handles video compression using FFmpeg."""
    
    def __init__(self, input_path: Path, output_path: Path):
        self.input_path = input_path
        self.output_path = output_path
        self.original_size = input_path.stat().st_size
    
    def compress(self, request: CompressionRequest) -> Path:
        """Compress video based on strategy."""
        if request.strategy == CompressionStrategy.QUALITY:
            return self._compress_by_quality(request.quality)
        elif request.strategy == CompressionStrategy.TARGET_SIZE:
            return self._compress_to_target_size(request.target_size_mb)
        elif request.strategy == CompressionStrategy.PERCENTAGE:
            return self._compress_by_percentage(request.reduction_percentage)
        
        raise ValueError(f"Unknown compression strategy: {request.strategy}")
    
    def _compress_by_quality(self, quality: int) -> Path:
        """Compress video with specified quality using CRF."""
        # CRF scale: 0-51, where 0 is lossless and 51 is worst quality
        # Convert quality (1-100) to CRF (51-18)
        crf = int(51 - (quality / 100) * 33)
        
        try:
            (
                ffmpeg
                .input(str(self.input_path))
                .output(
                    str(self.output_path),
                    vcodec='libx264',
                    crf=crf,
                    preset='medium',
                    acodec='aac',
                    audio_bitrate='128k'
                )
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
        except ffmpeg.Error as e:
            raise RuntimeError(f"FFmpeg error: {e.stderr.decode()}")
        
        return self.output_path
    
    def _compress_to_target_size(self, target_size_mb: float) -> Path:
        """Compress video to target file size."""
        target_size_bytes = int(target_size_mb * 1024 * 1024)
        
        # Get video duration
        probe = ffmpeg.probe(str(self.input_path))
        duration = float(probe['format']['duration'])
        
        # Calculate target bitrate (accounting for audio)
        audio_bitrate = 128 * 1024  # 128 kbps
        target_total_bitrate = (target_size_bytes * 8) / duration
        video_bitrate = int(target_total_bitrate - audio_bitrate)
        
        if video_bitrate < 100000:  # Minimum 100kbps
            video_bitrate = 100000
        
        try:
            (
                ffmpeg
                .input(str(self.input_path))
                .output(
                    str(self.output_path),
                    vcodec='libx264',
                    video_bitrate=video_bitrate,
                    preset='medium',
                    acodec='aac',
                    audio_bitrate='128k',
                    maxrate=video_bitrate,
                    bufsize=video_bitrate * 2
                )
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
        except ffmpeg.Error as e:
            raise RuntimeError(f"FFmpeg error: {e.stderr.decode()}")
        
        return self.output_path
    
    def _compress_by_percentage(self, reduction_percentage: int) -> Path:
        """Compress video by reduction percentage."""
        target_size = self.original_size * (100 - reduction_percentage) / 100
        return self._compress_to_target_size(target_size / (1024 * 1024))
