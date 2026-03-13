@echo off
title GESTURE CONTROL - Setup & Launch
color 0B

:: Always run from the folder this .bat file lives in
cd /d "%~dp0"

echo.
echo  ==========================================
echo     GESTURE CONTROL -- Windows Setup
echo  ==========================================
echo.

:: ── Check Python 3.11 specifically (mediapipe requires it) ──
py -3.11 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [ERROR] Python 3.11 not found!
    echo.
    echo  MediaPipe does not support Python 3.14 yet.
    echo  You need to install Python 3.11 alongside your current Python.
    echo.
    echo  Steps:
    echo    1. Go to: https://www.python.org/downloads/release/python-3119/
    echo    2. Download "Windows installer (64-bit)"
    echo    3. Install it - check "Add Python to PATH"
    echo    4. Run this file again
    echo.
    pause
    exit /b 1
)

echo  [OK] Python 3.11 found
echo.
echo  Installing dependencies for Python 3.11...
echo  (This only happens once, takes ~2 minutes)
echo.

py -3.11 -m pip install mediapipe opencv-python pyautogui numpy pycaw comtypes

if %errorlevel% neq 0 (
    echo.
    echo  [ERROR] Install failed. Try right-clicking START.bat
    echo  and selecting "Run as Administrator".
    pause
    exit /b 1
)

echo.
echo  ==========================================
echo    All dependencies installed!
echo    Launching Gesture Control...
echo  ==========================================
echo.

py -3.11 "%~dp0gesture_control.py"

pause
