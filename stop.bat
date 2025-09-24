@echo off
echo ========================================
echo    AI Health Assistant - Stop Script
echo ========================================
echo.

echo Stopping all AI Health Assistant servers...

REM Kill Python processes (backend)
echo Stopping backend server...
taskkill /f /im python.exe >nul 2>&1
if errorlevel 1 (
    echo No Python processes found
) else (
    echo ✅ Backend server stopped
)

REM Kill Node.js processes (frontend)
echo Stopping frontend server...
taskkill /f /im node.exe >nul 2>&1
if errorlevel 1 (
    echo No Node.js processes found
) else (
    echo ✅ Frontend server stopped
)

REM Kill any remaining cmd processes with our titles
echo Cleaning up server windows...
taskkill /f /fi "WINDOWTITLE eq AI Health Assistant - Backend*" >nul 2>&1
taskkill /f /fi "WINDOWTITLE eq AI Health Assistant - Frontend*" >nul 2>&1
taskkill /f /fi "WINDOWTITLE eq 🤖 AI Health Assistant - Backend*" >nul 2>&1
taskkill /f /fi "WINDOWTITLE eq 🌐 AI Health Assistant - Frontend*" >nul 2>&1

echo.
echo ========================================
echo    ✅ All servers stopped successfully!
echo ========================================
echo.
echo Press any key to exit...
pause >nul
