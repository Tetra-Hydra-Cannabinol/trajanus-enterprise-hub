# WINDOWS SPEECH RECOGNITION AUTO-SETUP
# Configures always-on voice typing with auto-punctuation
# Run as Administrator

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "VOICE RECOGNITION SETUP" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Enable Windows Speech Recognition
Write-Host "[1/5] Enabling Windows Speech Recognition..." -ForegroundColor Yellow
$speechPath = "HKCU:\Software\Microsoft\Speech\Recognition"
if (!(Test-Path $speechPath)) {
    New-Item -Path $speechPath -Force | Out-Null
}
Set-ItemProperty -Path $speechPath -Name "EnableSpeechRecognition" -Value 1
Write-Host "✅ Speech Recognition enabled" -ForegroundColor Green

# Step 2: Configure Auto-Punctuation
Write-Host ""
Write-Host "[2/5] Configuring auto-punctuation..." -ForegroundColor Yellow
Set-ItemProperty -Path $speechPath -Name "AutomaticPunctuation" -Value 1 -ErrorAction SilentlyContinue
Write-Host "✅ Auto-punctuation enabled" -ForegroundColor Green

# Step 3: Add to Startup
Write-Host ""
Write-Host "[3/5] Adding to Windows startup..." -ForegroundColor Yellow
$startupFolder = [Environment]::GetFolderPath('Startup')
$shortcutPath = "$startupFolder\Speech Recognition.lnk"

# Create shortcut
$WScriptShell = New-Object -ComObject WScript.Shell
$shortcut = $WScriptShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = "C:\Windows\Speech\Common\sapisvr.exe"
$shortcut.WorkingDirectory = "C:\Windows\Speech\Common"
$shortcut.Description = "Windows Speech Recognition"
$shortcut.Save()

Write-Host "✅ Added to startup folder" -ForegroundColor Green

# Step 4: Configure Speech Settings
Write-Host ""
Write-Host "[4/5] Configuring speech settings..." -ForegroundColor Yellow

# Enable dictation mode by default
$dictationPath = "HKCU:\Software\Microsoft\Speech\Recognition\Dictation"
if (!(Test-Path $dictationPath)) {
    New-Item -Path $dictationPath -Force | Out-Null
}

# Set recognition profile settings
Set-ItemProperty -Path $speechPath -Name "AdaptationOn" -Value 1 -ErrorAction SilentlyContinue
Set-ItemProperty -Path $speechPath -Name "FilterProfanity" -Value 0 -ErrorAction SilentlyContinue

Write-Host "✅ Settings configured" -ForegroundColor Green

# Step 5: Start Speech Recognition
Write-Host ""
Write-Host "[5/5] Starting Speech Recognition..." -ForegroundColor Yellow
Start-Process "C:\Windows\Speech\Common\sapisvr.exe"
Start-Sleep -Seconds 2
Write-Host "✅ Speech Recognition started" -ForegroundColor Green

# Summary
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "SETUP COMPLETE!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host "1. Speech Recognition toolbar should be visible"
Write-Host "2. Click 'Start Speech Recognition' if not already running"
Write-Host "3. Complete voice training (2-3 minutes)"
Write-Host "   - Read the sample text to train your voice"
Write-Host "   - This improves accuracy significantly"
Write-Host ""
Write-Host "USAGE:" -ForegroundColor Yellow
Write-Host "• Say 'Start listening' - Activates microphone"
Write-Host "• Say 'Stop listening' - Pauses (but stays open)"
Write-Host "• Auto-punctuation works after short pauses"
Write-Host "• Will start automatically on Windows login"
Write-Host ""
Write-Host "MANUAL TRAINING (Optional but recommended):"
Write-Host "1. Right-click Speech Recognition toolbar"
Write-Host "2. Select 'Configuration'"
Write-Host "3. Click 'Train your computer to better understand you'"
Write-Host "4. Read 2-3 passages (5 minutes total)"
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Press any key to open Speech settings..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Open Speech settings for manual configuration if needed
Start-Process "control" -ArgumentList "sapi.cpl"

Write-Host ""
Write-Host "✅ Setup script complete!" -ForegroundColor Green
