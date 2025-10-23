# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Prerequisites

Make sure you have these installed:
- **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
- **Node.js 16+**: [Download Node.js](https://nodejs.org/)
- **FFmpeg**: Required for video/audio compression

**Install FFmpeg:**
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### Step 2: Run the Application

**Option A: Use the startup script (Recommended)**

macOS/Linux:
```bash
./start.sh
```

Windows:
```bash
start.bat
```

**Option B: Manual start**

Terminal 1 (Backend):
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Terminal 2 (Frontend):
```bash
cd frontend
npm install
npm run dev
```

### Step 3: Use the Application

1. Open your browser to `http://localhost:5173`
2. Upload a file (drag & drop or click)
3. Choose compression strategy
4. Click "Compress File"
5. Download your compressed file!

## 📱 Screenshots & Features

### Supported File Types
- **Images**: JPG, PNG, GIF, WebP, BMP, TIFF
- **Videos**: MP4, AVI, MOV, MKV, WebM, FLV, WMV
- **Audio**: MP3, WAV, FLAC, AAC, OGG, M4A
- **Documents**: PDF, DOCX

### Compression Strategies

1. **Quality** (Recommended for most uses)
   - Adjust quality slider (1-100)
   - Higher number = better quality but larger file
   - Example: Quality 75 gives great balance

2. **Target Size** (When you need exact file size)
   - Enter desired size in MB
   - Tool will compress to match your target
   - Example: Enter "2.5" for 2.5MB file

3. **Percentage** (Reduce by specific amount)
   - Choose reduction percentage (1-99%)
   - Example: 50% will halve the file size

## 💡 Usage Tips

### For Best Results

**Images:**
- Use Quality 75-85 for photos
- Use PNG for screenshots and graphics
- Use JPEG for photos and complex images

**Videos:**
- Quality 70-85 gives excellent results
- MP4 format works best for compatibility
- Consider target size for specific needs (e.g., email attachments)

**Audio:**
- Quality 70-90 for music
- MP3 works best for compatibility
- FLAC for lossless quality

**Documents:**
- PDF compression removes redundant data
- Best for PDFs with many images

### File Size Limits
- Maximum upload: 500MB (configurable)
- Recommended: Keep files under 100MB for best performance

## 🔧 Troubleshooting

### "FFmpeg not found"
Install FFmpeg using the commands in Step 1

### "Port already in use"
Someone else is using port 8000 or 5173:
- Stop the other application
- Or change ports in config files

### Dependencies won't install
Python issues:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Node issues:
```bash
npm cache clean --force
npm install
```

## 📚 Additional Resources

- [Full README](README.md) - Complete documentation
- [API Documentation](API.md) - API reference
- [Development Guide](DEVELOPMENT.md) - For developers

## 🎯 Common Use Cases

### Email Attachments
1. Select "Target Size" strategy
2. Enter size limit (e.g., "10" for 10MB)
3. Compress and attach

### Website Images
1. Select "Quality" strategy
2. Set quality to 75-80
3. Use for faster page loads

### Social Media
1. Each platform has size limits
2. Use "Target Size" for exact requirements
3. Instagram: ~5MB, Twitter: ~5MB, Facebook: ~25MB

### Archive/Backup
1. Use "Percentage" strategy
2. Set to 30-50% reduction
3. Balance between size and quality

## 🌟 Tips for Power Users

### Batch Processing
Currently supports single files. For batch:
1. Use API endpoints directly
2. Write a script to loop through files
3. See [API Documentation](API.md)

### API Usage
Access the API programmatically:
- Endpoint: `http://localhost:8000/api/compress/`
- Documentation: `http://localhost:8000/docs`
- Interactive testing available

### Custom Configuration
Edit `backend/app/config.py`:
- Change max file size
- Add/remove supported formats
- Modify compression settings

## ❓ FAQ

**Q: Is my file uploaded to a server?**  
A: Files are processed locally on your machine. Nothing is sent to external servers.

**Q: Where are compressed files stored?**  
A: Temporarily in the `backend/compressed/` directory. They're deleted after download.

**Q: Can I compress multiple files at once?**  
A: Currently single file only. Batch support can be added using the API.

**Q: What's the best quality setting?**  
A: 70-85 gives excellent results for most files.

**Q: Why is video compression slow?**  
A: Video processing is CPU-intensive. Larger files take longer.

## 🎉 You're Ready!

Start compressing files and enjoy the tool!

Need help? Check the [full documentation](README.md) or [API reference](API.md).
