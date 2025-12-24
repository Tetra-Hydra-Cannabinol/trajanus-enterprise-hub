#!/usr/bin/env python3
"""
GENERATE NEW GOOGLE DRIVE CREDENTIALS
=====================================
Run this script to authenticate with the Google account that owns
the "00 - Trajanus USA" folder.

This will open a browser window - sign in with the CORRECT account
(the one that has your Trajanus USA files).
"""

import os
import pickle
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Scopes needed for Drive access
SCOPES = ['https://www.googleapis.com/auth/drive']

# Paths
CREDS_DIR = Path('G:/My Drive/00 - Trajanus USA/00-Command-Center/Credentials')
CLIENT_SECRETS = CREDS_DIR / 'credentials.json'
TOKEN_PICKLE = CREDS_DIR / 'token.pickle'
TOKEN_JSON = CREDS_DIR / 'token.json'

def main():
    print("=" * 60)
    print("GENERATE NEW GOOGLE DRIVE CREDENTIALS")
    print("=" * 60)
    print()

    # Check for client secrets file
    if not CLIENT_SECRETS.exists():
        print("[ERROR] credentials.json not found!")
        print(f"        Expected at: {CLIENT_SECRETS}")
        print()
        print("To get credentials.json:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a project or select existing one")
        print("3. Enable Google Drive API")
        print("4. Create OAuth 2.0 credentials (Desktop app)")
        print("5. Download and save as credentials.json")
        return

    print(f"[INFO] Using client secrets: {CLIENT_SECRETS}")
    print()
    print("IMPORTANT: When the browser opens, sign in with the account")
    print("           that owns the '00 - Trajanus USA' folder!")
    print()

    # Delete old tokens to force re-authentication
    if TOKEN_PICKLE.exists():
        print("[INFO] Removing old token.pickle...")
        os.remove(TOKEN_PICKLE)

    if TOKEN_JSON.exists():
        print("[INFO] Removing old token.json...")
        os.remove(TOKEN_JSON)

    # Run OAuth flow
    print("[AUTH] Opening browser for authentication...")
    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS), SCOPES)
    creds = flow.run_local_server(port=0)

    # Save credentials
    print("[SAVE] Saving new credentials...")

    # Save as pickle
    with open(TOKEN_PICKLE, 'wb') as token:
        pickle.dump(creds, token)
    print(f"  Saved: {TOKEN_PICKLE}")

    # Save as JSON
    with open(TOKEN_JSON, 'w') as token:
        token.write(creds.to_json())
    print(f"  Saved: {TOKEN_JSON}")

    # Verify by checking account info
    print()
    print("[VERIFY] Checking connected account...")
    service = build('drive', 'v3', credentials=creds)
    about = service.about().get(fields='user').execute()

    print()
    print("=" * 60)
    print("SUCCESS!")
    print("=" * 60)
    print(f"Connected to: {about['user']['emailAddress']}")
    print(f"Display name: {about['user']['displayName']}")
    print()

    # Check for Trajanus folder
    print("[CHECK] Looking for '00 - Trajanus USA' folder...")
    results = service.files().list(
        q="name='00 - Trajanus USA' and mimeType='application/vnd.google-apps.folder' and trashed=false",
        fields='files(id, name)'
    ).execute()

    folders = results.get('files', [])
    if folders:
        print(f"  FOUND! Folder ID: {folders[0]['id']}")
        print()
        print("Credentials are correct! You can now run CONVERT_MD_TO_GDOCS_PERMANENT.py")
    else:
        print("  NOT FOUND!")
        print()
        print("WARNING: The '00 - Trajanus USA' folder was not found in this account.")
        print("         You may have signed in with the wrong account.")
        print("         Run this script again and sign in with the correct account.")

if __name__ == '__main__':
    main()
