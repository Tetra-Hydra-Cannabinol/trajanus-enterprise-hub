# RALPH Stop Hook - Recursive Auto-Loop Prompt Handler
# Checks for completion signal and re-triggers if not found

param()

# Read hook input from stdin
$hookInput = $input | Out-String

try {
    $data = $hookInput | ConvertFrom-Json
    $transcriptPath = $data.transcript_path
    $sessionId = $data.session_id
    $stopHookActive = $data.stop_hook_active
} catch {
    # Not valid JSON, allow normal stop
    exit 0
}

# State file location
$stateFile = "$env:TEMP\ralph-state-$sessionId.json"

# If no state file exists, this isn't a RALPH session - allow normal stop
if (-not (Test-Path $stateFile)) {
    exit 0
}

# Read state
try {
    $state = Get-Content $stateFile -Raw | ConvertFrom-Json
    $iteration = [int]$state.iteration
    $maxIterations = [int]$state.max_iterations
    $signal = $state.signal
    $prompt = $state.prompt
} catch {
    # Invalid state file, clean up and exit
    Remove-Item $stateFile -Force -ErrorAction SilentlyContinue
    exit 0
}

# Check if transcript contains the completion signal
$signalFound = $false

if ($transcriptPath -and (Test-Path $transcriptPath)) {
    $transcriptContent = Get-Content $transcriptPath -Raw -ErrorAction SilentlyContinue
    if ($transcriptContent) {
        if ($transcriptContent -match [regex]::Escape($signal)) {
            $signalFound = $true
        }
        # Also check for RALPH_SIGNAL_FOUND marker
        if ($transcriptContent -match "RALPH_SIGNAL_FOUND") {
            $signalFound = $true
        }
    }
}

# If signal found, clean up and allow stop
if ($signalFound) {
    Remove-Item $stateFile -Force -ErrorAction SilentlyContinue
    Write-Host "RALPH: Completion signal '$signal' found after $iteration iteration(s)" -ForegroundColor Green
    exit 0
}

# Check if max iterations reached
if ($iteration -ge $maxIterations) {
    Remove-Item $stateFile -Force -ErrorAction SilentlyContinue
    Write-Host "RALPH: Max iterations ($maxIterations) reached without finding signal '$signal'" -ForegroundColor Yellow
    exit 0
}

# Increment iteration and save state
$newIteration = $iteration + 1
$newState = @{
    iteration = $newIteration
    max_iterations = $maxIterations
    signal = $signal
    prompt = $prompt
} | ConvertTo-Json -Compress

$newState | Out-File -FilePath $stateFile -Encoding utf8 -Force

# Block stop and re-prompt
$response = @{
    decision = "block"
    reason = "RALPH Iteration $newIteration/$maxIterations`: Completion signal '$signal' not found. Continue working on: $prompt"
} | ConvertTo-Json -Compress

Write-Output $response
exit 0
