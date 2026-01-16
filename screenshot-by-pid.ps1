Add-Type @"
using System;
using System.Runtime.InteropServices;
public class User32 {
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")]
    public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    [DllImport("user32.dll")]
    public static extern IntPtr FindWindow(string lpClassName, string lpWindowName);
}
"@

# Get the trajanus process
$proc = Get-Process -Name "trajanus-command-center" -ErrorAction SilentlyContinue
if ($proc) {
    Write-Host "Found process: $($proc.Id)"
    Write-Host "MainWindowHandle: $($proc.MainWindowHandle)"
    Write-Host "MainWindowTitle: '$($proc.MainWindowTitle)'"

    if ($proc.MainWindowHandle -ne [IntPtr]::Zero) {
        [User32]::ShowWindow($proc.MainWindowHandle, 9) | Out-Null
        [User32]::SetForegroundWindow($proc.MainWindowHandle) | Out-Null
        Start-Sleep -Milliseconds 500
    } else {
        Write-Host "Window handle is zero - window may not be visible"
    }
} else {
    Write-Host "Process not found"
}

# Take screenshot
Add-Type -AssemblyName System.Windows.Forms
$bitmap = New-Object System.Drawing.Bitmap([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width, [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Location, [System.Drawing.Point]::Empty, [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Size)
$bitmap.Save('C:\Dev\trajanus-command-center\screenshot-pid.png')
Write-Host "Screenshot saved"
