# TRAJANUS FILE CONVERSION - 3 STEP PROCESS
# Location: G:\My Drive\00 - Trajanus USA\00-Command-Center\

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "TRAJANUS FILE CONVERSION WORKFLOW" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# STEP 1: SCAN
Write-Host "STEP 1: SCANNING FOR UNCONVERTED FILES" -ForegroundColor Yellow
Write-Host "---------------------------------------" -ForegroundColor Yellow

$rootPath = "G:\My Drive\00 - Trajanus USA"

# Count by type
$mdCount = (Get-ChildItem -Path $rootPath -Recurse -Filter "*.md" -ErrorAction SilentlyContinue).Count
$docxCount = (Get-ChildItem -Path $rootPath -Recurse -Filter "*.docx" -ErrorAction SilentlyContinue).Count
$xlsxCount = (Get-ChildItem -Path $rootPath -Recurse -Filter "*.xlsx" -ErrorAction SilentlyContinue).Count
$pptxCount = (Get-ChildItem -Path $rootPath -Recurse -Filter "*.pptx" -ErrorAction SilentlyContinue).Count

Write-Host ""
Write-Host "Markdown files (.md): $mdCount" -ForegroundColor White
Write-Host "Word docs (.docx): $docxCount" -ForegroundColor White
Write-Host "Excel files (.xlsx): $xlsxCount" -ForegroundColor White
Write-Host "PowerPoint files (.pptx): $pptxCount" -ForegroundColor White
Write-Host ""

$totalFiles = $mdCount + $docxCount + $xlsxCount + $pptxCount

if ($totalFiles -eq 0) {
    Write-Host "✅ NO FILES TO CONVERT - All done!" -ForegroundColor Green
    Write-Host ""
    exit
}

Write-Host "Total files to convert: $totalFiles" -ForegroundColor Yellow
Write-Host ""

# STEP 2: CONFIRM
Write-Host "STEP 2: CONFIRM CONVERSION" -ForegroundColor Yellow
Write-Host "--------------------------" -ForegroundColor Yellow
Write-Host ""
Write-Host "This will convert ALL unconverted files to Google Docs format." -ForegroundColor White
Write-Host ""
$response = Read-Host "Do you want to proceed? (Y/N)"

if ($response -ne "Y" -and $response -ne "y") {
    Write-Host ""
    Write-Host "Conversion cancelled." -ForegroundColor Red
    Write-Host ""
    exit
}

# STEP 3: CONVERT
Write-Host ""
Write-Host "STEP 3: CONVERTING FILES" -ForegroundColor Yellow
Write-Host "------------------------" -ForegroundColor Yellow
Write-Host ""

$convertedCount = 0
$failedCount = 0

# Get list of folders with unconverted files
Write-Host "Finding folders with files to convert..." -ForegroundColor Cyan
Write-Host ""

cd "$rootPath\00-Command-Center"

# Convert Markdown files by folder
Get-ChildItem -Path $rootPath -Directory | ForEach-Object {
    $folderPath = $_.FullName
    $mdFiles = Get-ChildItem -Path $folderPath -Recurse -Filter "*.md" -ErrorAction SilentlyContinue
    
    if ($mdFiles.Count -gt 0) {
        Write-Host "Converting $($mdFiles.Count) .md files in: $($_.Name)" -ForegroundColor White
        python batch_convert_to_gdocs.py $folderPath
        
        if ($LASTEXITCODE -eq 0) {
            $convertedCount += $mdFiles.Count
        } else {
            $failedCount += $mdFiles.Count
        }
    }
}

# Convert Office files (Excel/PowerPoint)
$officeFiles = @()
$officeFiles += Get-ChildItem -Path $rootPath -Recurse -Filter "*.xlsx" -ErrorAction SilentlyContinue
$officeFiles += Get-ChildItem -Path $rootPath -Recurse -Filter "*.pptx" -ErrorAction SilentlyContinue

if ($officeFiles.Count -gt 0) {
    Write-Host ""
    Write-Host "Converting $($officeFiles.Count) Excel/PowerPoint files..." -ForegroundColor White
    
    foreach ($file in $officeFiles) {
        python convert_office_to_google.py $file.FullName
        if ($LASTEXITCODE -eq 0) {
            $convertedCount++
        } else {
            $failedCount++
        }
    }
}

# Convert Word documents
$docxFiles = Get-ChildItem -Path $rootPath -Recurse -Filter "*.docx" -ErrorAction SilentlyContinue

if ($docxFiles.Count -gt 0) {
    Write-Host ""
    Write-Host "Converting $($docxFiles.Count) Word documents..." -ForegroundColor White
    
    foreach ($file in $docxFiles) {
        python convert_to_google_docs.py $file.FullName
        if ($LASTEXITCODE -eq 0) {
            $convertedCount++
        } else {
            $failedCount++
        }
    }
}

# RESULTS
Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "CONVERSION COMPLETE" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "✅ Converted: $convertedCount" -ForegroundColor Green
Write-Host "❌ Failed: $failedCount" -ForegroundColor Red
Write-Host ""

if ($failedCount -eq 0) {
    Write-Host "All files converted successfully!" -ForegroundColor Green
} else {
    Write-Host "Some files failed. Check output above for details." -ForegroundColor Yellow
}

Write-Host ""
