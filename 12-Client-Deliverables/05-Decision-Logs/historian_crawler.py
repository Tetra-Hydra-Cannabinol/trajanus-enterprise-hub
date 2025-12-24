"""
HISTORIAN AGENT - KNOWLEDGE CRAWLER
===================================
Builds comprehensive US & World History knowledge base from non-biased,
non-government sources with constitutional originalist perspective.

Primary Sources:
- Hillsdale College (@HCPodcasts)
- S2 Underground (@S2Underground)
- Veritasium (history of science/tech only)

PROHIBITED: National Archives, Library of Congress, Smithsonian,
            Government universities, UNESCO, UN historical projects

Uses yt-dlp for searching and subtitle download.
Requires youtube_cookies.txt for authenticated requests.
Run export_youtube_cookies.py as Administrator to generate cookies.
"""

import os
import sys
import subprocess
import json
import time
import re
import tempfile
from datetime import datetime

# Output directory
OUTPUT_DIR = "G:/My Drive/00 - Trajanus USA/01-Morning-Sessions/Research/Historian_Knowledge"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Scripts directory (for cookies file)
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
COOKIES_FILE = os.path.join(SCRIPTS_DIR, "youtube_cookies.txt")

# Priority channels (prefer these in search)
PRIORITY_CHANNELS = [
    "hillsdale",
    "hcpodcasts",
    "s2underground",
    "s2 underground",
    "veritasium",
    "victor davis hanson",
    "larry arnn",
    "prager",
    "prageru",
    "epoch times",
    "daily wire",
    "history hit",
    "epic history",
    "timeline",
    "great courses"
]

# Prohibited terms in channel names (reject these sources)
PROHIBITED_TERMS = [
    "national archives",
    "library of congress",
    "smithsonian",
    ".gov",
    "government channel",
    "federal education",
    "unesco",
    "united nations",
    "pbs",
    "c-span",
    "vox",
    "vice news",
    "now this"
]

# All 50 search queries
QUERIES = [
    # US History (20 queries)
    "Hillsdale College US history founding fathers",
    "Hillsdale College Constitution 101",
    "Victor Davis Hanson American history lecture",
    "Larry Arnn constitutional history",
    "Hillsdale College Civil War",
    "Hillsdale College Revolutionary War",
    "founding fathers federalist papers",
    "constitutional originalism explained",
    "American Revolution causes documentary",
    "Civil War reconstruction history",
    "Progressive era American history",
    "World War 1 America entry",
    "World War 2 home front America",
    "Cold War America Soviet Union",
    "American economic history free market",
    "Bill of Rights amendments explained",
    "Supreme Court landmark cases history",
    "American westward expansion",
    "Industrial revolution America",
    "Great Depression causes effects",

    # World History (15 queries)
    "S2 Underground geopolitics history",
    "ancient Rome civilization history",
    "medieval Europe feudalism",
    "Renaissance European history",
    "Age of Enlightenment philosophy",
    "French Revolution causes timeline",
    "Napoleon Bonaparte military strategy",
    "British Empire rise fall",
    "World War 1 causes timeline",
    "World War 2 Eastern front",
    "Cold War origins Iron Curtain",
    "fall of Soviet Union 1991",
    "ancient Greece democracy philosophy",
    "Industrial Revolution Britain",
    "decolonization 20th century",

    # Constitutional & Political (10 queries)
    "Hillsdale College Federalist Papers",
    "Constitution framers intent",
    "separation of powers explained",
    "checks and balances government",
    "limited government principles",
    "individual rights natural law",
    "Second Amendment original meaning",
    "First Amendment free speech history",
    "Tenth Amendment states rights",
    "Electoral College purpose explained",

    # Military History (5 queries)
    "Victor Davis Hanson military history",
    "ancient warfare tactics strategy",
    "World War 2 military strategy",
    "American Civil War battles",
    "Napoleon military campaigns"
]

def is_approved_source(channel_title, video_title):
    """
    Check if source is approved (not government-affiliated).
    Returns (True, reason) if approved, (False, reason) if prohibited.
    """
    combined = (channel_title + " " + video_title).lower()

    # Reject if prohibited term found
    for term in PROHIBITED_TERMS:
        if term in combined:
            return False, f"Prohibited: contains '{term}'"

    return True, "Approved"

def is_priority_channel(channel_title):
    """Check if channel is a priority source"""
    channel_lower = channel_title.lower()
    for priority in PRIORITY_CHANNELS:
        if priority in channel_lower:
            return True
    return False

def sanitize_filename(text):
    """Remove invalid filename characters and limit length"""
    sanitized = re.sub(r'[<>:"/\\|?*]', '', text)
    sanitized = re.sub(r'\s+', '_', sanitized)
    return sanitized[:60]

def check_cookies():
    """Check if cookies file exists"""
    if os.path.exists(COOKIES_FILE):
        return True
    return False

def search_youtube_ytdlp(query, max_results=3):
    """
    Search YouTube using yt-dlp (no API key required).
    Returns list of video metadata dicts.
    """
    try:
        # Use yt-dlp to search YouTube
        cmd = [
            'yt-dlp',
            '--js-runtimes', 'node',
            f'ytsearch{max_results * 3}:{query}',  # Get extra results to filter
            '--flat-playlist',
            '--dump-json',
            '--no-warnings',
            '--quiet'
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            encoding='utf-8',
            errors='replace'
        )

        videos = []
        rejected = []

        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            try:
                video_data = json.loads(line)
                video_id = video_data.get('id', '')
                title = video_data.get('title', '')
                channel = video_data.get('channel', video_data.get('uploader', ''))
                duration = video_data.get('duration', 0)

                # Skip very short videos (likely not substantive content)
                if duration and duration < 180:  # Less than 3 minutes
                    continue

                # Skip very long videos (likely full courses, harder to process)
                if duration and duration > 7200:  # More than 2 hours
                    continue

                # Check if approved source
                approved, reason = is_approved_source(channel, title)

                if not approved:
                    rejected.append({
                        'channel': channel,
                        'title': title,
                        'reason': reason
                    })
                    continue

                video_info = {
                    'video_id': video_id,
                    'title': title,
                    'channel': channel,
                    'duration': duration,
                    'is_priority': is_priority_channel(channel)
                }

                videos.append(video_info)

                if len(videos) >= max_results:
                    break

            except json.JSONDecodeError:
                continue

        # Sort to prioritize preferred channels
        videos.sort(key=lambda x: (0 if x['is_priority'] else 1, x['title']))

        return videos[:max_results], rejected

    except subprocess.TimeoutExpired:
        print(f"  [TIMEOUT] Search timed out for query")
        return [], []
    except Exception as e:
        print(f"  [ERROR] Search failed: {e}")
        return [], []

def parse_vtt(vtt_content):
    """Parse VTT subtitle file and extract plain text"""
    lines = vtt_content.split('\n')
    text_lines = []

    skip_header = True
    for line in lines:
        line = line.strip()

        # Skip empty lines and header
        if not line:
            continue
        if skip_header and (line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:')):
            continue
        skip_header = False

        # Skip timestamp lines
        if '-->' in line:
            continue

        # Skip numeric cue identifiers
        if line.isdigit():
            continue

        # Clean up the text
        # Remove HTML-like tags
        line = re.sub(r'<[^>]+>', '', line)
        # Remove VTT positioning tags
        line = re.sub(r'<c[^>]*>', '', line)
        line = re.sub(r'</c>', '', line)

        if line:
            text_lines.append(line)

    # Join and clean up
    text = ' '.join(text_lines)
    # Remove duplicate phrases (common in auto-captions)
    text = re.sub(r'\b(\w+)\s+\1\b', r'\1', text)
    return text

def get_transcript_ytdlp(video_id, use_cookies=False):
    """
    Get transcript using yt-dlp subtitle download.
    Returns (transcript_text, status_message)
    """
    try:
        # Create temporary directory for subtitle file
        with tempfile.TemporaryDirectory() as temp_dir:
            output_template = os.path.join(temp_dir, '%(id)s')

            cmd = [
                'yt-dlp',
                '--js-runtimes', 'node',
                '--write-auto-sub',
                '--write-sub',
                '--sub-lang', 'en',
                '--sub-format', 'vtt',
                '--skip-download',
                '-o', output_template,
                '--quiet',
                '--no-warnings'
            ]

            # Add cookies if available
            if use_cookies and os.path.exists(COOKIES_FILE):
                cmd.extend(['--cookies', COOKIES_FILE])

            cmd.append(f'https://www.youtube.com/watch?v={video_id}')

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                encoding='utf-8',
                errors='replace'
            )

            # Check for subtitle file
            for ext in ['.en.vtt', '.en-orig.vtt', '.vtt']:
                sub_file = os.path.join(temp_dir, f'{video_id}{ext}')
                if os.path.exists(sub_file):
                    with open(sub_file, 'r', encoding='utf-8') as f:
                        vtt_content = f.read()
                    transcript = parse_vtt(vtt_content)
                    if transcript and len(transcript) > 100:  # Minimum length check
                        return transcript, "Success"

            # Check error message
            if 'Sign in to confirm' in result.stderr or 'bot' in result.stderr.lower():
                return None, "Blocked: Need cookies"
            elif 'No subtitles' in result.stderr:
                return None, "No subtitles available"

            return None, "No transcript found"

    except subprocess.TimeoutExpired:
        return None, "Timeout"
    except Exception as e:
        return None, str(e)[:50]

def get_transcript_api(video_id):
    """
    Fallback: Get transcript using youtube-transcript-api.
    Returns (transcript_text, status_message)
    """
    try:
        from youtube_transcript_api import YouTubeTranscriptApi

        api = YouTubeTranscriptApi()
        transcript_data = api.fetch(video_id, languages=['en'])

        texts = []
        for entry in transcript_data:
            if hasattr(entry, 'text'):
                texts.append(entry.text)
            elif isinstance(entry, dict):
                texts.append(entry.get('text', ''))

        transcript_text = ' '.join(texts)
        if transcript_text:
            return transcript_text, "Success"

        return None, "Empty transcript"

    except Exception as e:
        error_msg = str(e)
        if "blocked" in error_msg.lower() or "bot" in error_msg.lower():
            return None, "Blocked by YouTube"
        elif "disabled" in error_msg.lower():
            return None, "Transcripts disabled"
        return None, error_msg[:40]

def get_transcript(video_id, use_cookies=False):
    """
    Get transcript for a video, trying multiple methods.
    """
    # Method 1: Try yt-dlp with cookies
    if use_cookies:
        transcript, status = get_transcript_ytdlp(video_id, use_cookies=True)
        if transcript:
            return transcript, status

    # Method 2: Try yt-dlp without cookies
    transcript, status = get_transcript_ytdlp(video_id, use_cookies=False)
    if transcript:
        return transcript, status

    # Method 3: Fallback to youtube-transcript-api
    transcript, status = get_transcript_api(video_id)
    if transcript:
        return transcript, status

    return None, status

def categorize_query(query):
    """Determine the category of a query for organization"""
    query_lower = query.lower()

    if any(term in query_lower for term in ['hillsdale', 'constitution', 'federalist', 'amendment', 'framers', 'bill of rights', 'electoral', 'separation of powers', 'checks and balances', 'limited government', 'natural law']):
        return "Constitutional"
    elif any(term in query_lower for term in ['military', 'warfare', 'battle', 'campaign', 'strategy', 'napoleon']):
        return "Military"
    elif any(term in query_lower for term in ['american', 'civil war', 'revolutionary', 'founding', 'us history', 'progressive era', 'great depression', 'westward', 'world war.*america', 'cold war.*america']):
        return "US_History"
    else:
        return "World_History"

def main():
    start_time = datetime.now()

    print(f"\n{'='*70}")
    print(f"  HISTORIAN AGENT - KNOWLEDGE CRAWLER")
    print(f"  Non-Biased US & World History Knowledge Base Builder")
    print(f"{'='*70}\n")
    print(f"  Primary Sources: Hillsdale College, S2 Underground, Veritasium")
    print(f"  Prohibited: Government archives, PBS, UNESCO, State universities")
    print(f"  Output: {OUTPUT_DIR}")
    print(f"  Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Check for cookies
    has_cookies = check_cookies()
    if has_cookies:
        print(f"  [OK] Cookies file found: {COOKIES_FILE}")
    else:
        print(f"  [!] No cookies file. YouTube may block requests.")
        print(f"      Run 'python export_youtube_cookies.py' as Admin to fix.")

    print(f"\n{'='*70}\n")

    # Statistics tracking
    stats = {
        'total_queries': len(QUERIES),
        'total_searched': 0,
        'total_downloaded': 0,
        'no_transcript': 0,
        'blocked': 0,
        'rejected_government': 0,
        'priority_sources': 0,
        'by_category': {
            'Constitutional': 0,
            'Military': 0,
            'US_History': 0,
            'World_History': 0
        },
        'downloaded_videos': [],
        'rejected_sources': [],
        'blocked_videos': [],
        'processed_video_ids': set()  # Avoid duplicates
    }

    for i, query in enumerate(QUERIES, 1):
        category = categorize_query(query)
        print(f"\n[{i}/{len(QUERIES)}] [{category}] {query[:55]}...")

        video_results, rejected = search_youtube_ytdlp(query, max_results=2)

        # Track rejected government sources
        for rej in rejected:
            stats['rejected_government'] += 1
            stats['rejected_sources'].append({
                'channel': rej['channel'],
                'title': rej['title'],
                'reason': rej['reason'],
                'query': query
            })

        if not video_results:
            print(f"  [SKIP] No approved sources found for this query")
            continue

        for video in video_results:
            video_id = video['video_id']
            title = video['title']
            channel = video['channel']
            is_priority = video['is_priority']

            # Skip if already processed
            if video_id in stats['processed_video_ids']:
                print(f"  [DUP] Already processed: {title[:40]}...")
                continue

            stats['processed_video_ids'].add(video_id)
            stats['total_searched'] += 1

            priority_marker = "[PRIORITY]" if is_priority else ""
            print(f"  {priority_marker} [{channel[:25]}] {title[:40]}...")

            if is_priority:
                stats['priority_sources'] += 1

            transcript, status = get_transcript(video_id, use_cookies=has_cookies)

            if transcript:
                # Create organized filename with category
                safe_title = sanitize_filename(title)
                filename = f"{category}_{video_id}_{safe_title}.txt"
                filepath = os.path.join(OUTPUT_DIR, filename)

                # Write transcript with metadata
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"=" * 70 + "\n")
                    f.write(f"HISTORIAN KNOWLEDGE BASE - TRANSCRIPT\n")
                    f.write(f"=" * 70 + "\n\n")
                    f.write(f"Title: {title}\n")
                    f.write(f"Channel: {channel}\n")
                    f.write(f"Video ID: {video_id}\n")
                    f.write(f"URL: https://www.youtube.com/watch?v={video_id}\n")
                    f.write(f"Category: {category}\n")
                    f.write(f"Search Query: {query}\n")
                    f.write(f"Source Type: APPROVED (Non-government)\n")
                    f.write(f"Priority Source: {'Yes' if is_priority else 'No'}\n")
                    f.write(f"Downloaded: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"\n" + "=" * 70 + "\n")
                    f.write(f"TRANSCRIPT\n")
                    f.write(f"=" * 70 + "\n\n")
                    f.write(transcript)

                file_size = len(transcript) // 1024
                stats['total_downloaded'] += 1
                stats['by_category'][category] += 1
                stats['downloaded_videos'].append({
                    'video_id': video_id,
                    'title': title,
                    'channel': channel,
                    'category': category,
                    'size_kb': file_size,
                    'is_priority': is_priority
                })

                print(f"    [OK] Downloaded ({file_size} KB)")
            else:
                if "block" in status.lower() or "cookie" in status.lower():
                    stats['blocked'] += 1
                    stats['blocked_videos'].append({
                        'video_id': video_id,
                        'title': title,
                        'channel': channel,
                        'status': status
                    })
                else:
                    stats['no_transcript'] += 1
                print(f"    [SKIP] {status}")

            # Rate limiting
            time.sleep(1.5)

        # Additional delay between queries
        time.sleep(0.5)

    # Calculate runtime
    end_time = datetime.now()
    runtime = end_time - start_time

    # Generate summary report
    print(f"\n\n{'='*70}")
    print(f"  HISTORIAN AGENT - CRAWL COMPLETE")
    print(f"{'='*70}\n")

    print(f"  STATISTICS:")
    print(f"  {'-'*50}")
    print(f"  Total queries executed:     {stats['total_queries']}")
    print(f"  Videos processed:           {stats['total_searched']}")
    print(f"  Transcripts downloaded:     {stats['total_downloaded']}")
    print(f"  No transcript available:    {stats['no_transcript']}")
    print(f"  Blocked by YouTube:         {stats['blocked']}")
    print(f"  Government sources rejected:{stats['rejected_government']}")
    print(f"  Priority sources captured:  {stats['priority_sources']}")

    if stats['total_searched'] > 0:
        success_rate = (stats['total_downloaded'] / stats['total_searched']) * 100
        print(f"  Success rate:               {success_rate:.1f}%")

    print(f"\n  BY CATEGORY:")
    print(f"  {'-'*50}")
    for cat, count in stats['by_category'].items():
        print(f"  {cat:20s}: {count} transcripts")

    print(f"\n  RUNTIME:")
    print(f"  {'-'*50}")
    print(f"  Started:  {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Finished: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Duration: {runtime}")

    print(f"\n  OUTPUT:")
    print(f"  {'-'*50}")
    print(f"  Directory: {OUTPUT_DIR}")

    # Calculate total size
    total_size = 0
    file_count = 0
    for f in os.listdir(OUTPUT_DIR):
        if f.endswith('.txt') and not f.startswith('_'):
            total_size += os.path.getsize(os.path.join(OUTPUT_DIR, f))
            file_count += 1
    print(f"  Total files: {file_count}")
    print(f"  Total size: {total_size / (1024*1024):.2f} MB")

    if stats['blocked'] > 0:
        print(f"\n  [!] {stats['blocked']} videos were blocked by YouTube.")
        print(f"      Run 'python export_youtube_cookies.py' as Admin")
        print(f"      then re-run this crawler to get blocked transcripts.")

    print(f"\n{'='*70}")
    print(f"  Ready for TKB/Supabase ingestion!")
    print(f"{'='*70}\n")

    # Write detailed report
    report_path = os.path.join(OUTPUT_DIR, "_CRAWL_REPORT.txt")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("HISTORIAN KNOWLEDGE CRAWLER - DETAILED REPORT\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Crawl Date: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Duration: {runtime}\n")
        f.write(f"Total Transcripts: {stats['total_downloaded']}\n")
        f.write(f"Blocked Videos: {stats['blocked']}\n")
        f.write(f"Government Sources Rejected: {stats['rejected_government']}\n\n")

        f.write("BY CATEGORY:\n")
        f.write("-" * 40 + "\n")
        for cat, count in stats['by_category'].items():
            f.write(f"  {cat}: {count}\n")
        f.write("\n")

        f.write("DOWNLOADED VIDEOS:\n")
        f.write("-" * 70 + "\n")
        for vid in stats['downloaded_videos']:
            priority = "[PRIORITY]" if vid['is_priority'] else ""
            f.write(f"{priority} [{vid['category']}] {vid['title'][:50]}\n")
            f.write(f"   Channel: {vid['channel']}\n")
            f.write(f"   URL: https://www.youtube.com/watch?v={vid['video_id']}\n")
            f.write(f"   Size: {vid['size_kb']} KB\n\n")

        if stats['blocked_videos']:
            f.write("\nBLOCKED VIDEOS (need cookies):\n")
            f.write("-" * 70 + "\n")
            for vid in stats['blocked_videos']:
                f.write(f"[BLOCKED] {vid['title'][:50]}\n")
                f.write(f"   Channel: {vid['channel']}\n")
                f.write(f"   URL: https://www.youtube.com/watch?v={vid['video_id']}\n")
                f.write(f"   Status: {vid['status']}\n\n")

        if stats['rejected_sources']:
            f.write("\nREJECTED GOVERNMENT/PROHIBITED SOURCES:\n")
            f.write("-" * 70 + "\n")
            for rej in stats['rejected_sources'][:30]:
                f.write(f"[REJECTED] {rej['channel']}: {rej['title'][:50]}\n")
                f.write(f"   Reason: {rej['reason']}\n\n")

    print(f"  Detailed report saved: {report_path}\n")

    return stats

if __name__ == '__main__':
    main()
