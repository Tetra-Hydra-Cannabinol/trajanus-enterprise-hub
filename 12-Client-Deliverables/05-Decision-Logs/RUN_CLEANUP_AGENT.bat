@echo off
REM ========================================
REM Google Drive Cleanup Agent Launcher
REM ========================================
REM This batch file runs the cleanup agent in the background
REM You can minimize this window and keep working

title Google Drive Cleanup Agent

echo.
echo ========================================
echo   GOOGLE DRIVE CLEANUP AGENT
echo ========================================
echo.
echo Starting scan of your Google Drive...
echo This will take 5-10 minutes.
echo.
echo You can minimize this window and continue working.
echo Check back later for results.
echo.
echo ========================================
echo.

REM Change to the scripts directory
cd /d "G:\My Drive\00 - Trajanus USA\00-Command-Center\05-Scripts"

REM Run the cleanup agent
python gdrive_cleanup_agent.py --mode scan

echo.
echo ========================================
echo   SCAN COMPLETE!
echo ========================================
echo.
echo Reports saved in current directory:
echo   - cleanup_report_*.txt (human-readable)
echo   - cleanup_report_*.json (machine-readable)
echo.
echo Review the .txt file to see what was found.
echo.
echo Press any key to close this window...
pause > nul
