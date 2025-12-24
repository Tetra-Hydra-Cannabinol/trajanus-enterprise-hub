#!/usr/bin/env python3
"""
TRAJANUS FOLDER CONSOLIDATION - SELF-CONTAINED
"""

import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive']

def get_service():
    creds = None
    token_path = r"G:\My Drive\00 - Trajanus USA\00-Command-Center\token.json"
    creds_path = r"G:\My Drive\00 - Trajanus USA\00-Command-Center\credentials.json"
    
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    
    return build('drive', 'v3', credentials=creds)

print("=" * 60)
print("TRAJANUS FOLDER CONSOLIDATION")
print("=" * 60)

service = get_service()
print("Connected to Google Drive")

CANONICAL_07 = '1xYB2RiKId7zVbKydrfXNbFJ4TAEMTuao'
DUP_07_PLURAL = '1gJ5vQ6JEHXb_9iY7KmEv5QOLZO5F27z7'
DUP_NO_PREFIX = '1CHgMzw2UBhv4HBtJl1pOdUUltaqc0n5Z'

def move_files(source_id, dest_id, source_name):
    print(f"\n{source_name} -> 07-Session-Journal")
    results = service.files().list(
        q=f"'{source_id}' in parents and trashed=false",
        fields="files(id, name)"
    ).execute()
    files = results.get('files', [])
    if not files:
        print("  (empty)")
        return 0
    moved = 0
    for f in files:
        try:
            file = service.files().get(fileId=f['id'], fields='parents').execute()
            prev_parents = ",".join(file.get('parents', []))
            service.files().update(
                fileId=f['id'],
                addParents=dest_id,
                removeParents=prev_parents
            ).execute()
            print(f"  Moved: {f['name']}")
            moved += 1
        except Exception as e:
            print(f"  Error: {f['name']}: {e}")
    return moved

total = 0
total += move_files(DUP_07_PLURAL, CANONICAL_07, "07-Session-Journals")
total += move_files(DUP_NO_PREFIX, CANONICAL_07, "Session-Summaries")

print(f"\nCOMPLETE: {total} files moved")
print("Now run: .\\CONVERT_NEW_FILES_ONLY.ps1")
