# CONVERT_NEW_FILES_ONLY.ps1
# Smart conversion - only converts files modified in last 24 hours

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "SMART FILE CONVERSION (NEW FILES ONLY)" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

$rootPath = "G:\My Drive\00 - Trajanus USA"
$cutoffTime = (Get-Date).AddHours(-24)

Write-Host "Looking for files modified after: $($cutoffTime.ToString())" -ForegroundColor Cyan
Write-Host ""

# Find NEW files only (modified in last 24 hours)
$newMdFiles = Get-ChildItem -Path $rootPath -Recurse -Filter "*.md" -ErrorAction SilentlyContinue | 
    Where-Object { $_.LastWriteTime -gt $cutoffTime }

$newDocxFiles = Get-ChildItem -Path $rootPath -Recurse -Filter "*.docx" -ErrorAction SilentlyContinue | 
    Where-Object { $_.LastWriteTime -gt $cutoffTime }

$newOfficeFiles = @()
$newOfficeFiles += Get-ChildItem -Path $rootPath -Recurse -Filter "*.xlsx" -ErrorAction SilentlyContinue | 
    Where-Object { $_.LastWriteTime -gt $cutoffTime }
$newOfficeFiles += Get-ChildItem -Path $rootPath -Recurse -Filter "*.pptx" -ErrorAction SilentlyContinue | 
    Where-Object { $_.LastWriteTime -gt $cutoffTime }

$totalNewFiles = $newMdFiles.Count + $newDocxFiles.Count + $newOfficeFiles.Count

Write-Host "New markdown files: $($newMdFiles.Count)" -ForegroundColor White
Write-Host "New Word docs: $($newDocxFiles.Count)" -ForegroundColor White  
Write-Host "New Excel/PowerPoint: $($newOfficeFiles.Count)" -ForegroundColor White
Write-Host ""
Write-Host "Total NEW files to convert: $totalNewFiles" -ForegroundColor Yellow
Write-Host ""

if ($totalNewFiles -eq 0) {
    Write-Host "✅ NO NEW FILES TO CONVERT" -ForegroundColor Green
    Write-Host ""
    exit
}

# Convert new files by their parent folders
Write-Host "Converting NEW files..." -ForegroundColor Yellow
Write-Host ""

cd "$rootPath\00-Command-Center"

$convertedCount = 0
$failedCount = 0

# Group markdown files by folder and convert
$newMdFiles | Group-Object DirectoryName | ForEach-Object {
    $folderPath = $_.Name
    $fileCount = $_.Count
    
    Write-Host "Converting $fileCount new .md file(s) in: $(Split-Path $folderPath -Leaf)" -ForegroundColor White
    python batch_convert_to_gdocs.py $folderPath
    
    if ($LASTEXITCODE -eq 0) {
        $convertedCount += $fileCount
    } else {
        $failedCount += $fileCount
    }
}

# Convert new Office files individually  
if ($newOfficeFiles.Count -gt 0) {
    Write-Host ""
    Write-Host "Converting $($newOfficeFiles.Count) new Excel/PowerPoint file(s)..." -ForegroundColor White
    
    foreach ($file in $newOfficeFiles) {
        Write-Host "  - $($file.Name)" -ForegroundColor Gray
        python convert_office_to_google.py $file.FullName
        
        if ($LASTEXITCODE -eq 0) {
            $convertedCount++
        } else {
            $failedCount++
        }
    }
}

# Summary
Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "CONVERSION COMPLETE" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "✅ Converted: $convertedCount" -ForegroundColor Green
if ($failedCount -gt 0) {
    Write-Host "❌ Failed: $failedCount" -ForegroundColor Red
}
Write-Host ""
