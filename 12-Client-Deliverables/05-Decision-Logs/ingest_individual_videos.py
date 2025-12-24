"""
Batch ingest individual video transcripts from 2025-12-20 research files to Supabase
"""

import os
import re
from datetime import datetime
from supabase import create_client

def load_env():
    env_path = r'G:\My Drive\00 - Trajanus USA\00-Command-Center\.env'
    env_vars = {}
    with open(env_path, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if line and '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    return env_vars

env = load_env()
supabase = create_client(env['SUPABASE_URL'], env['SUPABASE_ANON_KEY'])

def chunk_text(text, chunk_size=3000):
    chunks = []
    current = ''
    for line in text.split('\n'):
        if len(current) + len(line) + 1 <= chunk_size:
            current = current + '\n' + line if current else line
        else:
            if current:
                chunks.append(current.strip())
            current = line
    if current.strip():
        chunks.append(current.strip())
    return chunks

def parse_transcript_file(filepath):
    """Parse a saved transcript file and extract metadata and content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split header from transcript
    parts = content.split('=' * 78)
    if len(parts) < 2:
        parts = content.split('=' * 70)  # Try alternate separator

    if len(parts) < 2:
        print(f"  Could not parse header in {filepath}")
        return None

    header = parts[0]
    transcript = parts[1].strip()

    # Parse header fields
    metadata = {}
    for line in header.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip().lower().replace(' ', '_')
            metadata[key] = value.strip()

    # Parse topics into list
    topics_str = metadata.get('topics', '')
    topics = [t.strip() for t in topics_str.split(',') if t.strip()]

    return {
        'title': metadata.get('title', 'Unknown'),
        'channel': metadata.get('channel', 'MyOnlineTrainingHub'),
        'video_id': metadata.get('video_id', ''),
        'url': metadata.get('url', ''),
        'duration': metadata.get('duration', ''),
        'level': metadata.get('level', 'INTERMEDIATE'),
        'application': metadata.get('application', 'Microsoft Excel'),
        'topics': topics,
        'transcript': transcript
    }

def ingest_video(video_data):
    """Ingest a video transcript to Supabase."""
    url = video_data['url'] or f"https://www.youtube.com/watch?v={video_data['video_id']}"
    chunks = chunk_text(video_data['transcript'])

    full_metadata = {
        'channel': video_data['channel'],
        'video_id': video_data['video_id'],
        'duration': video_data['duration'],
        'level': video_data['level'],
        'application': video_data['application'],
        'topics': video_data['topics'],
        'source': 'YouTube Transcript',
        'ingested_date': datetime.now().strftime('%Y-%m-%d'),
        'content_type': 'youtube_tutorial',
        'category': 'Microsoft_Office'
    }

    inserted = 0
    for i, chunk in enumerate(chunks):
        summary = chunk[:200].replace('\n', ' ').strip()
        if len(chunk) > 200:
            summary += '...'

        record = {
            'url': url,
            'chunk_number': i + 1,
            'title': video_data['title'],
            'summary': summary,
            'content': chunk,
            'metadata': full_metadata
        }

        try:
            supabase.table('knowledge_base').insert(record).execute()
            inserted += 1
        except Exception as e:
            print(f'    Error chunk {i+1}: {e}')

    return inserted, len(chunks)

# Process all 2025-12-20 transcript files
research_dir = r'G:\My Drive\00 - Trajanus USA\01-Morning-Sessions\Research\Microsoft_Office_Tutorials'
files = [f for f in os.listdir(research_dir) if f.startswith('2025-12-20_') and f.endswith('.txt')]

print(f"Found {len(files)} transcript files to process\n")

total_inserted = 0
total_videos = 0

for filename in sorted(files):
    filepath = os.path.join(research_dir, filename)
    print(f"Processing: {filename}")

    video_data = parse_transcript_file(filepath)
    if video_data:
        inserted, total_chunks = ingest_video(video_data)
        total_inserted += inserted
        total_videos += 1
        print(f"  -> {video_data['title'][:50]}...")
        print(f"  -> {inserted}/{total_chunks} chunks inserted")
    else:
        print(f"  -> Skipped (parse error)")
    print()

print(f"\n{'='*60}")
print(f"SUMMARY: {total_videos} videos processed, {total_inserted} total chunks inserted")
