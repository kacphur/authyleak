@echo off
setlocal enabledelayedexpansion

:: ── Force UTF-8 ───────────────────────────────────────
chcp 65001 >nul

:: ── Elevate to Admin ──────────────────────────────────
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting Administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: ── Change to script directory ────────────────────────
cd /d "%~dp0"

:: ── ANSI colour codes ─────────────────────────────────
for /f %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"
set "PINK=%ESC%[38;2;255;102;170m"
set "WHITE=%ESC%[97m"
set "DIM=%ESC%[90m"
set "RESET=%ESC%[0m"

title AUTHYLEAK Installer

:: ── Clear and draw ASCII art ──────────────────────────
cls
echo %PINK%
echo     █████╗ ██╗   ██╗████████╗██╗  ██╗██╗   ██╗██╗     ███████╗ █████╗ ██╗  ██╗
echo    ██╔══██╗██║   ██║╚══██╔══╝██║  ██║╚██╗ ██╔╝██║     ██╔════╝██╔══██╗██║ ██╔╝
echo    ███████║██║   ██║   ██║   ███████║ ╚████╔╝ ██║     █████╗  ███████║█████╔╝ 
echo    ██╔══██║██║   ██║   ██║   ██╔══██║  ╚██╔╝  ██║     ██╔══╝  ██╔══██║██╔═██╗ 
echo    ██║  ██║╚██████╔╝   ██║   ██║  ██║   ██║   ███████╗███████╗██║  ██║██║  ██╗
echo    ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝
echo %WHITE%               Osu! Auth Leaker ^& Offset Finder – Installer%RESET%
echo %DIM%------------------------------------------------------------%RESET%
echo.

:: ── Check Python ──────────────────────────────────────
echo %WHITE%[1/3] Checking Python...%RESET%
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo %PINK%ERROR: Python not found!%RESET%
    echo %WHITE%Please install Python 3.8+ from https://python.org and ensure it's in PATH.
    pause
    exit /b 1
)
python --version 2>nul
echo %WHITE%Python detected.%RESET%
echo.

:: ── Install dependencies ──────────────────────────────
echo %WHITE%[2/3] Installing required packages...%RESET%
echo %DIM%(pymem, rich, psutil, pywin32)%RESET%
python -m pip install --upgrade pymem rich psutil pywin32 >nul 2>&1
if %errorlevel% neq 0 (
    echo %PINK%Installation failed. Trying without upgrade flag...%RESET%
    python -m pip install pymem rich psutil pywin32
    if %errorlevel% neq 0 (
        echo %PINK%Failed to install packages. Please check your internet and try again.%RESET%
        pause
        exit /b 1
    )
)
echo %WHITE%All packages installed successfully!%RESET%
echo.

:: ── Check for authyleak.py ─────────────────────────────
if not exist "authyleak.py" (
    echo %PINK%ERROR: authyleak.py not found!%RESET%
    echo %WHITE%Put authyleak.py in the same folder as this installer.%RESET%
    pause
    exit /b 1
)

:: ── Launch Python script ───────────────────────────────
echo %WHITE%[3/3] Launching authyleak...%RESET%
echo %DIM%─────────────────────────────────────────────────%RESET%
echo.
:: Flush the batch output before starting Python
>nul ping -n 1 localhost
python -u authyleak.py
echo.
echo %PINK%Authyleak session ended.%RESET%
pause
exit /b 0