@echo off
echo ========================================
echo    AI Health Assistant - Start Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js and try again
    pause
    exit /b 1
)

echo Python and Node.js are installed ✓
echo.

REM Navigate to AI directory
cd /d "%~dp0ai"

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating Python virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)

echo Python dependencies installed ✓
echo.

REM Navigate to frontend directory
cd /d "%~dp0frontend"

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing Node.js dependencies...
    npm install
    if errorlevel 1 (
        echo ERROR: Failed to install Node.js dependencies
        pause
        exit /b 1
    )
)

echo Node.js dependencies installed ✓
echo.

REM Start backend server in new window
echo Starting backend server...
start "AI Health Assistant - Backend" cmd /k "cd /d %~dp0ai && call venv\Scripts\activate.bat && python disease_prediction_api.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend server in new window
echo Starting frontend server...
start "AI Health Assistant - Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ========================================
echo    Servers Starting...
echo ========================================
echo.
echo Backend Server:  http://localhost:5000
echo Frontend Server: http://localhost:8080
echo.
echo Both servers are starting in separate windows.
echo Close those windows to stop the servers.
echo.
echo Press any key to exit this script...
pause >nul
