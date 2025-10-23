"""Document compression service."""
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
from app.models import CompressionStrategy, CompressionRequest


class DocumentCompressor:
    """Handles document compression."""
    
    def __init__(self, input_path: Path, output_path: Path):
        self.input_path = input_path
        self.output_path = output_path
        self.original_size = input_path.stat().st_size
    
    def compress(self, request: CompressionRequest) -> Path:
        """Compress document based on file type."""
        if self.input_path.suffix.lower() == '.pdf':
            return self._compress_pdf()
        else:
            raise ValueError(f"Unsupported document format: {self.input_path.suffix}")
    
    def _compress_pdf(self) -> Path:
        """Compress PDF by removing redundant data."""
        reader = PdfReader(str(self.input_path))
        writer = PdfWriter()
        
        # Copy all pages
        for page in reader.pages:
            # Compress page content
            page.compress_content_streams()
            writer.add_page(page)
        
        # Remove duplicate images
        writer.add_metadata(reader.metadata)
        
        # Write compressed PDF
        with open(self.output_path, 'wb') as f:
            writer.write(f)
        
        return self.output_path
