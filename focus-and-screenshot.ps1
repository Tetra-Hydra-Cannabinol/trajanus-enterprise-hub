Add-Type @"
using System;
using System.Runtime.InteropServices;
public class User32 {
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")]
    public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
}
"@

# Find the Trajanus window
$process = Get-Process | Where-Object { $_.MainWindowTitle -like "*Trajanus*" -or $_.ProcessName -like "*trajanus*" } | Select-Object -First 1

if ($process) {
    $hwnd = $process.MainWindowHandle
    [User32]::ShowWindow($hwnd, 9)  # SW_RESTORE
    [User32]::SetForegroundWindow($hwnd)
    Start-Sleep -Seconds 1
}

# Take screenshot
Add-Type -AssemblyName System.Windows.Forms
$bitmap = New-Object System.Drawing.Bitmap([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width, [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Location, [System.Drawing.Point]::Empty, [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Size)
$bitmap.Save('C:\Dev\trajanus-command-center\screenshot-trajanus.png')
Write-Host 'Screenshot saved'
