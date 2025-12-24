"""
Living Document Updater for Trajanus USA - DRIVE API ONLY
Appends new session content to MASTER documents in Google Drive
Version 2.0 - November 23, 2025 (No Docs API Required)
"""

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload
from datetime import datetime
import os
import sys
import io

# MASTER Document IDs (Google Docs)
MASTER_DOCS = {
    'technical': '1LQnGWZVV5Ze30XH8OOYWqASEM2nLYSQxAL8ok0FY18s',
    'operational': '1W--Zf8mX57M9cYonAnoXJtgEFgXsrALxK-bjqMxxONI',
    'diary': '174kCDc4AU7LqvN2goFefjHAPFsMoG4la5q2CzvZ_TBY',
    'session': '1ug6hyU9kE-n369M0lr1ZAElaphfpP3IfNL3duCtnXu0'
}

def load_credentials():
    """Load Google Drive credentials"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Try Credentials subfolder first
    creds_path = os.path.join(script_dir, 'Credentials', 'token.json')
    
    # If not found, try current directory
    if not os.path.exists(creds_path):
        creds_path = 'token.json'
    
    if not os.path.exists(creds_path):
        print("❌ ERROR: token.json not found")
        print(f"   Looked in: {script_dir}\\Credentials\\token.json")
        print(f"   And: {os.getcwd()}\\token.json")
        sys.exit(1)
    
    print(f"✅ Using credentials from: {creds_path}")
    return Credentials.from_authorized_user_file(creds_path)

def read_google_doc_as_text(service, doc_id):
    """Read Google Doc content as plain text using Drive API export"""
    try:
        content = service.files().export(
            fileId=doc_id,
            mimeType='text/plain'
        ).execute()
        
        return content.decode('utf-8')
    except Exception as e:
        print(f"   ❌ Error reading document: {str(e)}")
        return None

def append_to_google_doc(service, doc_id, new_content, doc_name):
    """
    Append content to Google Doc using Drive API only
    Strategy: Download as text, append, upload as new version
    """
    try:
        # Step 1: Download current content
        print(f"   - Downloading current content...")
        current_content = read_google_doc_as_text(service, doc_id)
        
        if current_content is None:
            return False
        
        # Step 2: Prepare new content with formatting
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        separator = "\n" + "="*80 + "\n"
        header = f"SESSION ENTRY - {timestamp}\n"
        formatted_new = separator + header + separator + "\n" + new_content + "\n\n"
        
        # Step 3: Combine old + new
        updated_content = current_content + formatted_new
        
        # Step 4: Upload as plain text (Drive will convert to Google Doc)
        print(f"   - Uploading updated content...")
        
        # Create in-memory file
        fh = io.BytesIO(updated_content.encode('utf-8'))
        media = MediaIoBaseUpload(fh, mimetype='text/plain', resumable=True)
        
        # Update the existing file
        updated_file = service.files().update(
            fileId=doc_id,
            media_body=media,
            fields='id,name,modifiedTime'
        ).execute()
        
        print(f"   ✅ Updated: {doc_name}")
        print(f"      Modified: {updated_file.get('modifiedTime')}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error updating document: {str(e)}")
        return False

def find_local_files(directory='.'):
    """Find all new session files in current directory"""
    session_files = {
        'technical': [],
        'operational': [],
        'diary': [],
        'session': []
    }
    
    for filename in os.listdir(directory):
        if not filename.endswith(('.md', '.txt')):
            continue
        
        lower_name = filename.lower()
        
        if 'technical' in lower_name and 'journal' in lower_name:
            session_files['technical'].append(filename)
        elif 'operational' in lower_name and 'journal' in lower_name:
            session_files['operational'].append(filename)
        elif 'diary' in lower_name or 'personal' in lower_name:
            session_files['diary'].append(filename)
        elif 'session' in lower_name and 'summary' in lower_name:
            session_files['session'].append(filename)
    
    return session_files

def read_local_file(filepath):
    """Read content from local file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ Error reading {filepath}: {str(e)}")
        return None

def update_master_documents():
    """Main function to update all MASTER documents"""
    
    print("="*80)
    print("LIVING DOCUMENT UPDATER - Trajanus USA (Drive API Only)")
    print("="*80)
    print()
    
    # Load credentials
    creds = load_credentials()
    
    # Build Drive service only
    service = build('drive', 'v3', credentials=creds)
    
    print("✅ Connected to Google Drive")
    print()
    
    # Find local session files
    print("🔍 Scanning for new session files...")
    session_files = find_local_files()
    
    total_found = sum(len(files) for files in session_files.values())
    print(f"   Found {total_found} session files")
    print()
    
    if total_found == 0:
        print("⚠️  No new session files found in current directory")
        print("   Looking for files with keywords:")
        print("   - Technical Journal")
        print("   - Operational Journal")
        print("   - Personal Diary")
        print("   - Session Summary")
        print()
        return
    
    # Process each document type
    update_count = 0
    error_count = 0
    
    doc_types = {
        'technical': 'Technical_Journal_November_2025_MASTER',
        'operational': 'Operational_Journal_November_2025_MASTER',
        'diary': 'Personal_Diary_November_2025_MASTER',
        'session': 'Session_Summaries_November_2025_MASTER'
    }
    
    for doc_type, files in session_files.items():
        if not files:
            continue
        
        doc_name = doc_types[doc_type]
        doc_id = MASTER_DOCS[doc_type]
        
        print(f"📝 Processing {doc_name}...")
        print(f"   Files to append: {len(files)}")
        
        for filename in files:
            print(f"   - Reading: {filename}")
            content = read_local_file(filename)
            
            if content:
                if append_to_google_doc(service, doc_id, content, doc_name):
                    update_count += 1
                else:
                    error_count += 1
            else:
                error_count += 1
        
        print()
    
    # Print summary
    print("="*80)
    print("UPDATE COMPLETE")
    print("="*80)
    print(f"✅ Successfully updated: {update_count} documents")
    if error_count > 0:
        print(f"❌ Errors: {error_count}")
    print()
    
    # Print links to updated documents
    print("📁 VIEW UPDATED MASTER DOCUMENTS:")
    print()
    for doc_type, doc_id in MASTER_DOCS.items():
        doc_name = doc_types[doc_type]
        url = f"https://docs.google.com/document/d/{doc_id}/edit"
        print(f"   {doc_name}")
        print(f"   {url}")
        print()

if __name__ == '__main__':
    try:
        update_master_documents()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
    except Exception as e:
        print(f"\n\n❌ FATAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
