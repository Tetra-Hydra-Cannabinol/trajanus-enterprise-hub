# ORGANIZE_SESSION_FILES.ps1
# Moves session files from 08-EOS-Files subfolders to proper 07-Session-Journal locations

param(
    [switch]$DryRun = $false
)

$eosPath = "G:\My Drive\00 - Trajanus USA\08-EOS-Files"
$sessionJournalPath = "G:\My Drive\00 - Trajanus USA\07-Session-Journal"

# Define target folders
$targetFolders = @{
    "Technical" = "$sessionJournalPath\Technical-Journals"
    "Diary" = "$sessionJournalPath\Personal-Diaries"
    "Summary" = "$sessionJournalPath\Session-Summaries"
    "Repository" = "$sessionJournalPath\Code-Repositories"
    "Operational" = "$sessionJournalPath\Operational-Journals"
    "Handoff" = "$sessionJournalPath\Session-Handoffs"
    "Project_Journal" = "$sessionJournalPath\Project-Journals"
    "Project_Diary" = "$sessionJournalPath\Project-Diaries"
}

# Create target folders if they don't exist
foreach ($folder in $targetFolders.Values) {
    if (-not (Test-Path $folder)) {
        Write-Host "Creating folder: $folder" -ForegroundColor Cyan
        if (-not $DryRun) {
            New-Item -ItemType Directory -Path $folder -Force | Out-Null
        }
    }
}

Write-Host "============================================================" -ForegroundColor Green
Write-Host "SESSION FILE ORGANIZATION" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
if ($DryRun) {
    Write-Host "DRY RUN MODE - No files will be moved" -ForegroundColor Yellow
    Write-Host ""
}

# PHASE 1: SCAN FOR DUPLICATES
Write-Host "PHASE 1: Scanning for duplicates..." -ForegroundColor Cyan
Write-Host ""

$duplicates = @()
$allFiles = Get-ChildItem -Path $eosPath -Recurse -File -ErrorAction SilentlyContinue

foreach ($file in $allFiles) {
    $fileName = $file.Name
    
    # Skip non-session files
    if ($fileName -match "PROTOCOL|Manual|Command_Center|update_master|files\.zip|\.html$") {
        continue
    }
    
    # Determine target location
    $targetPath = $null
    if ($fileName -match "Technical.*Journal|Tech.*Journal|TECHNICAL.*JOURNAL") {
        $targetPath = $targetFolders["Technical"]
    }
    elseif ($fileName -match "Personal.*Diary|SESSION.*DIARY|.*Diary(?!.*Project)|DIARY") {
        $targetPath = $targetFolders["Diary"]
    }
    elseif ($fileName -match "Session.*Summary|SESSION.*SUMMARY|.*Summary|EOS.*Summary") {
        $targetPath = $targetFolders["Summary"]
    }
    elseif ($fileName -match "Code.*Repository|CODE.*REPOSITORY|Repository") {
        $targetPath = $targetFolders["Repository"]
    }
    elseif ($fileName -match "Operational.*Journal|OPERATIONAL.*JOURNAL") {
        $targetPath = $targetFolders["Operational"]
    }
    elseif ($fileName -match "Handoff|HANDOFF|Next.*Session") {
        $targetPath = $targetFolders["Handoff"]
    }
    elseif ($fileName -match "Trajanus.*Journal|Project.*Journal|PROJECT.*JOURNAL") {
        $targetPath = $targetFolders["Project_Journal"]
    }
    elseif ($fileName -match "Trajanus.*Diary|Project.*Diary|PROJECT.*DIARY") {
        $targetPath = $targetFolders["Project_Diary"]
    }
    
    if ($targetPath) {
        $targetFile = Join-Path $targetPath $fileName
        if (Test-Path $targetFile) {
            $sourceSize = $file.Length
            $targetSize = (Get-Item $targetFile).Length
            $sourceDate = $file.LastWriteTime
            $targetDate = (Get-Item $targetFile).LastWriteTime
            
            $duplicates += [PSCustomObject]@{
                FileName = $fileName
                SourcePath = $file.FullName
                TargetPath = $targetFile
                SourceSize = $sourceSize
                TargetSize = $targetSize
                SourceDate = $sourceDate
                TargetDate = $targetDate
                SameSize = ($sourceSize -eq $targetSize)
                Newer = ($sourceDate -gt $targetDate)
            }
        }
    }
}

if ($duplicates.Count -gt 0) {
    Write-Host "FOUND $($duplicates.Count) DUPLICATE FILES:" -ForegroundColor Yellow
    Write-Host ""
    foreach ($dup in $duplicates) {
        Write-Host "  $($dup.FileName)" -ForegroundColor Yellow
        Write-Host "    Source: $($dup.SourceSize) bytes, Modified: $($dup.SourceDate)" -ForegroundColor Gray
        Write-Host "    Target: $($dup.TargetSize) bytes, Modified: $($dup.TargetDate)" -ForegroundColor Gray
        if ($dup.SameSize) {
            Write-Host "    -> Same size (likely identical)" -ForegroundColor Green
        } elseif ($dup.Newer) {
            Write-Host "    -> Source is NEWER" -ForegroundColor Cyan
        } else {
            Write-Host "    -> Target is NEWER" -ForegroundColor Magenta
        }
        Write-Host ""
    }
    
    if (-not $DryRun) {
        Write-Host "What do you want to do with duplicates?" -ForegroundColor Yellow
        Write-Host "  1. SKIP duplicates (keep existing files)" -ForegroundColor White
        Write-Host "  2. OVERWRITE with source files (replace existing)" -ForegroundColor White
        Write-Host "  3. KEEP BOTH (rename source with timestamp)" -ForegroundColor White
        Write-Host ""
        $choice = Read-Host "Enter choice (1, 2, or 3)"
    } else {
        $choice = "1"  # Default to skip in dry run mode
    }
} else {
    Write-Host "No duplicates found. All files are unique." -ForegroundColor Green
    Write-Host ""
    $choice = "1"  # No duplicates, proceed normally
}

Write-Host ""
Write-Host "PHASE 2: Moving files..." -ForegroundColor Cyan
Write-Host ""

# Get all files recursively from EOS-Files
$allFiles = Get-ChildItem -Path $eosPath -Recurse -File -ErrorAction SilentlyContinue

$moved = 0
$skipped = 0
$errors = 0

foreach ($file in $allFiles) {
    $fileName = $file.Name
    $targetPath = $null
    $reason = ""
    
    # Skip non-session files
    if ($fileName -match "PROTOCOL|Manual|Command_Center|update_master|files\.zip|\.html$") {
        Write-Host "SKIP: $fileName (not a session file)" -ForegroundColor DarkGray
        $skipped++
        continue
    }
    
    # Determine target location based on filename (more flexible patterns)
    if ($fileName -match "Technical.*Journal|Tech.*Journal|TECHNICAL.*JOURNAL") {
        $targetPath = $targetFolders["Technical"]
        $reason = "Technical Journal"
    }
    elseif ($fileName -match "Personal.*Diary|SESSION.*DIARY|.*Diary(?!.*Project)|DIARY") {
        $targetPath = $targetFolders["Diary"]
        $reason = "Personal Diary"
    }
    elseif ($fileName -match "Session.*Summary|SESSION.*SUMMARY|.*Summary|EOS.*Summary") {
        $targetPath = $targetFolders["Summary"]
        $reason = "Session Summary"
    }
    elseif ($fileName -match "Code.*Repository|CODE.*REPOSITORY|Repository") {
        $targetPath = $targetFolders["Repository"]
        $reason = "Code Repository"
    }
    elseif ($fileName -match "Operational.*Journal|OPERATIONAL.*JOURNAL") {
        $targetPath = $targetFolders["Operational"]
        $reason = "Operational Journal"
    }
    elseif ($fileName -match "Handoff|HANDOFF|Next.*Session") {
        $targetPath = $targetFolders["Handoff"]
        $reason = "Session Handoff"
    }
    elseif ($fileName -match "Trajanus.*Journal|Project.*Journal|PROJECT.*JOURNAL") {
        $targetPath = $targetFolders["Project_Journal"]
        $reason = "Project Journal"
    }
    elseif ($fileName -match "Trajanus.*Diary|Project.*Diary|PROJECT.*DIARY") {
        $targetPath = $targetFolders["Project_Diary"]
        $reason = "Project Diary"
    }
    else {
        Write-Host "SKIP: $fileName (no matching pattern)" -ForegroundColor Yellow
        $skipped++
        continue
    }
    
    # Check if file already exists in target
    $targetFile = Join-Path $targetPath $fileName
    $isDuplicate = Test-Path $targetFile
    
    if ($isDuplicate) {
        # Handle duplicates based on user choice
        if ($choice -eq "1") {
            # Skip duplicates
            Write-Host "SKIP: $fileName (duplicate - keeping existing)" -ForegroundColor DarkYellow
            $skipped++
            continue
        }
        elseif ($choice -eq "2") {
            # Overwrite with source
            Write-Host "OVERWRITE: $fileName (replacing existing)" -ForegroundColor Magenta
            if (-not $DryRun) {
                Remove-Item $targetFile -Force -ErrorAction SilentlyContinue
            }
        }
        elseif ($choice -eq "3") {
            # Keep both - rename source with timestamp
            $timestamp = (Get-Date).ToString("HHmmss")
            $baseName = [System.IO.Path]::GetFileNameWithoutExtension($fileName)
            $extension = [System.IO.Path]::GetExtension($fileName)
            $newFileName = "${baseName}_${timestamp}${extension}"
            $targetFile = Join-Path $targetPath $newFileName
            Write-Host "KEEP BOTH: $fileName -> $newFileName" -ForegroundColor Cyan
        }
    }
    
    # Move the file
    try {
        Write-Host "MOVE: $fileName -> $reason" -ForegroundColor Cyan
        if (-not $DryRun) {
            Move-Item -Path $file.FullName -Destination $targetPath -ErrorAction Stop
        }
        $moved++
    }
    catch {
        Write-Host "ERROR: Failed to move $fileName - $($_.Exception.Message)" -ForegroundColor Red
        $errors++
    }
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "ORGANIZATION COMPLETE" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Files moved:   $moved" -ForegroundColor Green
Write-Host "Files skipped: $skipped" -ForegroundColor Yellow
Write-Host "Errors:        $errors" -ForegroundColor $(if ($errors -gt 0) { "Red" } else { "Green" })
Write-Host ""

if ($DryRun) {
    Write-Host "This was a DRY RUN. Run without -DryRun to actually move files." -ForegroundColor Yellow
}
else {
    Write-Host "All session files are now organized in 07-Session-Journal subfolders!" -ForegroundColor Green
}
