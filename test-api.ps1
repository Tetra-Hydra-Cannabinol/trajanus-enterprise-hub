# Test Anthropic API - reads key from environment variable
# Set ANTHROPIC_API_KEY environment variable before running

$apiKey = $env:ANTHROPIC_API_KEY
if (-not $apiKey) {
    Write-Error "ANTHROPIC_API_KEY environment variable not set"
    exit 1
}

$headers = @{
    "x-api-key" = $apiKey
    "anthropic-version" = "2023-06-01"
    "content-type" = "application/json"
}

$body = '{"model":"claude-sonnet-4-20250514","max_tokens":100,"messages":[{"role":"user","content":"hello"}]}'

Invoke-RestMethod -Uri "https://api.anthropic.com/v1/messages" -Method Post -Headers $headers -Body $body
