# Skill: Google Drive Integration

## Name
google-drive

## Description
Manage files on Google Drive, convert markdown to Google Docs, and handle the Trajanus folder structure. Integrated with the auto-conversion workflow.

## When to Use
- Converting markdown files to Google Docs format
- Navigating Trajanus Google Drive structure
- Managing EOS packages and session files
- Syncing between local and Drive locations

## Trajanus Drive Structure

```
G:\My Drive\00 - Trajanus USA\
├── 00-Command-Center\           # Main operations hub
│   ├── .claude\                 # Claude Code configuration
│   │   ├── skills\              # Skill definitions
│   │   └── commands\            # Slash commands
│   ├── 05-Scripts\              # Python, PS1, JS scripts
│   ├── 07-Learning\             # Training materials
│   ├── Skills\                  # Knowmad Agent skills
│   ├── Session_Archive\         # EOS files
│   │   ├── Living_Docs\         # DEV_SPEC, BILLS_DIARY
│   │   ├── CC_Prompts\          # Claude Code prompts
│   │   └── [Timestamped files]  # SESSION_SUMMARY, HANDOFF
│   └── knowledge_Archive\       # KB source materials
├── 01-Morning-Sessions\         # Research outputs
├── 12-Credentials\              # API keys, .env files
└── [Project folders]            # Individual projects
```

## Markdown to Google Docs Conversion

### Using CONVERT_MD_TO_GDOCS_PERMANENT.py
```bash
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center\05-Scripts"
python CONVERT_MD_TO_GDOCS_PERMANENT.py
```

### GUI Features
- Multi-select file picker
- Batch folder conversion
- Shows created Google Doc names
- OPEN FOLDER button
- PARSE TO KB / PARSE & INGEST buttons

### Programmatic Conversion
```python
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Convert MD content to Google Doc
def convert_to_gdoc(md_content, title, folder_id):
    docs_service = build('docs', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    # Create empty doc
    doc = docs_service.documents().create(body={'title': title}).execute()
    doc_id = doc['documentId']

    # Insert content
    docs_service.documents().batchUpdate(
        documentId=doc_id,
        body={'requests': [{'insertText': {'location': {'index': 1}, 'text': md_content}}]}
    ).execute()

    return doc_id
```

## EOS Package Workflow

### On Download (Auto-conversion)
1. Unzip EOS package to target folder
2. Auto-convert all `.md` files to Google Docs
3. Save BOTH versions (md + gdoc)
4. Parse and ingest to KB
5. Output accomplishments list

### File Categories
| Category | Format | Location |
|----------|--------|----------|
| Living Docs | Append/revise | Living_Docs/ |
| Session Files | Timestamped YYYY-MM-DD-HHMM | Session_Archive/ |
| CC Prompts | Versioned | CC_Prompts/ |
| Skills | Static reference | Skills/ |

## Sync Considerations
- Google Drive sync can have delays (30s-2min)
- Always verify file exists before reading after creation
- Use explicit paths, not relative references
- Handle BOM encoding in files from Windows

## Common Operations

### List Recent Files
```python
from pathlib import Path
folder = Path(r"G:\My Drive\00 - Trajanus USA\00-Command-Center\Session_Archive")
recent = sorted(folder.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)[:10]
```

### Check Folder Contents
```bash
dir "G:\My Drive\00 - Trajanus USA\00-Command-Center\Session_Archive" /od
```
