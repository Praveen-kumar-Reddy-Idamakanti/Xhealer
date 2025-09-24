@echo off
echo ========================================
echo  AI Health Assistant - Setup Script
echo ========================================
echo.

REM Check if Python is installed
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed
    echo Please install Python 3.8+ from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
) else (
    echo ✅ Python is installed
)

REM Check if Node.js is installed
echo [2/4] Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Node.js is not installed
    echo Please install Node.js from: https://nodejs.org/
    echo Download the LTS version
    pause
    exit /b 1
) else (
    echo ✅ Node.js is installed
)

echo.

REM Setup Python environment
echo [3/4] Setting up Python environment...
cd /d "%~dp0ai"

REM Create virtual environment
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
)

REM Activate and install dependencies
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)
echo ✅ Python dependencies installed

REM Download NLTK data
echo Downloading NLTK data...
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
echo ✅ NLTK data downloaded

echo.

REM Setup Node.js environment
echo [4/4] Setting up Node.js environment...
cd /d "%~dp0frontend"

echo Installing Node.js dependencies...
npm install
if errorlevel 1 (
    echo ❌ ERROR: Failed to install Node.js dependencies
    pause
    exit /b 1
)
echo ✅ Node.js dependencies installed

echo.

REM Check if models exist
cd /d "%~dp0ai"
if not exist "trained_models" (
    echo ⚠️  WARNING: trained_models directory not found
    echo You may need to train the models first
    echo Run: python model_training.py
)

echo.
echo ========================================
echo    ✅ Setup Complete!
echo ========================================
echo.
echo 🎉 AI Health Assistant is ready to use!
echo.
echo 📋 Next steps:
echo    1. Run start.bat to start both servers
echo    2. Open http://localhost:8080 in your browser
echo    3. Start chatting with the AI Health Assistant!
echo.
echo 📁 Project structure:
echo    - Backend: ai/ directory (Python Flask API)
echo    - Frontend: frontend/ directory (React app)
echo    - Documentation: ai/docs/ directory
echo.
echo Press any key to exit...
pause >nul
