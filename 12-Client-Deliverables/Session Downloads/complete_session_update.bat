@echo off
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center"
echo Running upload script...
python upload_session_docs.py
if errorlevel 1 (
    echo Upload failed!
    pause
    exit /b 1
)
echo.
echo Upload complete! Now updating MASTER documents...
echo.
python update_master_docs.py
if errorlevel 1 (
    echo Update failed!
    pause
    exit /b 1
)
echo.
echo ===================================
echo SESSION UPDATE COMPLETE!
echo ===================================
pause