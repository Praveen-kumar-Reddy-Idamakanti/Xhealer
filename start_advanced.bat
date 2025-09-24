@echo off
setlocal enabledelayedexpansion

echo ========================================
echo  AI Health Assistant - Advanced Start
echo ========================================
echo.

REM Set colors for better output
color 0A

REM Check if Python is installed
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo ✅ Python !PYTHON_VERSION! found
)

REM Check if Node.js is installed
echo [2/6] Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js and try again
    echo Download from: https://nodejs.org/
    pause
    exit /b 1
) else (
    for /f %%i in ('node --version 2^>^&1') do set NODE_VERSION=%%i
    echo ✅ Node.js !NODE_VERSION! found
)

REM Check if npm is available
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: npm is not available
    pause
    exit /b 1
) else (
    for /f %%i in ('npm --version 2^>^&1') do set NPM_VERSION=%%i
    echo ✅ npm !NPM_VERSION! found
)

echo.

REM Navigate to AI directory
cd /d "%~dp0ai"

REM Check if virtual environment exists
echo [3/6] Setting up Python environment...
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment exists
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✅ Virtual environment activated

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ❌ ERROR: Failed to install Python dependencies
    echo Try running: pip install -r requirements.txt
    pause
    exit /b 1
)
echo ✅ Python dependencies installed

REM Check if NLTK data is available
echo Checking NLTK data...
python -c "import nltk; nltk.data.find('tokenizers/punkt')" >nul 2>&1
if errorlevel 1 (
    echo Downloading NLTK data...
    python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
    echo ✅ NLTK data downloaded
) else (
    echo ✅ NLTK data available
)

echo.

REM Navigate to frontend directory
cd /d "%~dp0frontend"

REM Check if node_modules exists
echo [4/6] Setting up Node.js environment...
if not exist "node_modules" (
    echo Installing Node.js dependencies...
    npm install
    if errorlevel 1 (
        echo ❌ ERROR: Failed to install Node.js dependencies
        echo Try running: npm install
        pause
        exit /b 1
    )
    echo ✅ Node.js dependencies installed
) else (
    echo ✅ Node.js dependencies exist
)

echo.

REM Check if required files exist
echo [5/6] Checking required files...
cd /d "%~dp0ai"

if not exist "disease_prediction_api.py" (
    echo ❌ ERROR: disease_prediction_api.py not found
    pause
    exit /b 1
)

if not exist "disease_predictor.py" (
    echo ❌ ERROR: disease_predictor.py not found
    pause
    exit /b 1
)

if not exist "medical_dictionary.py" (
    echo ❌ ERROR: medical_dictionary.py not found
    pause
    exit /b 1
)

if not exist "trained_models" (
    echo ❌ ERROR: trained_models directory not found
    echo Please ensure the model training is complete
    pause
    exit /b 1
)

echo ✅ All required files found

echo.

REM Start backend server in new window
echo [6/6] Starting servers...
echo Starting backend server...
start "🤖 AI Health Assistant - Backend Server" cmd /k "cd /d %~dp0ai && call venv\Scripts\activate.bat && echo Backend Server Starting... && echo URL: http://localhost:5000 && echo. && python disease_prediction_api.py"

REM Wait for backend to start
echo Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

REM Start frontend server in new window
echo Starting frontend server...
start "🌐 AI Health Assistant - Frontend Server" cmd /k "cd /d %~dp0frontend && echo Frontend Server Starting... && echo URL: http://localhost:8080 && echo. && npm run dev"

echo.
echo ========================================
echo    🚀 Servers Started Successfully!
echo ========================================
echo.
echo 📍 Backend Server:  http://localhost:5000
echo 📍 Frontend Server: http://localhost:8080
echo.
echo 💡 Tips:
echo    - Both servers are running in separate windows
echo    - Close those windows to stop the servers
echo    - Backend API endpoints: /health, /predict, /comprehensive-analysis
echo    - Frontend will automatically open in your browser
echo.
echo 🔧 Troubleshooting:
echo    - If backend fails: Check if port 5000 is available
echo    - If frontend fails: Check if port 8080 is available
echo    - Check the server windows for detailed error messages
echo.
echo Press any key to exit this script...
pause >nul
