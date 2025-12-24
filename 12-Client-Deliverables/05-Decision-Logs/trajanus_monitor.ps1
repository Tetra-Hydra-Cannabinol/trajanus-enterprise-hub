<#
.SYNOPSIS
    Trajanus USA Knowledge Base - Live Processing Monitor v2.0

.DESCRIPTION
    Real-time dashboard for YouTube knowledge ingestion
    Displays progress, statistics, and activity log with Trajanus USA branding

.PARAMETER Compact
    Use compact display mode for smaller windows

.EXAMPLE
    .\trajanus_monitor.ps1
    .\trajanus_monitor.ps1 -Compact

.NOTES
    Author: Trajanus USA Development Team
    Date: December 20, 2025
    Version: 2.0
#>

param(
    [switch]$Compact
)

# Force UTF-8 output
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# ============================================================================
# BRAND COLORS
# ============================================================================

$Brand = @{
    Gold       = 'Yellow'
    DeepBlue   = 'DarkBlue'
    Success    = 'Green'
    Processing = 'Cyan'
    Warning    = 'Yellow'
    Error      = 'Red'
    Header     = 'White'
    Text       = 'Gray'
    Border     = 'DarkGray'
    Accent     = 'DarkCyan'
}

# ============================================================================
# CONFIGURATION
# ============================================================================

$Config = @{
    LogFile        = "G:\My Drive\00 - Trajanus USA\00-Command-Center\05-Scripts\LIVE_PROGRESS.log"
    RefreshSeconds = 2
    LogTailLines   = 25
    BoxWidth       = 68
}

# Box drawing characters (using Unicode)
$Box = @{
    TL = [char]0x250C  # Top-left corner
    TR = [char]0x2510  # Top-right corner
    BL = [char]0x2514  # Bottom-left corner
    BR = [char]0x2518  # Bottom-right corner
    H  = [char]0x2500  # Horizontal line
    V  = [char]0x2502  # Vertical line
    LT = [char]0x251C  # Left T
    RT = [char]0x2524  # Right T
    DH = [char]0x2550  # Double horizontal
    DV = [char]0x2551  # Double vertical
    DTL = [char]0x2554 # Double top-left
    DTR = [char]0x2557 # Double top-right
    DBL = [char]0x255A # Double bottom-left
    DBR = [char]0x255D # Double bottom-right
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

function Write-BoxTop {
    $line = $Box.H.ToString() * $Config.BoxWidth
    Write-Host "  $($Box.TL)$line$($Box.TR)" -ForegroundColor $Brand.Border
}

function Write-BoxBottom {
    $line = $Box.H.ToString() * $Config.BoxWidth
    Write-Host "  $($Box.BL)$line$($Box.BR)" -ForegroundColor $Brand.Border
}

function Write-BoxDivider {
    $line = $Box.H.ToString() * $Config.BoxWidth
    Write-Host "  $($Box.LT)$line$($Box.RT)" -ForegroundColor $Brand.Border
}

function Write-PaddedLine {
    param(
        [string]$Text,
        [string]$Color = $Brand.Text,
        [int]$Indent = 2
    )
    $spaces = " " * $Indent
    $available = $Config.BoxWidth - $Indent
    if ($Text.Length -gt $available) {
        $Text = $Text.Substring(0, $available - 3) + "..."
    }
    $padding = " " * ($available - $Text.Length)
    Write-Host "  $($Box.V)$spaces" -NoNewline -ForegroundColor $Brand.Border
    Write-Host $Text -NoNewline -ForegroundColor $Color
    Write-Host "$padding$($Box.V)" -ForegroundColor $Brand.Border
}

# ============================================================================
# LOGO DISPLAY
# ============================================================================

function Show-Logo {
    $dh = $Box.DH
    $dv = $Box.DV

    if ($Compact) {
        # Compact header
        Write-Host ""
        $line = $dh.ToString() * 70
        Write-Host "  $line" -ForegroundColor $Brand.DeepBlue
        Write-Host "  $dv  " -NoNewline -ForegroundColor $Brand.DeepBlue
        Write-Host "TRAJANUS USA" -NoNewline -ForegroundColor $Brand.Gold
        Write-Host " - Knowledge Base Monitor" -NoNewline -ForegroundColor $Brand.Header
        Write-Host "                          $dv" -ForegroundColor $Brand.DeepBlue
        Write-Host "  $line" -ForegroundColor $Brand.DeepBlue
    } else {
        # Full ASCII art logo
        Write-Host ""
        $line = $dh.ToString() * 68
        Write-Host "  $($Box.DTL)$line$($Box.DTR)" -ForegroundColor $Brand.DeepBlue
        Write-Host "  $dv                                                                    $dv" -ForegroundColor $Brand.DeepBlue

        # TRAJANUS ASCII art
        Write-Host "  $dv  " -NoNewline -ForegroundColor $Brand.DeepBlue
        Write-Host "TTTTTT RRRR    AAA       JJ   AAA  N   N U   U  SSSS" -NoNewline -ForegroundColor $Brand.Gold
        Write-Host "             $dv" -ForegroundColor $Brand.DeepBlue

        Write-Host "  $dv  " -NoNewline -ForegroundColor $Brand.DeepBlue
        Write-Host "  TT   R   R  A   A      JJ  A   A NN  N U   U S    " -NoNewline -ForegroundColor $Brand.Gold
        Write-Host "             $dv" -ForegroundColor $Brand.DeepBlue

        Write-Host "  $dv  " -NoNewline -ForegroundColor $Brand.DeepBlue
        Write-Host "  TT   RRRR   AAAAA      JJ  AAAAA N N N U   U  SSS " -NoNewline -ForegroundColor $Brand.Gold
        Write-Host "             $dv" -ForegroundColor $Brand.DeepBlue

        Write-Host "  $dv  " -NoNewline -ForegroundColor $Brand.DeepBlue
        Write-Host "  TT   R  R   A   A  J   J   A   A N  NN U   U     S" -NoNewline -ForegroundColor $Brand.Gold
        Write-Host "             $dv" -ForegroundColor $Brand.DeepBlue

        Write-Host "  $dv  " -NoNewline -ForegroundColor $Brand.DeepBlue
        Write-Host "  TT   R   R  A   A   JJJ    A   A N   N  UUU  SSSS " -NoNewline -ForegroundColor $Brand.Gold
        Write-Host "             $dv" -ForegroundColor $Brand.DeepBlue

        Write-Host "  $dv                                                                    $dv" -ForegroundColor $Brand.DeepBlue
        Write-Host "  $dv           " -NoNewline -ForegroundColor $Brand.DeepBlue
        Write-Host "KNOWLEDGE BASE PROCESSING MONITOR" -NoNewline -ForegroundColor $Brand.Header
        Write-Host "                    $dv" -ForegroundColor $Brand.DeepBlue
        Write-Host "  $dv        " -NoNewline -ForegroundColor $Brand.DeepBlue
        Write-Host "AI-Augmented Construction Management Excellence" -NoNewline -ForegroundColor $Brand.Text
        Write-Host "         $dv" -ForegroundColor $Brand.DeepBlue
        Write-Host "  $($Box.DBL)$line$($Box.DBR)" -ForegroundColor $Brand.DeepBlue
    }
    Write-Host ""
}

# ============================================================================
# TIME DISPLAY
# ============================================================================

function Show-TimeHeader {
    $time = Get-Date -Format 'HH:mm:ss'
    $date = Get-Date -Format 'dddd, MMMM dd, yyyy'
    Write-Host "  Time: " -NoNewline -ForegroundColor $Brand.Text
    Write-Host $time -NoNewline -ForegroundColor $Brand.Gold
    Write-Host " | " -NoNewline -ForegroundColor $Brand.Border
    Write-Host $date -NoNewline -ForegroundColor $Brand.Text
    Write-Host " | " -NoNewline -ForegroundColor $Brand.Border
    Write-Host "High Springs, FL" -ForegroundColor $Brand.Accent
    Write-Host ""
}

# ============================================================================
# PROGRESS BAR
# ============================================================================

function Show-ProgressBar {
    param([int]$Current, [int]$Total)

    if ($Total -eq 0) { return }

    $percent = [math]::Round(($Current / $Total) * 100)
    $barWidth = 40
    $filled = [math]::Floor(($percent / 100) * $barWidth)
    $empty = $barWidth - $filled

    # Use block characters for progress bar
    $filledChar = [char]0x2588  # Full block
    $emptyChar = [char]0x2591   # Light shade
    $bar = ($filledChar.ToString() * $filled) + ($emptyChar.ToString() * $empty)

    # Determine color based on progress
    $barColor = if ($percent -lt 30) { $Brand.Warning }
                elseif ($percent -lt 100) { $Brand.Processing }
                else { $Brand.Success }

    Write-BoxTop
    Write-Host "  $($Box.V)  " -NoNewline -ForegroundColor $Brand.Border
    Write-Host "PROGRESS " -NoNewline -ForegroundColor $Brand.Header
    Write-Host "[$bar]" -NoNewline -ForegroundColor $barColor

    # Right-align percentage
    $pctText = " $percent%"
    $remainingSpace = $Config.BoxWidth - 10 - $barWidth - 2 - $pctText.Length
    if ($remainingSpace -lt 0) { $remainingSpace = 1 }
    Write-Host (" " * $remainingSpace) -NoNewline
    Write-Host $pctText -NoNewline -ForegroundColor $Brand.Gold
    Write-Host " $($Box.V)" -ForegroundColor $Brand.Border

    # Video count line
    $vidText = "Videos: $Current of $Total completed"
    Write-Host "  $($Box.V)  " -NoNewline -ForegroundColor $Brand.Border
    Write-Host "Videos: " -NoNewline -ForegroundColor $Brand.Text
    Write-Host $Current -NoNewline -ForegroundColor $Brand.Gold
    Write-Host " of " -NoNewline -ForegroundColor $Brand.Text
    Write-Host $Total -NoNewline -ForegroundColor $Brand.Gold
    Write-Host " completed" -NoNewline -ForegroundColor $Brand.Text
    $padding = " " * ($Config.BoxWidth - 2 - $vidText.Length)
    Write-Host "$padding$($Box.V)" -ForegroundColor $Brand.Border

    Write-BoxBottom
    Write-Host ""
}

# ============================================================================
# STATISTICS PANEL
# ============================================================================

function Show-Statistics {
    param($Content)

    # Count occurrences
    $successCount = 0
    $failCount = 0
    $processingCount = 0

    foreach ($line in $Content) {
        if ($line -match 'SUCCESS') { $successCount++ }
        if ($line -match 'FAILED|ERROR') { $failCount++ }
        if ($line -match 'PROCESSING') { $processingCount++ }
    }

    Write-BoxTop
    Write-PaddedLine "SESSION STATISTICS" $Brand.Header
    Write-BoxDivider

    # Success
    $successText = "Completed: $successCount videos"
    $padLen = $Config.BoxWidth - 5 - 4 - $successText.Length
    if ($padLen -lt 1) { $padLen = 1 }
    Write-Host "  $($Box.V)    " -NoNewline -ForegroundColor $Brand.Border
    Write-Host "[OK]" -NoNewline -ForegroundColor $Brand.Success
    Write-Host " $successText" -NoNewline -ForegroundColor $Brand.Success
    Write-Host (" " * $padLen) -NoNewline
    Write-Host "$($Box.V)" -ForegroundColor $Brand.Border

    # Processing
    $procText = "Processing: $processingCount videos"
    $padLen = $Config.BoxWidth - 5 - 4 - $procText.Length
    if ($padLen -lt 1) { $padLen = 1 }
    Write-Host "  $($Box.V)    " -NoNewline -ForegroundColor $Brand.Border
    Write-Host "[..]" -NoNewline -ForegroundColor $Brand.Processing
    Write-Host " $procText" -NoNewline -ForegroundColor $Brand.Processing
    Write-Host (" " * $padLen) -NoNewline
    Write-Host "$($Box.V)" -ForegroundColor $Brand.Border

    # Failed (only if any)
    if ($failCount -gt 0) {
        $failText = "Failed: $failCount videos"
        $padLen = $Config.BoxWidth - 5 - 4 - $failText.Length
        if ($padLen -lt 1) { $padLen = 1 }
        Write-Host "  $($Box.V)    " -NoNewline -ForegroundColor $Brand.Border
        Write-Host "[XX]" -NoNewline -ForegroundColor $Brand.Error
        Write-Host " $failText" -NoNewline -ForegroundColor $Brand.Error
        Write-Host (" " * $padLen) -NoNewline
        Write-Host "$($Box.V)" -ForegroundColor $Brand.Border
    }

    Write-BoxBottom
    Write-Host ""
}

# ============================================================================
# LOG DISPLAY
# ============================================================================

function Show-LogEntries {
    param($Content)

    Write-BoxTop
    Write-PaddedLine "LIVE ACTIVITY LOG" $Brand.Header
    Write-BoxDivider

    $maxLines = if ($Compact) { 10 } else { 15 }
    $lines = @($Content | Select-Object -Last $maxLines)

    foreach ($line in $lines) {
        if ([string]::IsNullOrWhiteSpace($line)) { continue }

        # Timestamp lines [HH:MM:SS]
        if ($line -match '^\[(\d{2}:\d{2}:\d{2})\](.*)$') {
            $timestamp = $matches[1]
            $rest = $matches[2]

            # Determine color based on content
            $lineColor = $Brand.Text
            if ($line -match 'SUCCESS') { $lineColor = $Brand.Success }
            elseif ($line -match 'PROCESSING') { $lineColor = $Brand.Processing }
            elseif ($line -match 'FAILED|ERROR') { $lineColor = $Brand.Error }
            elseif ($line -match 'CHUNKING|EMBEDDING') { $lineColor = $Brand.Warning }

            # Truncate if needed
            $maxRest = $Config.BoxWidth - 12
            if ($rest.Length -gt $maxRest) {
                $rest = $rest.Substring(0, $maxRest - 3) + "..."
            }

            $padLen = $Config.BoxWidth - 3 - $timestamp.Length - $rest.Length
            if ($padLen -lt 0) { $padLen = 0 }

            Write-Host "  $($Box.V)  " -NoNewline -ForegroundColor $Brand.Border
            Write-Host $timestamp -NoNewline -ForegroundColor $Brand.Accent
            Write-Host " " -NoNewline
            Write-Host $rest -NoNewline -ForegroundColor $lineColor
            Write-Host (" " * $padLen) -NoNewline
            Write-Host "$($Box.V)" -ForegroundColor $Brand.Border
        }
        # Separator lines (double horizontal)
        elseif ($line -match '^[=]+$') {
            $sep = $Box.H.ToString() * ($Config.BoxWidth - 4)
            Write-Host "  $($Box.V)  $sep  $($Box.V)" -ForegroundColor $Brand.Border
        }
        # Detail lines (indented)
        else {
            $text = $line.Trim()
            if ($text.Length -gt 0) {
                $maxText = $Config.BoxWidth - 6
                if ($text.Length -gt $maxText) {
                    $text = $text.Substring(0, $maxText - 3) + "..."
                }
                $padLen = $Config.BoxWidth - 4 - $text.Length
                if ($padLen -lt 0) { $padLen = 0 }
                Write-Host "  $($Box.V)    " -NoNewline -ForegroundColor $Brand.Border
                Write-Host $text -NoNewline -ForegroundColor $Brand.Text
                Write-Host (" " * $padLen) -NoNewline
                Write-Host "$($Box.V)" -ForegroundColor $Brand.Border
            }
        }
    }

    Write-BoxBottom
}

# ============================================================================
# WAITING STATE
# ============================================================================

function Show-WaitingState {
    param([string]$Message = "Waiting for activity...")

    Write-BoxTop
    Write-PaddedLine $Message $Brand.Processing
    Write-BoxDivider

    # Animated dots based on second
    $dotCount = ((Get-Date).Second % 4) + 1
    $dots = "." * $dotCount
    Write-PaddedLine "Monitoring$dots" $Brand.Text
    Write-BoxBottom
}

# ============================================================================
# MAIN LOOP
# ============================================================================

# Initial display
Clear-Host
Show-Logo
Write-Host "  Starting monitor..." -ForegroundColor $Brand.Processing
Start-Sleep -Seconds 1

while ($true) {
    Clear-Host
    Show-Logo
    Show-TimeHeader

    if (Test-Path $Config.LogFile) {
        try {
            $content = @(Get-Content $Config.LogFile -Tail $Config.LogTailLines -ErrorAction Stop)

            if ($content -and $content.Count -gt 0) {
                # Find latest progress indicator [X/Y]
                $progressLines = @($content | Where-Object { $_ -match '\[(\d+)/(\d+)\]' })
                if ($progressLines.Count -gt 0) {
                    $lastProgress = $progressLines[-1]
                    if ($lastProgress -match '\[(\d+)/(\d+)\]') {
                        $current = [int]$matches[1]
                        $total = [int]$matches[2]
                        Show-ProgressBar -Current $current -Total $total
                    }
                }

                Show-Statistics -Content $content
                Show-LogEntries -Content $content
            }
            else {
                Show-WaitingState "Log file is empty - waiting for activity..."
            }
        }
        catch {
            Show-WaitingState "Error reading log: $($_.Exception.Message)"
        }
    }
    else {
        Show-WaitingState "Log file not found - will be created when processing starts"
    }

    Write-Host ""
    Write-Host "  Press " -NoNewline -ForegroundColor $Brand.Text
    Write-Host "Ctrl+C" -NoNewline -ForegroundColor $Brand.Gold
    Write-Host " to exit  |  Refreshing every $($Config.RefreshSeconds)s" -ForegroundColor $Brand.Text
    Write-Host ""

    Start-Sleep -Seconds $Config.RefreshSeconds
}
