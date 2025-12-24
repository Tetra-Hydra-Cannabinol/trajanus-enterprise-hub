#!/usr/bin/env python3
"""
YouTube Transcript Downloader using yt-dlp
Downloads auto-generated captions from YouTube videos.
"""

import subprocess
import re
import sys
import os
from pathlib import Path
from datetime import datetime

DEFAULT_OUTPUT_DIR = r"G:\My Drive\00 - Trajanus USA\00-Command-Center\13-Knowledge-Base\Transcripts\New_Videos"

def sanitize_filename(title: str, max_length: int = 50) -> str:
    """Convert title to safe filename."""
    safe = re.sub(r'[<>:"/\\|?*]', '', title)
    safe = re.sub(r'\s+', '_', safe)
    safe = safe[:max_length]
    return safe

def determine_level(duration_seconds: int, title: str) -> str:
    """Determine skill level based on duration and title keywords."""
    title_lower = title.lower()
    if any(word in title_lower for word in ['expert', 'mastery', 'professional']):
        return 'EXPERT'
    if any(word in title_lower for word in ['advanced', 'ninja', 'pro tips']):
        return 'ADVANCED'
    if any(word in title_lower for word in ['beginner', 'basics', 'introduction', 'getting started']):
        return 'BEGINNER'
    if duration_seconds < 600:
        return 'BEGINNER'
    elif duration_seconds < 1800:
        return 'INTERMEDIATE'
    elif duration_seconds < 3600:
        return 'ADVANCED'
    else:
        return 'COMPREHENSIVE'

def get_video_info(url: str) -> dict:
    """Get video metadata using yt-dlp."""
    try:
        result = subprocess.run(
            ['yt-dlp', '--dump-json', '--no-download', url],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            import json
            return json.loads(result.stdout)
    except Exception as e:
        print(f"  Error getting video info: {e}")
    return {}

def download_transcript(url: str, output_dir: str) -> dict:
    """Download transcript for a single video."""
    # Extract video ID
    video_id_match = re.search(r'(?:v=|/)([a-zA-Z0-9_-]{11})', url)
    if not video_id_match:
        return {'success': False, 'error': 'Invalid YouTube URL', 'url': url}

    video_id = video_id_match.group(1)
    result = {'video_id': video_id, 'url': url}

    print(f"\n[PROCESS] {video_id}")

    # Get video info
    info = get_video_info(url)
    title = info.get('title', 'Unknown_Title')
    channel = info.get('channel', 'Unknown')
    duration = info.get('duration', 0)

    print(f"  Title: {title}")
    print(f"  Duration: {duration // 60}:{duration % 60:02d}")

    # Create temp file for subtitle download
    temp_dir = Path(output_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_file = temp_dir / f"temp_{video_id}"

    # Download auto-generated English subtitles
    print("  Downloading transcript...")
    try:
        cmd = [
            'yt-dlp',
            '--skip-download',
            '--write-auto-sub',
            '--sub-lang', 'en',
            '--sub-format', 'vtt',
            '--convert-subs', 'srt',
            '-o', str(temp_file),
            url
        ]
        subprocess.run(cmd, capture_output=True, timeout=120)

        # Find the downloaded subtitle file
        srt_file = None
        for f in temp_dir.glob(f"temp_{video_id}*.srt"):
            srt_file = f
            break

        if not srt_file or not srt_file.exists():
            # Try .vtt
            for f in temp_dir.glob(f"temp_{video_id}*.vtt"):
                srt_file = f
                break

        if not srt_file or not srt_file.exists():
            result['success'] = False
            result['error'] = 'No subtitles downloaded'
            return result

        # Read and clean the subtitle content
        with open(srt_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Clean SRT format - remove timestamps and sequence numbers
        lines = content.split('\n')
        text_lines = []
        skip_next = False
        for line in lines:
            line = line.strip()
            # Skip empty lines, sequence numbers, and timestamps
            if not line:
                continue
            if re.match(r'^\d+$', line):
                continue
            if re.match(r'\d{2}:\d{2}:\d{2}', line):
                continue
            if '-->' in line:
                continue
            # Remove HTML tags
            line = re.sub(r'<[^>]+>', '', line)
            if line:
                text_lines.append(line)

        # Remove consecutive duplicates (common in auto-generated subs)
        cleaned = []
        prev_line = None
        for line in text_lines:
            if line != prev_line:
                cleaned.append(line)
                prev_line = line

        transcript = '\n'.join(cleaned)

        # Delete temp subtitle file
        srt_file.unlink()

        # Create final output file
        level = determine_level(duration, title)
        date_str = datetime.now().strftime('%Y-%m-%d')
        safe_title = sanitize_filename(title)
        filename = f"{date_str}_{level}_{video_id}_{safe_title}.txt"

        header = f"""Title: {title}
Channel: {channel}
Video ID: {video_id}
URL: https://www.youtube.com/watch?v={video_id}
Duration: {duration // 60}:{duration % 60:02d}
Level: {level}
Ingested: {date_str}
Source: yt-dlp Auto-Generated Captions
==============================================================================

"""

        output_path = temp_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(header + transcript)

        result['success'] = True
        result['title'] = title
        result['output_file'] = str(output_path)
        result['chars'] = len(transcript)
        print(f"  Saved: {filename} ({len(transcript)} chars)")

    except subprocess.TimeoutExpired:
        result['success'] = False
        result['error'] = 'Download timeout'
    except Exception as e:
        result['success'] = False
        result['error'] = str(e)
        print(f"  Error: {e}")

    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python download_youtube_transcripts.py <url1> [url2] ...")
        print("   or: python download_youtube_transcripts.py urls.json [output_dir]")
        sys.exit(1)

    # Check if first arg is a JSON file
    if sys.argv[1].endswith('.json'):
        import json
        with open(sys.argv[1], 'r') as f:
            urls = json.load(f)
        output_dir = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUTPUT_DIR
    else:
        urls = sys.argv[1:]
        output_dir = DEFAULT_OUTPUT_DIR

    print("=" * 70)
    print("YOUTUBE TRANSCRIPT DOWNLOADER")
    print("=" * 70)
    print(f"Videos to process: {len(urls)}")
    print(f"Output directory: {output_dir}")

    results = []
    for i, url in enumerate(urls):
        print(f"\n[{i+1}/{len(urls)}] Processing...")
        result = download_transcript(url, output_dir)
        results.append(result)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    success = [r for r in results if r.get('success')]
    failed = [r for r in results if not r.get('success')]

    print(f"Total: {len(results)}")
    print(f"Success: {len(success)}")
    print(f"Failed: {len(failed)}")

    if success:
        print("\nSuccessful:")
        for r in success:
            print(f"  - {r['video_id']}: {r.get('title', 'Unknown')[:50]}")

    if failed:
        print("\nFailed:")
        for r in failed:
            print(f"  - {r['video_id']}: {r.get('error', 'Unknown')}")

    print("=" * 70)

if __name__ == '__main__':
    main()
