#!/usr/bin/env python3
"""Verify 13-Knowledge-Base reorganization."""

import pickle
from pathlib import Path
from googleapiclient.discovery import build
from collections import defaultdict

CREDENTIALS_PATH = Path("G:/My Drive/00 - Trajanus USA/00-Command-Center/Credentials/token.pickle")
OUTPUT_DIR = Path("G:/My Drive/00 - Trajanus USA/00-Command-Center/outputs")

with open(CREDENTIALS_PATH, "rb") as token:
    creds = pickle.load(token)

service = build("drive", "v3", credentials=creds)

# 13-Knowledge-Base ID
KB_FOLDER_ID = "1E7kK8ZIZ9-9xZ4HtvbuVbY_iX3DKmEYM"

def count_docs(folder_id):
    """Count Google Docs in a folder."""
    query = f"'{folder_id}' in parents and mimeType = 'application/vnd.google-apps.document' and trashed = false"
    results = service.files().list(q=query, pageSize=200, fields="files(id)").execute()
    return len(results.get('files', []))

def scan_folder(folder_id, indent=0, path=""):
    """Recursively scan folder and count docs."""
    results = []

    # Get folders
    query = f"'{folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    folders = service.files().list(q=query, pageSize=100, fields="files(id, name)", orderBy="name").execute()

    for folder in folders.get('files', []):
        folder_name = folder['name']
        folder_path = f"{path}/{folder_name}" if path else folder_name
        doc_count = count_docs(folder['id'])

        prefix = "  " * indent
        entry = f"{prefix}{folder_name}/ ({doc_count} docs)"
        results.append(entry)

        try:
            print(entry)
        except UnicodeEncodeError:
            print(entry.encode('ascii', 'replace').decode())

        # Recurse into subfolders
        sub_results = scan_folder(folder['id'], indent + 1, folder_path)
        results.extend(sub_results)

    return results

print("=" * 70)
print("13-KNOWLEDGE-BASE VERIFICATION REPORT")
print("=" * 70)
print()

# Count docs at root
root_docs = count_docs(KB_FOLDER_ID)
print(f"13-Knowledge-Base/ ({root_docs} docs at root)")
print()

# Scan all folders
report_lines = ["13-Knowledge-Base/", ""]
lines = scan_folder(KB_FOLDER_ID)
report_lines.extend(lines)

# Save report
report_file = OUTPUT_DIR / "verification_report_13kb.txt"
with open(report_file, 'w', encoding='utf-8') as f:
    f.write("13-KNOWLEDGE-BASE VERIFICATION REPORT\n")
    f.write("=" * 70 + "\n\n")
    for line in report_lines:
        f.write(line + "\n")

print()
print("=" * 70)
print(f"Report saved to: {report_file}")
