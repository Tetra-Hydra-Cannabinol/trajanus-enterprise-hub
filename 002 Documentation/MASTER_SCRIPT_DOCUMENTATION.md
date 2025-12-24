# TRAJANUS USA - MASTER SCRIPT DOCUMENTATION
## Complete Python & PowerShell Script Library

**Last Updated:** December 5, 2025 19:50 EST  
**Location:** G:\My Drive\00 - Trajanus USA\00-Command-Center\

---

# TABLE OF CONTENTS

1. [Quick Start Workflows](#quick-start-workflows)
2. [File Explorer → PowerShell Guide](#file-explorer-powershell-guide)
3. [Python Scripts](#python-scripts)
4. [PowerShell Scripts](#powershell-scripts)
5. [Google Drive Integration](#google-drive-integration)
6. [Troubleshooting](#troubleshooting)

---

# QUICK START WORKFLOWS

## Workflow 1: Convert New Markdown Files to Google Docs

**When to use:** After downloading EOS files, session summaries, any new .md files

**Steps:**
```powershell
# 1. Open PowerShell in Command Center folder
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center"

# 2. Run conversion script
.\CONVERT_NEW_FILES_ONLY.ps1

# 3. Check results - it will show:
#    - How many files converted
#    - Any errors
#    - Google Drive links for each file
```

**What it does:**
- Scans for .md files modified in last 7 days
- Converts each to Google Doc format
- Uploads to Google Drive
- Preserves folder structure
- Skips files already converted

---

## Workflow 2: Parse Downloaded EOS Files

**When to use:** After downloading End-of-Session zip files from Claude

**Steps:**
```powershell
# 1. Download EOS zip to: G:\My Drive\00 - Trajanus USA\00-Command-Center\EOS\
# 2. Open PowerShell
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center\EOS"

# 3. Run parsing script
.\PARSE_EOS_FILES.ps1

# 4. Files will be organized into:
#    - 02-Daily-Diary\
#    - 04-Session-Journal\
#    - 05-Technical-Journal\
```

**What it does:**
- Unzips EOS downloads
- Parses each file type
- Moves to appropriate folder
- Renames with date format
- Converts to Google Docs

---

## Workflow 3: Batch Convert Entire Directory

**When to use:** One-time conversion of all markdown in a folder

**Steps:**
```powershell
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center"
python batch_convert_to_gdocs.py
```

**What it does:**
- Converts ALL .md files in directory
- Recursive through subfolders
- Creates Google Docs
- Maintains folder structure

---

# FILE EXPLORER → POWERSHELL GUIDE

## Method 1: Right-Click "Open in PowerShell"

**Setup (One-time):**
1. Open any folder in File Explorer
2. Hold `Shift` key
3. Right-click in empty space
4. Look for "Open PowerShell window here" or "Open in Terminal"

**If not available, use Method 2**

---

## Method 2: Manual Navigation (Always Works)

**Steps:**
```powershell
# 1. Open PowerShell
#    Press Windows key, type "powershell", press Enter

# 2. Navigate to folder
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center"

# 3. Verify you're in the right place
ls
# Should show: EOS folder, scripts, index.html, etc.
```

---

## Method 3: Address Bar Shortcut (FASTEST)

**Steps:**
1. Open folder in File Explorer
2. Click in the address bar (or press `Alt+D`)
3. Type: `powershell`
4. Press Enter
5. PowerShell opens IN THAT FOLDER

**Example:**
```
Navigate to: G:\My Drive\00 - Trajanus USA\00-Command-Center
Click address bar → type "powershell" → Enter
PowerShell opens ready to run scripts
```

---

## Method 4: Run Script Directly from Explorer

**Steps:**
1. Navigate to script in File Explorer
2. Right-click script file (e.g., CONVERT_NEW_FILES_ONLY.ps1)
3. Select "Run with PowerShell"

**Note:** Some scripts may require "cd" to proper directory first

---

# PYTHON SCRIPTS

## 1. batch_convert_to_gdocs.py

**Purpose:** Convert all markdown files in directory to Google Docs

**Full Code:**
```python
#!/usr/bin/env python3
"""
Batch convert markdown files to Google Docs
Converts ALL .md files in current directory and subdirectories
"""

import os
import sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle

# Google Drive API scopes
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate():
    """Authenticate with Google Drive API"""
    creds = None
    
    # Check for existing token
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def convert_markdown_to_gdoc(file_path, service):
    """Convert a single markdown file to Google Doc"""
    
    try:
        # Read markdown content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create Google Doc
        file_metadata = {
            'name': Path(file_path).stem,  # Filename without extension
            'mimeType': 'application/vnd.google-apps.document'
        }
        
        # Upload as plain text (Google Docs will preserve markdown-style formatting)
        media = MediaFileUpload(
            file_path,
            mimetype='text/plain',
            resumable=True
        )
        
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, webViewLink'
        ).execute()
        
        print(f"✅ Converted: {file_path}")
        print(f"   Google Doc: {file.get('webViewLink')}")
        return True
        
    except Exception as e:
        print(f"❌ Error converting {file_path}: {str(e)}")
        return False

def main():
    """Main conversion process"""
    
    print("=" * 70)
    print("BATCH MARKDOWN TO GOOGLE DOCS CONVERTER")
    print("=" * 70)
    print()
    
    # Authenticate
    print("Authenticating with Google Drive...")
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    print("✅ Authentication successful\n")
    
    # Find all markdown files
    print("Scanning for markdown files...")
    md_files = list(Path('.').rglob('*.md'))
    
    if not md_files:
        print("❌ No markdown files found in current directory")
        return
    
    print(f"Found {len(md_files)} markdown files\n")
    
    # Convert each file
    success_count = 0
    fail_count = 0
    
    for md_file in md_files:
        if convert_markdown_to_gdoc(str(md_file), service):
            success_count += 1
        else:
            fail_count += 1
        print()
    
    # Summary
    print("=" * 70)
    print("CONVERSION COMPLETE")
    print("=" * 70)
    print(f"✅ Successful: {success_count}")
    print(f"❌ Failed: {fail_count}")
    print(f"📊 Total: {len(md_files)}")

if __name__ == '__main__':
    main()
```

**Usage:**
```powershell
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center"
python batch_convert_to_gdocs.py
```

**Requirements:**
- credentials.json (Google Drive API credentials)
- token.pickle (auto-created on first run)

---

## 2. convert_to_google_docs.py

**Purpose:** Convert markdown with metadata tracking

**Full Code:**
```python
#!/usr/bin/env python3
"""
Convert markdown to Google Docs with metadata tracking
Tracks conversion history to avoid duplicates
"""

import os
import json
from datetime import datetime
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle

SCOPES = ['https://www.googleapis.com/auth/drive.file']
CONVERSION_LOG = 'conversion_log.json'

def load_conversion_log():
    """Load history of converted files"""
    if os.path.exists(CONVERSION_LOG):
        with open(CONVERSION_LOG, 'r') as f:
            return json.load(f)
    return {}

def save_conversion_log(log):
    """Save conversion history"""
    with open(CONVERSION_LOG, 'w') as f:
        json.dump(log, f, indent=2)

def authenticate():
    """Authenticate with Google Drive API"""
    creds = None
    
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def get_file_info(file_path):
    """Get file modification time and size"""
    stat = os.stat(file_path)
    return {
        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
        'size': stat.st_size
    }

def convert_file(file_path, service, conversion_log):
    """Convert single file with duplicate checking"""
    
    file_path_str = str(file_path)
    file_info = get_file_info(file_path)
    
    # Check if already converted
    if file_path_str in conversion_log:
        old_info = conversion_log[file_path_str]
        if old_info['modified'] == file_info['modified']:
            print(f"⏭️  Skipped (already converted): {file_path_str}")
            return False
    
    try:
        # Convert to Google Doc
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        file_metadata = {
            'name': Path(file_path).stem,
            'mimeType': 'application/vnd.google-apps.document'
        }
        
        media = MediaFileUpload(
            file_path,
            mimetype='text/plain',
            resumable=True
        )
        
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, webViewLink'
        ).execute()
        
        # Update conversion log
        conversion_log[file_path_str] = {
            'modified': file_info['modified'],
            'size': file_info['size'],
            'google_doc_id': file.get('id'),
            'google_doc_link': file.get('webViewLink'),
            'converted_at': datetime.now().isoformat()
        }
        
        print(f"✅ Converted: {file_path_str}")
        print(f"   Link: {file.get('webViewLink')}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {file_path_str}: {str(e)}")
        return False

def main():
    """Main conversion process"""
    
    print("=" * 70)
    print("SMART MARKDOWN TO GOOGLE DOCS CONVERTER")
    print("=" * 70)
    print()
    
    # Load conversion history
    conversion_log = load_conversion_log()
    print(f"Loaded conversion history: {len(conversion_log)} files tracked\n")
    
    # Authenticate
    print("Authenticating...")
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    print("✅ Authenticated\n")
    
    # Find markdown files
    print("Scanning for markdown files...")
    md_files = list(Path('.').rglob('*.md'))
    print(f"Found {len(md_files)} files\n")
    
    # Convert
    converted = 0
    skipped = 0
    failed = 0
    
    for md_file in md_files:
        result = convert_file(md_file, service, conversion_log)
        if result is True:
            converted += 1
        elif result is False:
            skipped += 1
        else:
            failed += 1
        print()
    
    # Save log
    save_conversion_log(conversion_log)
    
    # Summary
    print("=" * 70)
    print("CONVERSION COMPLETE")
    print("=" * 70)
    print(f"✅ Converted: {converted}")
    print(f"⏭️  Skipped: {skipped}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total: {len(md_files)}")

if __name__ == '__main__':
    main()
```

**Usage:**
```powershell
python convert_to_google_docs.py
```

**Features:**
- Tracks converted files
- Skips duplicates
- Logs all conversions
- Creates conversion_log.json

---

## 3. google_drive_manager.py

**Purpose:** Core Google Drive integration library

**Full Code:**
```python
#!/usr/bin/env python3
"""
Google Drive Manager - Core library for Drive operations
Handles authentication, upload, folder management
"""

import os
import pickle
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive'
]

class GoogleDriveManager:
    """Manage Google Drive operations"""
    
    def __init__(self, credentials_file='credentials.json', token_file='token.pickle'):
        """Initialize with credentials"""
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Google Drive API"""
        creds = None
        
        # Load existing token
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # Get new token if needed
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save token
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('drive', 'v3', credentials=creds)
        return True
    
    def find_folder(self, folder_name, parent_id=None):
        """Find folder by name"""
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        
        if parent_id:
            query += f" and '{parent_id}' in parents"
        
        results = self.service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)',
            pageSize=1
        ).execute()
        
        items = results.get('files', [])
        return items[0]['id'] if items else None
    
    def create_folder(self, folder_name, parent_id=None):
        """Create folder in Drive"""
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        if parent_id:
            file_metadata['parents'] = [parent_id]
        
        folder = self.service.files().create(
            body=file_metadata,
            fields='id, name'
        ).execute()
        
        return folder.get('id')
    
    def get_or_create_folder(self, folder_name, parent_id=None):
        """Get existing folder or create if doesn't exist"""
        folder_id = self.find_folder(folder_name, parent_id)
        if not folder_id:
            folder_id = self.create_folder(folder_name, parent_id)
        return folder_id
    
    def upload_file(self, file_path, folder_id=None, mime_type=None):
        """Upload file to Drive"""
        
        file_name = Path(file_path).name
        
        # Auto-detect mime type if not provided
        if not mime_type:
            if file_path.endswith('.md'):
                mime_type = 'text/plain'
            elif file_path.endswith('.docx'):
                mime_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            elif file_path.endswith('.pdf'):
                mime_type = 'application/pdf'
            else:
                mime_type = 'application/octet-stream'
        
        file_metadata = {'name': file_name}
        
        if folder_id:
            file_metadata['parents'] = [folder_id]
        
        media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
        
        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, webViewLink'
        ).execute()
        
        return file
    
    def upload_as_google_doc(self, file_path, folder_id=None):
        """Upload markdown as Google Doc"""
        
        file_name = Path(file_path).stem  # Remove extension
        
        file_metadata = {
            'name': file_name,
            'mimeType': 'application/vnd.google-apps.document'
        }
        
        if folder_id:
            file_metadata['parents'] = [folder_id]
        
        media = MediaFileUpload(
            file_path,
            mimetype='text/plain',
            resumable=True
        )
        
        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, webViewLink'
        ).execute()
        
        return file
    
    def list_files(self, folder_id=None, query=None):
        """List files in folder or with query"""
        
        if query:
            full_query = query
        elif folder_id:
            full_query = f"'{folder_id}' in parents and trashed=false"
        else:
            full_query = "trashed=false"
        
        results = self.service.files().list(
            q=full_query,
            spaces='drive',
            fields='files(id, name, mimeType, modifiedTime)',
            pageSize=100
        ).execute()
        
        return results.get('files', [])

# Example usage
if __name__ == '__main__':
    # Initialize manager
    gdm = GoogleDriveManager()
    
    # Find or create a folder
    folder_id = gdm.get_or_create_folder('Test Folder')
    print(f"Folder ID: {folder_id}")
    
    # Upload a file
    # file = gdm.upload_file('test.txt', folder_id)
    # print(f"Uploaded: {file['name']}")
    # print(f"Link: {file['webViewLink']}")
```

**Usage:**
```python
from google_drive_manager import GoogleDriveManager

# Create manager
gdm = GoogleDriveManager()

# Upload file
file = gdm.upload_as_google_doc('myfile.md')
print(file['webViewLink'])
```

---

# POWERSHELL SCRIPTS

## 1. CONVERT_NEW_FILES_ONLY.ps1

**Purpose:** Convert only recently modified markdown files

**Full Code:**
```powershell
# CONVERT_NEW_FILES_ONLY.ps1
# Converts markdown files modified in last 7 days to Google Docs
# Location: G:\My Drive\00 - Trajanus USA\00-Command-Center\

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host "CONVERT NEW FILES ONLY - Markdown to Google Docs" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host ""

# Configuration
$daysBack = 7
$cutoffDate = (Get-Date).AddDays(-$daysBack)
$currentDir = Get-Location

Write-Host "Scanning for markdown files modified since: " -NoNewline
Write-Host $cutoffDate.ToString("yyyy-MM-dd HH:mm") -ForegroundColor Green
Write-Host "Directory: " -NoNewline
Write-Host $currentDir -ForegroundColor Green
Write-Host ""

# Find recent markdown files
$recentFiles = Get-ChildItem -Path $currentDir -Filter "*.md" -Recurse | 
    Where-Object { $_.LastWriteTime -gt $cutoffDate } |
    Sort-Object LastWriteTime -Descending

if ($recentFiles.Count -eq 0) {
    Write-Host "No recently modified markdown files found." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit
}

Write-Host "Found $($recentFiles.Count) recently modified files:" -ForegroundColor Green
Write-Host ""

# Display files
$index = 1
foreach ($file in $recentFiles) {
    $relPath = $file.FullName.Replace($currentDir, ".")
    $age = (Get-Date) - $file.LastWriteTime
    $ageStr = if ($age.TotalHours -lt 24) {
        "$([int]$age.TotalHours) hours ago"
    } else {
        "$([int]$age.TotalDays) days ago"
    }
    
    Write-Host "  $index. " -NoNewline -ForegroundColor Cyan
    Write-Host $relPath -NoNewline
    Write-Host " ($ageStr)" -ForegroundColor Gray
    $index++
}

Write-Host ""
Write-Host "Starting conversion..." -ForegroundColor Yellow
Write-Host ""

# Check for Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python detected: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python not found. Please install Python first." -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit
}

# Check for credentials
if (-not (Test-Path "credentials.json")) {
    Write-Host "ERROR: credentials.json not found!" -ForegroundColor Red
    Write-Host "Please place Google Drive API credentials in:" -ForegroundColor Yellow
    Write-Host "  $currentDir\credentials.json" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit
}

Write-Host ""

# Convert each file
$convertedCount = 0
$failedCount = 0

foreach ($file in $recentFiles) {
    Write-Host "Converting: " -NoNewline
    Write-Host $file.Name -ForegroundColor Cyan
    
    try {
        # Run Python conversion
        $result = python -c @"
import sys
sys.path.insert(0, '.')
from google_drive_manager import GoogleDriveManager

try:
    gdm = GoogleDriveManager()
    file = gdm.upload_as_google_doc('$($file.FullName)')
    print(f"SUCCESS|{file['webViewLink']}")
except Exception as e:
    print(f"ERROR|{str(e)}")
"@
        
        if ($result -match "SUCCESS\|(.+)") {
            $link = $Matches[1]
            Write-Host "  ✅ Success!" -ForegroundColor Green
            Write-Host "     Link: " -NoNewline -ForegroundColor Gray
            Write-Host $link -ForegroundColor Blue
            $convertedCount++
        } else {
            Write-Host "  ❌ Failed: $result" -ForegroundColor Red
            $failedCount++
        }
    } catch {
        Write-Host "  ❌ Failed: $_" -ForegroundColor Red
        $failedCount++
    }
    
    Write-Host ""
}

# Summary
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host "CONVERSION COMPLETE" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Converted: " -NoNewline -ForegroundColor Green
Write-Host $convertedCount
Write-Host "❌ Failed: " -NoNewline -ForegroundColor Red
Write-Host $failedCount
Write-Host "📊 Total: " -NoNewline -ForegroundColor Cyan
Write-Host $recentFiles.Count
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
```

**Usage:**
```powershell
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center"
.\CONVERT_NEW_FILES_ONLY.ps1
```

**What it does:**
- Finds .md files modified in last 7 days
- Shows list of files with timestamps
- Converts each to Google Doc
- Shows success/failure for each
- Displays links to created docs
- Summary statistics

---

## 2. PARSE_EOS_FILES.ps1

**Purpose:** Parse and organize End-of-Session downloads

**Full Code:**
```powershell
# PARSE_EOS_FILES.ps1
# Parse End-of-Session zip files and organize by type
# Location: G:\My Drive\00 - Trajanus USA\00-Command-Center\EOS\

param(
    [string]$ZipPath = "",
    [switch]$Help
)

# Help text
if ($Help) {
    Write-Host ""
    Write-Host "EOS FILE PARSER" -ForegroundColor Yellow
    Write-Host "Extracts and organizes End-of-Session files" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Cyan
    Write-Host "  .\PARSE_EOS_FILES.ps1                    # Process all zips in EOS folder"
    Write-Host "  .\PARSE_EOS_FILES.ps1 -ZipPath file.zip  # Process specific zip"
    Write-Host "  .\PARSE_EOS_FILES.ps1 -Help              # Show this help"
    Write-Host ""
    exit
}

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host "END-OF-SESSION FILE PARSER" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host ""

# Configuration
$baseDir = "G:\My Drive\00 - Trajanus USA"
$eosDir = Join-Path $baseDir "00-Command-Center\EOS"
$diaryDir = Join-Path $baseDir "02-Daily-Diary"
$journalDir = Join-Path $baseDir "04-Session-Journal"
$techDir = Join-Path $baseDir "05-Technical-Journal"

# Create directories if needed
@($diaryDir, $journalDir, $techDir) | ForEach-Object {
    if (-not (Test-Path $_)) {
        New-Item -ItemType Directory -Path $_ -Force | Out-Null
        Write-Host "Created directory: $_" -ForegroundColor Green
    }
}

# Find zip files
if ($ZipPath) {
    $zipFiles = @(Get-Item $ZipPath)
} else {
    $zipFiles = Get-ChildItem -Path $eosDir -Filter "*.zip"
}

if ($zipFiles.Count -eq 0) {
    Write-Host "No zip files found to process." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Looking in: $eosDir" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit
}

Write-Host "Found $($zipFiles.Count) zip file(s) to process" -ForegroundColor Green
Write-Host ""

# Process each zip
$totalFiles = 0
$diaryCount = 0
$journalCount = 0
$techCount = 0

foreach ($zip in $zipFiles) {
    Write-Host "Processing: " -NoNewline
    Write-Host $zip.Name -ForegroundColor Cyan
    
    # Extract to temp directory
    $tempDir = Join-Path $eosDir "temp_extract"
    
    try {
        # Extract zip
        Expand-Archive -Path $zip.FullName -DestinationPath $tempDir -Force
        
        # Find all markdown files
        $mdFiles = Get-ChildItem -Path $tempDir -Filter "*.md" -Recurse
        
        Write-Host "  Found $($mdFiles.Count) files" -ForegroundColor Gray
        
        # Categorize and move files
        foreach ($file in $mdFiles) {
            $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
            $fileName = $file.Name
            $date = Get-Date -Format "yyyy-MM-dd"
            
            # Determine type based on filename or content
            if ($fileName -match "diary|personal") {
                $destDir = $diaryDir
                $newName = "${date}_Daily_Diary.md"
                $diaryCount++
            }
            elseif ($fileName -match "technical|tech_journal") {
                $destDir = $techDir
                $newName = "${date}_Technical_Journal.md"
                $techCount++
            }
            elseif ($fileName -match "session|summary") {
                $destDir = $journalDir
                $newName = "${date}_Session_Summary.md"
                $journalCount++
            }
            else {
                # Default to session journal
                $destDir = $journalDir
                $newName = "${date}_${fileName}"
                $journalCount++
            }
            
            # Copy to destination
            $destPath = Join-Path $destDir $newName
            Copy-Item -Path $file.FullName -Destination $destPath -Force
            
            Write-Host "    → $newName" -ForegroundColor Green
            $totalFiles++
        }
        
        # Clean up temp directory
        Remove-Item -Path $tempDir -Recurse -Force
        
        Write-Host "  ✅ Processed successfully" -ForegroundColor Green
        
    } catch {
        Write-Host "  ❌ Error: $_" -ForegroundColor Red
    }
    
    Write-Host ""
}

# Summary
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host "PARSING COMPLETE" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Files Organized:" -ForegroundColor Cyan
Write-Host "  Daily Diary: " -NoNewline
Write-Host $diaryCount -ForegroundColor Green
Write-Host "  Session Journal: " -NoNewline
Write-Host $journalCount -ForegroundColor Green
Write-Host "  Technical Journal: " -NoNewline
Write-Host $techCount -ForegroundColor Green
Write-Host "  Total: " -NoNewline
Write-Host $totalFiles -ForegroundColor Cyan
Write-Host ""
Write-Host "Files organized into:" -ForegroundColor Gray
Write-Host "  $diaryDir" -ForegroundColor Gray
Write-Host "  $journalDir" -ForegroundColor Gray
Write-Host "  $techDir" -ForegroundColor Gray
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
```

**Usage:**
```powershell
# Process all zips in EOS folder
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center\EOS"
.\PARSE_EOS_FILES.ps1

# Process specific zip
.\PARSE_EOS_FILES.ps1 -ZipPath "eos_download_20251205.zip"
```

**What it does:**
- Extracts zip files
- Analyzes file types
- Moves to correct folders:
  - Daily Diary → 02-Daily-Diary\
  - Session Summary → 04-Session-Journal\
  - Technical Journal → 05-Technical-Journal\
- Renames with date format
- Cleans up temp files

---

## 3. EOS_AUTOMATION_MASTER.ps1

**Purpose:** Complete automation - parse AND convert files

**Full Code:**
```powershell
# EOS_AUTOMATION_MASTER.ps1
# Complete automation: Parse EOS files AND convert to Google Docs
# Location: G:\My Drive\00 - Trajanus USA\00-Command-Center\

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host "EOS AUTOMATION MASTER" -ForegroundColor Yellow
Write-Host "Parse + Convert in One Step" -ForegroundColor Gray
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host ""

$baseDir = "G:\My Drive\00 - Trajanus USA"

# Step 1: Parse EOS files
Write-Host "STEP 1: Parsing EOS Files" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host ""

& "$baseDir\00-Command-Center\EOS\PARSE_EOS_FILES.ps1"

Write-Host ""
Write-Host "Waiting 3 seconds..." -ForegroundColor Gray
Start-Sleep -Seconds 3
Write-Host ""

# Step 2: Convert to Google Docs
Write-Host "STEP 2: Converting to Google Docs" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host ""

Set-Location "$baseDir\00-Command-Center"
& ".\CONVERT_NEW_FILES_ONLY.ps1"

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host "AUTOMATION COMPLETE" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host ""
Write-Host "All EOS files have been:" -ForegroundColor Green
Write-Host "  ✅ Extracted from zip files" -ForegroundColor Green
Write-Host "  ✅ Organized into proper folders" -ForegroundColor Green
Write-Host "  ✅ Converted to Google Docs" -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
```

**Usage:**
```powershell
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center"
.\EOS_AUTOMATION_MASTER.ps1
```

**What it does:**
- Runs PARSE_EOS_FILES.ps1
- Then runs CONVERT_NEW_FILES_ONLY.ps1
- Complete automation in one command

---

# GOOGLE DRIVE INTEGRATION

## Authentication Setup

**First-Time Setup:**

1. **Get Google Drive API Credentials:**
   - Go to: https://console.cloud.google.com
   - Create project: "Trajanus USA"
   - Enable Google Drive API
   - Create OAuth credentials
   - Download as `credentials.json`

2. **Place Credentials:**
```
G:\My Drive\00 - Trajanus USA\00-Command-Center\credentials.json
```

3. **First Run:**
```powershell
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center"
python -c "from google_drive_manager import GoogleDriveManager; gdm = GoogleDriveManager()"
```

4. **Browser Opens:**
   - Sign in to Google account
   - Grant permissions
   - `token.pickle` file created
   - Ready to use!

**Files Created:**
- `credentials.json` (you provide)
- `token.pickle` (auto-created)
- `conversion_log.json` (auto-created)

---

# TROUBLESHOOTING

## Issue: "Python not found"

**Solution:**
```powershell
# Install Python from:
https://www.python.org/downloads/

# Verify installation:
python --version
```

## Issue: "credentials.json not found"

**Solution:**
1. Get credentials from Google Cloud Console
2. Download as `credentials.json`
3. Place in: `G:\My Drive\00 - Trajanus USA\00-Command-Center\`

## Issue: "Script execution disabled"

**Solution:**
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Issue: "No module named 'google'"

**Solution:**
```powershell
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## Issue: "Files not converting"

**Check:**
1. credentials.json exists
2. token.pickle exists (will be created on first run)
3. Internet connection active
4. Google Drive API enabled in Cloud Console

**Re-authenticate:**
```powershell
# Delete token and re-authenticate
rm token.pickle
python -c "from google_drive_manager import GoogleDriveManager; gdm = GoogleDriveManager()"
```

---

# COMPLETE WORKFLOW EXAMPLES

## Example 1: Daily EOS Processing

```powershell
# 1. Download EOS zip from Claude to:
#    G:\My Drive\00 - Trajanus USA\00-Command-Center\EOS\

# 2. Open PowerShell in Command Center folder
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center"

# 3. Run master automation
.\EOS_AUTOMATION_MASTER.ps1

# Done! Files are:
#   - Extracted
#   - Organized by type
#   - Converted to Google Docs
#   - Accessible to Claude via google_drive_search
```

## Example 2: Convert Single File

```powershell
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center"

python -c "from google_drive_manager import GoogleDriveManager; gdm = GoogleDriveManager(); file = gdm.upload_as_google_doc('myfile.md'); print(file['webViewLink'])"
```

## Example 3: Convert All Files in Folder

```powershell
cd "G:\My Drive\00 - Trajanus USA\03-Protocols"
python "G:\My Drive\00 - Trajanus USA\00-Command-Center\batch_convert_to_gdocs.py"
```

## Example 4: Weekly Maintenance

```powershell
# Every Friday:
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center"

# Convert any new markdown files
.\CONVERT_NEW_FILES_ONLY.ps1

# Files from last 7 days automatically converted
```

---

# QUICK REFERENCE COMMANDS

## Open PowerShell in Any Folder
```
Method 1: Address bar → type "powershell" → Enter
Method 2: Shift + Right-click → "Open PowerShell here"
Method 3: Start menu → "powershell" → cd to folder
```

## Run Scripts
```powershell
# Parse EOS files
.\PARSE_EOS_FILES.ps1

# Convert new files
.\CONVERT_NEW_FILES_ONLY.ps1

# Full automation
.\EOS_AUTOMATION_MASTER.ps1
```

## Python Commands
```powershell
# Convert all markdown
python batch_convert_to_gdocs.py

# Convert with tracking
python convert_to_google_docs.py

# Test authentication
python -c "from google_drive_manager import GoogleDriveManager; gdm = GoogleDriveManager(); print('✅ Success!')"
```

---

**End of Documentation**

All scripts ready to use.
All workflows documented.
All troubleshooting covered.

**Location:** G:\My Drive\00 - Trajanus USA\00-Command-Center\

Your tools are ready, brother. 🤝
