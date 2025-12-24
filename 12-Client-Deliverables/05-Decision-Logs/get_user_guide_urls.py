# GET GOOGLE DOCS URLS FOR USER GUIDES
# Run this to get shareable Google Docs URLs for your user guide files

"""
This script searches your Google Drive for the user guide documents and
returns their Google Docs URLs so you can configure the User Guides modal.
"""

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import os

# Google Drive API scopes
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# List of user guide filenames to find
USER_GUIDES = [
    '6_Category_System_Guide.docx',
    'End_Of_Session_Closeout.docx',
    'File_Systems_User_Guide.docx',
    'Morning_Session_Startup.docx',
    'Operational_Protocols.docx',
    'The_Commandments_of_AI.docx',
    'Bills_Profile.docx',
    'START_HERE_Implementation_Guide.md',
    'DEVELOPMENT_WORKFLOW.md',
    'ADDING_UTILITY_BUTTONS.md',
    'OPERATIONAL_PROTOCOL.md',
    'Limitless_Integration_Guide.md'
]

def get_credentials():
    """Get or refresh Google API credentials."""
    creds = None
    token_path = 'token.pickle'
    
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def find_user_guides():
    """Find user guide documents and return their URLs."""
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)
    
    guide_urls = {}
    
    print("\n" + "="*70)
    print("SEARCHING FOR USER GUIDE DOCUMENTS")
    print("="*70 + "\n")
    
    for filename in USER_GUIDES:
        # Search for file by name
        query = f"name='{filename}'"
        results = service.files().list(
            q=query,
            fields='files(id, name, mimeType, webViewLink)',
            pageSize=10
        ).execute()
        
        files = results.get('files', [])
        
        if files:
            file = files[0]  # Take first match
            file_id = file['id']
            
            # For Google Docs, use webViewLink
            # For other files, construct the URL
            if 'google-apps' in file.get('mimeType', ''):
                url = file.get('webViewLink', f"https://docs.google.com/document/d/{file_id}/edit")
            else:
                url = f"https://drive.google.com/file/d/{file_id}/view"
            
            guide_urls[filename] = url
            print(f"✓ Found: {filename}")
            print(f"  URL: {url}\n")
        else:
            print(f"✗ NOT FOUND: {filename}\n")
    
    return guide_urls

def generate_javascript_code(guide_urls):
    """Generate the JavaScript array code for index.html."""
    print("\n" + "="*70)
    print("JAVASCRIPT CODE FOR INDEX.HTML")
    print("="*70 + "\n")
    
    print("const userGuides = [")
    
    for filename, url in guide_urls.items():
        # Get display name
        name = filename.replace('_', ' ').replace('.docx', '').replace('.md', '')
        
        # Handle special names
        name_map = {
            '6 Category System Guide': '6-Category System Guide',
            'Bills Profile': 'Bill\'s Profile',
            'START HERE Implementation Guide': 'START HERE - Implementation Guide',
            'Operational Protocol (MD)': 'Operational Protocol'
        }
        
        display_name = name_map.get(name, name)
        
        print(f"    {{ name: '{display_name}', url: '{url}', file: '{filename}' }},")
    
    print("];")
    print("\n" + "="*70 + "\n")

def main():
    """Main execution."""
    try:
        guide_urls = find_user_guides()
        
        if guide_urls:
            generate_javascript_code(guide_urls)
            
            print("\nINSTRUCTIONS:")
            print("-" * 70)
            print("1. Copy the JavaScript code above")
            print("2. Open index.html in your editor")
            print("3. Find the 'const userGuides = [' section")
            print("4. Replace it with the code above")
            print("5. Save and restart the app")
            print("-" * 70)
        else:
            print("\n⚠️  No user guide files found!")
            print("Make sure the files exist in your Google Drive")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\nMake sure you have:")
        print("1. credentials.json in the same folder as this script")
        print("2. Google Drive API enabled in your Google Cloud project")
        print("3. Proper authentication set up")

if __name__ == '__main__':
    main()
