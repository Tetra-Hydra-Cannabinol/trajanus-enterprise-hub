# GENERATE_SMART_INDEX.ps1
# Creates USEFUL file index - filters out junk, shows what matters

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
    '.gdoc',      # Google Drive cache files
    '.gsheet',    # Google Drive cache files
    '.gslides',   # Google Drive cache files
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

Write-Host "Filtering out cache, temp files, and duplicates..." -ForegroundColor Yellow

# Get ALL files first
$allFiles = Get-ChildItem -Path $rootPath -Recurse -File -ErrorAction SilentlyContinue

# Track duplicates (same name, different locations or extensions)
$fileTracker = @{}
$duplicatesFound = 0

# Filter intelligently
$usefulFiles = $allFiles | Where-Object {
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
    
    # Check for duplicates (same base name in same folder)
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
    $folderKey = "$($file.DirectoryName)\$baseName"
    
    if ($fileTracker.ContainsKey($folderKey)) {
        # We've seen this file name before in this folder
        $existing = $fileTracker[$folderKey]
        
        # Prefer original files over Google cache
        # Priority: .md > .docx > .xlsx > .pptx > everything else
        $priority = @{
            '.md' = 1
            '.docx' = 2
            '.xlsx' = 3
            '.pptx' = 3
            '.pdf' = 4
            '.ps1' = 5
            '.py' = 5
        }
        
        $currentPriority = if ($priority.ContainsKey($file.Extension.ToLower())) { $priority[$file.Extension.ToLower()] } else { 10 }
        $existingPriority = if ($priority.ContainsKey($existing.Extension.ToLower())) { $priority[$existing.Extension.ToLower()] } else { 10 }
        
        if ($currentPriority -lt $existingPriority) {
            # Current file has higher priority - replace the existing one
            $fileTracker[$folderKey] = $file
            $duplicatesFound++
            return $true
        } else {
            # Existing file has higher priority - skip this one
            $duplicatesFound++
            return $false
        }
    } else {
        # First time seeing this file - track it
        $fileTracker[$folderKey] = $file
    }
    
    # Keep useful extensions
    if ($keepExtensions -contains $file.Extension.ToLower()) { return $true }
    
    # Skip everything else
    return $false
}

Write-Host "Total files scanned: $($allFiles.Count)" -ForegroundColor Gray
Write-Host "Useful files found: $($usefulFiles.Count)" -ForegroundColor Green
Write-Host "Duplicates filtered: $duplicatesFound" -ForegroundColor Yellow
Write-Host ""

# Group by folder for analysis
$filesByFolder = $usefulFiles | Group-Object DirectoryName | Sort-Object Count -Descending

# Start building markdown
$markdown = @"
# TRAJANUS USA SMART FILE INDEX
**Human-Readable Table of Contents**
Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

**Filtered Results:**
- Total files scanned: $($allFiles.Count)
- Useful files: $($usefulFiles.Count)
- Duplicates removed: $duplicatesFound
- Folders with content: $($filesByFolder.Count)

**What's excluded:** Cache files (.gdoc, .gsheet), temp files, archives, node_modules, duplicates (keeps original over Google Doc version)

---

## 📊 QUICK STATS

"@

# File type breakdown
$byType = $usefulFiles | Group-Object Extension | Sort-Object Count -Descending
$markdown += "**By File Type:**`n"
foreach ($type in $byType | Select-Object -First 10) {
    $markdown += "- **$($type.Name)**: $($type.Count) files`n"
}

$markdown += "`n---`n`n"

# Recent work (last 7 days)
$recentCutoff = (Get-Date).AddDays(-7)
$recentFiles = $usefulFiles | Where-Object { $_.LastWriteTime -gt $recentCutoff } | Sort-Object LastWriteTime -Descending

if ($recentFiles.Count -gt 0) {
    $markdown += "## 🔥 RECENT WORK (Last 7 Days)`n`n"
    $markdown += "**$($recentFiles.Count) files modified:**`n`n"
    
    foreach ($file in $recentFiles | Select-Object -First 30) {
        $relPath = $file.DirectoryName.Replace($rootPath + "\", "")
        $date = $file.LastWriteTime.ToString("yyyy-MM-dd HH:mm")
        $markdown += "- **$($file.Name)** - $date`n"
        $markdown += "  - ``$relPath```n"
    }
    
    if ($recentFiles.Count -gt 30) {
        $markdown += "`n*...and $($recentFiles.Count - 30) more*`n"
    }
    
    $markdown += "`n---`n`n"
}

# Top folders by file count
$markdown += "## 📁 TOP FOLDERS`n`n"
$markdown += "**Most active folders:**`n`n"

foreach ($folder in $filesByFolder | Select-Object -First 20) {
    $folderName = $folder.Name.Replace($rootPath + "\", "")
    $markdown += "### $folderName`n"
    $markdown += "**$($folder.Count) files**`n`n"
    
    # Show file types in this folder
    $types = $folder.Group | Group-Object Extension | Sort-Object Count -Descending
    foreach ($t in $types) {
        $markdown += "- $($t.Name): $($t.Count)`n"
    }
    $markdown += "`n"
}

$markdown += "---`n`n"

# Key folders breakdown
$markdown += "## 🗂️ KEY FOLDERS DETAIL`n`n"

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
            $markdown += "### $keyFolder`n"
            $markdown += "**$($folderFiles.Count) files**`n`n"
            
            # Recent files in this folder (last 5)
            $recentInFolder = $folderFiles | Sort-Object LastWriteTime -Descending | Select-Object -First 5
            
            $markdown += "**Recent files:**`n"
            foreach ($file in $recentInFolder) {
                $date = $file.LastWriteTime.ToString("yyyy-MM-dd")
                $subPath = $file.DirectoryName.Replace($folderPath, "").TrimStart('\')
                if ($subPath) {
                    $markdown += "- $($file.Name) - $date - ``$subPath```n"
                } else {
                    $markdown += "- $($file.Name) - $date`n"
                }
            }
            
            $markdown += "`n"
        }
    }
}

$markdown += "---`n`n"

# Search guide
$markdown += @"
## 🔍 HOW TO USE THIS INDEX

### Quick Find:
- Press Ctrl+F to search
- Search for: file names, dates (YYYY-MM-DD), keywords

### Common Searches:
- Session from specific date: "2025-11-30"
- All protocols: "protocol"
- Scripts: ".ps1" or ".py"
- Recent sessions: Check "Recent Work" section above

### For Humans:
- Browse by folder sections
- Check "Recent Work" for latest files
- Look in "Top Folders" for most active areas

### For Claude:
- Search this document in project knowledge
- Use google_drive_search for content searches
- Reference exact folder paths from this index

---

## 🔄 UPDATE THIS INDEX

Regenerate anytime:

``````powershell
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center"
.\GENERATE_SMART_INDEX.ps1
``````

---

**Filtered index - showing what matters, hiding the noise**
"@

# Write to file
$markdown | Out-File -FilePath $outputFile -Encoding UTF8

Write-Host "================================================================================" -ForegroundColor Green
Write-Host "SMART INDEX COMPLETE" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "File saved to:" -ForegroundColor Green
Write-Host "  $outputFile" -ForegroundColor White
Write-Host ""
Write-Host "Useful files indexed: $($usefulFiles.Count)" -ForegroundColor Green
Write-Host "Duplicates filtered: $duplicatesFound" -ForegroundColor Yellow
Write-Host "Junk files filtered: $($allFiles.Count - $usefulFiles.Count - $duplicatesFound)" -ForegroundColor Yellow
Write-Host ""
Write-Host "This index is actually useful! 🎉" -ForegroundColor Cyan
Write-Host ""
