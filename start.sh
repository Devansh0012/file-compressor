#!/bin/bash

# File Compressor - Startup Script
# This script starts both backend and frontend servers

echo "🚀 Starting File Compressor Application..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

# Check if Node is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed. Please install Node.js 16 or higher.${NC}"
    exit 1
fi

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo -e "${RED}⚠️  Warning: FFmpeg is not installed. Video and audio compression will not work.${NC}"
    echo -e "${BLUE}Install FFmpeg:${NC}"
    echo -e "  macOS: brew install ffmpeg"
    echo -e "  Ubuntu: sudo apt install ffmpeg"
    echo ""
fi

# Start Backend
echo -e "${BLUE}📦 Starting Backend Server...${NC}"
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/.dependencies_installed" ]; then
    echo -e "${BLUE}Installing Python dependencies...${NC}"
    pip install -r requirements.txt
    touch venv/.dependencies_installed
fi

# Start backend in background
echo -e "${GREEN}✅ Starting FastAPI server on http://localhost:8000${NC}"
python main.py &
BACKEND_PID=$!

# Start Frontend
cd ../frontend

echo -e "${BLUE}📦 Starting Frontend Server...${NC}"

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo -e "${BLUE}Installing Node dependencies...${NC}"
    npm install
fi

echo -e "${GREEN}✅ Starting Vite dev server on http://localhost:5173${NC}"
npm run dev &
FRONTEND_PID=$!

echo ""
echo -e "${GREEN}🎉 Application is running!${NC}"
echo ""
echo -e "${BLUE}Frontend:${NC} http://localhost:5173"
echo -e "${BLUE}Backend API:${NC} http://localhost:8000"
echo -e "${BLUE}API Docs:${NC} http://localhost:8000/docs"
echo ""
echo -e "${RED}Press Ctrl+C to stop all servers${NC}"

# Trap Ctrl+C and cleanup
trap "echo ''; echo '🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT

# Wait for processes
wait
