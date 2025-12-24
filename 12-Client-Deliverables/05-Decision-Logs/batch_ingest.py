#!/usr/bin/env python3
"""
Batch Knowledge Base Ingestion
Processes multiple URLs at once - handles YouTube transcripts and web crawling
"""

import subprocess
import sys
from pathlib import Path

# URLs to process
URLS = [
    # YouTube videos - need transcript extraction
    ("https://www.youtube.com/watch?v=PEI_ePNNfJQ", "youtube", "YouTube - Supabase MCP"),
    ("https://www.youtube.com/watch?v=mNcXue7X8H0", "youtube", "YouTube - MCP Tutorial 2"),
    ("https://www.youtube.com/watch?v=d40gE6bKxPk", "youtube", "YouTube - MCP Tutorial 3"),
    ("https://www.youtube.com/watch?v=usQ2HBTTWxs", "youtube", "YouTube - MCP Tutorial 4"),
    ("https://www.youtube.com/watch?v=q0u5jmA24ng", "youtube", "YouTube - MCP Tutorial 5"),
    ("https://www.youtube.com/watch?v=UeOStalTSKk", "youtube", "YouTube - MCP Tutorial 6"),
    ("https://www.youtube.com/watch?v=4UXAhwWHF8Y", "youtube", "YouTube - MCP Tutorial 7"),
    
    # Web pages - crawl directly
    ("https://www.wbdg.org/dod/ufgs", "web", "DoD UFGS Specifications"),
    ("https://www.wbdg.org/dod/ufc", "web", "DoD UFC Criteria"),
    ("https://viasocket.com/integrations/anthropic-claude/oracle-primavera-cloud", "web", "Claude-Primavera Integration"),
    ("https://viasocket.com/integrations/procore/anthropic-claude", "web", "Procore-Claude Integration"),
]

def ingest_youtube(url, title):
    """Extract YouTube transcript and ingest"""
    print(f"\n{'='*60}")
    print(f"Processing YouTube: {title}")
    print(f"URL: {url}")
    print(f"{'='*60}\n")
    
    # Extract video ID
    video_id = url.split("watch?v=")[1].split("&")[0] if "watch?v=" in url else url.split("/")[-1]
    
    try:
        # Use youtube-transcript-api to get transcript
        from youtube_transcript_api import YouTubeTranscriptApi
        
        print(f"Fetching transcript for video ID: {video_id}")
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Combine transcript into single text
        full_text = " ".join([entry['text'] for entry in transcript_list])
        
        # Save to temp file
        temp_file = f"temp_transcript_{video_id}.txt"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(f"Title: {title}\n")
            f.write(f"URL: {url}\n")
            f.write(f"\n{'='*60}\n\n")
            f.write(full_text)
        
        print(f"✓ Transcript saved: {len(full_text)} characters")
        print(f"✓ Temp file: {temp_file}")
        
        # Now ingest this file
        print(f"\nIngesting transcript into knowledge base...")
        # This would call file_ingestion.py programmatically
        # For now, just report success
        print(f"✓ Ready for ingestion: {temp_file}")
        
        return temp_file
        
    except Exception as e:
        print(f"✗ Error processing YouTube video: {str(e)}")
        return None

def ingest_web(url, title):
    """Crawl web page and ingest"""
    print(f"\n{'='*60}")
    print(f"Processing Web Page: {title}")
    print(f"URL: {url}")
    print(f"{'='*60}\n")
    
    try:
        # Call live_crawler.py
        result = subprocess.run(
            [sys.executable, "live_crawler.py", url, title, "Technical Documentation"],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        print(result.stdout)
        
        if result.returncode == 0:
            print(f"✓ Successfully crawled and ingested: {title}")
            return True
        else:
            print(f"✗ Error crawling {title}")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"✗ Timeout crawling {title} (took > 5 minutes)")
        return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def main():
    """Process all URLs"""
    print(f"\n{'#'*60}")
    print("BATCH KNOWLEDGE BASE INGESTION")
    print(f"{'#'*60}\n")
    print(f"Total URLs to process: {len(URLS)}\n")
    
    # Check if youtube-transcript-api is installed
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        youtube_available = True
    except ImportError:
        print("⚠ WARNING: youtube-transcript-api not installed")
        print("  Install with: pip install youtube-transcript-api --break-system-packages")
        youtube_available = False
    
    results = {
        'success': [],
        'failed': [],
        'youtube_files': []
    }
    
    for url, url_type, title in URLS:
        if url_type == "youtube":
            if youtube_available:
                temp_file = ingest_youtube(url, title)
                if temp_file:
                    results['youtube_files'].append(temp_file)
                    results['success'].append(title)
                else:
                    results['failed'].append(title)
            else:
                print(f"✗ Skipping YouTube video (library not installed): {title}")
                results['failed'].append(title)
        
        elif url_type == "web":
            if ingest_web(url, title):
                results['success'].append(title)
            else:
                results['failed'].append(title)
    
    # Summary
    print(f"\n{'='*60}")
    print("BATCH INGESTION SUMMARY")
    print(f"{'='*60}")
    print(f"✓ Successful: {len(results['success'])}")
    print(f"✗ Failed: {len(results['failed'])}")
    
    if results['youtube_files']:
        print(f"\n📄 YouTube transcript files created ({len(results['youtube_files'])}):")
        for f in results['youtube_files']:
            print(f"  - {f}")
        print("\nNOTE: Run file_ingestion.py to add these transcripts to knowledge base")
    
    if results['failed']:
        print(f"\n✗ Failed items:")
        for item in results['failed']:
            print(f"  - {item}")

if __name__ == "__main__":
    main()
