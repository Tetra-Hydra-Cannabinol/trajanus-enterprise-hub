# YouTube Transcript Extractor

A Python tool for extracting transcripts from YouTube videos using Playwright browser automation. This approach bypasses YouTube API restrictions and rate limits by using actual browser rendering.

## Why This Approach?

Standard YouTube transcript APIs and libraries (like `youtube-transcript-api`) often fail due to:
- Bot detection and rate limiting
- Authentication requirements
- Regional restrictions
- Changes in YouTube's internal API

This tool uses **Playwright** to:
1. Launch a real browser instance
2. Navigate to the YouTube video page
3. Click the "Show transcript" button
4. Extract transcript segments from the rendered DOM

## Tools Used

| Tool | Purpose |
|------|---------|
| **Playwright** (Python) | Browser automation framework |
| **Chromium** | Browser engine (bundled with Playwright) |
| **JavaScript evaluation** | DOM traversal to extract transcript segments |

## Key Technical Details

### DOM Selectors Used
```javascript
// Transcript segments container
ytd-transcript-segment-renderer

// Timestamp within segment
.segment-timestamp

// Text within segment
.segment-text
```

### Transcript Panel Access
The script tries multiple methods to open the transcript:
1. Expand description (`tp-yt-paper-button#expand`)
2. Click "Show transcript" button (`button[aria-label="Show transcript"]`)
3. Click "More actions" menu and find transcript option

### Handling Large Videos
Videos over 1 hour may have thousands of segments. The script:
- Extracts in batches of 500 segments
- Removes duplicate lines (YouTube sometimes shows duplicates)
- Reports progress during extraction

## Installation

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install Playwright Browsers
```bash
playwright install chromium
```

Or install all browsers:
```bash
playwright install
```

## Usage

### Single Video
```bash
python extract_youtube_transcript.py https://www.youtube.com/watch?v=VIDEO_ID
```

### Multiple Videos (JSON file)
```bash
python extract_youtube_transcript.py target_urls.json
```

### Custom Output Directory
```bash
python extract_youtube_transcript.py https://www.youtube.com/watch?v=VIDEO_ID /path/to/output
```

## JSON Input Format

Create a `target_urls.json` file with URLs:

```json
[
    "https://www.youtube.com/watch?v=abc123",
    "https://www.youtube.com/watch?v=def456",
    "https://www.youtube.com/watch?v=ghi789"
]
```

Or with objects:
```json
{
    "urls": [
        "https://www.youtube.com/watch?v=abc123",
        "https://www.youtube.com/watch?v=def456"
    ]
}
```

Or with metadata:
```json
[
    {"url": "https://www.youtube.com/watch?v=abc123", "title": "Excel Basics"},
    {"url": "https://www.youtube.com/watch?v=def456", "title": "Word Advanced"}
]
```

## Output Format

Each transcript is saved as a text file with this structure:

```
Title: Excel Tutorial for Beginners
Channel: MyOnlineTrainingHub
Video ID: abc123
URL: https://www.youtube.com/watch?v=abc123
Duration: 15:30
Level: INTERMEDIATE
Application: Excel
Topics: Auto-generated from transcript
Ingested: 2025-12-20
Source: Playwright Browser Extraction
==============================================================================

0:00 Welcome to this Excel tutorial
0:05 In this video we'll cover the basics
...
```

### Filename Convention
```
{date}_{LEVEL}_{videoID}_{sanitized_title}.txt
```

Example:
```
2025-12-20_INTERMEDIATE_abc123_Excel_Tutorial_for_Beginners.txt
```

### Level Detection
The script auto-detects skill level based on:
- **Title keywords**: "beginner", "advanced", "expert", etc.
- **Duration fallback**:
  - < 10 min: BEGINNER
  - 10-30 min: INTERMEDIATE
  - 30-60 min: ADVANCED
  - > 1 hour: COMPREHENSIVE

### Application Detection
Auto-detects MS Office application from title keywords:
- Excel, Word, PowerPoint, Outlook, Access, Project, Power BI, Microsoft 365

## Example Usage with Bill's Videos

```bash
# Single video from Bill's collection
python extract_youtube_transcript.py https://www.youtube.com/watch?v=o2zZFchF6GU

# Expected output:
# Loading video: https://www.youtube.com/watch?v=o2zZFchF6GU
# Title: The 4 Most Important Excel Features Ever Released (MUST Know)
# Duration: 13:30
# Opening transcript panel...
# Extracting transcript segments...
# Found 267 segments
# Saved to: G:\My Drive\...\2025-12-20_INTERMEDIATE_o2zZFchF6GU_The_4_Most_Important_Excel_Features.txt
```

## Troubleshooting

### "Could not open transcript panel"
- The video may not have a transcript available
- Try running with `headless=False` to see what's happening:
  ```python
  result = await extract_single_video(url, output_dir, headless=False)
  ```

### "No transcript segments found"
- The transcript may be loading slowly
- Increase `WAIT_TIMEOUT` in the script
- The video may have disabled transcripts

### Rate Limiting
- The script waits 2 seconds between videos
- For large batches, consider increasing this delay
- Run in smaller batches if issues persist

### Browser Not Found
Run:
```bash
playwright install chromium
```

## Fixes Applied During Development

1. **YouTube Bot Detection**: Using full browser instead of API
2. **Dynamic Content Loading**: Added waits for transcript panel
3. **Large Transcripts**: Implemented batch extraction for videos > 500 segments
4. **Duplicate Lines**: Added deduplication (YouTube shows duplicates sometimes)
5. **Description Expansion**: Script clicks "more" before looking for transcript button

## Limitations

- Requires Chromium browser (~200MB download)
- Slower than API (~5-10 seconds per video)
- Cannot extract if YouTube disables transcript for a video
- Very long videos (5+ hours) may take several minutes

## Integration with Supabase KB

After extraction, transcripts can be ingested to Supabase knowledge base using:
```bash
python ingest_ms_office_tutorials.py
```

(See separate documentation for ingestion pipeline)
