#!/usr/bin/env python3
"""
convert_gdoc_to_docx.py
Trajanus USA - Command Center Script

Converts a single Google Doc to Word format (.docx) using file picker dialog.
Uses Google Drive API with OAuth credentials.

Author: Trajanus USA / Claude AI
Created: 2025-12-05
"""

import os
import sys
import io
import tkinter as tk
from tkinter import filedialog, messagebox
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import pickle

# Configuration
SCOPES = ['https://www.googleapis.com/auth/drive']
CREDENTIALS_PATH = r'G:\My Drive\00 - Trajanus USA\00-Command-Center\Credentials\credentials.json'
TOKEN_PATH = r'G:\My Drive\00 - Trajanus USA\00-Command-Center\Credentials\token.json'
DEFAULT_OUTPUT_DIR = r'G:\My Drive\00 - Trajanus USA\00-Command-Center'

def get_credentials():
    """Get or refresh Google Drive API credentials."""
    creds = None
    
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_PATH):
                messagebox.showerror("Error", f"Credentials file not found:\n{CREDENTIALS_PATH}")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def list_google_docs(service, folder_id=None):
    """List Google Docs in a folder or root."""
    query = "mimeType='application/vnd.google-apps.document' and trashed=false"
    if folder_id:
        query += f" and '{folder_id}' in parents"
    
    results = service.files().list(
        q=query,
        pageSize=100,
        fields="files(id, name, modifiedTime)"
    ).execute()
    
    return results.get('files', [])

def convert_doc_to_docx(service, file_id, file_name, output_dir):
    """Download Google Doc as .docx file."""
    try:
        # Export as Word document
        request = service.files().export_media(
            fileId=file_id,
            mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        
        # Create output filename
        output_name = file_name if file_name.endswith('.docx') else f"{file_name}.docx"
        output_path = os.path.join(output_dir, output_name)
        
        # Download file
        fh = io.FileIO(output_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        
        done = False
        while not done:
            status, done = downloader.next_chunk()
        
        fh.close()
        return output_path
        
    except Exception as e:
        raise Exception(f"Error converting {file_name}: {str(e)}")

def create_picker_window(docs):
    """Create a simple file picker window for Google Docs."""
    selected_doc = [None]
    
    def on_select():
        selection = listbox.curselection()
        if selection:
            selected_doc[0] = docs[selection[0]]
            root.destroy()
    
    def on_cancel():
        root.destroy()
    
    root = tk.Tk()
    root.title("Select Google Doc to Convert")
    root.geometry("500x400")
    root.configure(bg='#3d2a1f')
    
    # Title label
    title = tk.Label(root, text="Select a Google Doc to convert to Word:", 
                     bg='#3d2a1f', fg='#FFF8F0', font=('Segoe UI', 12))
    title.pack(pady=10)
    
    # Listbox with scrollbar
    frame = tk.Frame(root, bg='#3d2a1f')
    frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, 
                         bg='#1f1410', fg='#FFF8F0', 
                         selectbackground='#e8922a',
                         font=('Segoe UI', 10),
                         height=15)
    listbox.pack(fill=tk.BOTH, expand=True)
    scrollbar.config(command=listbox.yview)
    
    for doc in docs:
        listbox.insert(tk.END, f"  {doc['name']}")
    
    # Buttons
    btn_frame = tk.Frame(root, bg='#3d2a1f')
    btn_frame.pack(pady=15)
    
    select_btn = tk.Button(btn_frame, text="Convert Selected", command=on_select,
                           bg='#e8922a', fg='#1f1410', font=('Segoe UI', 10, 'bold'),
                           padx=20, pady=5)
    select_btn.pack(side=tk.LEFT, padx=10)
    
    cancel_btn = tk.Button(btn_frame, text="Cancel", command=on_cancel,
                           bg='#5c4033', fg='#FFF8F0', font=('Segoe UI', 10),
                           padx=20, pady=5)
    cancel_btn.pack(side=tk.LEFT, padx=10)
    
    root.mainloop()
    return selected_doc[0]

def main():
    """Main function."""
    print("=" * 50)
    print("Google Doc to DOCX Converter")
    print("Trajanus USA - Command Center")
    print("=" * 50)
    
    # Get credentials
    creds = get_credentials()
    if not creds:
        print("ERROR: Could not get credentials")
        return
    
    # Build service
    service = build('drive', 'v3', credentials=creds)
    
    # List Google Docs
    print("\nFetching Google Docs...")
    docs = list_google_docs(service)
    
    if not docs:
        messagebox.showinfo("No Documents", "No Google Docs found in your Drive.")
        return
    
    print(f"Found {len(docs)} Google Docs")
    
    # Show picker
    selected = create_picker_window(docs)
    
    if not selected:
        print("No document selected. Exiting.")
        return
    
    print(f"\nSelected: {selected['name']}")
    
    # Ask for output directory
    root = tk.Tk()
    root.withdraw()
    output_dir = filedialog.askdirectory(
        title="Select Output Folder",
        initialdir=DEFAULT_OUTPUT_DIR
    )
    root.destroy()
    
    if not output_dir:
        output_dir = DEFAULT_OUTPUT_DIR
    
    # Convert
    print(f"Converting to: {output_dir}")
    try:
        output_path = convert_doc_to_docx(service, selected['id'], selected['name'], output_dir)
        print(f"\n✓ SUCCESS: {output_path}")
        messagebox.showinfo("Success", f"Converted successfully!\n\n{output_path}")
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    main()
