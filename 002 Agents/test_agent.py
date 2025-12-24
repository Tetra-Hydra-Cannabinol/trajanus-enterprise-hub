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

def get_drive_service():
    creds = None
    token_path = CREDS_PATH / 'token.pickle'
    
    if token_path.exists():
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print('[ERROR] Auth required')
            return None
    
    return build('drive', 'v3', credentials=creds)

print('Agent ready')
