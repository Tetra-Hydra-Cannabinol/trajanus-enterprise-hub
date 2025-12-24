# ORGANIZE_COMMAND_CENTER.ps1
# Trajanus USA - Command Center Cleanup
# Created by Paul (Claude Opus 4.5) - December 6, 2025
#
# USAGE:
#   .\ORGANIZE_COMMAND_CENTER.ps1           # DRY RUN - shows what would happen
#   .\ORGANIZE_COMMAND_CENTER.ps1 -Execute  # ACTUALLY MOVES FILES
#

param(
    [switch]$Execute = $false
)

$CommandCenter = "G:\My Drive\00 - Trajanus USA\00-Command-Center"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  COMMAND CENTER ORGANIZATION" -ForegroundColor Cyan
if ($Execute) {
    Write-Host "  *** EXECUTE MODE ***" -ForegroundColor Yellow
} else {
    Write-Host "  (DRY RUN - no files will move)" -ForegroundColor Green
}
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# ============================================
# STEP 1: CREATE SUBFOLDERS
# ============================================

$folders = @("Scripts", "Index-Backups", "Session-Logs", "Documentation", "Temp-Archive")

Write-Host "STEP 1: Subfolders..." -ForegroundColor Yellow
foreach ($folder in $folders) {
    $path = Join-Path $CommandCenter $folder
    if (-not (Test-Path $path)) {
        if ($Execute) {
            New-Item -Path $path -ItemType Directory -Force | Out-Null
            Write-Host "  [CREATED] $folder" -ForegroundColor Green
        } else {
            Write-Host "  [WOULD CREATE] $folder" -ForegroundColor Gray
        }
    } else {
        Write-Host "  [EXISTS] $folder" -ForegroundColor DarkGray
    }
}
Write-Host ""

# ============================================
# STEP 2: CATEGORIZE FILES
# ============================================

Write-Host "STEP 2: Analyzing files..." -ForegroundColor Yellow

$allFiles = Get-ChildItem -Path $CommandCenter -File -ErrorAction SilentlyContinue

$scripts = $allFiles | Where-Object { $_.Extension -in '.py', '.ps1' }
$indexBackups = $allFiles | Where-Object { $_.Name -like 'index_*.html' }
$sessionLogs = $allFiles | Where-Object { $_.Name -match '^\d{4}-\d{2}-\d{2}' -and $_.Extension -eq '.md' }
$zipFiles = $allFiles | Where-Object { $_.Extension -eq '.zip' }
$docFiles = $allFiles | Where-Object { 
    $_.Extension -eq '.md' -and $_.Name -notmatch '^\d{4}-\d{2}-\d{2}'
}

$protected = @('index.html', 'token.json', 'credentials.json', 'main.js', 'preload.js', 'package.json')

Write-Host "  Scripts (.py/.ps1):   $($scripts.Count)" -ForegroundColor Cyan
Write-Host "  Index Backups:        $($indexBackups.Count)" -ForegroundColor Cyan
Write-Host "  Session Logs:         $($sessionLogs.Count)" -ForegroundColor Cyan
Write-Host "  Documentation:        $($docFiles.Count)" -ForegroundColor Cyan
Write-Host "  Zip files:            $($zipFiles.Count)" -ForegroundColor Cyan
Write-Host ""

# ============================================
# STEP 3: MOVE FILES
# ============================================

Write-Host "STEP 3: File moves..." -ForegroundColor Yellow
Write-Host ""

$moveCount = 0

# Scripts
foreach ($file in $scripts) {
    if ($file.Name -notin $protected) {
        $dest = Join-Path $CommandCenter "Scripts"
        if ($Execute) {
            Move-Item -Path $file.FullName -Destination $dest -Force -ErrorAction SilentlyContinue
            Write-Host "  [MOVED] $($file.Name) -> Scripts/" -ForegroundColor Green
        } else {
            Write-Host "  [WOULD MOVE] $($file.Name) -> Scripts/" -ForegroundColor Gray
        }
        $moveCount++
    }
}

# Index Backups
foreach ($file in $indexBackups) {
    $dest = Join-Path $CommandCenter "Index-Backups"
    if ($Execute) {
        Move-Item -Path $file.FullName -Destination $dest -Force -ErrorAction SilentlyContinue
        Write-Host "  [MOVED] $($file.Name) -> Index-Backups/" -ForegroundColor Green
    } else {
        Write-Host "  [WOULD MOVE] $($file.Name) -> Index-Backups/" -ForegroundColor Gray
    }
    $moveCount++
}

# Session Logs
foreach ($file in $sessionLogs) {
    $dest = Join-Path $CommandCenter "Session-Logs"
    if ($Execute) {
        Move-Item -Path $file.FullName -Destination $dest -Force -ErrorAction SilentlyContinue
        Write-Host "  [MOVED] $($file.Name) -> Session-Logs/" -ForegroundColor Green
    } else {
        Write-Host "  [WOULD MOVE] $($file.Name) -> Session-Logs/" -ForegroundColor Gray
    }
    $moveCount++
}

# Documentation
foreach ($file in $docFiles) {
    if ($file.Name -notin $protected) {
        $dest = Join-Path $CommandCenter "Documentation"
        if ($Execute) {
            Move-Item -Path $file.FullName -Destination $dest -Force -ErrorAction SilentlyContinue
            Write-Host "  [MOVED] $($file.Name) -> Documentation/" -ForegroundColor Green
        } else {
            Write-Host "  [WOULD MOVE] $($file.Name) -> Documentation/" -ForegroundColor Gray
        }
        $moveCount++
    }
}

# Zip Files
foreach ($file in $zipFiles) {
    $dest = Join-Path $CommandCenter "Temp-Archive"
    if ($Execute) {
        Move-Item -Path $file.FullName -Destination $dest -Force -ErrorAction SilentlyContinue
        Write-Host "  [MOVED] $($file.Name) -> Temp-Archive/" -ForegroundColor Green
    } else {
        Write-Host "  [WOULD MOVE] $($file.Name) -> Temp-Archive/" -ForegroundColor Gray
    }
    $moveCount++
}

# ============================================
# SUMMARY
# ============================================

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  TOTAL FILES: $moveCount" -ForegroundColor White
Write-Host "============================================" -ForegroundColor Cyan

if (-not $Execute) {
    Write-Host ""
    Write-Host "  DRY RUN complete. No files moved." -ForegroundColor Yellow
    Write-Host "  To execute: .\ORGANIZE_COMMAND_CENTER.ps1 -Execute" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "  ORGANIZATION COMPLETE!" -ForegroundColor Green
    [console]::beep(800, 200)
    [console]::beep(1000, 200)
    [console]::beep(1200, 300)
}
Write-Host ""
