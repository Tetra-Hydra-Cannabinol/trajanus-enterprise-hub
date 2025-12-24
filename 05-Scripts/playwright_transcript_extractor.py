#!/usr/bin/env python3
"""
Playwright YouTube Transcript Extractor
Uses authenticated browser session to extract transcripts from Bill's curated videos
Bypasses YouTube bot detection by using existing browser session
"""

import asyncio
import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

# Load environment
from dotenv import load_dotenv
env_path = Path(__file__).parent / '.env'
if not env_path.exists():
    env_path = Path(__file__).parent / 'env.env'
load_dotenv(env_path)

# Output directory
OUTPUT_DIR = Path(r"G:\My Drive\00 - Trajanus USA\01-Morning-Sessions\Research\Microsoft_Office_Tutorials")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Bill's curated video collection
INDIVIDUAL_VIDEOS = [
    ('zpgFl4N4DIc', 'Excel Tutorial'),
    ('35X6v3aE86o', 'MS Project 2019 Full Course'),
    ('Uq4C9htBzU8', 'MS Office Tutorial'),
    ('mj_6BVpotgg', 'Office Tutorial'),
    ('2ms9ZUJbmpg', 'Office Training'),
    ('vQlFiLUaw4k', 'Office Course'),
    ('2H7aOHKZ6PY', 'Office Basics'),
    ('Z2t7l8b1uWU', 'Office Advanced'),
    ('1d3u3lmK1mQ', 'Word Tutorial'),
    ('I0k6zNC0OYQ', 'Word Course'),
    ('o2zZFchF6GU', 'Word Training'),
    ('9oYA5Vo_5LY', 'Word Advanced'),
    ('rgm8T1CI0xk', 'PowerPoint Tutorial'),
    ('Xa10Eb8pOuc', 'PowerPoint Course'),
    ('5qtSioTE2wY', 'Excel Formulas'),
    ('vhOHxMjrF7c', 'Excel Functions'),
    ('rUGQcyUYKoI', 'Excel Advanced'),
    ('DXOq1xiIaF0', 'Excel VBA'),
    ('Ss3WMhTDM5U', 'Excel Macros'),
    ('xT3gMWjQzdE', 'Excel Pivot'),
    ('vWmUfzVQSuY', 'Excel Data'),
    ('jCG2MTH9Ftw', 'Excel Charts'),
]

PLAYLIST_IDS = [
    'PLmd91OWgLVSLhrnAJo7A-mTxQmxhO-ekb',
    'PLmd91OWgLVSLi25rFhPR6Vt3nLBKg-EBJ',
    'PLmd91OWgLVSLlL6zSc-Nb0b9BSY9w9cPO',
]

# ANSI colors
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

async def extract_transcript_playwright(page, video_id, description=""):
    """Extract transcript from a single video using Playwright"""
    url = f"https://www.youtube.com/watch?v={video_id}"
    print(f"\n{Colors.CYAN}{'='*60}")
    print(f"Processing: {video_id}")
    print(f"URL: {url}")
    print(f"{'='*60}{Colors.END}")

    try:
        # Navigate to video
        await page.goto(url, wait_until='networkidle', timeout=30000)
        await asyncio.sleep(2)

        # Get video metadata
        title = await page.title()
        title = title.replace(' - YouTube', '').strip()
        print(f"  Title: {title[:60]}...")

        # Try to get channel name
        channel = "Unknown"
        try:
            channel_elem = await page.query_selector('ytd-channel-name a')
            if channel_elem:
                channel = await channel_elem.inner_text()
        except:
            pass
        print(f"  Channel: {channel}")

        # Expand description to find transcript button
        try:
            # Click "...more" to expand description
            more_btn = await page.query_selector('tp-yt-paper-button#expand')
            if more_btn:
                await more_btn.click()
                await asyncio.sleep(1)
        except:
            pass

        # Look for and click "Show transcript" button
        transcript_found = False
        try:
            # Try multiple selectors for transcript button
            selectors = [
                'button:has-text("Show transcript")',
                '[aria-label="Show transcript"]',
                'ytd-video-description-transcript-section-renderer button',
            ]

            for selector in selectors:
                try:
                    btn = await page.query_selector(selector)
                    if btn:
                        await btn.click()
                        await asyncio.sleep(2)
                        transcript_found = True
                        break
                except:
                    continue
        except Exception as e:
            print(f"  {Colors.YELLOW}Could not click transcript button: {e}{Colors.END}")

        if not transcript_found:
            # Try JavaScript approach
            try:
                await page.evaluate('''() => {
                    const btns = document.querySelectorAll('button');
                    for (let btn of btns) {
                        if (btn.innerText.includes('Show transcript')) {
                            btn.click();
                            return true;
                        }
                    }
                    return false;
                }''')
                await asyncio.sleep(2)
            except:
                pass

        # Extract transcript content
        transcript = await page.evaluate('''() => {
            // Method 1: Try transcript segments
            const segments = document.querySelectorAll('ytd-transcript-segment-renderer');
            if (segments.length > 0) {
                return Array.from(segments).map(seg => {
                    const time = seg.querySelector('.segment-timestamp')?.textContent?.trim() || '';
                    const text = seg.querySelector('.segment-text')?.textContent?.trim() || '';
                    return time + ' ' + text;
                }).join('\\n');
            }

            // Method 2: Try transcript body
            const body = document.querySelector('ytd-transcript-body-renderer');
            if (body) {
                return body.innerText;
            }

            // Method 3: Try engagement panel
            const panel = document.querySelector('ytd-engagement-panel-section-list-renderer[target-id="engagement-panel-transcript"]');
            if (panel) {
                return panel.innerText;
            }

            return null;
        }''')

        if transcript and len(transcript) > 100:
            print(f"  {Colors.GREEN}Transcript: {len(transcript):,} characters{Colors.END}")

            # Determine application type
            application = "Microsoft Office"
            title_lower = title.lower()
            if 'excel' in title_lower or 'vba' in title_lower:
                application = "Excel"
            elif 'word' in title_lower:
                application = "Word"
            elif 'powerpoint' in title_lower or 'ppt' in title_lower:
                application = "PowerPoint"
            elif 'project' in title_lower:
                application = "MS Project"
            elif 'outlook' in title_lower:
                application = "Outlook"
            elif 'access' in title_lower:
                application = "Access"

            # Determine level
            level = "COMPREHENSIVE"
            if 'advanced' in title_lower:
                level = "ADVANCED"
            elif 'expert' in title_lower:
                level = "EXPERT"
            elif 'beginner' in title_lower or 'basics' in title_lower:
                level = "BEGINNER"

            return {
                'success': True,
                'video_id': video_id,
                'title': title,
                'channel': channel,
                'application': application,
                'level': level,
                'transcript': transcript,
                'char_count': len(transcript)
            }
        else:
            print(f"  {Colors.RED}No transcript available{Colors.END}")
            return {
                'success': False,
                'video_id': video_id,
                'title': title,
                'error': 'No transcript found'
            }

    except Exception as e:
        print(f"  {Colors.RED}Error: {str(e)[:60]}{Colors.END}")
        return {
            'success': False,
            'video_id': video_id,
            'error': str(e)
        }

async def get_playlist_videos(page, playlist_id):
    """Extract video IDs from a YouTube playlist"""
    url = f"https://www.youtube.com/playlist?list={playlist_id}"
    print(f"\n{Colors.CYAN}Extracting playlist: {playlist_id}{Colors.END}")

    try:
        await page.goto(url, wait_until='networkidle', timeout=30000)
        await asyncio.sleep(2)

        # Scroll to load all videos
        for _ in range(5):
            await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            await asyncio.sleep(1)

        # Extract video IDs
        video_ids = await page.evaluate('''() => {
            const links = document.querySelectorAll('a#video-title');
            const ids = [];
            links.forEach(link => {
                const href = link.getAttribute('href');
                if (href && href.includes('watch?v=')) {
                    const match = href.match(/v=([^&]+)/);
                    if (match) {
                        ids.push({
                            id: match[1],
                            title: link.textContent.trim()
                        });
                    }
                }
            });
            return ids;
        }''')

        print(f"  Found {len(video_ids)} videos in playlist")
        return video_ids

    except Exception as e:
        print(f"  {Colors.RED}Error extracting playlist: {e}{Colors.END}")
        return []

def save_transcript(result, output_dir):
    """Save transcript to file"""
    if not result.get('success'):
        return None

    timestamp = datetime.now().strftime("%Y-%m-%d")
    video_id = result['video_id']

    # Create safe filename
    safe_title = "".join(c for c in result['title'][:40] if c.isalnum() or c in ' -_').strip()
    safe_title = safe_title.replace(' ', '_')

    filename = f"{timestamp}_{result['level']}_{video_id}_{safe_title}.txt"
    filepath = output_dir / filename

    content = f"""Title: {result['title']}
Channel: {result['channel']}
Video ID: {result['video_id']}
URL: https://www.youtube.com/watch?v={result['video_id']}
Level: {result['level']}
Application: {result['application']}
Characters: {result['char_count']:,}
Ingested: {datetime.now().isoformat()}
Source: Playwright Browser Extraction
{'='*70}

{result['transcript']}
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  {Colors.GREEN}Saved: {filename}{Colors.END}")
    return filepath

async def main():
    """Main extraction function"""
    from playwright.async_api import async_playwright

    print(f"\n{Colors.CYAN}{'='*70}")
    print(f"{'PLAYWRIGHT YOUTUBE TRANSCRIPT EXTRACTOR':^70}")
    print(f"{'='*70}{Colors.END}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Individual Videos: {len(INDIVIDUAL_VIDEOS)}")
    print(f"Playlists: {len(PLAYLIST_IDS)}")

    results = []

    async with async_playwright() as p:
        # Connect to existing browser or launch new one
        # Using chromium with persistent context to maintain login
        user_data_dir = Path.home() / '.playwright-youtube'

        browser = await p.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            headless=False,  # Keep visible so user can verify login
            viewport={'width': 1280, 'height': 720}
        )

        page = browser.pages[0] if browser.pages else await browser.new_page()

        # Process individual videos
        print(f"\n{Colors.YELLOW}Processing {len(INDIVIDUAL_VIDEOS)} individual videos...{Colors.END}")

        for video_id, description in INDIVIDUAL_VIDEOS:
            result = await extract_transcript_playwright(page, video_id, description)
            results.append(result)

            if result.get('success'):
                save_transcript(result, OUTPUT_DIR)

            await asyncio.sleep(2)  # Rate limiting

        # Process playlists
        all_playlist_videos = []
        for playlist_id in PLAYLIST_IDS:
            videos = await get_playlist_videos(page, playlist_id)
            all_playlist_videos.extend(videos)

        # Deduplicate
        seen = set(v[0] for v in INDIVIDUAL_VIDEOS)
        playlist_videos = [(v['id'], v['title']) for v in all_playlist_videos if v['id'] not in seen]

        print(f"\n{Colors.YELLOW}Processing {len(playlist_videos)} playlist videos...{Colors.END}")

        for video_id, title in playlist_videos:
            result = await extract_transcript_playwright(page, video_id, title)
            results.append(result)

            if result.get('success'):
                save_transcript(result, OUTPUT_DIR)

            await asyncio.sleep(2)

        await browser.close()

    # Summary
    success = sum(1 for r in results if r.get('success'))
    failed = len(results) - success
    total_chars = sum(r.get('char_count', 0) for r in results if r.get('success'))

    print(f"\n{Colors.CYAN}{'='*70}")
    print(f"{'EXTRACTION COMPLETE':^70}")
    print(f"{'='*70}{Colors.END}")
    print(f"Videos Processed: {len(results)}")
    print(f"Transcripts Extracted: {Colors.GREEN}{success}{Colors.END}")
    print(f"Failed: {Colors.RED if failed > 0 else ''}{failed}{Colors.END}")
    print(f"Total Content: {total_chars:,} characters ({total_chars/1024/1024:.1f} MB)")
    print(f"Output Directory: {OUTPUT_DIR}")

    # Save results JSON
    json_file = OUTPUT_DIR / f"{datetime.now().strftime('%Y-%m-%d_%H%M%S')}_extraction_results.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"Results JSON: {json_file.name}")

    return {
        'total': len(results),
        'success': success,
        'failed': failed,
        'total_chars': total_chars
    }

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result['success'] > 0 else 1)
