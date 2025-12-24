# GENERATE_SMART_INDEX.ps1
# Creates USEFUL file index - filters out junk, shows what matters
# NO EMOJIS VERSION

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "TRAJANUS SMART FILE INDEX GENERATOR" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

$rootPath = "G:\My Drive\00 - Trajanus USA"
$outputFile = "$rootPath\00-Command-Center\TRAJANUS_SMART_INDEX.md"

Write-Host "Scanning useful files only..." -ForegroundColor Yellow
Write-Host ""

# FILTERS - Skip the bullshit
$skipFolders = @(
    'archives',
    '.git',
    'node_modules',
    '__pycache__',
    'cache',
    '.vscode',
    'temp'
)

$skipExtensions = @(
    '.gdoc',
    '.gsheet',
    '.gslides',
    '.tmp',
    '.cache',
    '.log',
    '.bak'
)

# KEEP - What actually matters
$keepExtensions = @(
    '.md',
    '.docx',
    '.xlsx',
    '.pptx',
    '.pdf',
    '.ps1',
    '.py',
    '.html',
    '.js',
    '.json',
    '.csv',
    '.txt'
)

Write-Host "Filtering out cache, temp, and duplicate files..." -ForegroundColor Yellow

# Get ALL files first
$allFiles = Get-ChildItem -Path $rootPath -Recurse -File -ErrorAction SilentlyContinue

# Step 1: Filter out junk
$filteredFiles = $allFiles | Where-Object {
    $file = $_
    
    # Skip if in a junk folder
    $inJunkFolder = $false
    foreach ($skipFolder in $skipFolders) {
        if ($file.DirectoryName -like "*\$skipFolder\*" -or $file.DirectoryName -like "*\$skipFolder") {
            $inJunkFolder = $true
            break
        }
    }
    if ($inJunkFolder) { return $false }
    
    # Skip junk extensions
    if ($skipExtensions -contains $file.Extension.ToLower()) { return $false }
    
    # Keep useful extensions only
    if ($keepExtensions -contains $file.Extension.ToLower()) { return $true }
    
    return $false
}

# Step 2: Remove duplicates (same name in same folder, keep best version)
$fileTracker = @{}
$usefulFiles = @()
$duplicatesFound = 0

$priority = @{
    '.md' = 1
    '.docx' = 2
    '.xlsx' = 3
    '.pptx' = 3
    '.pdf' = 4
    '.ps1' = 5
    '.py' = 5
    '.html' = 6
    '.js' = 6
}

foreach ($file in $filteredFiles) {
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
    $folderKey = "$($file.DirectoryName)\$baseName"
    
    if ($fileTracker.ContainsKey($folderKey)) {
        # Duplicate found - compare priorities
        $existing = $fileTracker[$folderKey]
        
        $currentPriority = if ($priority.ContainsKey($file.Extension.ToLower())) { $priority[$file.Extension.ToLower()] } else { 10 }
        $existingPriority = if ($priority.ContainsKey($existing.Extension.ToLower())) { $priority[$existing.Extension.ToLower()] } else { 10 }
        
        if ($currentPriority -lt $existingPriority) {
            # Current file is better - replace
            $fileTracker[$folderKey] = $file
            $duplicatesFound++
        } else {
            # Existing file is better - skip current
            $duplicatesFound++
        }
    } else {
        # New file - add to tracker
        $fileTracker[$folderKey] = $file
    }
}

# Extract the final list
$usefulFiles = $fileTracker.Values | Sort-Object FullName

Write-Host "Total files scanned: $($allFiles.Count)" -ForegroundColor Gray
Write-Host "After filtering junk: $($filteredFiles.Count)" -ForegroundColor Cyan
Write-Host "Duplicates removed: $duplicatesFound" -ForegroundColor Yellow
Write-Host "Final useful files: $($usefulFiles.Count)" -ForegroundColor Green
Write-Host ""

# Group by folder for analysis
$filesByFolder = $usefulFiles | Group-Object DirectoryName | Sort-Object Count -Descending

# Start building markdown - NO EMOJIS
$output = ""
$output += "# TRAJANUS USA SMART FILE INDEX`n"
$output += "**Human-Readable Table of Contents**`n"
$output += "Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n`n"

$output += "**Filtered Results:**`n"
$output += "- Total files scanned: $($allFiles.Count)`n"
$output += "- After filtering junk: $($filteredFiles.Count)`n"
$output += "- Duplicates removed: $duplicatesFound`n"
$output += "- Final useful files: $($usefulFiles.Count)`n"
$output += "- Folders with content: $($filesByFolder.Count)`n`n"

$output += "**What's excluded:** Cache files (.gdoc, .gsheet), temp files, archives, duplicates (keeps .md over .docx, etc.)`n`n"
$output += "---`n`n"

$output += "## QUICK STATS`n`n"

# File type breakdown
$byType = $usefulFiles | Group-Object Extension | Sort-Object Count -Descending
$output += "**By File Type:**`n"
foreach ($type in $byType | Select-Object -First 10) {
    $output += "- **$($type.Name)**: $($type.Count) files`n"
}

$output += "`n---`n`n"

# Recent work (last 7 days)
$recentCutoff = (Get-Date).AddDays(-7)
$recentFiles = $usefulFiles | Where-Object { $_.LastWriteTime -gt $recentCutoff } | Sort-Object LastWriteTime -Descending

if ($recentFiles.Count -gt 0) {
    $output += "## RECENT WORK (Last 7 Days)`n`n"
    $output += "**$($recentFiles.Count) files modified:**`n`n"
    
    foreach ($file in $recentFiles | Select-Object -First 30) {
        $relPath = $file.DirectoryName.Replace($rootPath + "\", "")
        $date = $file.LastWriteTime.ToString("yyyy-MM-dd HH:mm")
        $output += "- **$($file.Name)** - $date`n"
        $output += "  - Location: $relPath`n"
    }
    
    if ($recentFiles.Count -gt 30) {
        $output += "`n*...and $($recentFiles.Count - 30) more*`n"
    }
    
    $output += "`n---`n`n"
}

# Top folders by file count
$output += "## TOP FOLDERS`n`n"
$output += "**Most active folders:**`n`n"

foreach ($folder in $filesByFolder | Select-Object -First 20) {
    $folderName = $folder.Name.Replace($rootPath + "\", "")
    $output += "### $folderName`n"
    $output += "**$($folder.Count) files**`n`n"
    
    # Show file types in this folder
    $types = $folder.Group | Group-Object Extension | Sort-Object Count -Descending
    foreach ($t in $types) {
        $output += "- $($t.Name): $($t.Count)`n"
    }
    $output += "`n"
}

$output += "---`n`n"

# Key folders breakdown
$output += "## KEY FOLDERS DETAIL`n`n"

$keyFolders = @(
    '00-Command-Center',
    '01-Core-Protocols',
    '07-Session-Journal',
    '08-EOS-Files',
    '09-Active-Projects'
)

foreach ($keyFolder in $keyFolders) {
    $folderPath = Join-Path $rootPath $keyFolder
    
    if (Test-Path $folderPath) {
        $folderFiles = $usefulFiles | Where-Object { $_.DirectoryName -like "$folderPath*" }
        
        if ($folderFiles.Count -gt 0) {
            $output += "### $keyFolder`n"
            $output += "**$($folderFiles.Count) files**`n`n"
            
            # Recent files in this folder (last 5)
            $recentInFolder = $folderFiles | Sort-Object LastWriteTime -Descending | Select-Object -First 5
            
            $output += "**Recent files:**`n"
            foreach ($file in $recentInFolder) {
                $date = $file.LastWriteTime.ToString("yyyy-MM-dd")
                $subPath = $file.DirectoryName.Replace($folderPath, "").TrimStart('\')
                if ($subPath) {
                    $output += "- $($file.Name) - $date - Location: $subPath`n"
                } else {
                    $output += "- $($file.Name) - $date`n"
                }
            }
            
            $output += "`n"
        }
    }
}

$output += "---`n`n"

# Search guide
$output += "## HOW TO USE THIS INDEX`n`n"
$output += "### Quick Find:`n"
$output += "- Press Ctrl+F to search`n"
$output += "- Search for: file names, dates (YYYY-MM-DD), keywords`n`n"

$output += "### Common Searches:`n"
$output += "- Session from specific date: `"2025-11-30`"`n"
$output += "- All protocols: `"protocol`"`n"
$output += "- Scripts: `".ps1`" or `".py`"`n"
$output += "- Recent sessions: Check 'Recent Work' section above`n`n"

$output += "### For Humans:`n"
$output += "- Browse by folder sections`n"
$output += "- Check 'Recent Work' for latest files`n"
$output += "- Look in 'Top Folders' for most active areas`n`n"

$output += "### For Claude:`n"
$output += "- Search this document in project knowledge`n"
$output += "- Use google_drive_search for content searches`n"
$output += "- Reference exact folder paths from this index`n`n"

$output += "---`n`n"

$output += "## UPDATE THIS INDEX`n`n"
$output += "Regenerate anytime:`n`n"
$output += "PowerShell command:`n"
$output += "cd `"G:\My Drive\00 - Trajanus USA\00-Command-Center`"`n"
$output += ".\GENERATE_SMART_INDEX.ps1`n`n"
$output += "---`n`n"
$output += "**Filtered, de-duplicated index - showing what matters**`n"

# Write to file
$output | Out-File -FilePath $outputFile -Encoding UTF8

Write-Host "================================================================================" -ForegroundColor Green
Write-Host "SMART INDEX COMPLETE" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "File saved to:" -ForegroundColor Green
Write-Host "  $outputFile" -ForegroundColor White
Write-Host ""

# CRITICAL: Auto-convert to Google Docs format
Write-Host "Converting to Google Docs format..." -ForegroundColor Cyan
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
python "$scriptDir\convert_single_md.py" "$outputFile"

if ($LASTEXITCODE -eq 0) {
    Write-Host "SUCCESS: Index converted to Google Docs" -ForegroundColor Green
    Write-Host "Claude can now read this file via google_drive_search" -ForegroundColor Green
} else {
    Write-Host "WARNING: Conversion failed - Claude won't be able to read this file" -ForegroundColor Red
}

Write-Host ""
Write-Host "This index is clean and useful!" -ForegroundColor Cyan
Write-Host ""
