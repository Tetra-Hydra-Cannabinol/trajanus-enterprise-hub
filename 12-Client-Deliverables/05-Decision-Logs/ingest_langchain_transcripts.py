"""
Ingest LangChain YouTube transcript files into Supabase knowledge_base table.

This script:
1. Reads transcript files from test_output directory
2. Parses header metadata (Title, Channel, Video ID, etc.)
3. Chunks content into ~2000 character segments
4. Inserts into knowledge_base table with proper metadata
"""

import os
import re
import json
from datetime import datetime
from supabase import create_client

# Supabase configuration
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://jyvxouzdnreqnafmpbtq.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_KEY:
    raise ValueError("SUPABASE_SERVICE_ROLE_KEY environment variable required")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Directory containing transcript files
TRANSCRIPT_DIR = r"G:\My Drive\00 - Trajanus USA\00-Command-Center\05-Scripts\test_output"

# Chunk size in characters
CHUNK_SIZE = 2500
CHUNK_OVERLAP = 200

def parse_header(content):
    """Parse the header section of a transcript file."""
    # Split at the separator line
    parts = content.split("=" * 78)
    if len(parts) < 2:
        parts = content.split("=" * 50)

    header_text = parts[0] if len(parts) >= 2 else ""
    transcript_text = parts[1] if len(parts) >= 2 else content

    metadata = {}

    # Parse header fields
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

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split text into overlapping chunks by paragraph/timestamp boundaries."""
    chunks = []

    # Split by timestamp patterns (0:00, 1:23, etc.)
    timestamp_pattern = r'\n(\d{1,2}:\d{2})'
    segments = re.split(timestamp_pattern, text)

    current_chunk = ""
    current_timestamp = "0:00"

    for i, segment in enumerate(segments):
        # Check if this is a timestamp
        if re.match(r'^\d{1,2}:\d{2}$', segment.strip()):
            current_timestamp = segment.strip()
            continue

        # Add segment with its timestamp
        segment_with_time = f"{current_timestamp} {segment.strip()}"

        if len(current_chunk) + len(segment_with_time) < chunk_size:
            current_chunk += "\n" + segment_with_time if current_chunk else segment_with_time
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = segment_with_time

    # Don't forget the last chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks

def ingest_transcript(filepath):
    """Ingest a single transcript file into knowledge_base."""
    print(f"\nProcessing: {os.path.basename(filepath)}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse header and content
    metadata, transcript = parse_header(content)

    if not metadata.get('title'):
        print(f"  WARNING: No title found, skipping")
        return 0

    # Create chunks
    chunks = chunk_text(transcript)
    print(f"  Title: {metadata.get('title')}")
    print(f"  Chunks: {len(chunks)}")

    # Prepare URL
    url = metadata.get('url', f"https://www.youtube.com/watch?v={metadata.get('video_id', 'unknown')}")

    # Check if already ingested
    existing = supabase.table("knowledge_base").select("id").eq("url", url).execute()
    if existing.data:
        print(f"  Already exists ({len(existing.data)} chunks), skipping...")
        return 0

    inserted = 0
    for i, chunk in enumerate(chunks):
        # Prepare summary (first 200 chars of chunk)
        summary = chunk[:200].replace('\n', ' ').strip()
        if len(chunk) > 200:
            summary += "..."

        # Prepare full metadata
        full_metadata = {
            "channel": metadata.get('channel', 'Unknown'),
            "video_id": metadata.get('video_id', ''),
            "duration": metadata.get('duration', ''),
            "level": metadata.get('level', 'INTERMEDIATE'),
            "application": metadata.get('application', 'LangChain'),
            "topics": [t.strip() for t in metadata.get('topics', '').split(',') if t.strip()],
            "source": metadata.get('source', 'YouTube Transcript'),
            "ingested_date": metadata.get('ingested', datetime.now().strftime('%Y-%m-%d')),
            "content_type": "youtube_tutorial",
            "category": "LangChain"
        }

        # Insert into knowledge_base
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
        except Exception as e:
            print(f"  ERROR inserting chunk {i+1}: {e}")

    print(f"  Inserted: {inserted} chunks")
    return inserted

def main():
    """Main ingestion function."""
    print("=" * 60)
    print("LangChain Transcript Ingestion")
    print("=" * 60)

    # Find all 2025-12-21 transcript files
    transcript_files = []
    for filename in os.listdir(TRANSCRIPT_DIR):
        if filename.startswith("2025-12-21") and filename.endswith(".txt"):
            transcript_files.append(os.path.join(TRANSCRIPT_DIR, filename))

    print(f"Found {len(transcript_files)} transcript files")

    total_chunks = 0
    for filepath in sorted(transcript_files):
        try:
            chunks = ingest_transcript(filepath)
            total_chunks += chunks
        except Exception as e:
            print(f"  ERROR processing {filepath}: {e}")

    print("\n" + "=" * 60)
    print(f"INGESTION COMPLETE")
    print(f"Total chunks inserted: {total_chunks}")
    print("=" * 60)

if __name__ == "__main__":
    main()
