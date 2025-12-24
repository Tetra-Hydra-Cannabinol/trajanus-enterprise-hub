#!/usr/bin/env python3
import requests
import os
from datetime import datetime
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import time

TAVILY_API_KEY = os.environ.get('TAVILY_API_KEY', '')
CREDS_PATH = Path('G:/My Drive/00 - Trajanus USA/00-Command-Center/Credentials')
OUTPUT_FOLDER_ID = '1ngzU3PYD4Z9rM8XJ0hL5vKQw2N6tE7fR'

SEARCH_TOPICS = [
    'Claude Sonnet 4.5 new features December 2025',
    'Anthropic MCP protocol servers 2025',
    'Supabase pgvector best practices 2025',
    'Electron Python bridge integration',
    'Anthropic API computer use beta features'
]

def search_tavily(query):
    if not TAVILY_API_KEY:
        print('[ERROR] TAVILY_API_KEY not set')
        return None
    endpoint = 'https://api.tavily.com/search'
    payload = {'api_key': TAVILY_API_KEY, 'query': query, 'search_depth': 'basic', 'max_results': 5}
    try:
        response = requests.post(endpoint, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f'[ERROR] {e}')
        return None

print('=== RESEARCH AGENT ===')
for idx, topic in enumerate(SEARCH_TOPICS, 1):
    print(f'[{idx}/5] {topic[:50]}...')
    results = search_tavily(topic)
    if results and 'results' in results:
        print(f'  Found {len(results["results"])} results')
    time.sleep(1)
print('=== COMPLETE ===')
