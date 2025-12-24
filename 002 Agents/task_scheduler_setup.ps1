# Task Scheduler Setup for Trajanus Morning Research Agent
# Run this script as Administrator to create the scheduled task

$taskName = "Trajanus Morning Research"
$taskDescription = "Daily research agent for Trajanus Command Center - Runs at 6:00 AM"

# Paths
$pythonPath = "python"
$scriptPath = "G:\My Drive\00 - Trajanus USA\00-Command-Center\agents\morning_research_agent.py"
$workingDir = "G:\My Drive\00 - Trajanus USA\00-Command-Center\agents"
$logPath = "G:\My Drive\00 - Trajanus USA\00-Command-Center\logs"

# Ensure log directory exists
if (-not (Test-Path $logPath)) {
    New-Item -ItemType Directory -Path $logPath -Force
}

# Create the action
$action = New-ScheduledTaskAction `
    -Execute $pythonPath `
    -Argument "`"$scriptPath`"" `
    -WorkingDirectory $workingDir

# Create the trigger (6:00 AM daily)
$trigger = New-ScheduledTaskTrigger -Daily -At 6:00AM

# Create settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Hours 1)

# Principal (run whether user is logged on or not)
$principal = New-ScheduledTaskPrincipal `
    -UserId "$env:USERNAME" `
    -LogonType Interactive `
    -RunLevel Highest

# Check if task already exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

if ($existingTask) {
    Write-Host "Task '$taskName' already exists. Updating..." -ForegroundColor Yellow
    Set-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings
} else {
    Write-Host "Creating new task '$taskName'..." -ForegroundColor Green
    Register-ScheduledTask `
        -TaskName $taskName `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Principal $principal `
        -Description $taskDescription
}

Write-Host ""
Write-Host "Task setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Task Details:" -ForegroundColor Cyan
Write-Host "  Name: $taskName"
Write-Host "  Schedule: Daily at 6:00 AM"
Write-Host "  Script: $scriptPath"
Write-Host ""
Write-Host "To test the task now, run:" -ForegroundColor Yellow
Write-Host "  Start-ScheduledTask -TaskName '$taskName'"
Write-Host ""
Write-Host "To view task status:" -ForegroundColor Yellow
Write-Host "  Get-ScheduledTask -TaskName '$taskName' | Get-ScheduledTaskInfo"
Write-Host ""
Write-Host "To remove the task:" -ForegroundColor Yellow
Write-Host "  Unregister-ScheduledTask -TaskName '$taskName' -Confirm:`$false"
