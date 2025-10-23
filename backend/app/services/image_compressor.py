"""Image compression service."""
from pathlib import Path
from PIL import Image
import io
from app.models import CompressionStrategy, CompressionRequest


class ImageCompressor:
    """Handles image compression using various strategies."""
    
    def __init__(self, input_path: Path, output_path: Path):
        self.input_path = input_path
        self.output_path = output_path
        self.original_size = input_path.stat().st_size
    
    def compress(self, request: CompressionRequest) -> Path:
        """Compress image based on strategy."""
        img = Image.open(self.input_path)
        
        # Convert RGBA to RGB if saving as JPEG
        if img.mode in ('RGBA', 'LA', 'P') and self.output_path.suffix.lower() in ['.jpg', '.jpeg']:
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = rgb_img
        
        if request.strategy == CompressionStrategy.QUALITY:
            return self._compress_by_quality(img, request.quality)
        elif request.strategy == CompressionStrategy.TARGET_SIZE:
            return self._compress_to_target_size(img, request.target_size_mb)
        elif request.strategy == CompressionStrategy.PERCENTAGE:
            return self._compress_by_percentage(img, request.reduction_percentage)
        
        raise ValueError(f"Unknown compression strategy: {request.strategy}")
    
    def _compress_by_quality(self, img: Image.Image, quality: int) -> Path:
        """Compress image with specified quality."""
        save_params = {
            'optimize': True,
            'quality': quality
        }
        
        if self.output_path.suffix.lower() == '.png':
            # For PNG, use compression level instead of quality
            save_params = {'optimize': True, 'compress_level': 9 - (quality // 11)}
        
        img.save(self.output_path, **save_params)
        return self.output_path
    
    def _compress_to_target_size(self, img: Image.Image, target_size_mb: float) -> Path:
        """Compress image to target file size."""
        target_size_bytes = int(target_size_mb * 1024 * 1024)
        
        # Start with high quality and reduce until target size is reached
        quality = 95
        min_quality = 10
        
        while quality >= min_quality:
            buffer = io.BytesIO()
            temp_img = img.copy()
            
            save_params = {'optimize': True, 'quality': quality}
            if self.output_path.suffix.lower() == '.png':
                save_params = {'optimize': True, 'compress_level': 9}
            
            temp_img.save(buffer, format=img.format or 'JPEG', **save_params)
            size = buffer.tell()
            
            if size <= target_size_bytes:
                with open(self.output_path, 'wb') as f:
                    f.write(buffer.getvalue())
                return self.output_path
            
            quality -= 5
        
        # If still too large, resize the image
        return self._resize_and_compress(img, target_size_bytes)
    
    def _compress_by_percentage(self, img: Image.Image, reduction_percentage: int) -> Path:
        """Compress image by reduction percentage."""
        target_size = self.original_size * (100 - reduction_percentage) / 100
        return self._compress_to_target_size(img, target_size / (1024 * 1024))
    
    def _resize_and_compress(self, img: Image.Image, target_size_bytes: int) -> Path:
        """Resize image and compress to reach target size."""
        scale_factor = 0.9
        current_img = img.copy()
        
        while True:
            new_size = (int(current_img.width * scale_factor), int(current_img.height * scale_factor))
            resized_img = current_img.resize(new_size, Image.Resampling.LANCZOS)
            
            buffer = io.BytesIO()
            save_params = {'optimize': True, 'quality': 85}
            if self.output_path.suffix.lower() == '.png':
                save_params = {'optimize': True, 'compress_level': 9}
            
            resized_img.save(buffer, format=img.format or 'JPEG', **save_params)
            
            if buffer.tell() <= target_size_bytes or new_size[0] < 100:
                with open(self.output_path, 'wb') as f:
                    f.write(buffer.getvalue())
                return self.output_path
            
            current_img = resized_img
