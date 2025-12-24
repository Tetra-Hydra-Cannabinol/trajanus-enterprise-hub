# CONVERT_RESEARCH_FILES.ps1
# Converts markdown files from research folder to Google Docs format

param(
    [string]$SourceFolder = "G:\My Drive\00 - Trajanus USA\00-Command-Center\agents\research",
    [string]$OutputFolder = "G:\My Drive\00 - Trajanus USA\03-Living-Documents\Research-Findings"
)

Write-Host "=" -ForegroundColor Cyan -NoNewline
Write-Host ("=" * 78) -ForegroundColor Cyan
Write-Host "RESEARCH FINDINGS CONVERTER" -ForegroundColor Yellow
Write-Host "=" -ForegroundColor Cyan -NoNewline
Write-Host ("=" * 78) -ForegroundColor Cyan

# Check source folder
if (!(Test-Path $SourceFolder)) {
    Write-Host "[ERROR] Source folder not found: $SourceFolder" -ForegroundColor Red
    exit 1
}

# Create output folder if needed
if (!(Test-Path $OutputFolder)) {
    Write-Host "[CREATE] Output folder: $OutputFolder" -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $OutputFolder -Force | Out-Null
}

# Get all markdown files
$mdFiles = Get-ChildItem -Path $SourceFolder -Filter "*.md" | Sort-Object Name
$totalFiles = $mdFiles.Count

Write-Host "`n[FOUND] $totalFiles markdown files to convert`n" -ForegroundColor Green

if ($totalFiles -eq 0) {
    Write-Host "[WARNING] No markdown files found in $SourceFolder" -ForegroundColor Yellow
    exit 0
}

# Process each file
$converted = 0
$skipped = 0

foreach ($file in $mdFiles) {
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
    $docxPath = Join-Path $SourceFolder "$baseName.docx"
    
    Write-Host "[PROCESS] $($file.Name)" -ForegroundColor Cyan
    
    # Convert markdown to DOCX using pandoc
    try {
        & pandoc $file.FullName -o $docxPath 2>&1 | Out-Null
        
        if (Test-Path $docxPath) {
            Write-Host "  ✓ Converted to DOCX" -ForegroundColor Green
            
            # Move DOCX to output folder
            $finalPath = Join-Path $OutputFolder "$baseName.docx"
            Move-Item -Path $docxPath -Destination $finalPath -Force
            Write-Host "  ✓ Moved to: $OutputFolder" -ForegroundColor Green
            
            $converted++
        } else {
            Write-Host "  ✗ Conversion failed" -ForegroundColor Red
            $skipped++
        }
    }
    catch {
        Write-Host "  ✗ Error: $_" -ForegroundColor Red
        $skipped++
    }
    
    Write-Host ""
}

# Summary
Write-Host "=" -ForegroundColor Cyan -NoNewline
Write-Host ("=" * 78) -ForegroundColor Cyan
Write-Host "CONVERSION COMPLETE" -ForegroundColor Yellow
Write-Host "=" -ForegroundColor Cyan -NoNewline
Write-Host ("=" * 78) -ForegroundColor Cyan
Write-Host "`nTotal Files: $totalFiles" -ForegroundColor White
Write-Host "Converted: $converted" -ForegroundColor Green
Write-Host "Skipped: $skipped" -ForegroundColor $(if ($skipped -gt 0) { "Red" } else { "Green" })
Write-Host "`nOutput Location: $OutputFolder" -ForegroundColor Cyan
Write-Host "`n[NEXT STEP] Google Drive Desktop will sync these DOCX files" -ForegroundColor Yellow
Write-Host "[THEN] Claude can read them as Google Docs" -ForegroundColor Yellow
Write-Host ""
