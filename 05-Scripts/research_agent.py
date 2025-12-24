#!/usr/bin/env python3
"""
RESEARCH AGENT v2.1 - Dynamic Topics
Creates individual Google Docs for each finding with duplicate checking
Now uses rotating topics to avoid 100% duplicates
"""

import requests
import os
import random
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
OUTPUT_FOLDER_ID = '1R4wHCFewBva7YLA98KNGUUbGuzQe0tV4'  # Research-Findings folder

# Topic categories for dynamic selection Coffee
TOPIC_CATEGORIES = {
    'ai_development': [
        'Claude AI latest updates',
        'Anthropic announcements',
        'MCP server implementations',
        'AI coding assistants',
        'LLM development tools',
        'Claude computer use features',
        'Anthropic API new features',
        'AI agent frameworks'
    ],
    'construction_tech': [
        'Construction management software',
        'Project scheduling algorithms',
        'Quality control automation',
        'BIM integration tools',
        'Construction robotics',
        'Digital twin construction',
        'Construction AI applications',
        'Prefab construction technology'
    ],
    'federal_contracting': [
        'Federal contracting regulations',
        'USACE project requirements',
        'DoD construction standards',
        'Government contract updates',
        'Federal acquisition news',
        'GSA schedule updates',
        'Defense infrastructure projects',
        'Federal construction bidding'
    ],
    'databases': [
        'Supabase new features',
        'PostgreSQL optimization',
        'Vector database implementations',
        'Database scaling strategies',
        'Real-time database sync',
        'pgvector best practices',
        'Edge database solutions',
        'Database migration tools'
    ],
    'integration': [
        'Python automation tools',
        'Electron desktop apps',
        'API integration patterns',
        'OAuth implementation',
        'Webhook automation',
        'Desktop app frameworks',
        'Cross-platform development',
        'Process automation tools'
    ]
}

def generate_daily_topics():
    """Generate 5 dynamic topics for today's research"""
    today = datetime.now()
    topics = []

    # 1. Date-specific AI news (always fresh)
    topics.append(f'AI development news {today.strftime("%B %d %Y")}')

    # 2. Weekly construction tech
    topics.append(f'Construction technology trends week {today.strftime("%U %Y")}')

    # 3-5. Random from categories (seeded by date for consistency within day)
    random.seed(today.strftime('%Y-%m-%d'))

    # Pick 3 random categories
    selected_categories = random.sample(list(TOPIC_CATEGORIES.keys()), 3)

    for category in selected_categories:
        # Pick random topic from category
        topic = random.choice(TOPIC_CATEGORIES[category])
        topics.append(f'{topic} {today.strftime("%Y")}')

    return topics

# Generate today's topics
SEARCH_TOPICS = generate_daily_topics()

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
        
        print(f'  [OK] Created: {title}')
        return doc_id
        
    except Exception as e:
        print(f'  [FAIL] Failed: {e}')
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

STATUS: [OK] Research cycle complete
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
        print(f'\n[INDEX] Master Index: https://docs.google.com/document/d/{index_id}/edit')
    
    print(f'\n[DONE] All documents saved to Research-Findings folder')
    print('=' * 70)

if __name__ == '__main__':
    main()
