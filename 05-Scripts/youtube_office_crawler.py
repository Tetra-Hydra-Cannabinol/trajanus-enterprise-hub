#!/usr/bin/env python3
"""
YouTube Office Tutorials Crawler
Downloads transcripts from curated Office tutorial videos
For TKB ingestion - Excel, Word, PowerPoint mastery content
"""

import os
import sys
import io
import json
import time
from datetime import datetime
import requests

# Force UTF-8 encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Output directory
OUTPUT_DIR = r"G:\My Drive\00 - Trajanus USA\01-Morning-Sessions\Research\Microsoft_Office_Tutorials"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Curated Office Tutorial Video IDs - VERIFIED REAL IDs
# Source: Top channels - Kevin Stratvert, Technology for Teachers, ExcelIsFun, freeCodeCamp
OFFICE_VIDEOS = [
    # === EXCEL - Kevin Stratvert (VERIFIED) ===
    ("e7xGuGqgp-Q", "Excel Tutorial for Beginners - Kevin Stratvert"),
    ("Y8xhrUa3KH4", "Excel Formulas and Functions Full Course"),
    ("m0wI61ahfLc", "Pivot Table Excel Tutorial"),
    ("OpNnMH6iY4A", "SUMIF Function in Excel Tutorial"),
    ("MTlQvyNQ3PM", "Excel Interactive Dashboard Tutorial"),

    # === EXCEL - Technology for Teachers (VERIFIED) ===
    ("wbJcJCkBcMg", "Excel for Beginners Complete Course"),

    # === EXCEL - freeCodeCamp (VERIFIED) ===
    ("Vl0H-qTclOg", "MS Excel Tutorial for Beginners - freeCodeCamp"),
    ("OOWAk2aLEfk", "Excel Data Analytics Full Course"),

    # === EXCEL - ExcelIsFun Mike Girvin (VERIFIED) ===
    ("auVDxCgrZAw", "Excel Magic Trick 1551 Lookup Discounted Price"),
    ("Q5ATZdAihl4", "MSPTDA 23 Two Fact Tables DAX Power Query"),
    ("RhPzRk-wEYw", "MSPTDA 22 DAX Data Modeling Date Time Dimension"),
    ("2D65INlQK9Y", "Excel Data Analysis Basics Class 00"),
    ("xjy6Rylp7ic", "Excel Data Analysis Basics Class 10"),
    ("VsCdU0e4Hcg", "Excel Data Analysis Basics Class 09"),
    ("wAlLqKFu9Tw", "Excel Data Analysis Basics Class 08"),
    ("MH2g-8191V8", "Excel Data Analysis Basics Class 07"),
    ("FLzKnNmE4Ms", "Excel Data Analysis Basics Class 06"),
    ("UVZcamKLJgU", "Excel Data Analysis Basics Class 05"),

    # === EXCEL - Power Query (VERIFIED) ===
    ("3ZkIwKBVkVE", "Power Query M Code Class Basic to Advanced"),
    ("BC_H6tJsxX0", "Power Query Excel Tutorial"),
    ("aIkul71ydvg", "Clean Data in Excel using Power Query"),
    ("BDHX8GT6UpQ", "3 HIDDEN tricks in Power Query editor"),
    ("fHFUh6EhBcw", "Combine Multiple Excel Files into ONE"),
    ("-787a_89BZk", "Power Query combining files in folder"),
    ("6jeSIRpjv0M", "File From Folder Power Query Tutorial"),
    ("jLpgt-wptH4", "Advanced Group By Power Query"),

    # === EXCEL - VLOOKUP (VERIFIED) ===
    ("-WAEzokHSJM", "Excel VLOOKUP Tutorial"),
    ("E7gQ-PgYkMc", "Excel VLOOKUP Tutorial 2"),

    # === WORD - Technology for Teachers (VERIFIED) ===
    ("2MCmnr2L50o", "Microsoft Word for Beginners Complete Course"),
    ("Jde2j55OCAA", "Most Useful Microsoft Word Keyboard Shortcuts"),

    # === POWERPOINT - Technology for Teachers (VERIFIED) ===
    ("XF34-Wu6qWU", "Microsoft PowerPoint Beginners Guide"),

    # === OFFICE 365 / OUTLOOK (VERIFIED) ===
    ("psHKqAJ03HQ", "Office 365 Tutorial Introduction"),
    ("pWGtXWumb4A", "Microsoft Outlook Tutorial for Beginners"),

    # === POWER BI (VERIFIED) ===
    ("wvsAzTqSDVg", "Mastering Power BI Tutorial"),
]

def get_video_info(video_id):
    """Get video metadata via oembed API (no API key needed)"""
    try:
        url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                'video_id': video_id,
                'url': f"https://www.youtube.com/watch?v={video_id}",
                'title': data.get('title', 'Unknown'),
                'channel': data.get('author_name', 'Unknown'),
                'thumbnail': data.get('thumbnail_url', '')
            }
    except Exception as e:
        print(f"  [WARN] Could not fetch metadata for {video_id}: {e}")

    return {
        'video_id': video_id,
        'url': f"https://www.youtube.com/watch?v={video_id}",
        'title': 'Unknown',
        'channel': 'Unknown',
        'thumbnail': ''
    }

def get_video_transcript(video_id):
    """Get transcript for a YouTube video using multiple methods"""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        from youtube_transcript_api.proxies import WebshareProxyConfig
        import http.cookiejar
        from pathlib import Path

        # Method 1: Try with cookies from browser (if available)
        cookies_path = Path.home() / 'youtube_cookies.txt'

        if cookies_path.exists():
            try:
                cookie_jar = http.cookiejar.MozillaCookieJar(str(cookies_path))
                cookie_jar.load()
                api = YouTubeTranscriptApi(cookie_jar=cookie_jar)
            except:
                api = YouTubeTranscriptApi()
        else:
            api = YouTubeTranscriptApi()

        # Try fetching with different language preferences
        languages_to_try = [['en'], ['en-US'], ['en-GB'], None]

        for lang in languages_to_try:
            try:
                if lang:
                    transcript_data = api.fetch(video_id, languages=lang)
                else:
                    # Try without language preference
                    transcript_list = api.list(video_id)
                    for transcript in transcript_list:
                        transcript_data = transcript.fetch()
                        full_text = ' '.join([segment.text for segment in transcript_data])
                        return {
                            'available': True,
                            'transcript': full_text,
                            'language': transcript.language,
                            'char_count': len(full_text)
                        }
                    continue

                full_text = ' '.join([segment.text for segment in transcript_data])
                return {
                    'available': True,
                    'transcript': full_text,
                    'language': lang[0] if lang else 'auto',
                    'char_count': len(full_text)
                }
            except Exception as fetch_err:
                # Check if IP blocked
                if 'IP' in str(fetch_err) or 'blocked' in str(fetch_err).lower():
                    return {'available': False, 'error': 'IP blocked by YouTube - try VPN or cookies'}
                continue

        return {'available': False, 'error': 'No transcript available'}

    except Exception as e:
        error_msg = str(e)
        if 'IP' in error_msg or 'blocked' in error_msg.lower():
            return {'available': False, 'error': 'IP blocked by YouTube'}
        return {'available': False, 'error': error_msg[:100]}

def crawl_office_tutorials():
    """Main crawling function"""
    print("=" * 70)
    print("YOUTUBE OFFICE TUTORIALS CRAWLER")
    print("=" * 70)
    print(f"Output Directory: {OUTPUT_DIR}")
    print(f"Videos to Process: {len(OFFICE_VIDEOS)}")
    print("-" * 70)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")

    results = []
    transcripts_success = 0
    transcripts_failed = 0
    total_chars = 0

    for idx, (video_id, description) in enumerate(OFFICE_VIDEOS, 1):
        print(f"\n[{idx}/{len(OFFICE_VIDEOS)}] {description}")
        print(f"  Video ID: {video_id}")

        # Get video metadata
        video_info = get_video_info(video_id)
        print(f"  Title: {video_info['title'][:55]}...")
        print(f"  Channel: {video_info['channel']}")

        # Get transcript
        transcript_data = get_video_transcript(video_id)

        if transcript_data.get('available'):
            transcripts_success += 1
            char_count = transcript_data['char_count']
            total_chars += char_count
            print(f"  Transcript: YES ({char_count:,} chars)")

            # Create safe filename
            safe_title = "".join(c for c in video_info['title'][:40] if c.isalnum() or c in ' -_').strip()
            safe_title = safe_title.replace(' ', '_')
            transcript_file = os.path.join(OUTPUT_DIR, f"{timestamp}_{video_id}_{safe_title}.txt")

            # Write transcript file
            with open(transcript_file, 'w', encoding='utf-8') as f:
                f.write(f"Title: {video_info['title']}\n")
                f.write(f"Channel: {video_info['channel']}\n")
                f.write(f"URL: {video_info['url']}\n")
                f.write(f"Description: {description}\n")
                f.write(f"Language: {transcript_data.get('language', 'en')}\n")
                f.write("=" * 70 + "\n\n")
                f.write(transcript_data['transcript'])

            video_info['transcript_file'] = os.path.basename(transcript_file)
            video_info['transcript_length'] = char_count
            video_info['has_transcript'] = True
        else:
            transcripts_failed += 1
            error = transcript_data.get('error', 'Unknown error')[:50]
            print(f"  Transcript: NO ({error})")
            video_info['has_transcript'] = False
            video_info['transcript_error'] = transcript_data.get('error', 'Unknown')

        video_info['description'] = description
        results.append(video_info)

        # Rate limiting
        time.sleep(0.5)

    # Save JSON results
    json_file = os.path.join(OUTPUT_DIR, f"{timestamp}_office_tutorials_results.json")
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Create summary markdown
    md_content = f"""# Microsoft Office Tutorials - Crawler Results

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Videos Processed**: {len(OFFICE_VIDEOS)}
**Transcripts Retrieved**: {transcripts_success}
**Transcripts Failed**: {transcripts_failed}
**Total Content**: {total_chars:,} characters ({total_chars/1024:.1f} KB)

---

## Videos with Transcripts

"""

    for video in results:
        if video.get('has_transcript'):
            md_content += f"### {video['title']}\n\n"
            md_content += f"- **Channel**: {video['channel']}\n"
            md_content += f"- **Category**: {video['description']}\n"
            md_content += f"- **URL**: {video['url']}\n"
            md_content += f"- **Transcript Length**: {video.get('transcript_length', 0):,} characters\n"
            md_content += f"- **File**: `{video.get('transcript_file', 'N/A')}`\n\n"

    md_content += "\n---\n\n## Videos Without Transcripts\n\n"

    for video in results:
        if not video.get('has_transcript'):
            md_content += f"- [{video['title']}]({video['url']}) - {video.get('transcript_error', 'No transcript')[:40]}\n"

    md_content += f"""

---

## Content Categories

### Excel
- Pivot Tables & Dashboards
- Formulas (VLOOKUP, XLOOKUP, INDEX/MATCH)
- Charts and Data Visualization
- Power Query & Power Pivot
- VBA & Macros

### Word
- Document Formatting
- Styles and Templates
- Headers, Footers, TOC
- Collaboration Features

### PowerPoint
- Presentation Design
- Master Slides
- Animations & Transitions
- Professional Tips

---

**Output Directory**: `{OUTPUT_DIR}`
**JSON Data**: `{os.path.basename(json_file)}`
**Status**: Complete
"""

    md_file = os.path.join(OUTPUT_DIR, f"{timestamp}_office_tutorials_summary.md")
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(md_content)

    # Print final summary
    print("\n" + "=" * 70)
    print("CRAWLER COMPLETE")
    print("=" * 70)
    print(f"Videos Processed: {len(OFFICE_VIDEOS)}")
    print(f"Transcripts Retrieved: {transcripts_success}")
    print(f"Transcripts Failed: {transcripts_failed}")
    print(f"Success Rate: {transcripts_success/len(OFFICE_VIDEOS)*100:.1f}%")
    print(f"Total Content: {total_chars:,} chars ({total_chars/1024:.1f} KB)")
    print("-" * 70)
    print(f"Output Directory: {OUTPUT_DIR}")
    print(f"JSON File: {os.path.basename(json_file)}")
    print(f"Summary File: {os.path.basename(md_file)}")
    print("=" * 70)

    return {
        'total': len(OFFICE_VIDEOS),
        'success': transcripts_success,
        'failed': transcripts_failed,
        'total_chars': total_chars,
        'output_dir': OUTPUT_DIR,
        'json_file': json_file,
        'md_file': md_file
    }

if __name__ == "__main__":
    result = crawl_office_tutorials()
    sys.exit(0 if result['success'] > 0 else 1)
