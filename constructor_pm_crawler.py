#!/usr/bin/env python3
"""
CONSTRUCTOR PM AGENT - MASTER KNOWLEDGE CRAWLER
================================================
Comprehensive Construction Project Management Knowledge Base Builder

Categories:
- Project Management Reports (30 queries)
- Quality Control & QCM (30 queries)
- Safety Management (25 queries)
- Traffic Studies & Engineering (25 queries)
- Federal Construction Standards (20 queries)
- Building Codes (20 queries)
- CSI MasterFormat & Specifications (15 queries)
- Software & Estimating (15 queries)

Total: 180 queries x 2 results = 360 video target
Expected transcripts: 200-250 (accounting for unavailable transcripts)

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
# SEARCH QUERIES - 180 TOTAL
# ============================================================

# Project Management Reports (30 queries)
PM_QUERIES = [
    "construction monthly progress report tutorial",
    "earned value management construction explained",
    "CPM scheduling construction tutorial",
    "Primavera P6 construction scheduling",
    "construction cost control forecasting",
    "construction risk management plan",
    "change order management construction",
    "construction project closeout checklist",
    "construction schedule narrative report",
    "three week lookahead schedule",
    "construction progress photos documentation",
    "construction delay analysis methods",
    "critical path method construction",
    "construction manpower loading",
    "construction resource leveling",
    "construction cash flow forecasting",
    "construction performance metrics KPI",
    "construction project dashboard",
    "construction variance analysis",
    "construction project status reporting",
    "construction milestone tracking",
    "construction schedule baseline",
    "construction recovery schedule",
    "construction time impact analysis",
    "construction claims documentation",
    "construction productivity tracking",
    "construction subcontractor coordination",
    "construction submittal log management",
    "construction RFI tracking system",
    "construction punch list management",
]

# Quality Control & QCM (30 queries)
QC_QUERIES = [
    "construction quality control plan tutorial",
    "QCM 3 phase construction",
    "construction submittal review process",
    "construction RFI management system",
    "construction daily QC report",
    "construction deficiency report writing",
    "construction non-conformance report NCR",
    "construction material testing requirements",
    "construction inspection checklist",
    "concrete inspection procedures",
    "steel inspection construction",
    "construction workmanship standards",
    "construction quality surveillance",
    "construction acceptance criteria",
    "construction test and inspection plan",
    "construction calibration requirements",
    "construction documentation requirements",
    "construction as-built documentation",
    "construction warranty documentation",
    "construction O&M manuals",
    "construction commissioning procedures",
    "construction punchlist procedures",
    "construction final inspection",
    "USACE quality control CQC",
    "USACE quality management CQM",
    "construction 3 phase inspection",
    "construction preparatory meeting",
    "construction initial inspection",
    "construction follow-up inspection",
    "construction quality control manager duties",
]

# Safety Management (25 queries)
SAFETY_QUERIES = [
    "OSHA construction safety standards",
    "Job Safety Analysis JSA construction",
    "construction site safety plan",
    "construction accident investigation",
    "construction fall protection requirements",
    "construction excavation safety",
    "construction confined space procedures",
    "construction scaffolding safety",
    "construction electrical safety",
    "construction crane safety requirements",
    "construction personal protective equipment PPE",
    "construction toolbox talk topics",
    "construction safety meetings",
    "OSHA 1926 construction standards",
    "construction safety inspection checklist",
    "construction incident reporting",
    "construction near miss reporting",
    "construction emergency action plan",
    "construction fire prevention plan",
    "construction hazard communication",
    "construction lockout tagout procedures",
    "construction hot work permit",
    "construction safety orientation",
    "construction competent person requirements",
    "construction safety program development",
]

# Traffic Studies & Engineering (25 queries)
TRAFFIC_QUERIES = [
    "traffic impact study tutorial complete",
    "traffic impact analysis methodology professional",
    "level of service LOS calculation detailed",
    "traffic control plan TCP design engineering",
    "maintenance of traffic MOT plan development",
    "MUTCD traffic control devices standards",
    "traffic signal warrant analysis tutorial",
    "traffic count data collection methods",
    "peak hour traffic analysis procedure",
    "trip generation analysis ITE manual",
    "traffic distribution assignment modeling",
    "intersection capacity analysis HCM",
    "pedestrian impact study methodology",
    "parking demand analysis calculation",
    "traffic safety audit procedures",
    "work zone traffic control engineering",
    "temporary traffic signal design",
    "construction zone traffic management plan",
    "traffic detour planning engineering",
    "MUTCD temporary traffic control standards",
    "traffic signal timing optimization",
    "roundabout design analysis",
    "highway capacity manual tutorial",
    "traffic modeling software VISSIM Synchro",
    "access management engineering",
]

# Federal Construction Standards (20 queries)
FEDERAL_QUERIES = [
    "USACE construction quality management",
    "USACE CQC system explained",
    "USACE 3 phase inspection",
    "USACE ER 1180-1-6 tutorial",
    "DoD construction requirements",
    "federal construction specifications",
    "USACE quality control manager",
    "USACE submittal requirements",
    "USACE RFI procedures",
    "USACE contractor quality control",
    "military construction standards",
    "TRACES system USACE",
    "RMS 3.0 reporting USACE",
    "DD Form 1354 completion",
    "CEFMS construction reporting",
    "federal acquisition regulations construction",
    "Davis Bacon wage requirements",
    "Buy America requirements construction",
    "federal project closeout",
    "USACE final inspection procedures",
]

# Building Codes (20 queries)
CODES_QUERIES = [
    "International Building Code IBC 2024 changes",
    "IBC structural requirements tutorial",
    "International Residential Code IRC explained",
    "National Electrical Code NEC 2023",
    "International Plumbing Code IPC requirements",
    "International Mechanical Code IMC tutorial",
    "International Energy Conservation Code IECC",
    "International Fire Code IFC life safety",
    "building code compliance checklist",
    "code requirements residential construction",
    "commercial building code requirements",
    "accessibility requirements ADA building codes",
    "egress requirements building code",
    "fire separation building code",
    "structural design building code",
    "building code occupancy classification",
    "building permit requirements codes",
    "building code inspection process",
    "code compliance documentation",
    "building code amendments local",
]

# CSI MasterFormat & Specifications (15 queries)
CSI_QUERIES = [
    "CSI MasterFormat divisions explained",
    "construction specification writing tutorial",
    "CSI spec writing best practices",
    "MasterFormat 2024 divisions",
    "Division 01 general requirements specs",
    "Division 03 concrete specifications",
    "Division 04 masonry specifications",
    "Division 05 metals specifications",
    "Division 09 finishes specifications",
    "technical specifications construction",
    "product data submittal requirements",
    "construction specifications institute CSI",
    "spec section organization",
    "performance specifications vs prescriptive",
    "specification coordination drawings",
]

# Software & Estimating (15 queries)
SOFTWARE_QUERIES = [
    "Procore construction management tutorial",
    "Primavera P6 advanced scheduling",
    "RMS 3.0 for USACE reporting",
    "Microsoft Project construction scheduling",
    "RS Means cost estimating tutorial",
    "RS Means unit price book",
    "construction cost estimating methods",
    "quantity takeoff tutorial",
    "Bluebeam for QC markup",
    "construction management software comparison",
    "BIM 360 construction management",
    "construction document management",
    "construction scheduling software tutorial",
    "project controls software",
    "earned value management software",
]

# Combine all queries
ALL_QUERIES = (
    PM_QUERIES +
    QC_QUERIES +
    SAFETY_QUERIES +
    TRAFFIC_QUERIES +
    FEDERAL_QUERIES +
    CODES_QUERIES +
    CSI_QUERIES +
    SOFTWARE_QUERIES
)

# Category definitions with index ranges
CATEGORIES = {
    "PM_Reports": {
        "name": "Project Management Reports",
        "start": 0,
        "end": 30,
        "expected": 60
    },
    "Quality_Control": {
        "name": "Quality Control & QCM",
        "start": 30,
        "end": 60,
        "expected": 60
    },
    "Safety": {
        "name": "Safety Management",
        "start": 60,
        "end": 85,
        "expected": 50
    },
    "Traffic_Engineering": {
        "name": "Traffic Studies & Engineering",
        "start": 85,
        "end": 110,
        "expected": 50
    },
    "Federal_Construction": {
        "name": "Federal Construction Standards",
        "start": 110,
        "end": 130,
        "expected": 40
    },
    "Building_Codes": {
        "name": "Building Codes (IBC/IRC/NEC/IPC/IMC/IECC/IFC)",
        "start": 130,
        "end": 150,
        "expected": 40
    },
    "CSI_Specs": {
        "name": "CSI MasterFormat & Specifications",
        "start": 150,
        "end": 165,
        "expected": 30
    },
    "Software_Estimating": {
        "name": "Software & Estimating (Procore/P6/RMS/MS Project/RS Means)",
        "start": 165,
        "end": 180,
        "expected": 30
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

def get_category_for_index(index):
    """Get category name for a given query index."""
    for cat_key, cat_info in CATEGORIES.items():
        if cat_info["start"] <= index < cat_info["end"]:
            return cat_key, cat_info["name"]
    return "Unknown", "Unknown"

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
            videoDuration='medium',  # 4-20 minutes
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
    print(f"  CONSTRUCTOR PM AGENT - MASTER KNOWLEDGE CRAWLER")
    print(f"{'='*70}")
    print(f"\n  Comprehensive Construction Project Management Knowledge Base")
    print(f"\n  COVERAGE AREAS:")
    print(f"  - Project Management Reports & Scheduling")
    print(f"  - Quality Control & QCM (3-Phase Inspection)")
    print(f"  - OSHA Safety Management")
    print(f"  - Traffic Studies & Engineering (MUTCD/HCM)")
    print(f"  - Federal Construction (USACE/DoD)")
    print(f"  - Building Codes (IBC/IRC/NEC/IPC/IMC/IECC/IFC)")
    print(f"  - CSI MasterFormat Specifications")
    print(f"  - Software (Procore/P6/RMS/MS Project/RS Means)")
    print(f"\n  Total Queries: {len(ALL_QUERIES)}")
    print(f"  Results per Query: 2")
    print(f"  Target Videos: {len(ALL_QUERIES) * 2}")
    print(f"  Expected Transcripts: 200-250")
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
                        f.write(f"CONSTRUCTOR PM KNOWLEDGE BASE - VIDEO TRANSCRIPT\n")
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
    print(f"  CONSTRUCTOR PM AGENT - CRAWL COMPLETE")
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
        print(f"  {cat_info['name'][:35]:35} {downloaded:3}/{searched:3} ({downloaded/max(expected,1)*100:5.1f}%)")

    print(f"\n  OUTPUT LOCATION")
    print(f"  {'-'*40}")
    print(f"  {OUTPUT_DIR}")

    print(f"\n  NEXT STEPS")
    print(f"  {'-'*40}")
    print(f"  1. Review downloaded transcripts")
    print(f"  2. Run Supabase ingestion script")
    print(f"  3. Verify TKB vector embeddings")
    print(f"  4. Test RAG retrieval quality")

    print(f"\n{'='*70}\n")

    # Write summary log
    log_path = os.path.join(OUTPUT_DIR, "_CRAWL_LOG.txt")
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(f"CONSTRUCTOR PM AGENT - CRAWL LOG\n")
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
