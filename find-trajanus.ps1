Get-Process | Where-Object { $_.ProcessName -like "*trajanus*" } | ForEach-Object {
    Write-Host "ProcessName: $($_.ProcessName)"
    Write-Host "MainWindowHandle: $($_.MainWindowHandle)"
    Write-Host "MainWindowTitle: '$($_.MainWindowTitle)'"
    Write-Host "---"
}
