# EOS_AUTOMATION_MASTER.ps1
# Master automation script - Run this ONE command after downloading ZIP
# Automatically: Unzips, Creates folders, Parses files, Converts to Google Docs

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "EOS MASTER AUTOMATION - Trajanus USA" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Step 1: Parse and distribute files (includes unzipping)
Write-Host "STEP 1: Extracting ZIP and organizing files..." -ForegroundColor Yellow
Write-Host ""

python "$scriptDir\parse_eos_files.py" --auto

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: File parsing failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Step 2: Convert NEW files only (not reconverting everything)
Write-Host "STEP 2: Converting new files to Google Docs..." -ForegroundColor Yellow
Write-Host ""

& "$scriptDir\CONVERT_NEW_FILES_ONLY.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: File conversion failed" -ForegroundColor Red
    exit 1
}

# Step 3: Success notification
Write-Host ""
Write-Host "================================================================================" -ForegroundColor Green
Write-Host "✓✓✓ EOS AUTOMATION COMPLETE ✓✓✓" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "SUMMARY:" -ForegroundColor Green
Write-Host "  ✓ ZIP file extracted and archived" -ForegroundColor Green
Write-Host "  ✓ Files organized into folders by type" -ForegroundColor Green
Write-Host "  ✓ NEW files converted to Google Docs (skipped already converted)" -ForegroundColor Green
Write-Host "  ✓ Next Claude session has complete access" -ForegroundColor Green
Write-Host ""
Write-Host "Your session is ready for next time!" -ForegroundColor Green
Write-Host ""
Write-Host "================================================================================" -ForegroundColor Green
Write-Host ""

# Play a beep/notification sound
[console]::beep(800,200)
[console]::beep(1000,200)
[console]::beep(1200,300)
