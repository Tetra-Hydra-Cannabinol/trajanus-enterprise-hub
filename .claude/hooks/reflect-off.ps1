# Disable auto-reflect on session stop
$stateFile = Join-Path $PSScriptRoot "reflect-state.txt"
"disabled" | Out-File -FilePath $stateFile -Encoding UTF8 -NoNewline
Write-Host "Auto-reflect DISABLED - sessions will end without reflection prompt"
