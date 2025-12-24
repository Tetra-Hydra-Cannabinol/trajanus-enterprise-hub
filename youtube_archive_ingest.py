"""
YouTube Video Archive & Ingest System
======================================
For each video:
1. Extract transcript via Playwright
2. Save to Supabase KB
3. Download video via yt-dlp
4. Save video to archive
5. Save transcript to archive
6. Update archive index

Usage:
    python youtube_archive_ingest.py --video <video_id> --category <category>
    python youtube_archive_ingest.py --playlist <playlist_url> --category <category>
"""

import os
import re
import json
import subprocess
import argparse
from datetime import datetime

# Supabase setup
try:
    from supabase import create_client
except ImportError:
    subprocess.check_call(['pip', 'install', 'supabase'])
    from supabase import create_client

# Configuration
BASE_DIR = r"G:\My Drive\00 - Trajanus USA\00-Command-Center"
ARCHIVE_DIR = os.path.join(BASE_DIR, "13-Knowledge-Base")
TRANSCRIPT_OUTPUT_DIR = os.path.join(BASE_DIR, "05-Scripts", "test_output")
INDEX_FILE = os.path.join(ARCHIVE_DIR, "Index", "archive_index.json")

def load_env():
    """Load environment variables from .env file."""
    env_path = os.path.join(BASE_DIR, ".env")
    env_vars = {}
    with open(env_path, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if line and '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    return env_vars

env = load_env()
supabase = create_client(env["SUPABASE_URL"], env["SUPABASE_ANON_KEY"])


def check_if_exists(video_id):
    """Check if video already exists in Supabase KB."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        result = supabase.table("knowledge_base").select("id, title").eq("url", url).limit(1).execute()
        if result.data:
            return True, result.data[0].get('title', 'Unknown')
        return False, None
    except Exception as e:
        print(f"  Error checking existence: {e}")
        return False, None


def get_video_info(video_id):
    """Get video metadata using yt-dlp."""
    try:
        result = subprocess.run(
            ['yt-dlp', '--dump-json', '--no-download', f'https://www.youtube.com/watch?v={video_id}'],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception as e:
        print(f"  Error getting video info: {e}")
    return None


def get_playlist_videos(playlist_url):
    """Get all video IDs from a playlist."""
    try:
        result = subprocess.run(
            ['yt-dlp', '--flat-playlist', '--dump-json', playlist_url],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            videos = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    data = json.loads(line)
                    videos.append({
                        'id': data.get('id'),
                        'title': data.get('title', 'Unknown'),
                        'duration': data.get('duration', 0)
                    })
            return videos
    except Exception as e:
        print(f"Error getting playlist: {e}")
    return []


def download_video(video_id, category, video_title=""):
    """Download video using yt-dlp."""
    output_dir = os.path.join(ARCHIVE_DIR, "Videos", category)
    os.makedirs(output_dir, exist_ok=True)

    # Clean filename
    safe_title = re.sub(r'[<>:"/\\|?*]', '', video_title)[:80] if video_title else video_id
    output_template = os.path.join(output_dir, f"{video_id}_{safe_title}.%(ext)s")

    try:
        result = subprocess.run([
            'yt-dlp',
            '-f', 'bestvideo[height<=720]+bestaudio/best[height<=720]',
            '--merge-output-format', 'mp4',
            '-o', output_template,
            '--no-playlist',
            f'https://www.youtube.com/watch?v={video_id}'
        ], capture_output=True, text=True, timeout=600)

        if result.returncode == 0:
            # Find the downloaded file
            for f in os.listdir(output_dir):
                if f.startswith(video_id):
                    return os.path.join(output_dir, f)
        else:
            print(f"  yt-dlp error: {result.stderr[:200]}")
    except subprocess.TimeoutExpired:
        print(f"  Download timed out for {video_id}")
    except Exception as e:
        print(f"  Download error: {e}")
    return None


def save_transcript_to_archive(video_id, category, title, content, metadata):
    """Save transcript to archive directory."""
    output_dir = os.path.join(ARCHIVE_DIR, "Transcripts", category)
    os.makedirs(output_dir, exist_ok=True)

    safe_title = re.sub(r'[<>:"/\\|?*]', '', title)[:60]
    filename = f"{datetime.now().strftime('%Y-%m-%d')}_{metadata.get('level', 'INTERMEDIATE')}_{video_id}_{safe_title}.txt"
    filepath = os.path.join(output_dir, filename)

    # Build header
    header = f"""Title: {title}
Channel: {metadata.get('channel', 'Unknown')}
Video ID: {video_id}
URL: https://www.youtube.com/watch?v={video_id}
Duration: {metadata.get('duration', 'Unknown')}
Level: {metadata.get('level', 'INTERMEDIATE')}
Application: {metadata.get('application', category)}
Topics: {', '.join(metadata.get('topics', []))}
Ingested: {datetime.now().strftime('%Y-%m-%d')}
Source: Playwright Browser Extraction
{'='*78}

"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(header + content)

    return filepath


def chunk_text(text, chunk_size=3000):
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


def ingest_to_supabase(video_id, title, content, metadata, category):
    """Ingest transcript chunks to Supabase."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    chunks = chunk_text(content)

    full_metadata = {
        "channel": metadata.get('channel', 'Unknown'),
        "video_id": video_id,
        "duration": metadata.get('duration', ''),
        "level": metadata.get('level', 'INTERMEDIATE'),
        "application": metadata.get('application', category),
        "topics": metadata.get('topics', []),
        "source": "YouTube Transcript",
        "ingested_date": datetime.now().strftime('%Y-%m-%d'),
        "content_type": "youtube_tutorial",
        "category": category
    }

    inserted = 0
    for i, chunk in enumerate(chunks):
        summary = chunk[:200].replace('\n', ' ').strip()
        if len(chunk) > 200:
            summary += "..."

        record = {
            "url": url,
            "chunk_number": i + 1,
            "title": title,
            "summary": summary,
            "content": chunk,
            "metadata": full_metadata
        }

        try:
            supabase.table("knowledge_base").insert(record).execute()
            inserted += 1
        except Exception as e:
            print(f"    Error inserting chunk {i+1}: {e}")

    return inserted


def update_index(video_id, title, category, transcript_path, video_path):
    """Update the archive index file."""
    index = {}
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            index = json.load(f)

    if 'videos' not in index:
        index['videos'] = {}

    index['videos'][video_id] = {
        'title': title,
        'category': category,
        'transcript_path': transcript_path,
        'video_path': video_path,
        'archived_at': datetime.now().isoformat(),
        'in_supabase': True
    }

    index['last_updated'] = datetime.now().isoformat()
    index['total_videos'] = len(index['videos'])

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2)


def process_video(video_id, category, transcript_content=None, metadata=None, download=True):
    """Process a single video: archive and ingest."""
    print(f"\n{'='*60}")
    print(f"Processing: {video_id}")
    print(f"{'='*60}")

    # Check if already exists
    exists, existing_title = check_if_exists(video_id)
    if exists:
        print(f"  SKIP: Already in KB - {existing_title}")
        return {'status': 'skipped', 'reason': 'exists', 'title': existing_title}

    # Get video info if not provided
    if not metadata:
        info = get_video_info(video_id)
        if info:
            duration_secs = info.get('duration', 0)
            mins, secs = divmod(duration_secs, 60)
            hours, mins = divmod(mins, 60)
            duration_str = f"{hours}:{mins:02d}:{secs:02d}" if hours else f"{mins}:{secs:02d}"

            metadata = {
                'title': info.get('title', 'Unknown'),
                'channel': info.get('channel', info.get('uploader', 'Unknown')),
                'duration': duration_str,
                'level': 'INTERMEDIATE',
                'application': category,
                'topics': info.get('tags', [])[:10] if info.get('tags') else []
            }
        else:
            metadata = {
                'title': 'Unknown',
                'channel': 'Unknown',
                'duration': 'Unknown',
                'level': 'INTERMEDIATE',
                'application': category,
                'topics': []
            }

    title = metadata.get('title', 'Unknown')
    print(f"  Title: {title}")
    print(f"  Channel: {metadata.get('channel')}")

    result = {'status': 'processed', 'title': title, 'video_id': video_id}

    # Download video if requested
    video_path = None
    if download:
        print("  Downloading video...")
        video_path = download_video(video_id, category, title)
        if video_path:
            print(f"  Video saved: {os.path.basename(video_path)}")
            result['video_path'] = video_path
        else:
            print("  Video download failed (continuing with transcript)")

    # If transcript content provided, use it; otherwise return for Playwright extraction
    if transcript_content:
        # Save transcript to archive
        print("  Saving transcript to archive...")
        transcript_path = save_transcript_to_archive(video_id, category, title, transcript_content, metadata)
        print(f"  Transcript saved: {os.path.basename(transcript_path)}")
        result['transcript_path'] = transcript_path

        # Ingest to Supabase
        print("  Ingesting to Supabase...")
        chunks = ingest_to_supabase(video_id, title, transcript_content, metadata, category)
        print(f"  Inserted {chunks} chunks")
        result['chunks'] = chunks

        # Update index
        update_index(video_id, title, category, transcript_path, video_path)
        print("  Index updated")
    else:
        print("  NEEDS TRANSCRIPT: Use Playwright to extract, then call with content")
        result['needs_transcript'] = True

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='YouTube Archive & Ingest')
    parser.add_argument('--video', help='Single video ID')
    parser.add_argument('--playlist', help='Playlist URL')
    parser.add_argument('--category', default='General', help='Category for filing')
    parser.add_argument('--no-download', action='store_true', help='Skip video download')

    args = parser.parse_args()

    if args.playlist:
        print(f"Getting playlist videos from: {args.playlist}")
        videos = get_playlist_videos(args.playlist)
        print(f"Found {len(videos)} videos")

        for v in videos:
            result = process_video(v['id'], args.category, download=not args.no_download)
            print(f"  -> {result['status']}")

    elif args.video:
        result = process_video(args.video, args.category, download=not args.no_download)
        print(f"\nResult: {result}")

    else:
        print("Usage: python youtube_archive_ingest.py --video <id> --category <cat>")
        print("   or: python youtube_archive_ingest.py --playlist <url> --category <cat>")
