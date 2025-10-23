#!/usr/bin/env python3
"""
Example Python Script: Using the File Compressor API

This script demonstrates how to use the File Compressor API programmatically.

Prerequisites:
    pip install requests

Usage:
    python python_example.py
"""

import requests
import json
from pathlib import Path


class FileCompressorClient:
    """Client for the File Compressor API."""
    
    def __init__(self, base_url="http://localhost:8000/api"):
        self.base_url = base_url
    
    def get_info(self):
        """Get API information and supported formats."""
        response = requests.get(f"{self.base_url}/compress/info")
        response.raise_for_status()
        return response.json()
    
    def compress_file(self, file_path, strategy, **kwargs):
        """
        Compress a file using specified strategy.
        
        Args:
            file_path: Path to file to compress
            strategy: Compression strategy ('quality', 'target_size', 'percentage')
            **kwargs: Strategy-specific parameters
                - quality: int (1-100) for quality strategy
                - target_size_mb: float for target_size strategy
                - reduction_percentage: int (1-99) for percentage strategy
        
        Returns:
            dict: Compression result with download URL
        """
        # Prepare compression data
        compression_data = {"strategy": strategy}
        compression_data.update(kwargs)
        
        # Prepare request
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {'compression_data': json.dumps(compression_data)}
            
            # Make request
            response = requests.post(
                f"{self.base_url}/compress/",
                files=files,
                data=data
            )
            response.raise_for_status()
            
        return response.json()
    
    def download_file(self, download_url, output_path):
        """
        Download a compressed file.
        
        Args:
            download_url: URL returned from compress_file
            output_path: Path where to save the file
        """
        # Download file
        full_url = f"http://localhost:8000{download_url}"
        response = requests.get(full_url)
        response.raise_for_status()
        
        # Save file
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"File saved to: {output_path}")


def example_compress_image_quality():
    """Example: Compress image with quality strategy."""
    print("\n=== Example 1: Compress Image by Quality ===")
    
    client = FileCompressorClient()
    
    # Compress with quality 75
    result = client.compress_file(
        file_path="sample_image.jpg",
        strategy="quality",
        quality=75
    )
    
    print(f"Original size: {result['original_size'] / 1024:.2f} KB")
    print(f"Compressed size: {result['compressed_size'] / 1024:.2f} KB")
    print(f"Reduction: {result['reduction_percentage']:.2f}%")
    
    # Download compressed file
    client.download_file(result['download_url'], "compressed_image.jpg")


def example_compress_video_target_size():
    """Example: Compress video to target size."""
    print("\n=== Example 2: Compress Video to Target Size ===")
    
    client = FileCompressorClient()
    
    # Compress to 10MB
    result = client.compress_file(
        file_path="sample_video.mp4",
        strategy="target_size",
        target_size_mb=10.0
    )
    
    print(f"Original size: {result['original_size'] / (1024*1024):.2f} MB")
    print(f"Compressed size: {result['compressed_size'] / (1024*1024):.2f} MB")
    print(f"Reduction: {result['reduction_percentage']:.2f}%")
    
    client.download_file(result['download_url'], "compressed_video.mp4")


def example_compress_audio_percentage():
    """Example: Compress audio by percentage."""
    print("\n=== Example 3: Compress Audio by Percentage ===")
    
    client = FileCompressorClient()
    
    # Reduce by 50%
    result = client.compress_file(
        file_path="sample_audio.mp3",
        strategy="percentage",
        reduction_percentage=50
    )
    
    print(f"Original size: {result['original_size'] / (1024*1024):.2f} MB")
    print(f"Compressed size: {result['compressed_size'] / (1024*1024):.2f} MB")
    print(f"Reduction: {result['reduction_percentage']:.2f}%")
    
    client.download_file(result['download_url'], "compressed_audio.mp3")


def example_batch_compress():
    """Example: Batch compress multiple files."""
    print("\n=== Example 4: Batch Compress Multiple Files ===")
    
    client = FileCompressorClient()
    
    files_to_compress = [
        ("image1.jpg", "quality", {"quality": 80}),
        ("image2.png", "quality", {"quality": 75}),
        ("video.mp4", "target_size", {"target_size_mb": 5.0}),
    ]
    
    results = []
    for file_path, strategy, params in files_to_compress:
        try:
            result = client.compress_file(file_path, strategy, **params)
            results.append({
                'file': file_path,
                'success': True,
                'reduction': result['reduction_percentage']
            })
            
            # Download with prefix
            output_name = f"compressed_{Path(file_path).name}"
            client.download_file(result['download_url'], output_name)
            
        except Exception as e:
            results.append({
                'file': file_path,
                'success': False,
                'error': str(e)
            })
    
    # Print summary
    print("\nBatch Compression Summary:")
    for r in results:
        if r['success']:
            print(f"✅ {r['file']}: {r['reduction']:.2f}% reduction")
        else:
            print(f"❌ {r['file']}: {r['error']}")


def example_get_api_info():
    """Example: Get API information."""
    print("\n=== Example 5: Get API Information ===")
    
    client = FileCompressorClient()
    info = client.get_info()
    
    print(f"Max file size: {info['max_file_size_mb']} MB")
    print(f"\nSupported formats:")
    for category, formats in info['supported_formats'].items():
        print(f"  {category}: {', '.join(formats)}")
    print(f"\nCompression strategies: {', '.join(info['compression_strategies'])}")


if __name__ == "__main__":
    print("File Compressor API - Usage Examples")
    print("=" * 50)
    
    # Get API info first
    example_get_api_info()
    
    # Note: Uncomment examples below if you have sample files
    # example_compress_image_quality()
    # example_compress_video_target_size()
    # example_compress_audio_percentage()
    # example_batch_compress()
    
    print("\n" + "=" * 50)
    print("Examples complete!")
    print("\nNote: Make sure the API server is running at http://localhost:8000")
