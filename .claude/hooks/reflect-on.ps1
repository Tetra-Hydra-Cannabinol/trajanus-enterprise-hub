# Enable auto-reflect on session stop
$stateFile = Join-Path $PSScriptRoot "reflect-state.txt"
"enabled" | Out-File -FilePath $stateFile -Encoding UTF8 -NoNewline
Write-Host "Auto-reflect ENABLED - /reflect will be prompted at session end"
