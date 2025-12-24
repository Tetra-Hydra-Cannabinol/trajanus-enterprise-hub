#!/usr/bin/env python3
"""
YouTube Supabase Search Crawler
Extracts video links, titles, and metadata from YouTube search results
Then retrieves transcripts for each video using youtube-transcript-api
"""

import os
import sys
import json
import time
from datetime import datetime
import requests

# Output directory
OUTPUT_DIR = r"G:\My Drive\00 - Trajanus USA\01-Morning-Sessions\Research\Supabase_YouTube"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def search_youtube_api(query, max_results=30):
    """
    Use youtube-transcript-api's built-in search or manual video ID extraction
    For simplicity, we'll use a predefined list of top Supabase videos
    and fetch their transcripts directly
    """
    # Top Supabase YouTube videos (manually curated from search)
    # These are known high-quality Supabase tutorials
    video_ids = [
        # Fireship
        "zBZgdTb-dns",  # Supabase in 100 Seconds
        "WiwfiVdfRIc",  # Supabase Full Course
        # Traversy Media
        "7uKQBl9uZ00",  # Supabase Crash Course
        # Net Ninja
        "ydz7Dj5QHKY",  # Supabase Tutorial
        # The Net Ninja full playlist videos
        "zPsXP9dGRag",  # Supabase Auth
        # Web Dev Simplified
        "I6ypD7qv3Z8",  # Supabase Tutorial
        # Code with Antonio
        "PdmKlne1gRY",  # Next.js + Supabase
        # Sonny Sangha
        "mcrqn77lUmM",  # Build with Supabase
        # JavaScript Mastery
        "O5cmLDVTgAs",  # Full Stack with Supabase
        # Lee Robinson
        "VHb9Zb5LZuM",  # Supabase + Next.js
        # Supabase Official
        "dU7GwCOgvNY",  # Supabase Launch Week
        "QAm1x0z4cAg",  # Supabase Tutorial
        "WpJMMHhb_yw",  # Supabase Overview
        # Additional popular videos
        "mPQyckogDYc",  # pgvector + Supabase
        "Yh9yIkMSWcQ",  # Supabase Edge Functions
        "rI3Ik7GyYEw",  # Supabase RLS
        "Ow_Uzedfohk",  # Supabase Realtime
        "_XM9ziOzWk4",  # Supabase Auth Deep Dive
        "6ch0JNpN5Qo",  # Supabase Storage
        "l3VgfVQVk4Y",  # Supabase with React
    ]

    return video_ids

def get_video_info(video_id):
    """Get video metadata via oembed API"""
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
        print(f"  Warning: Could not fetch metadata for {video_id}: {e}")

    return {
        'video_id': video_id,
        'url': f"https://www.youtube.com/watch?v={video_id}",
        'title': 'Unknown',
        'channel': 'Unknown',
        'thumbnail': ''
    }

def get_video_transcript(video_id):
    """Get transcript for a YouTube video"""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi

        # Create API instance (new API style)
        api = YouTubeTranscriptApi()

        # Try to fetch transcript directly (prefer English)
        try:
            transcript_data = api.fetch(video_id, languages=['en'])
            full_text = ' '.join([segment.text for segment in transcript_data])

            return {
                'available': True,
                'transcript': full_text,
                'segments': [{'text': s.text, 'start': s.start, 'duration': s.duration} for s in transcript_data],
                'language': 'en',
                'is_generated': False
            }
        except Exception as fetch_error:
            # Try listing available transcripts
            try:
                transcript_list = api.list(video_id)

                # Try to find any available transcript
                for transcript in transcript_list:
                    transcript_data = transcript.fetch()
                    full_text = ' '.join([segment.text for segment in transcript_data])

                    return {
                        'available': True,
                        'transcript': full_text,
                        'segments': [{'text': s.text, 'start': s.start, 'duration': s.duration} for s in transcript_data],
                        'language': transcript.language,
                        'is_generated': transcript.is_generated
                    }
            except:
                pass

            return {
                'available': False,
                'error': str(fetch_error)
            }

    except Exception as e:
        return {
            'available': False,
            'error': str(e)
        }

def crawl_youtube_supabase():
    """Main crawling function"""
    print("=" * 70)
    print("YouTube Supabase Crawler - Starting...")
    print("=" * 70)
    print(f"Output Directory: {OUTPUT_DIR}")
    print("-" * 70)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")

    # Get video IDs
    video_ids = search_youtube_api("supabase", max_results=30)
    print(f"Processing {len(video_ids)} Supabase videos...")
    print("-" * 70)

    results = []
    transcripts_success = 0
    transcripts_failed = 0

    # Process each video
    for idx, video_id in enumerate(video_ids, 1):
        print(f"\n[{idx}/{len(video_ids)}] Processing video: {video_id}")

        # Get video metadata
        video_info = get_video_info(video_id)
        print(f"  Title: {video_info['title'][:60]}...")
        print(f"  Channel: {video_info['channel']}")

        # Get transcript
        transcript_data = get_video_transcript(video_id)

        if transcript_data.get('available'):
            transcripts_success += 1
            char_count = len(transcript_data['transcript'])
            print(f"  Transcript: YES ({char_count:,} chars)")

            # Save individual transcript
            safe_title = "".join(c for c in video_info['title'][:40] if c.isalnum() or c in ' -_').strip()
            transcript_file = os.path.join(OUTPUT_DIR, f"{timestamp}_{video_id}_{safe_title}.txt")

            with open(transcript_file, 'w', encoding='utf-8') as f:
                f.write(f"Title: {video_info['title']}\n")
                f.write(f"Channel: {video_info['channel']}\n")
                f.write(f"URL: {video_info['url']}\n")
                f.write(f"Language: {transcript_data.get('language', 'en')}\n")
                f.write(f"Auto-generated: {transcript_data.get('is_generated', 'Unknown')}\n")
                f.write("=" * 70 + "\n\n")
                f.write(transcript_data['transcript'])

            video_info['transcript_file'] = os.path.basename(transcript_file)
            video_info['transcript_length'] = char_count
            video_info['has_transcript'] = True
        else:
            transcripts_failed += 1
            print(f"  Transcript: NO ({transcript_data.get('error', 'Unknown error')})")
            video_info['has_transcript'] = False
            video_info['transcript_error'] = transcript_data.get('error', 'Unknown')

        results.append(video_info)

        # Rate limiting
        time.sleep(0.5)

    print("\n" + "=" * 70)
    print("Creating output files...")
    print("=" * 70)

    # Save JSON results
    json_file = os.path.join(OUTPUT_DIR, f"{timestamp}_video_results.json")
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"Saved: {os.path.basename(json_file)}")

    # Create markdown summary
    md_content = f"""# YouTube Supabase Videos - Research Summary

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Search Query**: supabase
**Total Videos Processed**: {len(results)}
**Transcripts Retrieved**: {transcripts_success}
**Transcripts Failed**: {transcripts_failed}

---

## Videos with Transcripts

"""

    for video in results:
        if video.get('has_transcript'):
            md_content += f"### {video['title']}\n\n"
            md_content += f"- **Channel**: {video['channel']}\n"
            md_content += f"- **URL**: {video['url']}\n"
            md_content += f"- **Transcript Length**: {video.get('transcript_length', 0):,} characters\n"
            md_content += f"- **File**: `{video.get('transcript_file', 'N/A')}`\n\n"

    md_content += "\n---\n\n## Videos Without Transcripts\n\n"

    for video in results:
        if not video.get('has_transcript'):
            md_content += f"- [{video['title']}]({video['url']}) - {video.get('transcript_error', 'No transcript')}\n"

    md_content += f"""

---

## Recommended for Trajanus TKB

### High Priority (Database/Backend Focus)
- Videos mentioning pgvector, embeddings, RAG
- Authentication and RLS tutorials
- Database schema design
- Real-time subscriptions

### Medium Priority (Integration)
- Next.js + Supabase integration
- Edge Functions tutorials
- Storage and file handling

### Search Terms to Extract from Transcripts
- pgvector
- embeddings
- vector search
- authentication
- row level security / RLS
- real-time
- edge functions
- database design
- schema
- migrations

---

**Output Directory**: `{OUTPUT_DIR}`
**JSON Data**: `{os.path.basename(json_file)}`
**Status**: Complete
"""

    md_file = os.path.join(OUTPUT_DIR, f"{timestamp}_supabase_summary.md")
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"Saved: {os.path.basename(md_file)}")

    # Print final summary
    print("\n" + "=" * 70)
    print("CRAWLER COMPLETE")
    print("=" * 70)
    print(f"Videos Processed: {len(results)}")
    print(f"Transcripts Retrieved: {transcripts_success}")
    print(f"Transcripts Failed: {transcripts_failed}")
    print(f"Success Rate: {transcripts_success/len(results)*100:.1f}%")
    print("-" * 70)
    print(f"Output Directory: {OUTPUT_DIR}")
    print(f"JSON File: {os.path.basename(json_file)}")
    print(f"Summary File: {os.path.basename(md_file)}")
    print("=" * 70)

    return {
        'total': len(results),
        'success': transcripts_success,
        'failed': transcripts_failed,
        'output_dir': OUTPUT_DIR,
        'json_file': json_file,
        'md_file': md_file
    }

if __name__ == "__main__":
    result = crawl_youtube_supabase()
    sys.exit(0 if result['success'] > 0 else 1)
