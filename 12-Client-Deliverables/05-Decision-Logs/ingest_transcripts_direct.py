"""
Ingest LangChain transcripts directly to Supabase knowledge_base.
Uses the SUPABASE_ANON_KEY from .env file.
"""

import os
import re
import json
from datetime import datetime

# Try to import supabase
try:
    from supabase import create_client
except ImportError:
    print("Installing supabase-py...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'supabase'])
    from supabase import create_client

# Load environment
def load_env():
    env_path = r"G:\My Drive\00 - Trajanus USA\00-Command-Center\.env"
    env_vars = {}
    with open(env_path, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if line and '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    return env_vars

# Configuration
env = load_env()
SUPABASE_URL = env.get("SUPABASE_URL")
SUPABASE_KEY = env.get("SUPABASE_ANON_KEY")

print(f"Connecting to: {SUPABASE_URL}")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

TRANSCRIPT_DIR = r"G:\My Drive\00 - Trajanus USA\00-Command-Center\05-Scripts\test_output"
CHUNK_SIZE = 3000

def parse_header(content):
    """Parse the header section."""
    parts = content.split("=" * 78)
    if len(parts) < 2:
        parts = content.split("=" * 70)
    if len(parts) < 2:
        parts = content.split("=" * 50)

    header_text = parts[0] if len(parts) >= 2 else ""
    transcript_text = parts[1] if len(parts) >= 2 else content

    metadata = {}
    patterns = {
        'title': r'Title:\s*(.+)',
        'channel': r'Channel:\s*(.+)',
        'video_id': r'Video ID:\s*(.+)',
        'url': r'URL:\s*(.+)',
        'duration': r'Duration:\s*(.+)',
        'level': r'Level:\s*(.+)',
        'application': r'Application:\s*(.+)',
        'topics': r'Topics:\s*(.+)',
        'ingested': r'Ingested:\s*(.+)',
        'source': r'Source:\s*(.+)'
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, header_text, re.IGNORECASE)
        if match:
            metadata[key] = match.group(1).strip()

    return metadata, transcript_text.strip()

def chunk_text(text, chunk_size=CHUNK_SIZE):
    """Split text into chunks."""
    chunks = []
    current = ""

    for line in text.split('\n'):
        if len(current) + len(line) + 1 <= chunk_size:
            current = current + "\n" + line if current else line
        else:
            if current:
                chunks.append(current.strip())
            current = line

    if current.strip():
        chunks.append(current.strip())

    return chunks

def ingest_file(filepath):
    """Ingest a single transcript file."""
    filename = os.path.basename(filepath)
    print(f"\nProcessing: {filename}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    metadata, transcript = parse_header(content)

    if not metadata.get('title'):
        print(f"  WARNING: No title found, skipping")
        return 0

    url = metadata.get('url', f"https://www.youtube.com/watch?v={metadata.get('video_id', 'unknown')}")

    # Check if already exists
    try:
        existing = supabase.table("knowledge_base").select("id").eq("url", url).execute()
        if existing.data:
            print(f"  Already exists ({len(existing.data)} chunks)")
            return 0
    except Exception as e:
        print(f"  Warning checking existing: {e}")

    chunks = chunk_text(transcript)
    print(f"  Title: {metadata.get('title')}")
    print(f"  Chunks: {len(chunks)}")

    full_metadata = {
        "channel": metadata.get('channel', 'Unknown'),
        "video_id": metadata.get('video_id', ''),
        "duration": metadata.get('duration', ''),
        "level": metadata.get('level', 'INTERMEDIATE'),
        "application": metadata.get('application', 'LangChain'),
        "topics": [t.strip() for t in metadata.get('topics', '').split(',') if t.strip()],
        "source": metadata.get('source', 'YouTube Transcript'),
        "ingested_date": metadata.get('ingested', '2025-12-21'),
        "content_type": "youtube_tutorial",
        "category": "LangChain"
    }

    inserted = 0
    for i, chunk in enumerate(chunks):
        summary = chunk[:200].replace('\n', ' ').strip()
        if len(chunk) > 200:
            summary += "..."

        record = {
            "url": url,
            "chunk_number": i + 1,
            "title": metadata.get('title', 'Unknown'),
            "summary": summary,
            "content": chunk,
            "metadata": full_metadata
        }

        try:
            supabase.table("knowledge_base").insert(record).execute()
            inserted += 1
            print(f"  Inserted chunk {i+1}/{len(chunks)}")
        except Exception as e:
            print(f"  ERROR inserting chunk {i+1}: {e}")

    return inserted

def main():
    print("=" * 60)
    print("LangChain Transcript Ingestion - Direct to Supabase")
    print("=" * 60)

    transcript_files = []
    for filename in os.listdir(TRANSCRIPT_DIR):
        if filename.startswith("2025-12-21") and filename.endswith(".txt"):
            transcript_files.append(os.path.join(TRANSCRIPT_DIR, filename))

    print(f"Found {len(transcript_files)} transcript files")

    total_chunks = 0
    for filepath in sorted(transcript_files):
        try:
            chunks = ingest_file(filepath)
            total_chunks += chunks
        except Exception as e:
            print(f"  ERROR: {e}")

    print("\n" + "=" * 60)
    print(f"INGESTION COMPLETE - {total_chunks} chunks inserted")
    print("=" * 60)

if __name__ == "__main__":
    main()
