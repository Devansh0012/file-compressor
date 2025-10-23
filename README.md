# File Compressor Tool

A comprehensive web-based file compression tool that supports images, videos, audio files, and documents.

## Features

- **Multi-format Support**: Compress images (JPG, PNG, GIF, WebP, etc.), videos (MP4, AVI, MOV, etc.), audio (MP3, WAV, FLAC, etc.), and documents (PDF)
- **Multiple Compression Strategies**:
  - **Quality-based**: Set desired quality level (1-100)
  - **Target Size**: Specify exact file size you want
  - **Percentage Reduction**: Reduce file size by a specific percentage
- **Modern UI**: Clean, responsive interface with drag-and-drop file upload
- **Real-time Processing**: Async file processing with progress indication
- **Secure**: File validation, size limits, and automatic cleanup

## Technology Stack

### Backend
- **FastAPI**: Modern, high-performance Python web framework
- **Pillow**: Image processing
- **FFmpeg**: Video and audio processing
- **PyPDF2**: PDF compression
- **Pydantic**: Data validation

### Frontend
- **React 18**: Modern UI library
- **TypeScript**: Type-safe JavaScript
- **Vite**: Fast build tool
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client
- **React Dropzone**: File upload component

## Project Structure

```
file-compressor/
├── backend/
│   ├── app/
│   │   ├── routes/          # API endpoints
│   │   ├── services/        # Compression logic
│   │   ├── utils/           # Helper functions
│   │   ├── models.py        # Data models
│   │   └── config.py        # Configuration
│   ├── main.py              # Application entry point
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API services
│   │   ├── types/           # TypeScript types
│   │   ├── utils/           # Utility functions
│   │   └── App.tsx          # Main app component
│   ├── package.json         # Node dependencies
│   └── vite.config.ts       # Vite configuration
└── README.md
```

## Prerequisites

### System Requirements
- Python 3.8 or higher
- Node.js 16 or higher
- FFmpeg (for video/audio processing)

### Install FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

## Installation

### 1. Clone the Repository
```bash
cd file-compressor
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install
```

## Running the Application

### Start Backend Server

```bash
# From backend directory with venv activated
cd backend
python main.py
```

The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

### Start Frontend Development Server

```bash
# From frontend directory
cd frontend
npm run dev
```

The web interface will be available at `http://localhost:5173`

## Usage

1. **Open the Web Interface**: Navigate to `http://localhost:5173`
2. **Upload a File**: Drag and drop or click to browse for your file
3. **Choose Compression Strategy**:
   - **Quality**: Slide to select quality level (higher = better quality, larger file)
   - **Target Size**: Enter desired file size in MB
   - **Percentage**: Slide to select reduction percentage
4. **Compress**: Click "Compress File" button
5. **Download**: Once complete, download your compressed file

## API Endpoints

### POST `/api/compress/`
Compress a file with specified strategy

**Request:**
- `file`: File to compress (multipart/form-data)
- `compression_data`: JSON with compression parameters

**Response:**
```json
{
  "success": true,
  "original_size": 5242880,
  "compressed_size": 2621440,
  "reduction_percentage": 50.0,
  "filename": "compressed_image_abc123.jpg",
  "download_url": "/api/compress/download/compressed_image_abc123.jpg"
}
```

### GET `/api/compress/download/{filename}`
Download a compressed file

### GET `/api/compress/info`
Get API information and supported formats

## Configuration

### Backend Configuration

Edit `backend/app/config.py` to customize:
- `MAX_FILE_SIZE`: Maximum upload size (default: 500MB)
- `ALLOWED_ORIGINS`: CORS allowed origins
- File format support

### Environment Variables

Create `.env` file in backend directory:
```env
API_TITLE=File Compressor API
API_VERSION=1.0.0
MAX_FILE_SIZE=524288000  # 500MB in bytes
```

## Development Best Practices

This project follows modern development practices:

1. **Clean Architecture**: Separation of concerns with distinct layers
   - Routes (API endpoints)
   - Services (business logic)
   - Models (data structures)
   - Utils (helper functions)

2. **Type Safety**: TypeScript on frontend, Pydantic on backend

3. **Error Handling**: Comprehensive error handling and validation

4. **Security**: File type validation, size limits, automatic cleanup

5. **Code Quality**: Consistent formatting, clear naming conventions

6. **Async Processing**: Non-blocking file operations

## Supported Formats

### Images
JPG, JPEG, PNG, GIF, BMP, WebP, TIFF

### Videos
MP4, AVI, MOV, MKV, FLV, WMV, WebM

### Audio
MP3, WAV, FLAC, AAC, OGG, M4A

### Documents
PDF, DOCX

## Compression Strategies Explained

### Quality-based Compression
- Best for: General use when you want to balance quality and size
- How it works: Adjusts compression quality parameter
- Range: 1 (lowest quality, smallest size) to 100 (highest quality, largest size)

### Target Size Compression
- Best for: When you have specific size requirements
- How it works: Iteratively adjusts quality/resolution to reach target
- Note: For very small targets, resolution may be reduced

### Percentage Reduction
- Best for: Batch processing with consistent reduction
- How it works: Reduces file size by specified percentage
- Range: 1% to 99% reduction

## Troubleshooting

### FFmpeg Not Found
Ensure FFmpeg is installed and in your system PATH:
```bash
ffmpeg -version
```

### Port Already in Use
Change ports in configuration files:
- Backend: `backend/main.py` (default: 8000)
- Frontend: `frontend/vite.config.ts` (default: 5173)

### CORS Errors
Add your frontend URL to `ALLOWED_ORIGINS` in `backend/app/config.py`

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Built with ❤️ by Devansh
