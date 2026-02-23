@echo off
REM Quick Setup & Run Script for Windows
REM Run this from career_recommendation\v2 directory

echo.
echo 🚀 Career Path - Complete Setup
echo ================================
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if not errorlevel 1 (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
    echo ✓ Python !python_version! found
) else (
    echo ❌ Python is not installed. Please install Python 3.11+
    exit /b 1
)

REM Check Node
echo Checking Node.js installation...
node --version >nul 2>&1
if not errorlevel 1 (
    for /f "tokens=*" %%i in ('node --version') do set node_version=%%i
    echo ✓ Node.js !node_version! found
) else (
    echo ❌ Node.js is not installed. Please install Node.js 14+
    exit /b 1
)

echo.
echo Setting up Backend...
cd backend

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python dependencies...
python -m pip install --quiet --upgrade pip setuptools
pip install --quiet -r ../requirements-dev.txt

echo ✓ Backend setup complete

echo.
echo Setting up Frontend...
cd ..\frontend

if not exist "node_modules" (
    echo Installing Node dependencies...
    call npm install --silent
    echo ✓ Frontend dependencies installed
) else (
    echo ✓ Node modules already installed
)

cd ..\backend
if not exist ".env" (
    copy .env.example .env
    echo ✓ Created backend .env
)

cd ..\frontend
if not exist ".env" (
    copy .env.example .env
    echo ✓ Created frontend .env
)

cd ..

echo.
echo ✅ Setup Complete!
echo.
echo To start the application:
echo.
echo Terminal 1 ^(Backend^):
echo   cd backend
echo   venv\Scripts\activate.bat
echo   python app.py
echo.
echo Terminal 2 ^(Frontend^):
echo   cd frontend
echo   npm start
echo.
echo Then open: http://localhost:3000
echo.
echo Happy coding! 🚀
echo.
pause
