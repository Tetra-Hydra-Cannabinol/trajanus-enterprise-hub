#!/usr/bin/env python3
"""
BATCH FILE INGESTION - Non-interactive ingestion of specific files
Usage: python batch_ingest_files.py <source_category> <file1> [file2] [file3] ...
"""

import os
import sys
import io
from pathlib import Path
from datetime import datetime
import time

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from openai import OpenAI
from supabase import create_client, Client

def load_env():
    """Load .env file"""
    env_path = Path('G:/My Drive/00 - Trajanus USA/00-Command-Center/.env')
    with open(env_path, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if line and '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

load_env()

supabase: Client = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_ANON_KEY')
)
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def chunk_text(text, chunk_size=1000, overlap=200):
    """Split text into overlapping chunks"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        if end < len(text):
            search_start = max(start, end - 100)
            sentence_end = max(
                text.rfind('. ', search_start, end),
                text.rfind('! ', search_start, end),
                text.rfind('? ', search_start, end)
            )
            if sentence_end != -1:
                end = sentence_end + 1
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap
    return chunks

def process_file(filepath: Path, source_category: str):
    """Process a single file"""
    print(f"\n[PROCESS] {filepath.name}")

    # Read file
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  [ERROR] Could not read file: {e}")
        return 0

    if len(content) < 50:
        print(f"  [SKIP] File too short ({len(content)} chars)")
        return 0

    print(f"  [INFO] Read {len(content)} characters")

    # Chunk the content
    chunks = chunk_text(content)
    print(f"  [INFO] Created {len(chunks)} chunks")

    added = 0
    for i, chunk in enumerate(chunks, 1):
        # Generate embedding
        try:
            response = openai_client.embeddings.create(
                input=chunk,
                model="text-embedding-3-small"
            )
            embedding = response.data[0].embedding
        except Exception as e:
            print(f"  [ERROR] Chunk {i}: Embedding failed - {e}")
            continue

        # Store in database
        try:
            relative_path = str(filepath).replace("G:\\My Drive\\00 - Trajanus USA\\", "")
            data = {
                "url": f"file:///{relative_path}",
                "chunk_number": i,
                "title": f"{filepath.stem} (Part {i})",
                "summary": ' '.join(chunk.split()[:20]) + '...',
                "content": chunk,
                "metadata": {
                    "source": source_category,
                    "filename": filepath.name,
                    "file_type": filepath.suffix,
                    "total_chunks": len(chunks),
                    "processed_at": datetime.now().isoformat()
                },
                "embedding": embedding
            }
            supabase.table('knowledge_base').insert(data).execute()
            added += 1
            if i % 10 == 0:
                print(f"  [PROGRESS] {i}/{len(chunks)} chunks")
            time.sleep(0.2)
        except Exception as e:
            if '23505' in str(e):
                pass  # Duplicate - skip silently
            else:
                print(f"  [ERROR] Chunk {i}: DB insert failed - {e}")

    print(f"  [DONE] Added {added}/{len(chunks)} chunks")
    return added

def main():
    if len(sys.argv) < 3:
        print("Usage: python batch_ingest_files.py <source_category> <file1> [file2] ...")
        sys.exit(1)

    source_category = sys.argv[1]
    files = [Path(f) for f in sys.argv[2:]]

    print("=" * 70)
    print("BATCH FILE INGESTION")
    print("=" * 70)
    print(f"Category: {source_category}")
    print(f"Files: {len(files)}")

    total_added = 0
    for filepath in files:
        if filepath.exists():
            total_added += process_file(filepath, source_category)
        else:
            print(f"[ERROR] File not found: {filepath}")

    print("\n" + "=" * 70)
    print(f"COMPLETE - Added {total_added} total chunks")
    print("=" * 70)

if __name__ == "__main__":
    main()
