# Quick Version Save Script
# Saves timestamped copy of index.html
# Usage: .\save-version.ps1 [optional-description]

param(
    [string]$Description = ""
)

$CommandCenterPath = "G:\My Drive\00 - Trajanus USA\00-Command-Center"
$SourceFile = "$CommandCenterPath\index.html"

# Check if source exists
if (-not (Test-Path $SourceFile)) {
    Write-Host "ERROR: index.html not found in Command Center folder!" -ForegroundColor Red
    Write-Host "Looking for: $SourceFile" -ForegroundColor Yellow
    exit 1
}

# Create timestamp
$timestamp = Get-Date -Format "yyyy-MM-dd_HHmm"
$timestampedName = "index_$timestamp.html"

# Add description if provided
if ($Description) {
    $cleanDesc = $Description -replace '[^\w\s-]', '' -replace '\s+', '_'
    $timestampedName = "index_${timestamp}_${cleanDesc}.html"
}

$destPath = "$CommandCenterPath\$timestampedName"

# Copy file
try {
    Copy-Item $SourceFile -Destination $destPath -Force
    
    $fileSize = [math]::Round((Get-Item $destPath).Length / 1KB, 1)
    
    Write-Host ""
    Write-Host "✓ Version saved!" -ForegroundColor Green
    Write-Host "  File: $timestampedName" -ForegroundColor White
    Write-Host "  Size: $fileSize KB" -ForegroundColor Gray
    Write-Host "  Time: $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Gray
    Write-Host ""
    
} catch {
    Write-Host "ERROR: Failed to save version!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Yellow
    exit 1
}
