# Deploy Command Center - ONE CLICK
# Copies downloaded HTML to production location
# Run from your Downloads folder

param(
    [string]$SourceFile = ""
)

$CommandCenterPath = "G:\My Drive\00 - Trajanus USA\00-Command-Center"
$ProductionFile = "$CommandCenterPath\index.html"
$DownloadsPath = "$env:USERPROFILE\Downloads"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Command Center Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# If no source file specified, find the latest one
if (-not $SourceFile) {
    Write-Host "Looking for Command Center files in Downloads..." -ForegroundColor Yellow
    
    # Look for any HTML file with "Command" or "index" in name
    $candidates = Get-ChildItem -Path $DownloadsPath -Filter "*.html" | 
                  Where-Object { $_.Name -match "Command|index" } |
                  Sort-Object LastWriteTime -Descending
    
    if ($candidates.Count -eq 0) {
        Write-Host "ERROR: No Command Center HTML files found in Downloads!" -ForegroundColor Red
        Write-Host ""
        Write-Host "Expected files named like:" -ForegroundColor Yellow
        Write-Host "  - Command_Center_LATEST.html" -ForegroundColor White
        Write-Host "  - index.html" -ForegroundColor White
        Write-Host "  - index_2025-11-24_2025.html" -ForegroundColor White
        Write-Host ""
        Write-Host "Press any key to exit..." -ForegroundColor Gray
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        exit 1
    }
    
    Write-Host ""
    Write-Host "Found $($candidates.Count) file(s):" -ForegroundColor White
    Write-Host ""
    
    for ($i = 0; $i -lt [Math]::Min(5, $candidates.Count); $i++) {
        $file = $candidates[$i]
        $size = [math]::Round($file.Length / 1KB, 1)
        $time = $file.LastWriteTime.ToString("yyyy-MM-dd HH:mm")
        Write-Host "  [$($i+1)] $($file.Name)" -ForegroundColor Cyan
        Write-Host "      $size KB | $time" -ForegroundColor Gray
    }
    
    Write-Host ""
    Write-Host "Select file (1-$([Math]::Min(5, $candidates.Count))) or Enter for newest: " -ForegroundColor Yellow -NoNewline
    $selection = Read-Host
    
    if ($selection -eq "" -or $selection -eq "1") {
        $SourceFile = $candidates[0].FullName
    } elseif ([int]$selection -ge 1 -and [int]$selection -le $candidates.Count) {
        $SourceFile = $candidates[[int]$selection - 1].FullName
    } else {
        Write-Host "Invalid selection!" -ForegroundColor Red
        exit 1
    }
}

$sourceFileName = Split-Path $SourceFile -Leaf
Write-Host ""
Write-Host "Selected: $sourceFileName" -ForegroundColor Green

# Verify source exists
if (-not (Test-Path $SourceFile)) {
    Write-Host "ERROR: Source file not found!" -ForegroundColor Red
    Write-Host "Path: $SourceFile" -ForegroundColor Yellow
    exit 1
}

# Create Command Center folder if it doesn't exist
if (-not (Test-Path $CommandCenterPath)) {
    Write-Host ""
    Write-Host "Creating Command Center folder..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $CommandCenterPath -Force | Out-Null
    Write-Host "Created: $CommandCenterPath" -ForegroundColor Green
}

# Backup existing production file if it exists
if (Test-Path $ProductionFile) {
    $backupName = "index_BACKUP_$(Get-Date -Format 'yyyy-MM-dd_HHmm').html"
    $backupPath = "$CommandCenterPath\Archive\$backupName"
    
    # Create Archive folder if needed
    if (-not (Test-Path "$CommandCenterPath\Archive")) {
        New-Item -ItemType Directory -Path "$CommandCenterPath\Archive" -Force | Out-Null
    }
    
    Write-Host ""
    Write-Host "Backing up current production file..." -ForegroundColor Yellow
    Copy-Item $ProductionFile -Destination $backupPath -Force
    Write-Host "Backup saved: $backupName" -ForegroundColor Cyan
}

# Copy new file to production
Write-Host ""
Write-Host "Deploying new version..." -ForegroundColor Yellow

try {
    Copy-Item $SourceFile -Destination $ProductionFile -Force
    
    $newSize = [math]::Round((Get-Item $ProductionFile).Length / 1KB, 1)
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "DEPLOYMENT SUCCESSFUL!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Production file updated:" -ForegroundColor White
    Write-Host "  Location: $ProductionFile" -ForegroundColor Cyan
    Write-Host "  Size: $newSize KB" -ForegroundColor Gray
    Write-Host ""
    Write-Host "You can now:" -ForegroundColor Yellow
    Write-Host "  1. Open Command Center from Desktop shortcut" -ForegroundColor White
    Write-Host "  2. Or double-click: $ProductionFile" -ForegroundColor White
    Write-Host ""
    
    # Ask if user wants to open it now
    Write-Host "Open Command Center now? (Y/N): " -ForegroundColor Yellow -NoNewline
    $openNow = Read-Host
    
    if ($openNow -eq 'Y' -or $openNow -eq 'y') {
        Start-Process $ProductionFile
        Write-Host ""
        Write-Host "Command Center opened in browser!" -ForegroundColor Green
    }
    
} catch {
    Write-Host ""
    Write-Host "ERROR: Deployment failed!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
