@echo off
echo ========================================
echo KNOWMAD-6: EOS FILE CONVERSION
echo ========================================
echo.

cd /d "G:\My Drive\00 - Trajanus USA\00-Command-Center"

echo Running conversion on EOS Files folder...
echo.

python batch_convert_to_gdocs.py "G:\My Drive\00 - Trajanus USA\EOS Files\12-11-2025"

echo.
echo ========================================
echo CONVERSION COMPLETE
echo ========================================
echo.
echo Press any key to close...
pause
