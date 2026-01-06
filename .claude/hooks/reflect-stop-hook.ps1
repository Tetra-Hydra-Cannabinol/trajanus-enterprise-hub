# Reflect Stop Hook for Claude Code
# Triggers optional session reflection when Claude stops
# Toggle with: reflect-on / reflect-off commands or REFLECT_ENABLED env var

$ErrorActionPreference = "SilentlyContinue"

# Check if reflection is enabled
$reflectStateFile = Join-Path $PSScriptRoot "reflect-state.txt"
$reflectEnabled = $false

# Check state file first
if (Test-Path $reflectStateFile) {
    $state = Get-Content $reflectStateFile -Raw
    if ($state -match "enabled") {
        $reflectEnabled = $true
    }
}

# Environment variable override
if ($env:REFLECT_ENABLED -eq "true") {
    $reflectEnabled = $true
}
if ($env:REFLECT_ENABLED -eq "false") {
    $reflectEnabled = $false
}

# Read input from stdin (Claude Code passes JSON)
$stdinContent = [Console]::In.ReadToEnd()
$hookData = $null

try {
    $hookData = $stdinContent | ConvertFrom-Json
} catch {
    # If parsing fails, just exit
    exit 0
}

# Prevent infinite loops - don't trigger if already in a stop hook
# Handle both boolean true and string "true" from JSON
if ($hookData.stop_hook_active -eq $true -or $hookData.stop_hook_active -eq "true" -or $hookData.stop_hook_active -eq "True") {
    # Output approve to let Claude stop
    Write-Output '{"decision": "approve"}'
    exit 0
}

# If reflection is not enabled, approve stop
if (-not $reflectEnabled) {
    Write-Output '{"decision": "approve"}'
    exit 0
}

# Reflection is enabled - block stop and request reflection
$reason = @"
AUTO-REFLECT TRIGGERED: Before ending this session, please run /reflect to capture any learnings, corrections, or patterns from this conversation. After reflection is complete, you may stop.

If there are no meaningful learnings to capture, acknowledge this and stop.
"@

$response = @{
    decision = "block"
    reason = $reason
} | ConvertTo-Json -Compress

Write-Output $response
