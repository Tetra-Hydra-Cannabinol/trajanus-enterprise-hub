#!/usr/bin/env python3
"""Extract Claude Code video transcripts using Playwright"""

import asyncio
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

OUTPUT_DIR = Path(r"G:\My Drive\00 - Trajanus USA\00-Command-Center\07-Learning")

VIDEOS = [
    ('OdtGN27LchE', 'Claude Code Skills just Built me an AI Agent Team (2026 Guide)', 'Riley Brown'),
    ('o-pMCoVPN_k', 'How to Run Claude Code For Hours Autonomously', 'Developers Digest'),
    ('uBJdwRPO1QE', 'Full Tutorial: Build Your Personal OS with Claude Code in 50 Min', 'Peter Yang'),
]

async def extract_transcript(page, video_id, title, channel):
    url = f'https://www.youtube.com/watch?v={video_id}'
    print(f'\nLoading: {title[:50]}...')

    await page.goto(url, wait_until='domcontentloaded', timeout=60000)
    await asyncio.sleep(8)

    # Scroll and expand description
    await page.evaluate('window.scrollBy(0, 400)')
    await asyncio.sleep(1)

    # Click expand button
    try:
        expand = await page.query_selector('#expand, tp-yt-paper-button#expand')
        if expand:
            await expand.click()
            await asyncio.sleep(2)
    except:
        pass

    # Find and click transcript button
    clicked = await page.evaluate("""
        () => {
            const section = document.querySelector('ytd-video-description-transcript-section-renderer');
            if (section) {
                const btn = section.querySelector('button');
                if (btn) {
                    btn.click();
                    return 'section-btn';
                }
            }
            return null;
        }
    """)

    if clicked:
        print(f'  Clicked: {clicked}')
        await asyncio.sleep(5)

        # Extract transcript
        transcript = await page.evaluate("""
            () => {
                const segments = document.querySelectorAll('ytd-transcript-segment-renderer');
                if (segments.length > 0) {
                    return {
                        count: segments.length,
                        text: Array.from(segments).map(seg => {
                            const time = seg.querySelector('.segment-timestamp');
                            const text = seg.querySelector('.segment-text');
                            const timeStr = time ? time.textContent.trim() : '';
                            const textStr = text ? text.textContent.trim() : '';
                            return timeStr + ' ' + textStr;
                        }).join('\\n')
                    };
                }
                return {count: 0, text: null};
            }
        """)

        if transcript['text']:
            print(f"  Got {transcript['count']} segments")
            return transcript['text']

    print('  No transcript extracted')
    return None

async def main():
    user_data_dir = Path.home() / '.playwright-youtube'

    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            headless=False,
            viewport={'width': 1400, 'height': 900}
        )

        page = browser.pages[0] if browser.pages else await browser.new_page()

        results = []
        for video_id, title, channel in VIDEOS:
            transcript = await extract_transcript(page, video_id, title, channel)

            if transcript:
                filename = f'CC_VIDEO_TRANSCRIPT_{video_id}.md'
                filepath = OUTPUT_DIR / filename

                content = f"""# {title}

## Metadata
- **URL:** https://www.youtube.com/watch?v={video_id}
- **Channel:** {channel}
- **Extracted:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Full Transcript

{transcript}

## Key Concepts

### Hooks
*To be extracted*

### Commands
*To be extracted*

### Sub-agents
*To be extracted*

### Workflows
*To be extracted*

## Actionable Takeaways

*To be extracted*
"""
                filepath.write_text(content, encoding='utf-8')
                print(f'  Saved: {filename}')
                results.append({'video_id': video_id, 'success': True, 'words': len(transcript.split())})
            else:
                results.append({'video_id': video_id, 'success': False})

        await browser.close()

        # Summary
        print('\n' + '='*50)
        print('EXTRACTION SUMMARY')
        print('='*50)
        success = [r for r in results if r['success']]
        print(f"Success: {len(success)}/{len(results)}")
        for r in success:
            print(f"  - {r['video_id']}: {r['words']} words")

if __name__ == '__main__':
    asyncio.run(main())
