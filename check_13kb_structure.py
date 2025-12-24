#!/usr/bin/env python3
"""Check 13-Knowledge-Base folder structure."""

import pickle
from pathlib import Path
from googleapiclient.discovery import build

CREDENTIALS_PATH = Path("G:/My Drive/00 - Trajanus USA/00-Command-Center/Credentials/token.pickle")
with open(CREDENTIALS_PATH, "rb") as token:
    creds = pickle.load(token)

service = build("drive", "v3", credentials=creds)

# 13-Knowledge-Base folder ID
KB_FOLDER_ID = "1E7kK8ZIZ9-9xZ4HtvbuVbY_iX3DKmEYM"

print("=" * 60)
print("13-Knowledge-Base Current Structure")
print("=" * 60)

# Get folder info
folder = service.files().get(fileId=KB_FOLDER_ID, fields="name, parents").execute()
print(f"Folder Name: {folder.get('name')}")
print(f"Folder ID: {KB_FOLDER_ID}")
print()

# List all items in 13-Knowledge-Base
query = f"'{KB_FOLDER_ID}' in parents and trashed = false"
results = service.files().list(
    q=query,
    pageSize=100,
    fields="files(id, name, mimeType)",
    orderBy="name"
).execute()

folders = []
files = []
for item in results.get('files', []):
    if item['mimeType'] == 'application/vnd.google-apps.folder':
        folders.append(item)
    else:
        files.append(item)

print(f"Subfolders ({len(folders)}):")
for f in folders:
    print(f"  - {f['name']} ({f['id']})")

print()
print(f"Files at root ({len(files)}):")
for f in files[:10]:
    print(f"  - {f['name']}")
if len(files) > 10:
    print(f"  ... and {len(files) - 10} more")

# Also check the old TKB folder
print()
print("=" * 60)
print("Old TKB-Trajanus-Knowledge-Base (where we put docs earlier)")
print("=" * 60)

old_tkb_categories = {
    "AI-Development": "1VVeotAPnechdDPfLnDTiOZqKA5ZEQDRM",
    "Software-Tools": "1xMWr71AGbZOfnOjAy8IoVOt75Kf_KMAx",
    "Technical-Guides": "1guwUKpc4vUnsuZ0pibalGV0jzBnYZO1n",
    "QCM-Quality": "1ehvTr0P1xQzpKmqOVyiIE-FHR8B66Zpv"
}

total_in_old = 0
for name, fid in old_tkb_categories.items():
    # Count all docs recursively
    def count_docs(folder_id):
        count = 0
        query = f"'{folder_id}' in parents and trashed = false"
        results = service.files().list(q=query, pageSize=200, fields="files(id, mimeType)").execute()
        for item in results.get('files', []):
            if item['mimeType'] == 'application/vnd.google-apps.document':
                count += 1
            elif item['mimeType'] == 'application/vnd.google-apps.folder':
                count += count_docs(item['id'])
        return count

    doc_count = count_docs(fid)
    total_in_old += doc_count
    print(f"  {name}: {doc_count} docs")

print(f"\nTotal docs in old TKB: {total_in_old}")
