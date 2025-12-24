#!/usr/bin/env python3
"""
EXPERT KNOWLEDGE CRAWLER - 10-KEY ROTATION SYSTEM
==================================================
Comprehensive crawler for Office, Construction Software, and Traffic Studies

Categories:
- Microsoft Office Expert Level (30 queries)
- Primavera P6 Expert Level (15 queries)
- MS Project Expert Level (15 queries)
- RS Means Expert Level (10 queries)
- RMS 3.0 Expert Level (10 queries)
- Traffic Studies Comprehensive (40 queries)

Total: 120 queries x 2 results = 240 video target
Expected transcripts: 200-240

10 API Keys = 100,000 units available
Crawler needs ~12,000 units = 830% capacity buffer

Author: Trajanus USA
Date: 2024
"""

import os
import sys
import json
import time
import re
from datetime import datetime
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def clean_text(text):
    """Remove problematic Unicode characters."""
    if not text:
        return text
    return text.encode('ascii', 'ignore').decode('ascii')

# ============================================================
# API KEY ROTATION SYSTEM - 10 KEYS
# ============================================================

API_KEYS = [
    "REDACTED_YOUTUBE_KEY_1",  # Key 1 - FRESH NEW PROJECT
    "REDACTED_YOUTUBE_KEY_2",  # Key 2
    "REDACTED_YOUTUBE_KEY_3",  # Key 3
    "REDACTED_YOUTUBE_KEY_4",  # Key 4
    "REDACTED_YOUTUBE_KEY_5",  # Key 5
    "REDACTED_YOUTUBE_KEY_6",  # Key 6
    "REDACTED_YOUTUBE_KEY_7",  # Key 7
    "REDACTED_YOUTUBE_KEY_8",  # Key 8
    "REDACTED_YOUTUBE_KEY_9",  # Key 9
    "REDACTED_YOUTUBE_KEY_10",  # Key 10
    "REDACTED_YOUTUBE_KEY_11",  # Key 11
]

# Key management
current_key_index = 0
key_status = {i: {"status": "untested", "queries": 0, "exhausted_at": None} for i in range(len(API_KEYS))}

# ============================================================
# CONFIGURATION
# ============================================================

OUTPUT_DIR = "G:/My Drive/00 - Trajanus USA/01-Morning-Sessions/Research/Expert_Knowledge_Complete"
PROGRESS_FILE = os.path.join(OUTPUT_DIR, "_PROGRESS.json")
LOG_FILE = os.path.join(OUTPUT_DIR, "_CRAWL_LOG.txt")

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# SEARCH QUERIES - 120 TOTAL
# ============================================================

# Microsoft Office Expert Level (30 queries)
OFFICE_QUERIES = [
    "Excel advanced formulas INDEX MATCH INDIRECT",
    "Excel Power Query advanced transformations",
    "Excel VBA macros automation complete",
    "Excel pivot tables advanced techniques",
    "Excel Power Pivot data modeling",
    "Excel dynamic arrays XLOOKUP FILTER",
    "Excel conditional formatting advanced",
    "Excel data validation complex rules",
    "Excel dashboard design advanced",
    "Excel financial modeling techniques",
    "Word mail merge advanced automation",
    "Word styles formatting master document",
    "Word macros VBA automation",
    "Word tables advanced formatting",
    "Word document templates professional",
    "PowerPoint advanced animations",
    "PowerPoint slide master design",
    "PowerPoint VBA automation",
    "PowerPoint data visualization charts",
    "PowerPoint presentation design advanced",
    "Outlook VBA automation rules",
    "Outlook advanced email management",
    "Access database design normalization",
    "Access queries advanced SQL",
    "Access forms reports advanced",
    "Excel Power BI integration",
    "Office 365 integration automation",
    "Excel array formulas advanced",
    "Excel scenario analysis what-if",
    "Excel solver optimization",
]

# Primavera P6 Expert Level (15 queries)
P6_QUERIES = [
    "Primavera P6 advanced scheduling techniques",
    "P6 baseline management best practices",
    "P6 resource optimization leveling",
    "P6 earned value management advanced",
    "P6 critical path analysis methods",
    "P6 schedule compression techniques",
    "P6 activity codes WBS structure",
    "P6 global change advanced",
    "P6 advanced reporting dashboards",
    "P6 risk analysis Monte Carlo",
    "P6 multi-project management",
    "P6 activity step templates",
    "P6 schedule performance metrics",
    "P6 integration API automation",
    "P6 advanced filters layouts",
]

# MS Project Expert Level (15 queries)
MSPROJECT_QUERIES = [
    "Microsoft Project advanced scheduling",
    "MS Project resource leveling optimization",
    "MS Project earned value advanced",
    "MS Project custom fields formulas",
    "MS Project VBA macros automation",
    "MS Project baseline management",
    "MS Project critical chain method",
    "MS Project portfolio management",
    "MS Project advanced reporting",
    "MS Project integration SharePoint",
    "MS Project constraint management",
    "MS Project cost management advanced",
    "MS Project risk analysis",
    "MS Project multi-project consolidation",
    "MS Project advanced views filters",
]

# RS Means Expert Level (10 queries)
RSMEANS_QUERIES = [
    "RS Means cost estimating complete guide",
    "RS Means unit price book detailed",
    "construction cost estimating RS Means advanced",
    "RS Means quantity takeoff methods",
    "RS Means labor productivity rates",
    "RS Means material cost analysis",
    "RS Means location factors adjustment",
    "conceptual estimating detailed estimating",
    "construction cost database estimating",
    "RS Means online estimating tools",
]

# RMS 3.0 Expert Level (10 queries)
RMS_QUERIES = [
    "RMS 3.0 USACE complete tutorial",
    "RMS quality control reporting advanced",
    "RMS submittal tracking management",
    "RMS deficiency report workflow",
    "RMS progress reporting detailed",
    "RMS TRACES integration",
    "RMS CQC plan development",
    "RMS inspection documentation",
    "RMS closeout procedures",
    "RMS reporting requirements USACE",
]

# Traffic Studies - TIS Fundamentals (12 queries)
TIS_QUERIES = [
    "traffic impact study complete methodology",
    "traffic impact analysis professional tutorial",
    "TIS scoping study area determination",
    "traffic data collection comprehensive methods",
    "peak hour traffic analysis detailed",
    "traffic study report preparation standards",
    "baseline traffic conditions methodology",
    "future traffic conditions modeling",
    "traffic impact mitigation measures design",
    "traffic study peer review requirements",
    "multi-modal traffic impact analysis",
    "traffic study public hearing presentation",
]

# Traffic Studies - Trip Generation (8 queries)
TRIP_GEN_QUERIES = [
    "trip generation ITE manual complete",
    "trip generation rates all land uses",
    "internal capture reduction methodology",
    "pass-by trip analysis detailed",
    "trip distribution gravity model",
    "trip assignment traffic modeling",
    "site traffic generation calculation",
    "mixed use trip generation analysis",
]

# Traffic Studies - LOS & Capacity (10 queries)
LOS_QUERIES = [
    "level of service LOS complete calculation",
    "Highway Capacity Manual HCM tutorial",
    "intersection capacity analysis detailed",
    "signalized intersection LOS analysis",
    "roundabout capacity LOS analysis",
    "arterial LOS analysis methodology",
    "queue length analysis calculation",
    "volume capacity ratio analysis",
    "intersection delay calculation methods",
    "multi-lane highway capacity analysis",
]

# Traffic Studies - Traffic Control (10 queries)
TCP_QUERIES = [
    "traffic control plan TCP complete design",
    "MUTCD work zone traffic control",
    "temporary traffic control plan development",
    "MOT maintenance of traffic comprehensive",
    "construction work zone design standards",
    "traffic detour design methodology",
    "temporary traffic signal installation",
    "pedestrian accommodation work zones",
    "traffic control devices selection MUTCD",
    "phased construction traffic management",
]

# Combine all queries
ALL_QUERIES = (
    OFFICE_QUERIES +
    P6_QUERIES +
    MSPROJECT_QUERIES +
    RSMEANS_QUERIES +
    RMS_QUERIES +
    TIS_QUERIES +
    TRIP_GEN_QUERIES +
    LOS_QUERIES +
    TCP_QUERIES
)

# Category definitions
CATEGORIES = {
    "MS_Office": {"name": "Microsoft Office Expert", "start": 0, "end": 30},
    "Primavera_P6": {"name": "Primavera P6 Expert", "start": 30, "end": 45},
    "MS_Project": {"name": "MS Project Expert", "start": 45, "end": 60},
    "RS_Means": {"name": "RS Means Expert", "start": 60, "end": 70},
    "RMS_3": {"name": "RMS 3.0 USACE Expert", "start": 70, "end": 80},
    "TIS_Fundamentals": {"name": "TIS Fundamentals", "start": 80, "end": 92},
    "Trip_Generation": {"name": "Trip Generation", "start": 92, "end": 100},
    "LOS_Capacity": {"name": "LOS & Capacity", "start": 100, "end": 110},
    "Traffic_Control": {"name": "Traffic Control Plans", "start": 110, "end": 120},
}

# ============================================================
# KEY ROTATION FUNCTIONS
# ============================================================

def get_current_key():
    """Get the current API key."""
    global current_key_index
    return API_KEYS[current_key_index]

def rotate_key():
    """Rotate to the next available API key."""
    global current_key_index, key_status

    key_status[current_key_index]["status"] = "exhausted"
    key_status[current_key_index]["exhausted_at"] = datetime.now().isoformat()

    log_message(f"[KEY] Key {current_key_index + 1} exhausted after {key_status[current_key_index]['queries']} queries")

    # Find next working key
    for i in range(current_key_index + 1, len(API_KEYS)):
        if key_status[i]["status"] != "exhausted":
            current_key_index = i
            key_status[i]["status"] = "active"
            log_message(f"[KEY] Switched to Key {i + 1}")
            return True

    log_message("[KEY] ALL KEYS EXHAUSTED")
    return False

def test_all_keys():
    """Test all API keys and return the first working one."""
    global current_key_index, key_status

    print("\n" + "=" * 60)
    print("  TESTING ALL 10 API KEYS")
    print("=" * 60)

    for i, key in enumerate(API_KEYS):
        print(f"  [{i+1}/10] Testing key ...{key[-8:]}", end=" ")
        try:
            youtube = build('youtube', 'v3', developerKey=key)
            request = youtube.search().list(
                q="test",
                part='snippet',
                type='video',
                maxResults=1
            )
            response = request.execute()
            print("[OK] - AVAILABLE")
            key_status[i]["status"] = "available"
        except Exception as e:
            if 'quota' in str(e).lower():
                print("[EXHAUSTED]")
                key_status[i]["status"] = "exhausted"
            else:
                print(f"[ERROR]")
                key_status[i]["status"] = "error"

    # Find first working key
    for i, status in key_status.items():
        if status["status"] == "available":
            current_key_index = i
            key_status[i]["status"] = "active"
            print(f"\n  Starting with Key {i + 1}")
            print("=" * 60 + "\n")
            return True

    print("\n  NO WORKING KEYS FOUND!")
    print("=" * 60 + "\n")
    return False

def get_key_summary():
    """Get a summary of key usage."""
    summary = []
    for i, status in key_status.items():
        s = status["status"]
        q = status["queries"]
        summary.append(f"Key {i+1}: {s} ({q} queries)")
    return summary

# ============================================================
# LOGGING FUNCTIONS
# ============================================================

def log_message(msg):
    """Log a message to the log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {msg}\n"
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry)

def save_progress(data):
    """Save progress to JSON file."""
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def load_progress():
    """Load progress from JSON file."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def sanitize_filename(text):
    """Remove invalid characters from filename."""
    sanitized = re.sub(r'[<>:"/\\|?*]', '', text)
    sanitized = re.sub(r'\s+', '_', sanitized)
    return sanitized[:50]

def format_duration(seconds):
    """Format seconds into human-readable duration."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    return f"{secs}s"

def get_category_for_index(idx):
    """Get category key and name for query index."""
    for cat_key, cat_info in CATEGORIES.items():
        if cat_info["start"] <= idx < cat_info["end"]:
            return cat_key, cat_info["name"]
    return "Unknown", "Unknown"

# ============================================================
# YOUTUBE API FUNCTIONS
# ============================================================

def search_youtube(query, max_results=2):
    """Search YouTube with automatic key rotation."""
    global key_status

    while True:
        try:
            youtube = build('youtube', 'v3', developerKey=get_current_key())
            request = youtube.search().list(
                q=query,
                part='snippet',
                type='video',
                maxResults=max_results,
                relevanceLanguage='en',
                videoDuration='medium',
                order='relevance'
            )
            response = request.execute()

            key_status[current_key_index]["queries"] += 1

            results = []
            for item in response.get('items', []):
                results.append({
                    'video_id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'channel': item['snippet']['channelTitle'],
                    'description': item['snippet']['description'],
                    'published': item['snippet']['publishedAt']
                })
            return results

        except Exception as e:
            if 'quota' in str(e).lower():
                if not rotate_key():
                    return None  # All keys exhausted
            else:
                log_message(f"[ERROR] Search failed: {e}")
                return []

def get_transcript(video_id):
    """Get transcript for a YouTube video - tries multiple methods."""
    try:
        ytt = YouTubeTranscriptApi()

        # First try to list available transcripts
        try:
            transcripts = ytt.list(video_id)

            # Try English first
            for t in transcripts:
                if t.language_code == 'en' and not t.is_generated:
                    transcript_list = t.fetch()
                    return ' '.join([entry.text for entry in transcript_list])

            # Try auto-generated English
            for t in transcripts:
                if t.language_code == 'en' and t.is_generated:
                    transcript_list = t.fetch()
                    return ' '.join([entry.text for entry in transcript_list])

            # Try any English variant
            for t in transcripts:
                if 'en' in t.language_code.lower():
                    transcript_list = t.fetch()
                    return ' '.join([entry.text for entry in transcript_list])

            # Try first available
            for t in transcripts:
                transcript_list = t.fetch()
                return ' '.join([entry.text for entry in transcript_list])

        except:
            pass

        # Fallback - direct fetch
        transcript_list = ytt.fetch(video_id)
        return ' '.join([entry.text for entry in transcript_list])

    except:
        return None

# ============================================================
# MAIN CRAWLER FUNCTION
# ============================================================

def main():
    """Main crawler execution."""
    global key_status

    start_time = time.time()

    # Initialize log
    log_message("=" * 60)
    log_message("EXPERT KNOWLEDGE CRAWLER - SESSION STARTED")
    log_message("=" * 60)

    print("\n" + "=" * 70)
    print("  EXPERT KNOWLEDGE CRAWLER - 10-KEY ROTATION SYSTEM")
    print("=" * 70)
    print("\n  COVERAGE AREAS:")
    print("  - Microsoft Office Expert (30 queries)")
    print("  - Primavera P6 Expert (15 queries)")
    print("  - MS Project Expert (15 queries)")
    print("  - RS Means Expert (10 queries)")
    print("  - RMS 3.0 USACE Expert (10 queries)")
    print("  - Traffic Studies Comprehensive (40 queries)")
    print(f"\n  Total Queries: {len(ALL_QUERIES)}")
    print(f"  API Keys Available: {len(API_KEYS)}")
    print(f"  Total Capacity: {len(API_KEYS) * 10000:,} units")
    print(f"  Required: ~{len(ALL_QUERIES) * 100:,} units")
    print(f"\n  Output: {OUTPUT_DIR}")
    print("=" * 70 + "\n")

    # Test all keys
    if not test_all_keys():
        print("  [FATAL] No working API keys available!")
        return

    # Statistics
    stats = {
        'total_queries': len(ALL_QUERIES),
        'completed_queries': 0,
        'total_videos': 0,
        'total_transcripts': 0,
        'total_bytes': 0,
        'by_category': {k: {'queries': 0, 'transcripts': 0} for k in CATEGORIES},
        'processed_ids': set()
    }

    # Check for resume
    progress = load_progress()
    start_query = 0
    if progress:
        start_query = progress.get('last_query', 0) + 1
        stats['completed_queries'] = progress.get('completed_queries', 0)
        stats['total_transcripts'] = progress.get('total_transcripts', 0)
        stats['processed_ids'] = set(progress.get('processed_ids', []))
        if start_query > 0:
            print(f"  [RESUME] Continuing from query {start_query + 1}")
            log_message(f"Resuming from query {start_query + 1}")

    # Process all queries
    for query_idx in range(start_query, len(ALL_QUERIES)):
        query = ALL_QUERIES[query_idx]
        cat_key, cat_name = get_category_for_index(query_idx)

        # Progress report every 10 queries
        if query_idx > 0 and query_idx % 10 == 0:
            elapsed = time.time() - start_time
            print(f"\n  {'='*60}")
            print(f"  PROGRESS REPORT - Query {query_idx}/{len(ALL_QUERIES)}")
            print(f"  {'='*60}")
            print(f"  Transcripts: {stats['total_transcripts']}")
            print(f"  Current Key: {current_key_index + 1}")
            print(f"  Elapsed: {format_duration(elapsed)}")
            print(f"  Key Status:")
            for ks in get_key_summary():
                print(f"    {ks}")
            print(f"  {'='*60}\n")

        print(f"  [{query_idx + 1}/{len(ALL_QUERIES)}] [{cat_key}] {query[:45]}...")

        # Search YouTube
        results = search_youtube(query, max_results=4)

        if results is None:
            print("  [FATAL] All keys exhausted!")
            log_message("ALL KEYS EXHAUSTED - STOPPING")
            break

        if not results:
            print("    [WARN] No results")
            continue

        stats['by_category'][cat_key]['queries'] += 1

        for video in results:
            video_id = video['video_id']
            title = video['title']
            channel = video['channel']

            stats['total_videos'] += 1

            # Skip duplicates
            if video_id in stats['processed_ids']:
                continue
            stats['processed_ids'].add(video_id)

            print(f"    [{clean_text(channel)[:18]}] {clean_text(title)[:38]}...", end=" ")

            # Get transcript
            transcript = get_transcript(video_id)

            if transcript:
                # Save transcript
                safe_title = sanitize_filename(title)
                filename = f"{cat_key}_{video_id}_{safe_title}.txt"
                filepath = os.path.join(OUTPUT_DIR, filename)

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"{'='*70}\n")
                    f.write(f"EXPERT KNOWLEDGE BASE - TRANSCRIPT\n")
                    f.write(f"{'='*70}\n\n")
                    f.write(f"Title: {title}\n")
                    f.write(f"Channel: {channel}\n")
                    f.write(f"Video ID: {video_id}\n")
                    f.write(f"URL: https://www.youtube.com/watch?v={video_id}\n")
                    f.write(f"Published: {video['published']}\n")
                    f.write(f"\nSearch Query: {query}\n")
                    f.write(f"Category: {cat_name}\n")
                    f.write(f"\nDescription:\n{video['description']}\n")
                    f.write(f"\n{'='*70}\n")
                    f.write(f"TRANSCRIPT\n")
                    f.write(f"{'='*70}\n\n")
                    f.write(transcript)
                    f.write(f"\n\n{'='*70}\n")

                stats['total_transcripts'] += 1
                stats['total_bytes'] += len(transcript)
                stats['by_category'][cat_key]['transcripts'] += 1

                print(f"[OK] {len(transcript)//1024}KB")
            else:
                print("[SKIP]")

            time.sleep(0.5)

        stats['completed_queries'] = query_idx + 1

        # Save progress
        save_progress({
            'last_query': query_idx,
            'completed_queries': stats['completed_queries'],
            'total_transcripts': stats['total_transcripts'],
            'processed_ids': list(stats['processed_ids']),
            'timestamp': datetime.now().isoformat()
        })

        time.sleep(0.5)

    # Final report
    elapsed = time.time() - start_time

    print(f"\n\n{'='*70}")
    print(f"  EXPERT KNOWLEDGE CRAWLER - COMPLETE")
    print(f"{'='*70}")
    print(f"\n  FINAL STATISTICS")
    print(f"  {'-'*50}")
    print(f"  Queries completed: {stats['completed_queries']}/{len(ALL_QUERIES)}")
    print(f"  Videos processed: {stats['total_videos']}")
    print(f"  Transcripts downloaded: {stats['total_transcripts']}")
    print(f"  Total data: {stats['total_bytes'] / (1024*1024):.2f} MB")
    print(f"  Elapsed time: {format_duration(elapsed)}")

    print(f"\n  BY CATEGORY")
    print(f"  {'-'*50}")
    for cat_key, cat_info in CATEGORIES.items():
        cat_stats = stats['by_category'][cat_key]
        print(f"  {cat_info['name']:30} {cat_stats['transcripts']:3} transcripts")

    print(f"\n  KEY USAGE SUMMARY")
    print(f"  {'-'*50}")
    for ks in get_key_summary():
        print(f"  {ks}")

    print(f"\n  EXPERTISE LEVELS ACHIEVED")
    print(f"  {'-'*50}")

    office_count = stats['by_category']['MS_Office']['transcripts']
    if office_count >= 40:
        print(f"  Microsoft Office: EXPERT ({office_count} transcripts)")
    elif office_count >= 20:
        print(f"  Microsoft Office: ADVANCED ({office_count} transcripts)")
    else:
        print(f"  Microsoft Office: INTERMEDIATE ({office_count} transcripts)")

    p6_count = stats['by_category']['Primavera_P6']['transcripts']
    if p6_count >= 20:
        print(f"  Primavera P6: EXPERT ({p6_count} transcripts)")
    elif p6_count >= 10:
        print(f"  Primavera P6: ADVANCED ({p6_count} transcripts)")
    else:
        print(f"  Primavera P6: PROFICIENT ({p6_count} transcripts)")

    traffic_count = sum(stats['by_category'][k]['transcripts']
                       for k in ['TIS_Fundamentals', 'Trip_Generation', 'LOS_Capacity', 'Traffic_Control'])
    if traffic_count >= 60:
        print(f"  Traffic Studies: EXPERT ({traffic_count} transcripts)")
    elif traffic_count >= 40:
        print(f"  Traffic Studies: ADVANCED ({traffic_count} transcripts)")
    else:
        print(f"  Traffic Studies: PROFICIENT ({traffic_count} transcripts)")

    print(f"\n  OUTPUT LOCATION")
    print(f"  {'-'*50}")
    print(f"  {OUTPUT_DIR}")
    print(f"\n{'='*70}\n")

    log_message(f"CRAWL COMPLETE - {stats['total_transcripts']} transcripts in {format_duration(elapsed)}")

# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  [INTERRUPTED] Progress saved. Run again to resume.\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n  [FATAL ERROR] {e}\n")
        log_message(f"FATAL ERROR: {e}")
        sys.exit(1)
