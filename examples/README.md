# API Usage Examples

This directory contains example scripts showing how to use the File Compressor API programmatically.

## Available Examples

### 1. Python Example (`python_example.py`)

**Prerequisites:**
```bash
pip install requests
```

**Usage:**
```bash
python python_example.py
```

**Features:**
- Client class for easy API interaction
- Image compression with quality strategy
- Video compression to target size
- Audio compression by percentage
- Batch file compression
- Get API information

### 2. JavaScript Example (`javascript_example.js`)

**Prerequisites:**
```bash
npm install axios form-data
```

**Usage:**
```bash
node javascript_example.js
```

**Features:**
- Client class for easy API interaction
- All compression strategies demonstrated
- Async/await patterns
- Error handling
- Batch processing

## Example Patterns

### Compress with Quality Strategy

**Python:**
```python
client = FileCompressorClient()
result = client.compress_file(
    file_path="image.jpg",
    strategy="quality",
    quality=75
)
```

**JavaScript:**
```javascript
const client = new FileCompressorClient();
const result = await client.compressFile('image.jpg', {
  strategy: 'quality',
  quality: 75
});
```

### Compress to Target Size

**Python:**
```python
result = client.compress_file(
    file_path="video.mp4",
    strategy="target_size",
    target_size_mb=10.0
)
```

**JavaScript:**
```javascript
const result = await client.compressFile('video.mp4', {
  strategy: 'target_size',
  target_size_mb: 10.0
});
```

### Compress by Percentage

**Python:**
```python
result = client.compress_file(
    file_path="audio.mp3",
    strategy="percentage",
    reduction_percentage=50
)
```

**JavaScript:**
```javascript
const result = await client.compressFile('audio.mp3', {
  strategy: 'percentage',
  reduction_percentage: 50
});
```

## cURL Examples

### Get API Info
```bash
curl http://localhost:8000/api/compress/info
```

### Compress Image
```bash
curl -X POST "http://localhost:8000/api/compress/" \
  -F "file=@image.jpg" \
  -F 'compression_data={"strategy":"quality","quality":75}'
```

### Compress Video to Target Size
```bash
curl -X POST "http://localhost:8000/api/compress/" \
  -F "file=@video.mp4" \
  -F 'compression_data={"strategy":"target_size","target_size_mb":10.0}'
```

### Download Compressed File
```bash
curl -O "http://localhost:8000/api/compress/download/compressed_file.jpg"
```

## Response Format

All compression requests return:
```json
{
  "success": true,
  "original_size": 5242880,
  "compressed_size": 2621440,
  "reduction_percentage": 50.0,
  "filename": "compressed_image_abc123.jpg",
  "download_url": "/api/compress/download/compressed_image_abc123.jpg",
  "message": "File compressed successfully"
}
```

## Error Handling

### Python
```python
try:
    result = client.compress_file("large_file.jpg", "quality", quality=75)
except requests.exceptions.HTTPError as e:
    print(f"API Error: {e.response.json()}")
except Exception as e:
    print(f"Error: {str(e)}")
```

### JavaScript
```javascript
try {
  const result = await client.compressFile('large_file.jpg', {
    strategy: 'quality',
    quality: 75
  });
} catch (error) {
  console.error('API Error:', error.response?.data || error.message);
}
```

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 413 | File too large | Use smaller file or increase MAX_FILE_SIZE |
| 400 | Invalid file type | Check supported formats |
| 404 | File not found | Check download URL |
| 500 | Compression failed | Check FFmpeg installation |

## Notes

- Ensure the API server is running at `http://localhost:8000`
- All examples include error handling
- Files are automatically cleaned up after download
- Modify `API_BASE_URL` if your server runs on a different port
