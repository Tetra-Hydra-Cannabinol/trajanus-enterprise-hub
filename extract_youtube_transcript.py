#!/usr/bin/env python3
"""
YouTube Transcript Extractor using Playwright
==============================================
Extracts transcripts from YouTube videos using browser automation.
Bypasses API restrictions by using actual browser rendering.

Author: Claude Code Assistant
Created: 2025-12-20
"""

import asyncio
import json
import re
import sys
import os
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

# Configuration
DEFAULT_OUTPUT_DIR = r"G:\My Drive\00 - Trajanus USA\01-Morning-Sessions\Research\Microsoft_Office_Tutorials"
MAX_SEGMENTS_PER_BATCH = 500  # For very long videos
WAIT_TIMEOUT = 10000  # 10 seconds


def sanitize_filename(title: str, max_length: int = 50) -> str:
    """Convert title to safe filename."""
    # Remove/replace unsafe characters
    safe = re.sub(r'[<>:"/\\|?*]', '', title)
    safe = re.sub(r'\s+', '_', safe)
    safe = safe[:max_length]
    return safe


def determine_level(duration_seconds: int, title: str) -> str:
    """Determine skill level based on duration and title keywords."""
    title_lower = title.lower()

    # Check title keywords first
    if any(word in title_lower for word in ['expert', 'mastery', 'professional']):
        return 'EXPERT'
    if any(word in title_lower for word in ['advanced', 'ninja', 'pro tips']):
        return 'ADVANCED'
    if any(word in title_lower for word in ['beginner', 'basics', 'introduction', 'getting started']):
        return 'BEGINNER'

    # Fall back to duration-based
    if duration_seconds < 600:  # < 10 min
        return 'BEGINNER'
    elif duration_seconds < 1800:  # < 30 min
        return 'INTERMEDIATE'
    elif duration_seconds < 3600:  # < 1 hour
        return 'ADVANCED'
    else:
        return 'COMPREHENSIVE'


def determine_application(title: str) -> str:
    """Determine MS Office application from title."""
    title_lower = title.lower()

    if 'power bi' in title_lower:
        return 'Power BI'
    if 'powerpoint' in title_lower:
        return 'PowerPoint'
    if 'outlook' in title_lower:
        return 'Outlook'
    if 'access' in title_lower:
        return 'Microsoft Access'
    if 'project' in title_lower:
        return 'Microsoft Project'
    if 'word' in title_lower:
        return 'Microsoft Word'
    if 'excel' in title_lower or 'pivot' in title_lower or 'formula' in title_lower:
        return 'Excel'
    if 'office' in title_lower or '365' in title_lower:
        return 'Microsoft 365'

    return 'Microsoft Office'


def parse_duration(duration_str: str) -> int:
    """Parse duration string like '12:34' or '1:23:45' to seconds."""
    parts = duration_str.split(':')
    if len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    elif len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    return 0


async def extract_video_metadata(page) -> dict:
    """Extract video metadata from the page using JavaScript for reliability."""
    metadata = await page.evaluate('''
        () => {
            const result = {
                title: 'Unknown',
                channel: 'Unknown',
                duration: 'Unknown'
            };

            // Get title - try multiple selectors
            const titleSelectors = [
                'h1.ytd-watch-metadata yt-formatted-string',
                'h1.title yt-formatted-string',
                '#title h1 yt-formatted-string',
                'h1.ytd-video-primary-info-renderer'
            ];
            for (const sel of titleSelectors) {
                const elem = document.querySelector(sel);
                if (elem && elem.textContent.trim()) {
                    result.title = elem.textContent.trim();
                    break;
                }
            }
            // Fallback to page title
            if (result.title === 'Unknown') {
                result.title = document.title.replace(' - YouTube', '').trim();
            }

            // Get channel name
            const channelSelectors = [
                '#channel-name a',
                'ytd-channel-name a',
                '.ytd-channel-name a'
            ];
            for (const sel of channelSelectors) {
                const elem = document.querySelector(sel);
                if (elem && elem.textContent.trim()) {
                    result.channel = elem.textContent.trim();
                    break;
                }
            }

            // Get duration from video player or time display
            const durationSelectors = [
                '.ytp-time-duration',
                'span.ytp-time-duration'
            ];
            for (const sel of durationSelectors) {
                const elem = document.querySelector(sel);
                if (elem && elem.textContent.trim() && elem.textContent !== '0:00') {
                    result.duration = elem.textContent.trim();
                    break;
                }
            }

            // Alternative: Get from video element if available
            if (result.duration === 'Unknown' || result.duration === '0:00') {
                const video = document.querySelector('video');
                if (video && video.duration && !isNaN(video.duration)) {
                    const mins = Math.floor(video.duration / 60);
                    const secs = Math.floor(video.duration % 60);
                    const hours = Math.floor(mins / 60);
                    if (hours > 0) {
                        result.duration = `${hours}:${String(mins % 60).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
                    } else {
                        result.duration = `${mins}:${String(secs).padStart(2, '0')}`;
                    }
                }
            }

            return result;
        }
    ''')

    return metadata


async def open_transcript_panel(page) -> bool:
    """Open the transcript panel on the video page."""
    try:
        # Scroll down to make description visible
        await page.evaluate('window.scrollBy(0, 300)')
        await page.wait_for_timeout(1000)

        # Try multiple methods to expand description and find transcript

        # Method 1: Click the description area to expand it
        desc_area = await page.query_selector('#description-inline-expander, #expand, ytd-text-inline-expander')
        if desc_area:
            await desc_area.click()
            await page.wait_for_timeout(2000)

        # Method 2: Click "...more" button if visible
        more_btn = await page.query_selector('tp-yt-paper-button#expand, button.yt-spec-button-shape-next--text')
        if more_btn:
            try:
                await more_btn.click()
                await page.wait_for_timeout(2000)
            except:
                pass

        # Method 3: Use JavaScript to find and click Show transcript button
        transcript_clicked = await page.evaluate('''
            () => {
                // Look for "Show transcript" button by text content
                const buttons = document.querySelectorAll('button');
                for (const btn of buttons) {
                    if (btn.textContent.toLowerCase().includes('show transcript') ||
                        btn.getAttribute('aria-label')?.toLowerCase().includes('transcript')) {
                        btn.click();
                        return true;
                    }
                }

                // Look in engagement panels
                const transcriptBtn = document.querySelector('button[aria-label="Show transcript"]');
                if (transcriptBtn) {
                    transcriptBtn.click();
                    return true;
                }

                // Look for transcript segment in description
                const segments = document.querySelectorAll('ytd-transcript-segment-list-renderer');
                if (segments.length > 0) {
                    return true;  // Already open
                }

                return false;
            }
        ''')

        if transcript_clicked:
            await page.wait_for_timeout(3000)
            return True

        # Method 4: Try "More actions" menu
        more_actions = await page.query_selector('button[aria-label="More actions"]')
        if more_actions:
            await more_actions.click()
            await page.wait_for_timeout(1000)

            # Look for transcript option using JavaScript
            found = await page.evaluate('''
                () => {
                    const items = document.querySelectorAll('ytd-menu-service-item-renderer, tp-yt-paper-item');
                    for (const item of items) {
                        if (item.textContent.toLowerCase().includes('transcript')) {
                            item.click();
                            return true;
                        }
                    }
                    return false;
                }
            ''')

            if found:
                await page.wait_for_timeout(3000)
                return True

            # Close menu
            await page.keyboard.press('Escape')
            await page.wait_for_timeout(500)

        # Final check: see if segments are now visible
        segments = await page.query_selector('ytd-transcript-segment-renderer')
        return segments is not None

    except Exception as e:
        print(f"Error opening transcript panel: {e}")
        return False


async def extract_transcript_segments(page, max_segments: int = None) -> dict:
    """Extract transcript segments using JavaScript evaluation."""
    js_code = """
    () => {
        const segments = document.querySelectorAll('ytd-transcript-segment-renderer');
        if (segments.length > 0) {
            const maxSegs = %s || segments.length;
            const actualMax = Math.min(segments.length, maxSegs);
            return {
                count: segments.length,
                extracted: actualMax,
                transcript: Array.from(segments).slice(0, actualMax).map(seg => {
                    const time = seg.querySelector('.segment-timestamp')?.textContent?.trim() || '';
                    const text = seg.querySelector('.segment-text')?.textContent?.trim() || '';
                    return time + ' ' + text;
                }).join('\\n')
            };
        }
        return { count: 0, extracted: 0, transcript: null };
    }
    """ % (max_segments if max_segments else 'null')

    result = await page.evaluate(js_code)
    return result


async def extract_all_segments_batched(page, total_segments: int, batch_size: int = 500) -> str:
    """Extract all segments in batches for very long videos."""
    all_transcript = []

    for offset in range(0, total_segments, batch_size):
        js_code = f"""
        () => {{
            const segments = document.querySelectorAll('ytd-transcript-segment-renderer');
            const start = {offset};
            const end = Math.min(start + {batch_size}, segments.length);
            return Array.from(segments).slice(start, end).map(seg => {{
                const time = seg.querySelector('.segment-timestamp')?.textContent?.trim() || '';
                const text = seg.querySelector('.segment-text')?.textContent?.trim() || '';
                return time + ' ' + text;
            }}).join('\\n');
        }}
        """
        batch_result = await page.evaluate(js_code)
        if batch_result:
            all_transcript.append(batch_result)
        print(f"  Extracted segments {offset} to {min(offset + batch_size, total_segments)}")

    return '\n'.join(all_transcript)


def create_transcript_file(video_id: str, metadata: dict, transcript: str,
                          output_dir: str = DEFAULT_OUTPUT_DIR) -> str:
    """Create the transcript file with metadata header."""
    title = metadata.get('title', 'Unknown Title')
    channel = metadata.get('channel', 'Unknown Channel')
    duration = metadata.get('duration', 'Unknown')

    # Parse duration for level determination
    duration_seconds = parse_duration(duration) if duration != 'Unknown' else 0
    level = determine_level(duration_seconds, title)
    application = determine_application(title)

    # Create filename
    date_str = datetime.now().strftime('%Y-%m-%d')
    safe_title = sanitize_filename(title)
    filename = f"{date_str}_{level}_{video_id}_{safe_title}.txt"

    # Create header
    header = f"""Title: {title}
Channel: {channel}
Video ID: {video_id}
URL: https://www.youtube.com/watch?v={video_id}
Duration: {duration}
Level: {level}
Application: {application}
Topics: Auto-generated from transcript
Ingested: {date_str}
Source: Playwright Browser Extraction
==============================================================================

"""

    # Write file
    output_path = Path(output_dir) / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(header + transcript)

    return str(output_path)


async def extract_single_video(url: str, output_dir: str = DEFAULT_OUTPUT_DIR,
                               headless: bool = False) -> dict:
    """Extract transcript from a single YouTube video."""
    # Extract video ID from URL
    video_id_match = re.search(r'(?:v=|/)([a-zA-Z0-9_-]{11})', url)
    if not video_id_match:
        return {'success': False, 'error': 'Invalid YouTube URL'}

    video_id = video_id_match.group(1)
    result = {'video_id': video_id, 'url': url}

    async with async_playwright() as p:
        # Launch browser (use headed mode for debugging)
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = await context.new_page()

        try:
            # Navigate to video (use domcontentloaded - networkidle hangs on YouTube)
            print(f"Loading video: {url}")
            await page.goto(url, wait_until='domcontentloaded', timeout=60000)
            await page.wait_for_timeout(3000)

            # Handle cookie consent dialog if present
            try:
                consent_btn = await page.query_selector('button[aria-label*="Accept"], button:has-text("Accept all"), button:has-text("Reject all")')
                if consent_btn:
                    await consent_btn.click()
                    await page.wait_for_timeout(2000)
            except:
                pass

            # Wait for video player to initialize
            await page.wait_for_timeout(3000)

            # Click on video to start loading if needed
            try:
                video_player = await page.query_selector('.html5-main-video, video')
                if video_player:
                    await video_player.click()
                    await page.wait_for_timeout(2000)
            except:
                pass

            # Get metadata
            metadata = await extract_video_metadata(page)
            result['metadata'] = metadata
            print(f"Title: {metadata.get('title', 'Unknown')}")
            print(f"Duration: {metadata.get('duration', 'Unknown')}")

            # Open transcript panel
            print("Opening transcript panel...")
            if not await open_transcript_panel(page):
                result['success'] = False
                result['error'] = 'Could not open transcript panel - transcript may not be available'
                return result

            # Wait for transcript to load
            await page.wait_for_timeout(2000)

            # Extract transcript
            print("Extracting transcript segments...")
            transcript_data = await extract_transcript_segments(page)

            if not transcript_data or transcript_data['count'] == 0:
                result['success'] = False
                result['error'] = 'No transcript segments found'
                return result

            total_segments = transcript_data['count']
            print(f"Found {total_segments} segments")

            # Handle very long videos with batched extraction
            if total_segments > MAX_SEGMENTS_PER_BATCH:
                print(f"Large transcript detected, extracting in batches...")
                transcript = await extract_all_segments_batched(page, total_segments, MAX_SEGMENTS_PER_BATCH)
            else:
                transcript = transcript_data['transcript']

            # Remove duplicate lines (YouTube sometimes shows duplicates)
            lines = transcript.split('\n')
            seen = set()
            unique_lines = []
            for line in lines:
                if line not in seen:
                    seen.add(line)
                    unique_lines.append(line)
            transcript = '\n'.join(unique_lines)

            # Save to file
            output_path = create_transcript_file(video_id, metadata, transcript, output_dir)

            result['success'] = True
            result['segments'] = total_segments
            result['unique_segments'] = len(unique_lines)
            result['output_file'] = output_path
            print(f"Saved to: {output_path}")

        except Exception as e:
            result['success'] = False
            result['error'] = str(e)
            print(f"Error: {e}")

        finally:
            await browser.close()

    return result


async def extract_from_json(json_path: str, output_dir: str = DEFAULT_OUTPUT_DIR) -> list:
    """Extract transcripts from all URLs in a JSON file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Support both list of URLs and list of objects with 'url' key
    urls = []
    if isinstance(data, list):
        for item in data:
            if isinstance(item, str):
                urls.append(item)
            elif isinstance(item, dict) and 'url' in item:
                urls.append(item['url'])
    elif isinstance(data, dict) and 'urls' in data:
        urls = data['urls']

    results = []
    for i, url in enumerate(urls):
        print(f"\n{'='*60}")
        print(f"Processing video {i+1}/{len(urls)}")
        print(f"{'='*60}")

        result = await extract_single_video(url, output_dir)
        results.append(result)

        # Brief pause between videos to avoid rate limiting
        if i < len(urls) - 1:
            await asyncio.sleep(2)

    return results


def print_summary(results: list):
    """Print extraction summary."""
    print(f"\n{'='*60}")
    print("EXTRACTION SUMMARY")
    print(f"{'='*60}")

    successful = [r for r in results if r.get('success')]
    failed = [r for r in results if not r.get('success')]

    print(f"Total videos processed: {len(results)}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")

    if successful:
        print(f"\nSuccessful extractions:")
        for r in successful:
            print(f"  - {r['video_id']}: {r.get('segments', 0)} segments -> {r.get('output_file', 'unknown')}")

    if failed:
        print(f"\nFailed extractions:")
        for r in failed:
            print(f"  - {r['video_id']}: {r.get('error', 'Unknown error')}")


async def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("YouTube Transcript Extractor")
        print("Usage:")
        print("  python extract_youtube_transcript.py <video_url>")
        print("  python extract_youtube_transcript.py <urls.json>")
        print("\nExamples:")
        print("  python extract_youtube_transcript.py https://www.youtube.com/watch?v=abc123")
        print("  python extract_youtube_transcript.py target_urls.json")
        sys.exit(1)

    input_arg = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUTPUT_DIR

    if input_arg.endswith('.json'):
        # Process JSON file with multiple URLs
        results = await extract_from_json(input_arg, output_dir)
        print_summary(results)
    else:
        # Process single URL
        result = await extract_single_video(input_arg, output_dir)
        if result['success']:
            print(f"\nSuccess! Transcript saved to: {result['output_file']}")
        else:
            print(f"\nFailed: {result.get('error', 'Unknown error')}")
            sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
