@echo off
REM ELBASHA Android App - Setup Script
REM This script will set up everything needed to build the APK

setlocal enabledelayedexpansion
color 0A
title ELBASHA Android Setup

cls
echo.
echo ================================================
echo    ELBASHA Downloader - Android Build Setup
echo ================================================
echo.

REM Check Python
echo [STEP 1] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please install Python first from https://python.org
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo [OK] Python %PYVER% found

echo.
echo [STEP 2] Installing required packages...
echo Installing buildozer...
pip install buildozer >nul 2>&1
echo [OK] buildozer installed

echo Installing Cython...
pip install cython >nul 2>&1
echo [OK] Cython installed

echo Installing kivy...
pip install kivy >nul 2>&1
echo [OK] kivy installed

echo Installing yt-dlp...
pip install yt-dlp >nul 2>&1
echo [OK] yt-dlp installed

echo.
echo [STEP 3] Downloading Android build tools...
echo This may take 5-10 minutes on first run
echo.

REM Create buildozer directory
if not exist ".buildozer" (
    mkdir .buildozer
)

echo.
echo ================================================
echo Setup Complete!
echo ================================================
echo.
echo Next steps:
echo 1. Copy all Python files to the same folder
echo 2. Run this command in PowerShell:
echo.
echo    buildozer android debug
echo.
echo 3. Wait 10-15 minutes for APK to build
echo 4. APK will be in: bin/elbasha-1.0-debug.apk
echo.
echo 5. Transfer APK to your phone and install!
echo.
pause
