# fix_emoji_encoding.ps1
# Run this in the Command Center folder to fix garbled emojis in index.html
# Usage: .\fix_emoji_encoding.ps1

$file = "index.html"
$content = Get-Content $file -Raw -Encoding UTF8

# Replace common broken emoji patterns with clean text
$replacements = @{
    # These are the garbled patterns -> clean replacements
    [regex]::Escape('ðŸ"š') = ''
    [regex]::Escape('ðŸ"˜') = ''
    [regex]::Escape('ðŸ"‚') = ''
    [regex]::Escape('ðŸ"') = ''
    [regex]::Escape('ðŸ"‹') = ''
    [regex]::Escape('ðŸ"¤') = ''
    [regex]::Escape('ðŸ¤–') = ''
    [regex]::Escape('ðŸ'ï¸') = ''
    [regex]::Escape('ðŸŽ¨') = ''
    [regex]::Escape('ðŸ') = ''
    [regex]::Escape('ðŸ"Š') = ''
    [regex]::Escape('ðŸ"–') = ''
    [regex]::Escape('ðŸ"—') = ''
    'â€"' = '—'
    'â€"' = '–'
    'â†'' = '→'
    'â–²' = '▲'
    'â–¼' = '▼'
    'â€¢' = '•'
    'Ã—' = '×'
}

foreach ($pattern in $replacements.Keys) {
    $content = $content -replace $pattern, $replacements[$pattern]
}

# Save with UTF-8 encoding (with BOM for Windows compatibility)
$utf8WithBom = New-Object System.Text.UTF8Encoding $true
[System.IO.File]::WriteAllText($file, $content, $utf8WithBom)

Write-Host "Emoji encoding fixed in $file" -ForegroundColor Green
