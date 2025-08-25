@echo off
echo Installing L.U.F.F.Y AI Assistant Dependencies...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python from https://python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo Python found. Installing dependencies...
python -m pip install --upgrade pip
python -m pip install speechrecognition==3.10.0
python -m pip install pyttsx3==2.90
python -m pip install requests==2.31.0
python -m pip install pyaudio==0.2.11

echo.
echo Installation complete!
echo.
echo To run L.U.F.F.Y:
echo   Command line version: python main.py
echo   GUI version: python gui.py
echo.
pause
