@echo off
echo ============================================================
echo TRAJANUS USA - ONE TIME SETUP
echo ============================================================
echo.
echo This will install all required Python packages.
echo.
pause

echo.
echo [1/2] Installing Python packages...
pip install google-auth google-auth-oauthlib google-api-python-client python-docx --break-system-packages

echo.
echo [2/2] Creating folder structure...
if not exist "G:\My Drive\00 - Trajanus USA\07-Session-Journals\Personal-Diaries" mkdir "G:\My Drive\00 - Trajanus USA\07-Session-Journals\Personal-Diaries"
if not exist "G:\My Drive\00 - Trajanus USA\07-Session-Journals\Technical-Journals" mkdir "G:\My Drive\00 - Trajanus USA\07-Session-Journals\Technical-Journals"
if not exist "G:\My Drive\00 - Trajanus USA\07-Session-Journals\Code-Repository" mkdir "G:\My Drive\00 - Trajanus USA\07-Session-Journals\Code-Repository"

echo.
echo ============================================================
echo SETUP COMPLETE!
echo ============================================================
echo.
echo Next steps:
echo   1. Edit EOS_DUAL_OUTPUT.py to set your preferred font name
echo   2. Run: python EOS_DUAL_OUTPUT.py
echo.
pause
