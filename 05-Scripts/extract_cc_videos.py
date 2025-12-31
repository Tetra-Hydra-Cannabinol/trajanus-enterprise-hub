#!/usr/bin/env python3
"""
Extract transcripts from Claude Code training videos
For Trajanus KB ingestion
"""

import asyncio
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

# Target videos for CC training
TARGET_VIDEOS = [
    ('OdtGN27LchE', 'CC_VIDEO_TRANSCRIPT_OdtGN27LchE.md'),
    ('o-pMCoVPN_k', 'CC_VIDEO_TRANSCRIPT_o-pMCoVPN_k.md'),
    ('uBJdwRPO1QE', 'CC_VIDEO_TRANSCRIPT_uBJdwRPO1QE.md'),
]

OUTPUT_DIR = Path(r"G:\My Drive\00 - Trajanus USA\00-Command-Center\07-Learning")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

async def extract_metadata(page):
    """Extract video metadata"""
    metadata = await page.evaluate('''
        () => {
            let title = document.title.replace(' - YouTube', '').trim();

            // Channel
            let channel = 'Unknown';
            const channelElem = document.querySelector('ytd-channel-name a, #channel-name a');
            if (channelElem) channel = channelElem.textContent.trim();

            // Duration
            let duration = 'Unknown';
            const durationElem = document.querySelector('.ytp-time-duration');
            if (durationElem) duration = durationElem.textContent.trim();

            // Description
            let description = '';
            const descElem = document.querySelector('#description-inline-expander');
            if (descElem) description = descElem.textContent.trim().substring(0, 500);

            return { title, channel, duration, description };
        }
    ''')
    return metadata

async def open_transcript(page):
    """Open the transcript panel with multiple approaches"""
    print("  Step 1: Scrolling page...")
    await page.evaluate('window.scrollBy(0, 400)')
    await asyncio.sleep(2)

    # Method 1: Click description area to expand
    print("  Step 2: Expanding description...")
    try:
        # Try multiple expand selectors
        expand_selectors = [
            '#description-inline-expander #expand',
            'tp-yt-paper-button#expand',
            '#expand',
            'button[aria-label="Show more"]',
            '#description ytd-text-inline-expander'
        ]
        for selector in expand_selectors:
            try:
                elem = await page.query_selector(selector)
                if elem:
                    await elem.click()
                    print(f"    Clicked: {selector}")
                    await asyncio.sleep(2)
                    break
            except:
                continue
    except Exception as e:
        print(f"    Expand error: {e}")

    # Method 2: Look for Show transcript button in description
    print("  Step 3: Looking for transcript button...")
    found = await page.evaluate('''
        () => {
            // Method A: Try the transcript section renderer button specifically
            const transcriptSection = document.querySelector('ytd-video-description-transcript-section-renderer');
            if (transcriptSection) {
                const btn = transcriptSection.querySelector('button');
                if (btn) {
                    btn.click();
                    return 'found-section-btn';
                }
            }

            // Method B: Look for transcript link in the description section chips
            const chips = document.querySelectorAll('yt-chip-cloud-chip-renderer, yt-formatted-string');
            for (const chip of chips) {
                if (chip.textContent.trim().toLowerCase() === 'transcript') {
                    chip.click();
                    return 'found-chip';
                }
            }

            // Method C: Try the engagement panel directly
            const transcriptEngagement = document.querySelector('button[aria-label="Show transcript"]');
            if (transcriptEngagement) {
                transcriptEngagement.click();
                return 'found-aria-btn';
            }

            // Method D: Find button with transcript text inside transcript section
            const section = document.querySelector('#structured-description ytd-video-description-transcript-section-renderer');
            if (section) {
                section.click();
                return 'found-section-click';
            }

            // Method E: Look for "Show transcript" specifically as a button
            const buttons = document.querySelectorAll('button, [role="button"]');
            for (const btn of buttons) {
                const text = btn.textContent?.toLowerCase() || '';
                const ariaLabel = btn.getAttribute('aria-label')?.toLowerCase() || '';
                if (text.includes('show transcript') || ariaLabel.includes('transcript')) {
                    btn.click();
                    return 'found-generic-btn';
                }
            }

            return null;
        }
    ''')

    if found:
        print(f"    Found via: {found}")
        # Wait longer for transcript to load
        print("    Waiting for transcript panel to open...")
        await asyncio.sleep(3)

        # Scroll the page to ensure transcript panel is visible
        await page.evaluate('window.scrollTo(0, 0)')
        await asyncio.sleep(2)

        # Try scrolling within any transcript segment list to trigger lazy loading
        await page.evaluate('''
            () => {
                const container = document.querySelector('ytd-transcript-segment-list-renderer, ytd-transcript-renderer');
                if (container) {
                    container.scrollTop = 100;
                }
            }
        ''')
        await asyncio.sleep(3)

        # Take screenshot for debugging
        screenshot_path = OUTPUT_DIR / f"debug_screenshot_{datetime.now().strftime('%H%M%S')}.png"
        await page.screenshot(path=str(screenshot_path))
        print(f"    Screenshot saved: {screenshot_path.name}")

        # Debug: Check what elements exist now
        debug_info = await page.evaluate('''
            () => {
                const info = {
                    segments: document.querySelectorAll('ytd-transcript-segment-renderer').length,
                    body: !!document.querySelector('ytd-transcript-body-renderer'),
                    renderer: !!document.querySelector('ytd-transcript-renderer'),
                    panel: !!document.querySelector('[target-id*="transcript"]'),
                    engagement: document.querySelectorAll('ytd-engagement-panel-section-list-renderer').length
                };

                // Check for transcript segment list
                info.segmentList = !!document.querySelector('ytd-transcript-segment-list-renderer');
                info.searchBox = !!document.querySelector('#search-box');

                // Get all engagement panel target IDs
                const panels = document.querySelectorAll('ytd-engagement-panel-section-list-renderer');
                info.panelIds = Array.from(panels).map(p => p.getAttribute('target-id') || 'none');

                // Check for the transcript panel specifically
                const transcriptPanel = document.querySelector('ytd-engagement-panel-section-list-renderer[target-id="engagement-panel-searchable-transcript"]');
                if (transcriptPanel) {
                    info.transcriptPanelVisible = transcriptPanel.getAttribute('visibility') || 'hidden';
                    // Look for segments inside
                    const segs = transcriptPanel.querySelectorAll('ytd-transcript-segment-renderer');
                    info.transcriptSegmentsInPanel = segs.length;
                    if (segs.length > 0) {
                        info.firstSegment = segs[0].textContent.trim().substring(0, 100);
                    }
                }

                // Also check for transcripts in any visible panel
                info.anyTranscriptText = '';
                panels.forEach(p => {
                    if (p.getAttribute('visibility') === 'ENGAGEMENT_PANEL_VISIBILITY_EXPANDED') {
                        const text = p.innerText;
                        if (text && text.length > info.anyTranscriptText.length) {
                            info.anyTranscriptText = text.substring(0, 500);
                        }
                    }
                });

                return info;
            }
        ''')
        print(f"    Debug: segments={debug_info.get('segments')}, segmentList={debug_info.get('segmentList')}")
        print(f"    Panel IDs: {debug_info.get('panelIds')}")
        if debug_info.get('transcriptPanelVisible'):
            print(f"    Transcript panel visibility: {debug_info['transcriptPanelVisible']}")
        if debug_info.get('anyTranscriptText'):
            print(f"    Visible panel text: {debug_info['anyTranscriptText'][:150]}...")

        return True

    # Method 3: Three-dot menu approach
    print("  Step 4: Trying three-dot menu...")
    try:
        # Scroll up to see video controls area
        await page.evaluate('window.scrollTo(0, 0)')
        await asyncio.sleep(1)

        more_btn = await page.query_selector('button[aria-label="More actions"], #button-shape button')
        if more_btn:
            await more_btn.click()
            await asyncio.sleep(2)

            found = await page.evaluate('''
                () => {
                    // Look in menu items
                    const menuItems = document.querySelectorAll('ytd-menu-service-item-renderer, tp-yt-paper-item, yt-list-item-view-model');
                    for (const item of menuItems) {
                        const text = item.textContent.toLowerCase();
                        if (text.includes('transcript') || text.includes('transcription')) {
                            item.click();
                            return true;
                        }
                    }
                    return false;
                }
            ''')

            if found:
                await asyncio.sleep(3)
                return True

            await page.keyboard.press('Escape')
            await asyncio.sleep(1)
    except Exception as e:
        print(f"    Menu error: {e}")

    # Method 4: Direct engagement panel click
    print("  Step 5: Checking engagement panels...")
    try:
        found = await page.evaluate('''
            () => {
                // Check if transcript panel already exists
                const panel = document.querySelector('ytd-engagement-panel-section-list-renderer[target-id="engagement-panel-searchable-transcript"]');
                if (panel) return true;

                // Try to open via keyboard shortcut simulation
                return false;
            }
        ''')
        if found:
            return True
    except:
        pass

    return False

async def extract_transcript(page):
    """Extract transcript text with multiple methods"""
    # Wait for transcript to load
    await asyncio.sleep(2)

    transcript = await page.evaluate('''
        () => {
            // Method 1: Standard segment renderer
            const segments = document.querySelectorAll('ytd-transcript-segment-renderer');
            if (segments.length > 0) {
                return {
                    count: segments.length,
                    method: 'segment-renderer',
                    text: Array.from(segments).map(seg => {
                        const time = seg.querySelector('.segment-timestamp')?.textContent?.trim() || '';
                        const text = seg.querySelector('.segment-text')?.textContent?.trim() || '';
                        return time + ' ' + text;
                    }).join('\\n')
                };
            }

            // Method 2: New transcript body format
            const transcriptBody = document.querySelector('ytd-transcript-renderer, ytd-transcript-body-renderer');
            if (transcriptBody) {
                const text = transcriptBody.innerText;
                if (text && text.length > 50) {
                    return {
                        count: text.split('\\n').length,
                        method: 'body-renderer',
                        text: text
                    };
                }
            }

            // Method 3: Engagement panel transcript
            const panel = document.querySelector('[target-id="engagement-panel-searchable-transcript"]');
            if (panel) {
                const text = panel.innerText;
                if (text && text.length > 50) {
                    return {
                        count: text.split('\\n').length,
                        method: 'engagement-panel',
                        text: text
                    };
                }
            }

            // Method 4: Any element with transcript cues
            const cues = document.querySelectorAll('[class*="transcript-cue"], [class*="caption-segment"]');
            if (cues.length > 0) {
                return {
                    count: cues.length,
                    method: 'cues',
                    text: Array.from(cues).map(c => c.textContent.trim()).join('\\n')
                };
            }

            return { count: 0, text: null, method: 'none' };
        }
    ''')

    if transcript.get('method'):
        print(f"    Extraction method: {transcript['method']}")

    return transcript

async def process_video(page, video_id, output_filename):
    """Process a single video using existing page"""
    print(f"\n{'='*60}")
    print(f"Processing: {video_id}")
    print(f"{'='*60}")

    url = f'https://www.youtube.com/watch?v={video_id}'

    try:
        # Load video
        print(f"Loading: {url}")
        await page.goto(url, wait_until='domcontentloaded', timeout=60000)
        await asyncio.sleep(5)

        # Handle cookie consent if needed
        try:
            consent = await page.query_selector('button:has-text("Accept all"), button:has-text("Reject all")')
            if consent:
                await consent.click()
                await asyncio.sleep(2)
        except:
            pass

        # Wait longer for page to fully load
        print("Waiting for page to fully load...")
        await asyncio.sleep(5)

        # Start video to trigger duration display
        try:
            video = await page.query_selector('video')
            if video:
                await video.click()
                await asyncio.sleep(2)
                # Pause it
                await video.click()
        except:
            pass

        # Get metadata
        metadata = await extract_metadata(page)
        print(f"Title: {metadata['title']}")
        print(f"Channel: {metadata['channel']}")
        print(f"Duration: {metadata['duration']}")

        # Open transcript
        print("Opening transcript panel...")
        if not await open_transcript(page):
            print("ERROR: Could not open transcript panel")
            return {'success': False, 'video_id': video_id, 'error': 'Could not open transcript'}

        # Extract transcript
        print("Extracting transcript...")
        transcript_data = await extract_transcript(page)

        if not transcript_data['text']:
            print("ERROR: No transcript found")
            return {'success': False, 'video_id': video_id, 'error': 'No transcript found'}

        print(f"Found {transcript_data['count']} segments")

        # Create markdown file
        content = f"""# {metadata['title']}

## Metadata
- **URL:** https://www.youtube.com/watch?v={video_id}
- **Channel:** {metadata['channel']}
- **Duration:** {metadata['duration']}
- **Extracted:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Description
{metadata['description']}

## Full Transcript

{transcript_data['text']}

## Key Concepts

*To be extracted after review*

### Hooks
- [ ] Identify hook patterns mentioned

### Commands
- [ ] List custom slash commands shown

### Sub-agents
- [ ] Document sub-agent patterns

### Workflows
- [ ] Capture workflow patterns

## Actionable Takeaways

*To be extracted after review*

## Integration Notes

*How this applies to Trajanus Enterprise Hub*
"""

        output_path = OUTPUT_DIR / output_filename
        output_path.write_text(content, encoding='utf-8')
        print(f"Saved: {output_path}")

        return {
            'success': True,
            'video_id': video_id,
            'title': metadata['title'],
            'segments': transcript_data['count'],
            'output_file': str(output_path),
            'word_count': len(transcript_data['text'].split())
        }

    except Exception as e:
        print(f"ERROR: {e}")
        return {'success': False, 'video_id': video_id, 'error': str(e)}

async def main():
    """Main extraction function"""
    print("\n" + "="*70)
    print("CLAUDE CODE VIDEO TRANSCRIPT EXTRACTOR")
    print("="*70)
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Videos to process: {len(TARGET_VIDEOS)}")

    user_data_dir = Path.home() / '.playwright-youtube'
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            headless=False,
            viewport={'width': 1280, 'height': 800}
        )

        # Use single page for all videos
        page = browser.pages[0] if browser.pages else await browser.new_page()

        for video_id, output_file in TARGET_VIDEOS:
            result = await process_video(page, video_id, output_file)
            results.append(result)

            # Brief pause between videos
            await asyncio.sleep(3)

        await browser.close()

    # Summary
    print("\n" + "="*70)
    print("EXTRACTION SUMMARY")
    print("="*70)

    success = [r for r in results if r.get('success')]
    failed = [r for r in results if not r.get('success')]

    print(f"Total: {len(results)}")
    print(f"Success: {len(success)}")
    print(f"Failed: {len(failed)}")

    if success:
        print("\nSuccessful extractions:")
        total_words = 0
        for r in success:
            print(f"  - {r['title'][:50]}...")
            print(f"    Segments: {r['segments']}, Words: {r['word_count']}")
            total_words += r['word_count']
        print(f"\nTotal word count: {total_words:,}")

    if failed:
        print("\nFailed extractions:")
        for r in failed:
            print(f"  - {r.get('video_id', 'Unknown')}: {r.get('error', 'Unknown error')}")

    # Save results JSON
    results_file = OUTPUT_DIR / f"extraction_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    results_file.write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(f"\nResults saved: {results_file}")

    return results

if __name__ == '__main__':
    results = asyncio.run(main())
    sys.exit(0 if any(r.get('success') for r in results) else 1)
