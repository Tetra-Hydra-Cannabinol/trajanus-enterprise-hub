"""
Generate SQL INSERT statements for LangChain transcripts.
Output: SQL file ready for execution via Supabase MCP.
"""

import os
import re
import json

# Directory containing transcript files
TRANSCRIPT_DIR = r"G:\My Drive\00 - Trajanus USA\00-Command-Center\05-Scripts\test_output"
OUTPUT_FILE = r"G:\My Drive\00 - Trajanus USA\00-Command-Center\05-Scripts\langchain_inserts.sql"

# Chunk size in characters
CHUNK_SIZE = 2500

def escape_sql(text):
    """Escape single quotes for SQL."""
    if text is None:
        return ''
    return text.replace("'", "''").replace('\x00', '')

def parse_header(content):
    """Parse the header section of a transcript file."""
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
    """Split text into chunks by paragraph/line boundaries."""
    chunks = []
    lines = text.split('\n')
    current_chunk = ""

    for line in lines:
        if len(current_chunk) + len(line) + 1 < chunk_size:
            current_chunk += "\n" + line if current_chunk else line
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = line

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks

def generate_insert(url, chunk_num, title, summary, content, metadata):
    """Generate a single INSERT statement."""
    metadata_json = json.dumps(metadata, ensure_ascii=False)

    sql = f"""INSERT INTO knowledge_base (url, chunk_number, title, summary, content, metadata)
VALUES (
  '{escape_sql(url)}',
  {chunk_num},
  '{escape_sql(title)}',
  '{escape_sql(summary[:500])}',
  '{escape_sql(content)}',
  '{escape_sql(metadata_json)}'::jsonb
);"""
    return sql

def process_file(filepath):
    """Process a single transcript file and return INSERT statements."""
    print(f"Processing: {os.path.basename(filepath)}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    metadata, transcript = parse_header(content)

    if not metadata.get('title'):
        print(f"  WARNING: No title found, skipping")
        return []

    chunks = chunk_text(transcript)
    print(f"  Title: {metadata.get('title')}")
    print(f"  Chunks: {len(chunks)}")

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

    inserts = []
    for i, chunk in enumerate(chunks):
        summary = chunk[:200].replace('\n', ' ').strip()
        if len(chunk) > 200:
            summary += "..."

        sql = generate_insert(url, i+1, metadata.get('title'), summary, chunk, full_metadata)
        inserts.append(sql)

    return inserts

def main():
    """Main function."""
    print("=" * 60)
    print("Generating SQL INSERT statements for LangChain transcripts")
    print("=" * 60)

    transcript_files = []
    for filename in os.listdir(TRANSCRIPT_DIR):
        if filename.startswith("2025-12-21") and filename.endswith(".txt"):
            transcript_files.append(os.path.join(TRANSCRIPT_DIR, filename))

    print(f"Found {len(transcript_files)} transcript files\n")

    all_inserts = []
    for filepath in sorted(transcript_files):
        try:
            inserts = process_file(filepath)
            all_inserts.extend(inserts)
        except Exception as e:
            print(f"  ERROR: {e}")

    # Write to output file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("-- LangChain Transcript Inserts\n")
        f.write(f"-- Generated: 2025-12-21\n")
        f.write(f"-- Total chunks: {len(all_inserts)}\n\n")
        for sql in all_inserts:
            f.write(sql + "\n\n")

    print(f"\n{'='*60}")
    print(f"Generated {len(all_inserts)} INSERT statements")
    print(f"Output: {OUTPUT_FILE}")
    print("=" * 60)

if __name__ == "__main__":
    main()
