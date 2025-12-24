# Recursive File Converter - Converts ALL files in all subfolders
# Run from Command-Center folder where batch_convert_to_gdocs.py lives

param(
    [string]$RootPath = "G:\My Drive\00 - Trajanus USA"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "RECURSIVE CONVERSION - ALL FOLDERS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Root: $RootPath" -ForegroundColor Yellow
Write-Host ""

# Find all folders
$folders = Get-ChildItem -Path $RootPath -Recurse -Directory -ErrorAction SilentlyContinue

Write-Host "Found $($folders.Count) folders to process" -ForegroundColor Green
Write-Host ""

$totalConverted = 0
$totalFailed = 0

# Process root folder first
Write-Host "Processing ROOT folder..." -ForegroundColor Cyan
$mdFiles = Get-ChildItem -Path $RootPath -Filter "*.md" -File -ErrorAction SilentlyContinue
if ($mdFiles.Count -gt 0) {
    python "G:\My Drive\00 - Trajanus USA\00-Command-Center\batch_convert_to_gdocs.py" $RootPath
}

# Process each subfolder
foreach ($folder in $folders) {
    # Skip certain folders
    if ($folder.Name -match "^(Credentials|\.git|node_modules)$") {
        Write-Host "Skipping: $($folder.Name)" -ForegroundColor DarkGray
        continue
    }
    
    # Check if folder has .md files
    $mdFiles = Get-ChildItem -Path $folder.FullName -Filter "*.md" -File -ErrorAction SilentlyContinue
    
    if ($mdFiles.Count -gt 0) {
        $relativePath = $folder.FullName.Replace($RootPath, "").TrimStart('\')
        Write-Host ""
        Write-Host "Converting $($mdFiles.Count) files in: $relativePath" -ForegroundColor Yellow
        
        # Run conversion
        python "G:\My Drive\00 - Trajanus USA\00-Command-Center\batch_convert_to_gdocs.py" $folder.FullName
        
        if ($LASTEXITCODE -eq 0) {
            $totalConverted += $mdFiles.Count
        } else {
            $totalFailed += $mdFiles.Count
        }
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "CONVERSION COMPLETE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Total Converted: $totalConverted" -ForegroundColor Green
Write-Host "Total Failed: $totalFailed" -ForegroundColor Red
