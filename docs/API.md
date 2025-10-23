# API Documentation

## Base URL
```
http://localhost:8000/api
```

## Endpoints

### 1. Compress File

**Endpoint:** `POST /compress/`

**Description:** Compress a file using specified strategy

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body:
  - `file`: File (required)
  - `compression_data`: JSON string (required)

**Compression Data Structure:**
```json
{
  "strategy": "quality" | "target_size" | "percentage",
  "quality": 1-100,              // For quality strategy
  "target_size_mb": number,      // For target_size strategy
  "reduction_percentage": 1-99   // For percentage strategy
}
```

**Examples:**

Quality-based compression:
```json
{
  "strategy": "quality",
  "quality": 75
}
```

Target size compression:
```json
{
  "strategy": "target_size",
  "target_size_mb": 2.5
}
```

Percentage reduction:
```json
{
  "strategy": "percentage",
  "reduction_percentage": 50
}
```

**Response:**
```json
{
  "success": true,
  "original_size": 10485760,
  "compressed_size": 5242880,
  "reduction_percentage": 50.0,
  "filename": "compressed_image_abc123.jpg",
  "download_url": "/api/compress/download/compressed_image_abc123.jpg",
  "message": "File compressed successfully"
}
```

**Error Responses:**

```json
{
  "detail": "File too large. Maximum size is 500MB"
}
```

```json
{
  "detail": "Unsupported file type: .xyz (application/octet-stream)"
}
```

### 2. Download Compressed File

**Endpoint:** `GET /compress/download/{filename}`

**Description:** Download a compressed file

**Parameters:**
- `filename`: Name of the compressed file (path parameter)

**Response:**
- File download (application/octet-stream)

**Note:** Files are automatically deleted after download

### 3. Get API Information

**Endpoint:** `GET /compress/info`

**Description:** Get information about supported formats and limits

**Response:**
```json
{
  "max_file_size_mb": 500,
  "supported_formats": {
    "images": ["jpg", "jpeg", "png", "gif", "bmp", "webp", "tiff"],
    "videos": ["mp4", "avi", "mov", "mkv", "flv", "wmv", "webm"],
    "audio": ["mp3", "wav", "flac", "aac", "ogg", "m4a"],
    "documents": ["pdf", "docx"]
  },
  "compression_strategies": ["quality", "target_size", "percentage"]
}
```

### 4. Health Check

**Endpoint:** `GET /health`

**Description:** Check API health status

**Response:**
```json
{
  "status": "healthy"
}
```

### 5. Root

**Endpoint:** `GET /`

**Description:** API root information

**Response:**
```json
{
  "message": "File Compressor API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

## Interactive Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Rate Limits

Currently no rate limits are enforced. In production, implement rate limiting based on:
- IP address
- User session
- File size and processing time

## File Size Limits

- Maximum file size: 500MB (configurable in `config.py`)
- Recommended: Keep files under 100MB for optimal performance

## Compression Quality Guidelines

### Images
- **High Quality (85-100)**: Minimal visible quality loss
- **Medium Quality (60-85)**: Good balance, recommended
- **Low Quality (1-60)**: Noticeable quality loss, maximum compression

### Videos
- **High Quality (85-100)**: CRF 18-23, near lossless
- **Medium Quality (60-85)**: CRF 24-28, good quality
- **Low Quality (1-60)**: CRF 29-51, high compression

### Audio
- **High Quality (85-100)**: 256-320 kbps
- **Medium Quality (60-85)**: 128-256 kbps
- **Low Quality (1-60)**: 32-128 kbps

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad Request (invalid file type, missing parameters) |
| 404 | File not found |
| 413 | File too large |
| 500 | Internal server error (compression failed) |

## Usage Examples

### Python
```python
import requests

# Compress image with quality strategy
with open('image.jpg', 'rb') as f:
    files = {'file': f}
    data = {
        'compression_data': '{"strategy": "quality", "quality": 75}'
    }
    response = requests.post('http://localhost:8000/api/compress/', files=files, data=data)
    result = response.json()
    
# Download compressed file
if result['success']:
    download_url = f"http://localhost:8000{result['download_url']}"
    compressed_file = requests.get(download_url)
    with open('compressed_image.jpg', 'wb') as f:
        f.write(compressed_file.content)
```

### JavaScript (Fetch)
```javascript
// Compress file
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('compression_data', JSON.stringify({
  strategy: 'quality',
  quality: 75
}));

const response = await fetch('http://localhost:8000/api/compress/', {
  method: 'POST',
  body: formData
});

const result = await response.json();

// Download compressed file
if (result.success) {
  window.location.href = result.download_url;
}
```

### cURL
```bash
curl -X POST "http://localhost:8000/api/compress/" \
  -F "file=@image.jpg" \
  -F 'compression_data={"strategy":"quality","quality":75}'
```
