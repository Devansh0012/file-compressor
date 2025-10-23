# File Compressor - Development Setup Guide

## Quick Start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Architecture Overview

### Backend Architecture (Clean Architecture Pattern)

```
┌─────────────────────────────────────────────┐
│           API Layer (routes/)               │
│  - HTTP endpoints                           │
│  - Request/response handling                │
│  - Input validation                         │
└─────────────┬───────────────────────────────┘
              │
┌─────────────▼───────────────────────────────┐
│        Service Layer (services/)            │
│  - Business logic                           │
│  - Compression algorithms                   │
│  - File processing                          │
└─────────────┬───────────────────────────────┘
              │
┌─────────────▼───────────────────────────────┐
│         Utility Layer (utils/)              │
│  - File handling                            │
│  - Helper functions                         │
└─────────────────────────────────────────────┘
```

### Frontend Architecture (Component-based)

```
┌─────────────────────────────────────────────┐
│              App.tsx                        │
│  - Main application logic                   │
│  - State management                         │
└─────────────┬───────────────────────────────┘
              │
┌─────────────▼───────────────────────────────┐
│          Components/                        │
│  - FileUpload                               │
│  - CompressionControls                      │
│  - ResultDisplay                            │
└─────────────┬───────────────────────────────┘
              │
┌─────────────▼───────────────────────────────┐
│          Services/                          │
│  - API communication                        │
│  - Data fetching                            │
└─────────────────────────────────────────────┘
```

## Development Workflow

### Adding a New File Format

1. **Update Configuration** (`backend/app/config.py`):
```python
SUPPORTED_NEW_FORMAT: set[str] = {"ext1", "ext2"}
```

2. **Add File Type** (`backend/app/models.py`):
```python
class FileType(str, Enum):
    NEW_FORMAT = "new_format"
```

3. **Create Compressor Service** (`backend/app/services/new_compressor.py`):
```python
class NewFormatCompressor:
    def compress(self, request: CompressionRequest) -> Path:
        # Implementation
        pass
```

4. **Update Route Handler** (`backend/app/routes/compression.py`):
```python
elif file_type == FileType.NEW_FORMAT:
    compressor = NewFormatCompressor(input_path, output_path)
```

### Adding a New Compression Strategy

1. **Update Model** (`backend/app/models.py`):
```python
class CompressionStrategy(str, Enum):
    NEW_STRATEGY = "new_strategy"
```

2. **Implement in Compressor Services**:
```python
def _compress_by_new_strategy(self, params) -> Path:
    # Implementation
    pass
```

3. **Update Frontend Types** (`frontend/src/types/index.ts`):
```typescript
export enum CompressionStrategy {
  NEW_STRATEGY = 'new_strategy',
}
```

4. **Add UI Controls** (`frontend/src/components/CompressionControls.tsx`)

## Testing

### Backend Testing
```bash
# Install pytest
pip install pytest pytest-asyncio

# Run tests
pytest
```

### Frontend Testing
```bash
# Install testing libraries
npm install --save-dev @testing-library/react @testing-library/jest-dom

# Run tests
npm test
```

## Performance Optimization

### Backend
- Use async file operations with `aiofiles`
- Implement file processing queue for large files
- Add caching for frequently compressed files

### Frontend
- Lazy load components
- Implement progress tracking for uploads
- Add file preview before compression

## Security Considerations

1. **File Validation**: Always validate file type and size
2. **Sanitization**: Clean filenames to prevent path traversal
3. **Rate Limiting**: Add rate limiting to prevent abuse
4. **Temporary Files**: Automatic cleanup of temporary files
5. **CORS**: Properly configure CORS for production

## Production Deployment

### Backend (Docker)
```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend (Build)
```bash
npm run build
# Serve dist/ folder with nginx or similar
```

### Environment Variables for Production
```env
API_TITLE=File Compressor API
API_VERSION=1.0.0
MAX_FILE_SIZE=524288000
ALLOWED_ORIGINS=https://yourdomain.com
```

## Monitoring and Logging

Add structured logging:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

## Common Issues and Solutions

### Issue: FFmpeg not found
**Solution**: Install FFmpeg and ensure it's in PATH

### Issue: Out of memory for large files
**Solution**: Implement chunked processing or set stricter size limits

### Issue: Slow compression
**Solution**: Use lower quality presets or implement background jobs

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [Pillow Documentation](https://pillow.readthedocs.io/)
