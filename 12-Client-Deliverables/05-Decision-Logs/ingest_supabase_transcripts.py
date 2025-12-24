#!/usr/bin/env python3
"""
Ingest Supabase YouTube Transcripts to TKB
Targeted ingestion for the 13 Supabase tutorial transcripts
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import time

# Load environment from .env
from dotenv import load_dotenv
# Try script directory first, then parent
env_path = Path(__file__).parent / '.env'
if not env_path.exists():
    env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)
print(f"Loaded .env from: {env_path}")

# Initialize clients
from supabase import create_client
from openai import OpenAI

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY') or os.getenv('SUPABASE_KEY')
OPENAI_KEY = os.getenv('OPENAI_API_KEY')

if not all([SUPABASE_URL, SUPABASE_KEY, OPENAI_KEY]):
    print("ERROR: Missing environment variables!")
    print(f"  SUPABASE_URL: {'SET' if SUPABASE_URL else 'MISSING'}")
    print(f"  SUPABASE_KEY: {'SET' if SUPABASE_KEY else 'MISSING'}")
    print(f"  OPENAI_API_KEY: {'SET' if OPENAI_KEY else 'MISSING'}")
    sys.exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
openai_client = OpenAI(api_key=OPENAI_KEY)

# Transcript directory
TRANSCRIPT_DIR = Path(r"G:\My Drive\00 - Trajanus USA\01-Morning-Sessions\Research\Supabase_YouTube")

def chunk_text(text, chunk_size=1500, overlap=200):
    """Split text into overlapping chunks"""
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # Try to break at sentence boundary
        if end < len(text):
            for sep in ['. ', '! ', '? ', '\n\n', '\n']:
                last_sep = text.rfind(sep, start + chunk_size - 200, end)
                if last_sep != -1:
                    end = last_sep + len(sep)
                    break

        chunk = text[start:end].strip()
        if chunk and len(chunk) > 50:
            chunks.append(chunk)

        start = end - overlap

    return chunks

def generate_embedding(text):
    """Generate embedding using OpenAI"""
    try:
        response = openai_client.embeddings.create(
            input=text[:8000],  # Limit input size
            model="text-embedding-3-small"
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"    Embedding error: {e}")
        return None

def ingest_file(filepath):
    """Ingest a single transcript file"""
    print(f"\n{'='*60}")
    print(f"Processing: {filepath.name}")
    print(f"{'='*60}")

    # Read file
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  ERROR reading file: {e}")
        return 0

    print(f"  Read {len(content):,} characters")

    # Extract metadata from file header
    lines = content.split('\n')
    title = lines[0].replace('Title: ', '') if lines[0].startswith('Title:') else filepath.stem
    channel = lines[1].replace('Channel: ', '') if len(lines) > 1 and lines[1].startswith('Channel:') else 'Unknown'
    url = lines[2].replace('URL: ', '') if len(lines) > 2 and lines[2].startswith('URL:') else ''

    # Get main content (skip header)
    main_content = content
    if '=' * 20 in content:
        main_content = content.split('=' * 20, 1)[-1].strip()

    # Chunk the content
    chunks = chunk_text(main_content)
    print(f"  Created {len(chunks)} chunks")

    success_count = 0

    for i, chunk in enumerate(chunks, 1):
        print(f"  Chunk {i}/{len(chunks)}: ", end='', flush=True)

        # Generate embedding
        embedding = generate_embedding(chunk)
        if not embedding:
            print("SKIP (no embedding)")
            continue

        # Create summary (first 100 chars)
        summary = chunk[:150].replace('\n', ' ').strip() + '...'

        # Insert into database
        try:
            data = {
                "url": url or f"youtube://{filepath.stem}",
                "chunk_number": i,
                "title": f"{title} (Part {i}/{len(chunks)})",
                "summary": summary,
                "content": chunk,
                "metadata": {
                    "source": "supabase-youtube-tutorials",
                    "category": "supabase-tutorials",
                    "channel": channel,
                    "filename": filepath.name,
                    "total_chunks": len(chunks),
                    "tags": ["supabase", "youtube", "tutorial", "database"],
                    "ingested_at": datetime.now().isoformat()
                },
                "embedding": embedding
            }

            result = supabase.table('knowledge_base').insert(data).execute()

            if result.data:
                print(f"OK (ID: {result.data[0].get('id', 'N/A')})")
                success_count += 1
            else:
                print("FAIL (no data returned)")

        except Exception as e:
            print(f"FAIL ({str(e)[:50]})")

        # Rate limiting
        time.sleep(0.3)

    print(f"\n  Result: {success_count}/{len(chunks)} chunks ingested")
    return success_count

def get_kb_stats():
    """Get current KB statistics"""
    try:
        result = supabase.table('knowledge_base').select('id', count='exact').execute()
        return result.count or 0
    except:
        return 0

def main():
    print("\n" + "=" * 70)
    print("SUPABASE TRANSCRIPT INGESTION TO TKB")
    print("=" * 70)
    print(f"Transcript Directory: {TRANSCRIPT_DIR}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Get initial stats
    initial_count = get_kb_stats()
    print(f"\nInitial TKB Document Count: {initial_count}")

    # Find transcript files
    transcript_files = list(TRANSCRIPT_DIR.glob("2025-12-19_104214_*.txt"))
    print(f"Found {len(transcript_files)} transcript files")

    if not transcript_files:
        print("ERROR: No transcript files found!")
        return

    # Process each file
    total_success = 0
    total_failed = 0
    file_results = []

    for filepath in transcript_files:
        success = ingest_file(filepath)
        total_success += success
        if success == 0:
            total_failed += 1
            file_results.append((filepath.name, "FAILED", 0))
        else:
            file_results.append((filepath.name, "SUCCESS", success))

    # Get final stats
    final_count = get_kb_stats()

    # Print summary
    print("\n" + "=" * 70)
    print("INGESTION COMPLETE")
    print("=" * 70)
    print(f"Files Processed: {len(transcript_files)}")
    print(f"Total Chunks Ingested: {total_success}")
    print(f"Files Failed: {total_failed}")
    print(f"\nTKB Document Count:")
    print(f"  Before: {initial_count}")
    print(f"  After:  {final_count}")
    print(f"  Added:  {final_count - initial_count}")

    print("\n" + "-" * 70)
    print("FILE RESULTS:")
    print("-" * 70)
    for filename, status, chunks in file_results:
        status_icon = "OK" if status == "SUCCESS" else "FAIL"
        print(f"  [{status_icon}] {filename[:50]}: {chunks} chunks")

    print("\n" + "=" * 70)

    return {
        'files_processed': len(transcript_files),
        'chunks_ingested': total_success,
        'files_failed': total_failed,
        'initial_count': initial_count,
        'final_count': final_count
    }

if __name__ == "__main__":
    result = main()
    sys.exit(0 if result and result['chunks_ingested'] > 0 else 1)
