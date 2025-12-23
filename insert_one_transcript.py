"""
Insert one transcript and print the SQL statements for manual execution.
Usage: python insert_one_transcript.py <filename>
"""

import sys
import os
import re
import json

TRANSCRIPT_DIR = r"G:\My Drive\00 - Trajanus USA\00-Command-Center\05-Scripts\test_output"
CHUNK_SIZE = 2000  # Smaller chunks

def escape_sql(text):
    """Escape for SQL."""
    if text is None:
        return ''
    return text.replace("'", "''").replace('\x00', '').replace('\\', '\\\\')

def parse_header(content):
    """Parse header."""
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

def main():
    if len(sys.argv) < 2:
        print("Usage: python insert_one_transcript.py <filename>")
        print("\nAvailable files:")
        for f in os.listdir(TRANSCRIPT_DIR):
            if f.startswith("2025-12-21") and f.endswith(".txt"):
                print(f"  {f}")
        return

    filename = sys.argv[1]
    filepath = os.path.join(TRANSCRIPT_DIR, filename)

    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    metadata, transcript = parse_header(content)
    chunks = chunk_text(transcript)

    print(f"File: {filename}")
    print(f"Title: {metadata.get('title')}")
    print(f"Chunks: {len(chunks)}")
    print()

    url = metadata.get('url', f"https://www.youtube.com/watch?v={metadata.get('video_id', 'unknown')}")

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

    metadata_json = json.dumps(full_metadata, ensure_ascii=False)

    for i, chunk in enumerate(chunks):
        summary = chunk[:150].replace('\n', ' ').strip()
        if len(chunk) > 150:
            summary += "..."

        print(f"-- Chunk {i+1}/{len(chunks)}")
        print(f"INSERT INTO knowledge_base (url, chunk_number, title, summary, content, metadata)")
        print(f"VALUES (")
        print(f"  E'{escape_sql(url)}',")
        print(f"  {i+1},")
        print(f"  E'{escape_sql(metadata.get('title', 'Unknown'))}',")
        print(f"  E'{escape_sql(summary)}',")
        print(f"  E'{escape_sql(chunk)}',")
        print(f"  E'{escape_sql(metadata_json)}'::jsonb")
        print(f");")
        print()

if __name__ == "__main__":
    main()
