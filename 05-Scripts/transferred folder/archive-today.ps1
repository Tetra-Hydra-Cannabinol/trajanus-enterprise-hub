# End of Day Archive Script
# Moves today's timestamped versions to dated archive folder
# Keeps workspace clean for next day

$CommandCenterPath = "G:\My Drive\00 - Trajanus USA\00-Command-Center"
$ArchiveBasePath = "$CommandCenterPath\Archive"

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "End of Day Archive" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Get today's date
$today = Get-Date -Format "yyyy-MM-dd"
$todayArchivePath = "$ArchiveBasePath\$today"

# Create archive folder if needed
if (-not (Test-Path $todayArchivePath)) {
    New-Item -ItemType Directory -Path $todayArchivePath -Force | Out-Null
    Write-Host "Created archive folder: $today" -ForegroundColor Green
} else {
    Write-Host "Using existing archive folder: $today" -ForegroundColor Gray
}

# Find today's timestamped files
$todayPattern = "index_$today*.html"
$todayFiles = Get-ChildItem -Path $CommandCenterPath -Filter $todayPattern -File

if ($todayFiles.Count -eq 0) {
    Write-Host ""
    Write-Host "No timestamped files found for today ($today)" -ForegroundColor Yellow
    Write-Host "Nothing to archive." -ForegroundColor Gray
    Write-Host ""
    Write-Host "Press any key to exit..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 0
}

Write-Host ""
Write-Host "Found $($todayFiles.Count) file(s) from today:" -ForegroundColor White
Write-Host ""

# List files to be archived
foreach ($file in $todayFiles) {
    $fileSize = [math]::Round($file.Length / 1KB, 1)
    $fileTime = $file.LastWriteTime.ToString("HH:mm:ss")
    Write-Host "  • $($file.Name)" -ForegroundColor Cyan
    Write-Host "    $fileSize KB | Modified: $fileTime" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Archive these files? (Y/N): " -ForegroundColor Yellow -NoNewline
$response = Read-Host

if ($response -ne 'Y' -and $response -ne 'y') {
    Write-Host ""
    Write-Host "Archive cancelled." -ForegroundColor Red
    Write-Host ""
    exit 0
}

# Archive files
Write-Host ""
Write-Host "Archiving..." -ForegroundColor Yellow

$archivedCount = 0
$totalSize = 0

foreach ($file in $todayFiles) {
    try {
        $destPath = "$todayArchivePath\$($file.Name)"
        
        # Check if file already exists in archive
        if (Test-Path $destPath) {
            Write-Host "  ! Duplicate: $($file.Name) - Skipping" -ForegroundColor Yellow
            Remove-Item $file.FullName -Force
        } else {
            Move-Item $file.FullName -Destination $destPath -Force
            $archivedCount++
            $totalSize += $file.Length
            Write-Host "  ✓ Archived: $($file.Name)" -ForegroundColor Green
        }
        
    } catch {
        Write-Host "  ✗ Failed: $($file.Name)" -ForegroundColor Red
        Write-Host "    $($_.Exception.Message)" -ForegroundColor DarkRed
    }
}

$totalSizeMB = [math]::Round($totalSize / 1MB, 2)

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Archive Complete!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Files archived: $archivedCount" -ForegroundColor White
Write-Host "Total size: $totalSizeMB MB" -ForegroundColor White
Write-Host "Location: Archive\$today\" -ForegroundColor White
Write-Host ""

# Check for old archives (optional cleanup)
$archiveFolders = Get-ChildItem -Path $ArchiveBasePath -Directory | Where-Object { $_.Name -match '^\d{4}-\d{2}-\d{2}$' }
$oldArchives = $archiveFolders | Where-Object { 
    $archiveDate = [DateTime]::ParseExact($_.Name, "yyyy-MM-dd", $null)
    $daysSince = (Get-Date) - $archiveDate
    $daysSince.Days -gt 30
}

if ($oldArchives.Count -gt 0) {
    Write-Host ""
    Write-Host "================================" -ForegroundColor Yellow
    Write-Host "Old Archives Found" -ForegroundColor Yellow
    Write-Host "================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Found $($oldArchives.Count) archive(s) older than 30 days:" -ForegroundColor White
    Write-Host ""
    
    foreach ($old in $oldArchives) {
        $fileCount = (Get-ChildItem $old.FullName -File).Count
        $folderSize = [math]::Round((Get-ChildItem $old.FullName -File | Measure-Object -Property Length -Sum).Sum / 1MB, 2)
        Write-Host "  • $($old.Name) - $fileCount files ($folderSize MB)" -ForegroundColor Gray
    }
    
    Write-Host ""
    Write-Host "Delete old archives? (Y/N): " -ForegroundColor Yellow -NoNewline
    $cleanupResponse = Read-Host
    
    if ($cleanupResponse -eq 'Y' -or $cleanupResponse -eq 'y') {
        Write-Host ""
        foreach ($old in $oldArchives) {
            try {
                Remove-Item $old.FullName -Recurse -Force
                Write-Host "  ✓ Deleted: $($old.Name)" -ForegroundColor Green
            } catch {
                Write-Host "  ✗ Failed to delete: $($old.Name)" -ForegroundColor Red
            }
        }
        Write-Host ""
        Write-Host "Cleanup complete!" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "Cleanup skipped." -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
