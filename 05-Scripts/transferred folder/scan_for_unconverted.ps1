# Scan for Unconverted Files
# Finds all .docx and .md files that need conversion to Google Docs

param(
    [string]$RootPath = "G:\My Drive\00 - Trajanus USA"
)

Write-Host "Scanning for unconverted files in: $RootPath" -ForegroundColor Cyan
Write-Host ""

# Find all .docx files
$docxFiles = Get-ChildItem -Path $RootPath -Recurse -Filter "*.docx" -File -ErrorAction SilentlyContinue
$mdFiles = Get-ChildItem -Path $RootPath -Recurse -Filter "*.md" -File -ErrorAction SilentlyContinue

Write-Host "=== UNCONVERTED FILES REPORT ===" -ForegroundColor Yellow
Write-Host ""

Write-Host "Word Documents (.docx): $($docxFiles.Count)" -ForegroundColor Green
Write-Host "Markdown Files (.md): $($mdFiles.Count)" -ForegroundColor Green
Write-Host "Total Files: $($docxFiles.Count + $mdFiles.Count)" -ForegroundColor Green
Write-Host ""

# Group by folder
Write-Host "=== BY FOLDER ===" -ForegroundColor Yellow
Write-Host ""

$allFiles = $docxFiles + $mdFiles
$byFolder = $allFiles | Group-Object DirectoryName | Sort-Object Count -Descending

foreach ($folder in $byFolder) {
    $relativePath = $folder.Name.Replace($RootPath, "").TrimStart('\')
    if ([string]::IsNullOrEmpty($relativePath)) { $relativePath = "(Root)" }
    Write-Host "$($folder.Count) files in: $relativePath" -ForegroundColor White
}

Write-Host ""
Write-Host "=== SUMMARY ===" -ForegroundColor Yellow
Write-Host "Run recursive conversion? Use: .\convert_all_recursive.ps1" -ForegroundColor Cyan
