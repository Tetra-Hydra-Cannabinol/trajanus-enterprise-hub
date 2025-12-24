"""
YouTube Scanner Module
Searches YouTube for relevant AI/Claude content using YouTube Data API v3
"""

from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import isodate
import config


def parse_duration(duration_str: str) -> int:
    """Convert ISO 8601 duration to minutes"""
    try:
        duration = isodate.parse_duration(duration_str)
        return int(duration.total_seconds() / 60)
    except:
        return 0


def parse_view_count(stats: dict) -> int:
    """Extract view count from statistics"""
    try:
        return int(stats.get("viewCount", 0))
    except:
        return 0


def scan_youtube(queries: list = None, max_results: int = 10) -> list:
    """
    Search YouTube for videos matching queries.

    Args:
        queries: List of search terms (defaults to config.YOUTUBE_QUERIES)
        max_results: Maximum results per query

    Returns:
        List of dicts with: title, channel, url, published, duration, views
    """
    if queries is None:
        queries = config.YOUTUBE_QUERIES

    # Check for API key
    if not config.YOUTUBE_API_KEY:
        print("WARNING: YOUTUBE_API_KEY not set. Returning empty results.")
        return []

    try:
        youtube = build("youtube", "v3", developerKey=config.YOUTUBE_API_KEY)
    except Exception as e:
        print(f"ERROR: Failed to build YouTube client: {e}")
        return []

    # Calculate date 7 days ago
    week_ago = (datetime.utcnow() - timedelta(days=7)).isoformat() + "Z"

    all_videos = []
    seen_ids = set()

    for query in queries:
        print(f"Searching: {query}")

        try:
            # Search for videos
            search_response = youtube.search().list(
                q=query,
                part="id,snippet",
                type="video",
                publishedAfter=week_ago,
                maxResults=max_results,
                order="viewCount",
                videoDuration="medium"  # 4-20 minutes
            ).execute()

            video_ids = [
                item["id"]["videoId"]
                for item in search_response.get("items", [])
                if item["id"]["videoId"] not in seen_ids
            ]

            if not video_ids:
                continue

            # Get video details (duration, view count)
            videos_response = youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=",".join(video_ids)
            ).execute()

            for video in videos_response.get("items", []):
                video_id = video["id"]
                snippet = video["snippet"]
                content = video["contentDetails"]
                stats = video["statistics"]

                duration_mins = parse_duration(content.get("duration", "PT0M"))
                views = parse_view_count(stats)

                # Filter: 5-60 minutes, 1000+ views
                if duration_mins < 5 or duration_mins > 60:
                    continue
                if views < 1000:
                    continue

                seen_ids.add(video_id)
                all_videos.append({
                    "title": snippet.get("title", ""),
                    "channel": snippet.get("channelTitle", ""),
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                    "published": snippet.get("publishedAt", ""),
                    "duration": duration_mins,
                    "views": views,
                    "query": query
                })

        except HttpError as e:
            print(f"HTTP Error for query '{query}': {e}")
        except Exception as e:
            print(f"Error for query '{query}': {e}")

    # Sort by views descending
    all_videos.sort(key=lambda x: x["views"], reverse=True)

    return all_videos


if __name__ == "__main__":
    print("=" * 60)
    print("YouTube Scanner Test")
    print("=" * 60)

    # Check config
    if not config.YOUTUBE_API_KEY:
        print("\nYOUTUBE_API_KEY not set in environment.")
        print("The scanner is ready but needs an API key to function.")
        print(f"\nExpected location: {config.CREDENTIALS_PATH}")
        print("Add: YOUTUBE_API_KEY=your_key_here")
    else:
        print("\nAPI key found. Running scan...")
        videos = scan_youtube(max_results=5)

        print(f"\nFound {len(videos)} videos:\n")
        for i, video in enumerate(videos, 1):
            print(f"{i}. {video['title']}")
            print(f"   Channel: {video['channel']}")
            print(f"   Views: {video['views']:,} | Duration: {video['duration']} min")
            print(f"   URL: {video['url']}")
            print()
