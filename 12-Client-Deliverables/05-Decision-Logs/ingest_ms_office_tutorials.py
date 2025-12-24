#!/usr/bin/env python3
"""
Ingest Microsoft Office Tutorial Transcripts to TKB
Targeted ingestion for Advanced/Expert level MS Office tutorials
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import time
import re

# Load environment from .env
from dotenv import load_dotenv
env_path = Path(__file__).parent / '.env'
if not env_path.exists():
    env_path = Path(__file__).parent / 'env.env'
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
TRANSCRIPT_DIR = Path(r"G:\My Drive\00 - Trajanus USA\01-Morning-Sessions\Research\Microsoft_Office_Tutorials")

# ANSI colors for terminal
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def chunk_text(text, chunk_size=1500, overlap=200):
    """Split text into overlapping chunks with sentence boundary detection"""
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
        print(f"    {Colors.RED}Embedding error: {e}{Colors.END}")
        return None

def parse_file_metadata(filepath, content):
    """Extract metadata from file header and filename"""
    lines = content.split('\n')

    # Parse header fields
    title = ""
    channel = ""
    video_id = ""
    url = ""
    duration = ""
    level = "ADVANCED"  # Default

    for line in lines[:10]:
        if line.startswith('Title:'):
            title = line.replace('Title:', '').strip()
        elif line.startswith('Channel:'):
            channel = line.replace('Channel:', '').strip()
        elif line.startswith('Video ID:'):
            video_id = line.replace('Video ID:', '').strip()
        elif line.startswith('URL:'):
            url = line.replace('URL:', '').strip()
        elif line.startswith('Duration:'):
            duration = line.replace('Duration:', '').strip()
        elif line.startswith('Level:'):
            level = line.replace('Level:', '').strip()

    # Extract level from filename if not in header
    filename = filepath.name
    if 'ADVANCED' in filename:
        level = 'ADVANCED'
    elif 'EXPERT' in filename:
        level = 'EXPERT'
    elif 'COMPREHENSIVE' in filename:
        level = 'COMPREHENSIVE'

    # Determine application from title/filename
    application = "Microsoft Office"
    title_lower = (title + filename).lower()
    if 'excel' in title_lower or 'vba' in title_lower or 'power query' in title_lower:
        application = "Excel"
    elif 'word' in title_lower:
        application = "Word"
    elif 'powerpoint' in title_lower:
        application = "PowerPoint"
    elif 'pivot' in title_lower:
        application = "Excel"
    elif 'vlookup' in title_lower or 'xlookup' in title_lower:
        application = "Excel"

    return {
        'title': title or filepath.stem,
        'channel': channel or 'Unknown',
        'video_id': video_id,
        'url': url,
        'duration': duration,
        'level': level,
        'application': application
    }

def get_tags_for_content(metadata, content):
    """Generate relevant tags based on content analysis"""
    tags = ['microsoft-office', 'tutorial', 'youtube-transcript']

    app = metadata['application'].lower()
    level = metadata['level'].lower()

    # Application tags
    if app == 'excel':
        tags.extend(['excel', 'spreadsheet'])
    elif app == 'word':
        tags.extend(['word', 'document'])
    elif app == 'powerpoint':
        tags.extend(['powerpoint', 'presentation'])

    # Level tags
    if 'advanced' in level:
        tags.append('advanced')
    if 'expert' in level:
        tags.append('expert')
    if 'comprehensive' in level:
        tags.extend(['beginner', 'intermediate', 'advanced', 'expert'])

    # Content-specific tags
    content_lower = content.lower()
    if 'vba' in content_lower or 'macro' in content_lower:
        tags.extend(['vba', 'macros', 'automation'])
    if 'power query' in content_lower:
        tags.extend(['power-query', 'data-transformation'])
    if 'pivot' in content_lower:
        tags.extend(['pivot-tables', 'data-analysis'])
    if 'vlookup' in content_lower or 'xlookup' in content_lower:
        tags.extend(['lookup-functions', 'formulas'])
    if 'slide master' in content_lower:
        tags.append('slide-master')
    if 'template' in content_lower:
        tags.append('templates')
    if 'animation' in content_lower:
        tags.append('animations')
    if 'copilot' in content_lower:
        tags.extend(['copilot', 'ai'])

    return list(set(tags))  # Remove duplicates

def ingest_file(filepath):
    """Ingest a single transcript file"""
    print(f"\n{Colors.CYAN}{'='*70}")
    print(f"Processing: {filepath.name}")
    print(f"{'='*70}{Colors.END}")

    # Read file
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  {Colors.RED}ERROR reading file: {e}{Colors.END}")
        return 0

    print(f"  Read {len(content):,} characters")

    # Extract metadata
    metadata = parse_file_metadata(filepath, content)
    print(f"  Title: {metadata['title'][:60]}...")
    print(f"  Application: {metadata['application']}")
    print(f"  Level: {metadata['level']}")
    print(f"  Channel: {metadata['channel']}")

    # Get main content (skip header)
    main_content = content
    if '=' * 20 in content:
        parts = content.split('=' * 20)
        if len(parts) > 1:
            main_content = parts[-1].strip()

    # Chunk the content
    chunks = chunk_text(main_content)
    print(f"  Created {Colors.GREEN}{len(chunks)}{Colors.END} chunks")

    # Get tags
    tags = get_tags_for_content(metadata, content)
    print(f"  Tags: {', '.join(tags[:5])}{'...' if len(tags) > 5 else ''}")

    success_count = 0

    for i, chunk in enumerate(chunks, 1):
        print(f"  Chunk {i}/{len(chunks)}: ", end='', flush=True)

        # Generate embedding
        embedding = generate_embedding(chunk)
        if not embedding:
            print(f"{Colors.RED}SKIP (no embedding){Colors.END}")
            continue

        # Create summary (first 150 chars)
        summary = chunk[:150].replace('\n', ' ').strip() + '...'

        # Insert into database
        try:
            data = {
                "url": metadata['url'] or f"youtube://{metadata['video_id'] or filepath.stem}",
                "chunk_number": i,
                "title": f"{metadata['title']} (Part {i}/{len(chunks)})",
                "summary": summary,
                "content": chunk,
                "metadata": {
                    "source": "ms-office-tutorials",
                    "category": f"{metadata['application'].lower()}-{metadata['level'].lower()}",
                    "application": metadata['application'],
                    "level": metadata['level'],
                    "channel": metadata['channel'],
                    "video_id": metadata['video_id'],
                    "duration": metadata['duration'],
                    "filename": filepath.name,
                    "total_chunks": len(chunks),
                    "tags": tags,
                    "ingested_at": datetime.now().isoformat()
                },
                "embedding": embedding
            }

            result = supabase.table('knowledge_base').insert(data).execute()

            if result.data:
                print(f"{Colors.GREEN}OK{Colors.END} (ID: {result.data[0].get('id', 'N/A')})")
                success_count += 1
            else:
                print(f"{Colors.RED}FAIL (no data returned){Colors.END}")

        except Exception as e:
            error_msg = str(e)[:60]
            print(f"{Colors.RED}FAIL ({error_msg}){Colors.END}")

        # Rate limiting
        time.sleep(0.3)

    print(f"\n  {Colors.GREEN}Result: {success_count}/{len(chunks)} chunks ingested{Colors.END}")
    return success_count

def get_kb_stats():
    """Get current KB statistics"""
    try:
        result = supabase.table('knowledge_base').select('id', count='exact').execute()
        return result.count or 0
    except:
        return 0

def get_ms_office_stats():
    """Get MS Office specific stats"""
    try:
        result = supabase.table('knowledge_base').select('metadata').execute()
        ms_office_count = sum(1 for d in result.data
                            if d.get('metadata', {}).get('source') == 'ms-office-tutorials')
        return ms_office_count
    except:
        return 0

def main():
    print(f"\n{Colors.CYAN}{'='*70}")
    print(f"{'MS OFFICE TUTORIAL INGESTION TO TKB':^70}")
    print(f"{'='*70}{Colors.END}")
    print(f"Transcript Directory: {TRANSCRIPT_DIR}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Get initial stats
    initial_count = get_kb_stats()
    initial_ms_count = get_ms_office_stats()
    print(f"\n{Colors.CYAN}Initial TKB Document Count: {initial_count}{Colors.END}")
    print(f"{Colors.CYAN}Existing MS Office Tutorials: {initial_ms_count}{Colors.END}")

    # Find transcript files - look for ADVANCED, EXPERT, COMPREHENSIVE
    patterns = [
        "2025-12-19_ADVANCED_*.txt",
        "2025-12-19_EXPERT_*.txt",
        "2025-12-19_COMPREHENSIVE_*.txt"
    ]

    transcript_files = []
    for pattern in patterns:
        transcript_files.extend(list(TRANSCRIPT_DIR.glob(pattern)))

    # Sort by name
    transcript_files = sorted(set(transcript_files), key=lambda x: x.name)

    print(f"\n{Colors.GREEN}Found {len(transcript_files)} Advanced/Expert tutorial files:{Colors.END}")
    for f in transcript_files:
        size = f.stat().st_size
        print(f"  - {f.name} ({size:,} bytes)")

    if not transcript_files:
        print(f"{Colors.RED}ERROR: No transcript files found!{Colors.END}")
        return

    # Confirm before proceeding (skip if --yes flag is passed)
    print(f"\n{Colors.YELLOW}Ready to ingest {len(transcript_files)} files to Supabase KB.{Colors.END}")
    if '--yes' not in sys.argv and '-y' not in sys.argv:
        confirm = input(f"{Colors.YELLOW}Continue? (y/n): {Colors.END}")
        if confirm.lower() != 'y':
            print("Aborted.")
            return
    else:
        print("Auto-confirmed with --yes flag")

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
    final_ms_count = get_ms_office_stats()

    # Print summary
    print(f"\n{Colors.CYAN}{'='*70}")
    print(f"{'INGESTION COMPLETE':^70}")
    print(f"{'='*70}{Colors.END}")
    print(f"Files Processed: {len(transcript_files)}")
    print(f"Total Chunks Ingested: {Colors.GREEN}{total_success}{Colors.END}")
    print(f"Files Failed: {Colors.RED if total_failed > 0 else Colors.END}{total_failed}{Colors.END}")
    print(f"\n{Colors.CYAN}TKB Document Count:{Colors.END}")
    print(f"  Before: {initial_count}")
    print(f"  After:  {final_count}")
    print(f"  Added:  {Colors.GREEN}{final_count - initial_count}{Colors.END}")
    print(f"\n{Colors.CYAN}MS Office Tutorials:{Colors.END}")
    print(f"  Before: {initial_ms_count}")
    print(f"  After:  {final_ms_count}")

    print(f"\n{'-'*70}")
    print("FILE RESULTS:")
    print(f"{'-'*70}")
    for filename, status, chunks in file_results:
        status_icon = f"{Colors.GREEN}OK{Colors.END}" if status == "SUCCESS" else f"{Colors.RED}FAIL{Colors.END}"
        print(f"  [{status_icon}] {filename[:55]}: {chunks} chunks")

    print(f"\n{Colors.CYAN}{'='*70}{Colors.END}\n")

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
