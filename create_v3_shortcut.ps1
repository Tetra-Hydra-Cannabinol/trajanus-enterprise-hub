$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("C:\Users\owner\Desktop\Trajanus v3.lnk")
$Shortcut.TargetPath = "C:\Dev\trajanus-command-center\src-tauri\target\release\trajanus-command-center-v3.exe"
$Shortcut.WorkingDirectory = "C:\Dev\trajanus-command-center"
$Shortcut.IconLocation = "C:\Dev\trajanus-command-center\src-tauri\icons\icon.ico"
$Shortcut.Description = "Trajanus Command Center v3 - Production Build"
$Shortcut.Save()
Write-Host "Shortcut created: Trajanus v3.lnk"
