#!/usr/bin/env python3
"""
RESEARCH AGENT v2.0 - Google Docs Native
Creates individual Google Docs for each finding with duplicate checking
"""

import requests
import os
from datetime import datetime
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import time

# Configuration
TAVILY_API_KEY = os.environ.get('TAVILY_API_KEY', '')
CREDS_PATH = Path(r'G:\My Drive\00 - Trajanus USA\00-Command-Center\Credentials')
OUTPUT_FOLDER_ID = '1ngzU3PYD4Z9rM8XJ0hL5vKQw2N6tE7fR'

SEARCH_TOPICS = [
    'Claude Sonnet 4.5 new features December 2025',
    'Anthropic MCP protocol servers 2025', 
    'Supabase pgvector best practices 2025',
    'Electron Python bridge integration',
    'Anthropic API computer use beta features'
]

def get_drive_service():
    """Authenticate and return Drive API service"""
    creds = None
    token_path = CREDS_PATH / 'token.pickle'
    
    if token_path.exists():
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
        else:
            print('[ERROR] Authentication required')
            return None
    
    return build('drive', 'v3', credentials=creds)

def check_duplicate(service, filename, folder_id):
    """Check if document already exists in folder"""
    try:
        query = f"name='{filename}' and '{folder_id}' in parents and trashed=false"
        results = service.files().list(q=query, fields='files(id, name)').execute()
        files = results.get('files', [])
        
        if files:
            print(f'  [SKIP] Duplicate: {filename}')
            return True
        return False
    except Exception as e:
        print(f'  [ERROR] Duplicate check failed: {e}')
        return False

def create_google_doc(service, title, content, folder_id):
    """Create Google Doc with duplicate checking"""
    if check_duplicate(service, title, folder_id):
        return None
    
    try:
        docs_service = build('docs', 'v1', credentials=service._http.credentials)
        
        doc_metadata = {
            'name': title,
            'mimeType': 'application/vnd.google-apps.document',
            'parents': [folder_id]
        }
        
        doc = service.files().create(body=doc_metadata).execute()
        doc_id = doc.get('id')
        
        requests_batch = [{
            'insertText': {
                'location': {'index': 1},
                'text': content
            }
        }]
        
        docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={'requests': requests_batch}
        ).execute()
        
        print(f'  ✅ Created: {title}')
        return doc_id
        
    except Exception as e:
        print(f'  ❌ Failed: {e}')
        return None

def search_tavily(query):
    """Search Tavily AI"""
    if not TAVILY_API_KEY:
        print('[ERROR] TAVILY_API_KEY not set!')
        return None
    
    endpoint = 'https://api.tavily.com/search'
    payload = {
        'api_key': TAVILY_API_KEY,
        'query': query,
        'search_depth': 'basic',
        'include_answer': True,
        'max_results': 5
    }
    
    try:
        response = requests.post(endpoint, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f'[ERROR] Search failed: {e}')
        return None

def main():
    """Run research cycle with Google Docs output"""
    print('=' * 70)
    print('RESEARCH AGENT v2.0 - GOOGLE DOCS NATIVE')
    print('=' * 70)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f'Topics: {len(SEARCH_TOPICS)}')
    print('=' * 70)
    
    if not TAVILY_API_KEY:
        print('\n[ERROR] TAVILY_API_KEY not set!')
        return
    
    print('\n[AUTH] Connecting to Google Drive...')
    service = get_drive_service()
    if not service:
        return
    print('[SUCCESS] Google Drive authenticated')
    
    print(f'\n[SEARCH] Querying {len(SEARCH_TOPICS)} topics...')
    all_results = {}
    
    for idx, topic in enumerate(SEARCH_TOPICS, 1):
        print(f'\n[{idx}/{len(SEARCH_TOPICS)}] {topic[:60]}...')
        results = search_tavily(topic)
        all_results[topic] = results
        time.sleep(1)
    
    print('\n' + '=' * 70)
    print('CREATING GOOGLE DOCS (25 FINDINGS)')
    print('=' * 70)
    
    created_docs = []
    doc_count = 0
    timestamp = datetime.now().strftime('%Y%m%d')
    
    for topic_idx, (topic, results) in enumerate(all_results.items(), 1):
        if not results or 'results' not in results:
            continue
        
        findings = results.get('results', [])
        print(f'\n[TOPIC {topic_idx}] {topic[:50]}... ({len(findings)} findings)')
        
        for finding_idx, finding in enumerate(findings, 1):
            doc_count += 1
            
            title_words = finding.get('title', 'No title')[:50].replace('/', '-')
            doc_title = f'{timestamp}_Finding_{doc_count:02d}_{title_words}'
            
            content = f"""RESEARCH FINDING #{doc_count}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Topic: {topic}

TITLE:
{finding.get('title', 'No title')}

URL:
{finding.get('url', 'No URL')}

PUBLISHED:
{finding.get('published_date', 'Unknown date')}

CONTENT:
{finding.get('content', 'No content available')}

---
Source: Research Agent v2.0
Search Provider: Tavily AI
Retrieved: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            
            doc_id = create_google_doc(service, doc_title, content, OUTPUT_FOLDER_ID)
            
            if doc_id:
                created_docs.append({
                    'title': doc_title,
                    'id': doc_id,
                    'url': f'https://docs.google.com/document/d/{doc_id}/edit'
                })
    
    print('\n' + '=' * 70)
    print('CREATING MASTER INDEX')
    print('=' * 70)
    
    index_content = f"""RESEARCH AGENT - MASTER INDEX
Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Total Findings: {len(created_docs)}
Topics Researched: {len(SEARCH_TOPICS)}

DOCUMENTS CREATED:

"""
    
    for idx, doc in enumerate(created_docs, 1):
        index_content += f"{idx}. {doc['title']}\n   {doc['url']}\n\n"
    
    index_content += f"""
---
SUMMARY:
- Search Provider: Tavily AI
- Agent Version: 2.0 (Google Docs Native)
- Duplicate Checking: Enabled
- Total Documents: {len(created_docs)}

STATUS: ✅ Research cycle complete
"""
    
    index_title = f'Research_Index_{timestamp}'
    index_id = create_google_doc(service, index_title, index_content, OUTPUT_FOLDER_ID)
    
    print('\n' + '=' * 70)
    print('RESEARCH CYCLE COMPLETE')
    print('=' * 70)
    print(f'Topics researched: {len(SEARCH_TOPICS)}')
    print(f'Findings retrieved: {doc_count}')
    print(f'Google Docs created: {len(created_docs)}')
    print(f'Duplicates skipped: {doc_count - len(created_docs)}')
    
    if index_id:
        print(f'\n📄 Master Index: https://docs.google.com/document/d/{index_id}/edit')
    
    print(f'\n📁 All documents saved to outputs folder')
    print('=' * 70)

if __name__ == '__main__':
    main()
