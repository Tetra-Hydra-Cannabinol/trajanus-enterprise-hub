@echo off
REM Trajanus USA - Quick Upload to Google Drive
REM Double-click this file to upload all session documents

echo ========================================
echo TRAJANUS USA - GOOGLE DRIVE UPLOADER
echo ========================================
echo.

cd /d "%~dp0"

python upload_session_docs.py

echo.
echo Press any key to close...
pause >nul
