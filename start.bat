@echo off
REM File Compressor - Windows Startup Script

echo Starting File Compressor Application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if Node is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Node.js is not installed. Please install Node.js 16 or higher.
    pause
    exit /b 1
)

REM Check if FFmpeg is installed
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo Warning: FFmpeg is not installed. Video and audio compression will not work.
    echo Download from: https://ffmpeg.org/download.html
    echo.
)

REM Start Backend
echo Starting Backend Server...
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment and install dependencies
call venv\Scripts\activate.bat

if not exist "venv\.dependencies_installed" (
    echo Installing Python dependencies...
    pip install -r requirements.txt
    type nul > venv\.dependencies_installed
)

REM Start backend server
echo Starting FastAPI server on http://localhost:8000
start /B python main.py

REM Start Frontend
cd ..\frontend

echo Starting Frontend Server...

REM Install dependencies if needed
if not exist "node_modules\" (
    echo Installing Node dependencies...
    call npm install
)

echo Starting Vite dev server on http://localhost:5173
start /B npm run dev

echo.
echo Application is running!
echo.
echo Frontend: http://localhost:5173
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop all servers
echo.

pause
