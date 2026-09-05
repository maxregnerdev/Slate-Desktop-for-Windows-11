@echo off
:: ============================================================================
:: Slate Desktop for Windows 11 - Windows 12 UI Transformation
:: Version: 2.0.0 - Next Valley Edition
:: Description: Complete Windows 12 UI transformation for Windows 11 25H2
:: Author: Slate Desktop Team
:: ============================================================================

:: Check for Administrator privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This script requires Administrator privileges.
    echo Please run as Administrator...
    pause
    exit /b
)

:: Set working directory
cd /d "%~dp0"

:: Display Windows 12 Transformation Header
python -m src.main

echo.
echo ============================================================================
echo Windows 12 UI Transformation Complete!
echo Check the /config/Windows12 folder for detailed configuration options
echo ============================================================================
echo.

pause
