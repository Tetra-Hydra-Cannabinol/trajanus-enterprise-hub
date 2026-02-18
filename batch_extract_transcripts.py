#!/usr/bin/env python3
"""
Batch YouTube Transcript Extractor
===================================
Processes multiple URLs from JSON configuration file.
Built during MS Office Knowledge Crawler session (2025-12-20).

Dependencies: playwright
Usage: python batch_extract_transcripts.py target_urls.json [output_dir]

JSON Format:
{
    "individual_videos": ["url1", "url2", ...],
    "playlists": ["playlist_url1", ...]  // Optional
}
"""

import asyncio
import json
import re
import sys
import os
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

# Import from the single-video extractor
from extract_youtube_transcript import (
    extract_single_video,
    DEFAULT_OUTPUT_DIR,
    sanitize_filename
)


async def extract_playlist_videos(page, playlist_url: str) -> list:
    """Extract all video URLs from a YouTube playlist."""
    video_urls = []

    try:
        await page.goto(playlist_url, wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(3000)

        # Extract video links from playlist
        video_links = await page.query_selector_all('a#video-title')

        for link in video_links:
            href = await link.get_attribute('href')
            if href and '/watch?v=' in href:
                # Clean up the URL (remove playlist params for individual processing)
                video_id_match = re.search(r'v=([a-zA-Z0-9_-]{11})', href)
                if video_id_match:
                    video_id = video_id_match.group(1)
                    clean_url = f"https://www.youtube.com/watch?v={video_id}"
                    if clean_url not in video_urls:
                        video_urls.append(clean_url)

        print(f"  Found {len(video_urls)} videos in playlist")

    except Exception as e:
        print(f"  Error extracting playlist: {e}")

    return video_urls


async def load_urls_from_json(json_path: str) -> list:
    """Load and expand all URLs from JSON config file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    urls = []

    # Handle different JSON formats
    if isinstance(data, list):
        # Simple list of URLs
        for item in data:
            if isinstance(item, str):
                urls.append(item)
            elif isinstance(item, dict) and 'url' in item:
                urls.append(item['url'])
    elif isinstance(data, dict):
        # Structured format with individual_videos and playlists
        if 'individual_videos' in data:
            urls.extend(data['individual_videos'])

        if 'urls' in data:
            urls.extend(data['urls'])

        # Handle playlists - need browser to extract
        if 'playlists' in data and data['playlists']:
            print(f"\nExpanding {len(data['playlists'])} playlist(s)...")

            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()

                for playlist_url in data['playlists']:
                    print(f"  Processing playlist: {playlist_url}")
                    playlist_videos = await extract_playlist_videos(page, playlist_url)

                    # Add only new videos (avoid duplicates)
                    for video_url in playlist_videos:
                        if video_url not in urls:
                            urls.append(video_url)

                await browser.close()

    # Remove duplicates while preserving order
    seen = set()
    unique_urls = []
    for url in urls:
        if url not in seen:
            seen.add(url)
            unique_urls.append(url)

    return unique_urls


async def batch_extract(json_path: str, output_dir: str = DEFAULT_OUTPUT_DIR) -> dict:
    """Process all URLs from JSON file."""

    print(f"Loading URLs from: {json_path}")
    urls = await load_urls_from_json(json_path)

    print(f"\nTotal unique URLs to process: {len(urls)}")
    print(f"Output directory: {output_dir}")
    print("=" * 60)

    results = {
        'total': len(urls),
        'successful': [],
        'failed': [],
        'skipped': []
    }

    for idx, url in enumerate(urls, 1):
        print(f"\n[{idx}/{len(urls)}] Processing: {url}")

        # Extract video ID for checking existing files
        video_id_match = re.search(r'v=([a-zA-Z0-9_-]{11})', url)
        video_id = video_id_match.group(1) if video_id_match else 'unknown'

        # Check if transcript already exists
        existing_files = list(Path(output_dir).glob(f"*_{video_id}_*.txt"))
        if existing_files:
            print(f"  SKIP: Transcript already exists: {existing_files[0].name}")
            results['skipped'].append({
                'url': url,
                'video_id': video_id,
                'existing_file': str(existing_files[0])
            })
            continue

        try:
            result = await extract_single_video(url, output_dir, headless=True)

            if result['success']:
                print(f"  ✓ SUCCESS: {result.get('segments', 0)} segments")
                results['successful'].append(result)
            else:
                print(f"  ✗ FAILED: {result.get('error', 'Unknown error')}")
                results['failed'].append(result)

        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            results['failed'].append({
                'url': url,
                'video_id': video_id,
                'error': str(e)
            })

        # Brief pause between videos
        if idx < len(urls):
            await asyncio.sleep(2)

    return results


def print_summary(results: dict):
    """Print extraction summary."""
    print("\n" + "=" * 60)
    print("BATCH EXTRACTION SUMMARY")
    print("=" * 60)

    print(f"Total URLs processed: {results['total']}")
    print(f"  ✓ Successful: {len(results['successful'])}")
    print(f"  ✗ Failed: {len(results['failed'])}")
    print(f"  ⊘ Skipped (existing): {len(results['skipped'])}")

    if results['successful']:
        total_segments = sum(r.get('segments', 0) for r in results['successful'])
        print(f"\nTotal segments extracted: {total_segments:,}")
        print("\nSuccessful extractions:")
        for r in results['successful']:
            print(f"  - {r['video_id']}: {r.get('segments', 0)} segments")

    if results['failed']:
        print("\nFailed extractions:")
        for r in results['failed']:
            print(f"  - {r.get('video_id', 'unknown')}: {r.get('error', 'Unknown error')}")

    if results['skipped']:
        print(f"\nSkipped {len(results['skipped'])} existing transcripts")


def save_results_log(results: dict, json_path: str):
    """Save extraction results to a log file."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_filename = f"batch_extraction_log_{timestamp}.json"
    log_path = Path(json_path).parent / log_filename

    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'source_file': json_path,
            'summary': {
                'total': results['total'],
                'successful': len(results['successful']),
                'failed': len(results['failed']),
                'skipped': len(results['skipped'])
            },
            'successful': [{'video_id': r.get('video_id'), 'segments': r.get('segments')}
                          for r in results['successful']],
            'failed': [{'video_id': r.get('video_id'), 'error': r.get('error')}
                      for r in results['failed']],
            'skipped': results['skipped']
        }, f, indent=2)

    print(f"\nResults log saved to: {log_path}")


async def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Batch YouTube Transcript Extractor")
        print("\nUsage:")
        print("  python batch_extract_transcripts.py <urls.json> [output_dir]")
        print("\nJSON Format:")
        print('  {"individual_videos": ["url1", "url2"], "playlists": ["playlist_url"]}')
        print("\nExamples:")
        print("  python batch_extract_transcripts.py target_urls.json")
        print("  python batch_extract_transcripts.py target_urls.json ./output")
        sys.exit(1)

    json_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUTPUT_DIR

    if not os.path.exists(json_path):
        print(f"Error: File not found: {json_path}")
        sys.exit(1)

    # Create output directory if needed
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Run batch extraction
    results = await batch_extract(json_path, output_dir)

    # Print summary
    print_summary(results)

    # Save results log
    save_results_log(results, json_path)

    # Exit with error code if any failures
    if results['failed']:
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
