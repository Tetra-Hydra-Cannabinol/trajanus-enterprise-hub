# SEARCH_FILES.ps1
# Interactive file search tool for Trajanus USA

param(
    [string]$SearchTerm = ""
)

$rootPath = "G:\My Drive\00 - Trajanus USA"

function Show-Menu {
    Write-Host ""
    Write-Host "================================================================================" -ForegroundColor Cyan
    Write-Host "TRAJANUS FILE SEARCH" -ForegroundColor Cyan
    Write-Host "================================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Search Options:" -ForegroundColor Yellow
    Write-Host "  1. Search by filename" -ForegroundColor White
    Write-Host "  2. Search by date (recent files)" -ForegroundColor White
    Write-Host "  3. Search by file type (.md, .docx, etc.)" -ForegroundColor White
    Write-Host "  4. Search by folder" -ForegroundColor White
    Write-Host "  5. Show recent session files" -ForegroundColor White
    Write-Host "  6. List all folders" -ForegroundColor White
    Write-Host "  Q. Quit" -ForegroundColor White
    Write-Host ""
}

function Search-ByName {
    param([string]$term)
    
    Write-Host ""
    Write-Host "Searching for: '$term'" -ForegroundColor Yellow
    Write-Host ""
    
    $results = Get-ChildItem -Path $rootPath -Recurse -Filter "*$term*" -File -ErrorAction SilentlyContinue
    
    if ($results.Count -eq 0) {
        Write-Host "No files found matching '$term'" -ForegroundColor Red
        return
    }
    
    Write-Host "Found $($results.Count) file(s):" -ForegroundColor Green
    Write-Host ""
    
    $i = 1
    foreach ($file in $results) {
        $relPath = $file.FullName.Replace($rootPath + "\", "")
        $size = if ($file.Length -lt 1KB) { 
            "$($file.Length) B" 
        } elseif ($file.Length -lt 1MB) { 
            "{0:N1} KB" -f ($file.Length / 1KB) 
        } else { 
            "{0:N1} MB" -f ($file.Length / 1MB) 
        }
        
        Write-Host "[$i] $($file.Name)" -ForegroundColor Cyan
        Write-Host "    Path: $relPath" -ForegroundColor Gray
        Write-Host "    Size: $size | Modified: $($file.LastWriteTime.ToString('yyyy-MM-dd HH:mm'))" -ForegroundColor Gray
        Write-Host ""
        $i++
    }
    
    Write-Host "Copy path? Enter number (1-$($results.Count)) or press Enter to continue: " -NoNewline
    $choice = Read-Host
    
    if ($choice -match '^\d+$' -and [int]$choice -le $results.Count) {
        $selectedFile = $results[[int]$choice - 1]
        Set-Clipboard -Value $selectedFile.FullName
        Write-Host "✓ Path copied to clipboard!" -ForegroundColor Green
    }
}

function Search-RecentFiles {
    param([int]$days = 7)
    
    Write-Host ""
    Write-Host "Files modified in last $days days:" -ForegroundColor Yellow
    Write-Host ""
    
    $cutoff = (Get-Date).AddDays(-$days)
    $results = Get-ChildItem -Path $rootPath -Recurse -File -ErrorAction SilentlyContinue | 
        Where-Object { $_.LastWriteTime -gt $cutoff } | 
        Sort-Object LastWriteTime -Descending
    
    if ($results.Count -eq 0) {
        Write-Host "No recent files found" -ForegroundColor Red
        return
    }
    
    Write-Host "Found $($results.Count) file(s):" -ForegroundColor Green
    Write-Host ""
    
    foreach ($file in $results | Select-Object -First 30) {
        $relPath = $file.FullName.Replace($rootPath + "\", "")
        $date = $file.LastWriteTime.ToString("yyyy-MM-dd HH:mm")
        
        Write-Host "• $($file.Name)" -ForegroundColor Cyan
        Write-Host "  $relPath" -ForegroundColor Gray
        Write-Host "  Modified: $date" -ForegroundColor Gray
        Write-Host ""
    }
    
    if ($results.Count -gt 30) {
        Write-Host "*...and $($results.Count - 30) more*" -ForegroundColor Yellow
    }
}

function Search-ByType {
    Write-Host ""
    Write-Host "Common file types:" -ForegroundColor Yellow
    Write-Host "  1. .md (Markdown)" -ForegroundColor White
    Write-Host "  2. .docx (Word)" -ForegroundColor White
    Write-Host "  3. .xlsx (Excel)" -ForegroundColor White
    Write-Host "  4. .pptx (PowerPoint)" -ForegroundColor White
    Write-Host "  5. .pdf" -ForegroundColor White
    Write-Host "  6. .ps1 (PowerShell)" -ForegroundColor White
    Write-Host "  7. .py (Python)" -ForegroundColor White
    Write-Host ""
    Write-Host "Enter file extension (e.g., .md): " -NoNewline
    $ext = Read-Host
    
    if (-not $ext.StartsWith('.')) {
        $ext = ".$ext"
    }
    
    Write-Host ""
    Write-Host "Searching for $ext files..." -ForegroundColor Yellow
    Write-Host ""
    
    $results = Get-ChildItem -Path $rootPath -Recurse -Filter "*$ext" -File -ErrorAction SilentlyContinue
    
    if ($results.Count -eq 0) {
        Write-Host "No $ext files found" -ForegroundColor Red
        return
    }
    
    Write-Host "Found $($results.Count) file(s)" -ForegroundColor Green
    Write-Host ""
    
    # Group by folder
    $byFolder = $results | Group-Object DirectoryName | Sort-Object Count -Descending
    
    foreach ($group in $byFolder | Select-Object -First 20) {
        $folderName = $group.Name.Replace($rootPath + "\", "")
        Write-Host "[$($group.Count) files] $folderName" -ForegroundColor Cyan
    }
    
    if ($byFolder.Count -gt 20) {
        Write-Host ""
        Write-Host "*...and $($byFolder.Count - 20) more folders*" -ForegroundColor Yellow
    }
}

function Show-SessionFiles {
    Write-Host ""
    Write-Host "Recent Session Files:" -ForegroundColor Yellow
    Write-Host ""
    
    # Check common session locations
    $sessionFolders = @(
        "08-EOS-Files",
        "07-Session-Journal\Session-Summaries",
        "07-Session-Journal\Technical-Journals",
        "07-Session-Journal\Personal-Diaries"
    )
    
    foreach ($folder in $sessionFolders) {
        $fullPath = Join-Path $rootPath $folder
        
        if (Test-Path $fullPath) {
            $files = Get-ChildItem -Path $fullPath -File -ErrorAction SilentlyContinue | 
                Sort-Object LastWriteTime -Descending | 
                Select-Object -First 5
            
            if ($files.Count -gt 0) {
                Write-Host "$folder (latest 5):" -ForegroundColor Cyan
                foreach ($file in $files) {
                    $date = $file.LastWriteTime.ToString("yyyy-MM-dd")
                    Write-Host "  • $($file.Name) - $date" -ForegroundColor White
                }
                Write-Host ""
            }
        }
    }
}

function Show-AllFolders {
    Write-Host ""
    Write-Host "All Folders:" -ForegroundColor Yellow
    Write-Host ""
    
    $folders = Get-ChildItem -Path $rootPath -Directory -Recurse -ErrorAction SilentlyContinue | 
        Sort-Object FullName
    
    foreach ($folder in $folders) {
        $relPath = $folder.FullName.Replace($rootPath + "\", "")
        $fileCount = (Get-ChildItem -Path $folder.FullName -File -ErrorAction SilentlyContinue).Count
        
        Write-Host "📁 $relPath" -ForegroundColor Cyan
        Write-Host "   ($fileCount files)" -ForegroundColor Gray
    }
    
    Write-Host ""
    Write-Host "Total folders: $($folders.Count)" -ForegroundColor Green
}

# Main loop
if ($SearchTerm) {
    # Direct search mode
    Search-ByName -term $SearchTerm
    exit
}

while ($true) {
    Show-Menu
    $choice = Read-Host "Select option"
    
    switch ($choice.ToUpper()) {
        "1" {
            Write-Host ""
            $term = Read-Host "Enter search term"
            Search-ByName -term $term
            Read-Host "Press Enter to continue"
        }
        "2" {
            Write-Host ""
            $days = Read-Host "How many days back? (default: 7)"
            if (-not $days) { $days = 7 }
            Search-RecentFiles -days $days
            Read-Host "Press Enter to continue"
        }
        "3" {
            Search-ByType
            Read-Host "Press Enter to continue"
        }
        "4" {
            Show-AllFolders
            Read-Host "Press Enter to continue"
        }
        "5" {
            Show-SessionFiles
            Read-Host "Press Enter to continue"
        }
        "6" {
            Show-AllFolders
            Read-Host "Press Enter to continue"
        }
        "Q" {
            Write-Host ""
            Write-Host "Goodbye!" -ForegroundColor Green
            Write-Host ""
            exit
        }
        default {
            Write-Host ""
            Write-Host "Invalid option. Please try again." -ForegroundColor Red
        }
    }
}
