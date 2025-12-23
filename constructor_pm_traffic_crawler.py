#!/usr/bin/env python3
"""
CONSTRUCTOR PM & TRAFFIC STUDIES KNOWLEDGE CRAWLER
===================================================
Focused Construction PM + Comprehensive Traffic Engineering

Categories:
- Construction PM Basics (30 queries)
- Traffic Studies - Comprehensive (50 queries)
  - TIS Fundamentals (15)
  - Trip Generation & Distribution (10)
  - Level of Service & Capacity (10)
  - Traffic Control Plans (10)
  - Traffic Engineering (5)

Total: 80 queries x 2 results = 160 video target
Expected transcripts: 130-160

Author: Trajanus USA
Date: 2024
"""

import os
import sys
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import time
import re
from datetime import datetime

# ============================================================
# CONFIGURATION
# ============================================================

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
if not YOUTUBE_API_KEY:
    print("[ERROR] YOUTUBE_API_KEY environment variable not set")
    print("Set it with: export YOUTUBE_API_KEY='your-api-key'")
    sys.exit(1)

OUTPUT_DIR = "G:/My Drive/00 - Trajanus USA/01-Morning-Sessions/Research/Constructor_PM_Knowledge"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# SEARCH QUERIES - 80 TOTAL
# ============================================================

# Construction PM Basics (30 queries)
PM_QUERIES = [
    "construction monthly progress report template",
    "construction earned value management SPI CPI",
    "construction schedule narrative writing",
    "construction cost tracking methods",
    "construction submittal log management",
    "construction RFI process workflow",
    "construction daily report format",
    "construction quality control plan",
    "construction safety plan template",
    "construction meeting minutes",
    "Job Safety Analysis JSA construction",
    "construction deficiency report",
    "construction punch list process",
    "construction closeout documentation",
    "construction change order management",
    "construction progress photos documentation",
    "construction project dashboard",
    "construction payment application",
    "construction lessons learned",
    "construction risk register",
    "USACE 3 phase inspection",
    "construction material testing",
    "construction as-built documentation",
    "construction warranty documentation",
    "OSHA construction safety basics",
    "construction toolbox talks",
    "construction fall protection",
    "construction PPE requirements",
    "construction accident investigation",
    "construction emergency action plan",
]

# TIS Fundamentals (15 queries)
TIS_FUNDAMENTALS = [
    "traffic impact study methodology complete tutorial",
    "traffic impact analysis step by step",
    "TIS scope development traffic study",
    "traffic study area determination",
    "traffic data collection methods",
    "traffic count procedures manual automatic",
    "peak hour traffic analysis procedure",
    "traffic growth rate projections",
    "traffic study report format requirements",
    "traffic impact mitigation measures",
    "traffic study peer review process",
    "traffic consultant selection criteria",
    "traffic study scoping meeting",
    "baseline traffic conditions analysis",
    "future traffic conditions modeling",
]

# Trip Generation & Distribution (10 queries)
TRIP_GENERATION = [
    "trip generation analysis ITE manual",
    "trip generation rates by land use",
    "trip generation equations ITE",
    "internal capture trip reduction",
    "pass-by trip analysis",
    "trip distribution methods gravity model",
    "trip assignment techniques",
    "multi-modal trip generation",
    "trip generation for mixed use",
    "site traffic generation calculation",
]

# Level of Service & Capacity (10 queries)
LOS_CAPACITY = [
    "level of service LOS calculation detailed",
    "intersection capacity analysis HCM",
    "highway capacity manual tutorial",
    "LOS criteria standards",
    "intersection delay analysis",
    "volume to capacity ratio calculation",
    "queue length analysis intersection",
    "roundabout capacity analysis",
    "signal timing optimization analysis",
    "arterial LOS analysis",
]

# Traffic Control Plans (10 queries)
TRAFFIC_CONTROL = [
    "traffic control plan TCP development",
    "construction work zone traffic control",
    "temporary traffic control plan design",
    "MOT maintenance of traffic planning",
    "MUTCD work zone standards",
    "traffic detour design planning",
    "temporary traffic signal design",
    "pedestrian accommodation work zones",
    "traffic control devices selection",
    "phased construction traffic management",
]

# Traffic Engineering (5 queries)
TRAFFIC_ENGINEERING = [
    "traffic signal warrant analysis",
    "traffic signal timing design",
    "traffic calming measures design",
    "access management principles",
    "sight distance analysis calculations",
]

# Combine all queries
ALL_QUERIES = (
    PM_QUERIES +
    TIS_FUNDAMENTALS +
    TRIP_GENERATION +
    LOS_CAPACITY +
    TRAFFIC_CONTROL +
    TRAFFIC_ENGINEERING
)

# Category definitions with index ranges
CATEGORIES = {
    "PM_Basics": {
        "name": "Construction PM Basics",
        "start": 0,
        "end": 30,
        "expected": 60
    },
    "TIS_Fundamentals": {
        "name": "TIS Fundamentals",
        "start": 30,
        "end": 45,
        "expected": 30
    },
    "Trip_Generation": {
        "name": "Trip Generation & Distribution",
        "start": 45,
        "end": 55,
        "expected": 20
    },
    "LOS_Capacity": {
        "name": "Level of Service & Capacity",
        "start": 55,
        "end": 65,
        "expected": 20
    },
    "Traffic_Control": {
        "name": "Traffic Control Plans",
        "start": 65,
        "end": 75,
        "expected": 20
    },
    "Traffic_Engineering": {
        "name": "Traffic Engineering",
        "start": 75,
        "end": 80,
        "expected": 10
    }
}

# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def sanitize_filename(text):
    """Remove invalid characters from filename and truncate."""
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
    else:
        return f"{secs}s"

# ============================================================
# YOUTUBE API FUNCTIONS
# ============================================================

def search_youtube(query, max_results=2):
    """Search YouTube for videos matching the query."""
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    try:
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

        results = []
        for item in response.get('items', []):
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            channel = item['snippet']['channelTitle']
            description = item['snippet']['description']
            published = item['snippet']['publishedAt']
            results.append({
                'video_id': video_id,
                'title': title,
                'channel': channel,
                'description': description,
                'published': published
            })

        return results

    except Exception as e:
        print(f"    [ERROR] Search failed: {e}")
        return []

def get_transcript(video_id):
    """Get transcript for a YouTube video."""
    try:
        ytt = YouTubeTranscriptApi()
        transcript_list = ytt.fetch(video_id)
        transcript_text = ' '.join([entry.text for entry in transcript_list])
        return transcript_text
    except Exception as e:
        return None

def get_video_details(video_id):
    """Get additional video details like duration and view count."""
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    try:
        request = youtube.videos().list(
            part='contentDetails,statistics',
            id=video_id
        )
        response = request.execute()

        if response.get('items'):
            item = response['items'][0]
            return {
                'duration': item['contentDetails'].get('duration', 'Unknown'),
                'view_count': item['statistics'].get('viewCount', 'Unknown'),
                'like_count': item['statistics'].get('likeCount', 'Unknown')
            }
    except:
        pass

    return {'duration': 'Unknown', 'view_count': 'Unknown', 'like_count': 'Unknown'}

# ============================================================
# MAIN CRAWLER FUNCTION
# ============================================================

def main():
    """Main crawler execution."""
    start_time = time.time()

    print(f"\n{'='*70}")
    print(f"  CONSTRUCTOR PM & TRAFFIC STUDIES KNOWLEDGE CRAWLER")
    print(f"{'='*70}")
    print(f"\n  Focused Construction PM + Comprehensive Traffic Engineering")
    print(f"\n  COVERAGE AREAS:")
    print(f"  - Construction PM Basics (30 queries)")
    print(f"  - TIS Fundamentals (15 queries)")
    print(f"  - Trip Generation & Distribution (10 queries)")
    print(f"  - Level of Service & Capacity (10 queries)")
    print(f"  - Traffic Control Plans (10 queries)")
    print(f"  - Traffic Engineering (5 queries)")
    print(f"\n  Total Queries: {len(ALL_QUERIES)}")
    print(f"  Results per Query: 2")
    print(f"  Target Videos: {len(ALL_QUERIES) * 2}")
    print(f"  Expected Transcripts: 130-160")
    print(f"\n  Output Directory:")
    print(f"  {OUTPUT_DIR}")
    print(f"\n{'='*70}\n")

    # Statistics tracking
    stats = {
        'total_searched': 0,
        'total_downloaded': 0,
        'total_skipped': 0,
        'total_errors': 0,
        'total_bytes': 0,
        'by_category': {}
    }

    # Initialize category stats
    for cat_key in CATEGORIES:
        stats['by_category'][cat_key] = {
            'searched': 0,
            'downloaded': 0,
            'skipped': 0
        }

    # Track processed video IDs to avoid duplicates
    processed_ids = set()

    # Process each category
    for cat_key, cat_info in CATEGORIES.items():
        cat_name = cat_info["name"]
        start_idx = cat_info["start"]
        end_idx = cat_info["end"]

        print(f"\n{'='*70}")
        print(f"  CATEGORY: {cat_name}")
        print(f"  Queries: {end_idx - start_idx}")
        print(f"{'='*70}")

        cat_queries = ALL_QUERIES[start_idx:end_idx]

        for i, query in enumerate(cat_queries, 1):
            query_num = start_idx + i
            print(f"\n  [{query_num}/{len(ALL_QUERIES)}] {query[:55]}...")

            video_results = search_youtube(query, max_results=2)

            if not video_results:
                print(f"    [WARN] No results found")
                continue

            for video in video_results:
                video_id = video['video_id']
                title = video['title']
                channel = video['channel']

                stats['total_searched'] += 1
                stats['by_category'][cat_key]['searched'] += 1

                # Skip duplicates
                if video_id in processed_ids:
                    print(f"    [SKIP] Duplicate: {title[:40]}...")
                    continue

                processed_ids.add(video_id)

                print(f"    [{channel[:20]}] {title[:40]}...")

                # Get transcript
                transcript = get_transcript(video_id)

                if transcript:
                    # Get additional details
                    details = get_video_details(video_id)

                    # Create filename
                    safe_title = sanitize_filename(title)
                    filename = f"{cat_key}_{video_id}_{safe_title}.txt"
                    filepath = os.path.join(OUTPUT_DIR, filename)

                    # Write transcript file
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(f"{'='*70}\n")
                        f.write(f"CONSTRUCTOR PM & TRAFFIC KNOWLEDGE BASE - TRANSCRIPT\n")
                        f.write(f"{'='*70}\n\n")
                        f.write(f"Title: {title}\n")
                        f.write(f"Channel: {channel}\n")
                        f.write(f"Video ID: {video_id}\n")
                        f.write(f"URL: https://www.youtube.com/watch?v={video_id}\n")
                        f.write(f"Published: {video['published']}\n")
                        f.write(f"Duration: {details['duration']}\n")
                        f.write(f"Views: {details['view_count']}\n")
                        f.write(f"Likes: {details['like_count']}\n")
                        f.write(f"\nSearch Query: {query}\n")
                        f.write(f"Category: {cat_name}\n")
                        f.write(f"Category Key: {cat_key}\n")
                        f.write(f"\nDescription:\n{video['description']}\n")
                        f.write(f"\n{'='*70}\n")
                        f.write(f"TRANSCRIPT\n")
                        f.write(f"{'='*70}\n\n")
                        f.write(transcript)
                        f.write(f"\n\n{'='*70}\n")
                        f.write(f"END OF TRANSCRIPT\n")
                        f.write(f"{'='*70}\n")

                    file_size = len(transcript)
                    stats['total_downloaded'] += 1
                    stats['total_bytes'] += file_size
                    stats['by_category'][cat_key]['downloaded'] += 1

                    print(f"      [OK] Downloaded ({file_size // 1024} KB)")
                else:
                    stats['total_skipped'] += 1
                    stats['by_category'][cat_key]['skipped'] += 1
                    print(f"      [SKIP] No transcript available")

                # Rate limiting
                time.sleep(1)

            # Brief pause between queries
            time.sleep(0.5)

    # Calculate elapsed time
    elapsed = time.time() - start_time

    # Print final report
    print(f"\n\n{'='*70}")
    print(f"  CONSTRUCTOR PM & TRAFFIC CRAWLER - COMPLETE")
    print(f"{'='*70}")
    print(f"\n  SUMMARY STATISTICS")
    print(f"  {'-'*40}")
    print(f"  Total videos processed: {stats['total_searched']}")
    print(f"  Transcripts downloaded: {stats['total_downloaded']}")
    print(f"  Skipped (no transcript): {stats['total_skipped']}")
    print(f"  Success rate: {(stats['total_downloaded']/max(stats['total_searched'],1))*100:.1f}%")
    print(f"  Total data: {stats['total_bytes'] / (1024*1024):.2f} MB")
    print(f"  Elapsed time: {format_duration(elapsed)}")

    print(f"\n  BREAKDOWN BY CATEGORY")
    print(f"  {'-'*40}")
    for cat_key, cat_info in CATEGORIES.items():
        cat_stats = stats['by_category'][cat_key]
        downloaded = cat_stats['downloaded']
        searched = cat_stats['searched']
        expected = cat_info['expected']
        print(f"  {cat_info['name'][:35]:35} {downloaded:3}/{searched:3}")

    print(f"\n  TRAFFIC STUDIES TOTAL")
    print(f"  {'-'*40}")
    traffic_downloaded = sum(stats['by_category'][k]['downloaded']
                            for k in ['TIS_Fundamentals', 'Trip_Generation',
                                      'LOS_Capacity', 'Traffic_Control', 'Traffic_Engineering'])
    traffic_searched = sum(stats['by_category'][k]['searched']
                          for k in ['TIS_Fundamentals', 'Trip_Generation',
                                    'LOS_Capacity', 'Traffic_Control', 'Traffic_Engineering'])
    print(f"  Traffic Studies Combined:         {traffic_downloaded:3}/{traffic_searched:3}")

    print(f"\n  OUTPUT LOCATION")
    print(f"  {'-'*40}")
    print(f"  {OUTPUT_DIR}")

    print(f"\n  EXPERTISE LEVEL ACHIEVED")
    print(f"  {'-'*40}")
    if traffic_downloaded >= 80:
        print(f"  Traffic Studies: EXPERT")
    elif traffic_downloaded >= 50:
        print(f"  Traffic Studies: ADVANCED")
    elif traffic_downloaded >= 30:
        print(f"  Traffic Studies: INTERMEDIATE")
    else:
        print(f"  Traffic Studies: FOUNDATIONAL")

    pm_downloaded = stats['by_category']['PM_Basics']['downloaded']
    if pm_downloaded >= 40:
        print(f"  Construction PM: COMPETENT")
    elif pm_downloaded >= 25:
        print(f"  Construction PM: PROFICIENT")
    else:
        print(f"  Construction PM: FAMILIAR")

    print(f"\n{'='*70}\n")

    # Write summary log
    log_path = os.path.join(OUTPUT_DIR, "_PM_TRAFFIC_CRAWL_LOG.txt")
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(f"CONSTRUCTOR PM & TRAFFIC CRAWLER - LOG\n")
        f.write(f"{'='*50}\n\n")
        f.write(f"Timestamp: {datetime.now().isoformat()}\n")
        f.write(f"Duration: {format_duration(elapsed)}\n\n")
        f.write(f"STATISTICS\n")
        f.write(f"-" * 30 + "\n")
        f.write(f"Videos processed: {stats['total_searched']}\n")
        f.write(f"Transcripts downloaded: {stats['total_downloaded']}\n")
        f.write(f"Skipped: {stats['total_skipped']}\n")
        f.write(f"Success rate: {(stats['total_downloaded']/max(stats['total_searched'],1))*100:.1f}%\n")
        f.write(f"Total data: {stats['total_bytes'] / (1024*1024):.2f} MB\n\n")
        f.write(f"BY CATEGORY\n")
        f.write(f"-" * 30 + "\n")
        for cat_key, cat_info in CATEGORIES.items():
            cat_stats = stats['by_category'][cat_key]
            f.write(f"{cat_info['name']}: {cat_stats['downloaded']}/{cat_stats['searched']}\n")
        f.write(f"\nTRAFFIC STUDIES TOTAL: {traffic_downloaded}/{traffic_searched}\n")

    print(f"  Log written to: {log_path}\n")

    return stats

# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  [INTERRUPTED] Crawl stopped by user\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n  [FATAL ERROR] {e}\n")
        sys.exit(1)
