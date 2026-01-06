# Check auto-reflect status
$stateFile = Join-Path $PSScriptRoot "reflect-state.txt"

if (Test-Path $stateFile) {
    $state = Get-Content $stateFile -Raw
    if ($state -match "enabled") {
        Write-Host "Auto-reflect is ENABLED"
    } else {
        Write-Host "Auto-reflect is DISABLED"
    }
} else {
    Write-Host "Auto-reflect is DISABLED (no state file)"
}
