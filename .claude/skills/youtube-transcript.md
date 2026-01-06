# Skill: YouTube Transcript Extraction

## Name
youtube-transcript

## Description
Extract transcripts from YouTube videos and ingest them into the Trajanus Knowledge Base. Handles API limitations, alternative sources, and proper formatting.

## When to Use
- User provides YouTube URL(s) for transcript extraction
- User requests video content for KB ingestion
- Research tasks requiring video content analysis

## Procedure

### Step 1: Identify Video IDs
Extract video ID from URL (the 11-character string after `v=`):
```
https://www.youtube.com/watch?v=VIDEO_ID
```

### Step 2: Get Video Metadata
Use YouTube Data API with available API keys:
```python
from googleapiclient.discovery import build

API_KEY = 'AIzaSyBl_lWBv86KeH4HnFaV0MoptSxMLaYgrSI'  # Primary key
youtube = build('youtube', 'v3', developerKey=API_KEY)

response = youtube.videos().list(
    part='snippet,contentDetails',
    id=video_id
).execute()
```

### Step 3: Attempt Transcript Extraction

**Method A: youtube-transcript-api**
```python
from youtube_transcript_api import YouTubeTranscriptApi
api = YouTubeTranscriptApi()
transcript = api.fetch(video_id)
```

**Method B: If API blocked, search web for summaries**
- lilys.ai/notes/
- creatoreconomy.so
- motlin.com/blog
- octospark.ai/blog

### Step 4: Format Output
Create markdown file:
```markdown
# [Video Title]

## Metadata
- **URL:** https://www.youtube.com/watch?v=[ID]
- **Channel:** [Channel Name]
- **Duration:** [Duration]
- **Extracted:** [Date]

## Full Transcript
[Content]

## Key Concepts
[Extracted patterns]

## Actionable Takeaways
[Bullet points]
```

### Step 5: Ingest to KB
```python
# Use knowledge_base table (NOT documents table - RLS issues)
supabase.table('knowledge_base').insert({
    'url': url,
    'title': title,
    'content': content,
    'embedding': embedding,
    'metadata': {'category': 'VIDEO_TRANSCRIPT'}
}).execute()
```

## Output Location
`G:\My Drive\00 - Trajanus USA\00-Command-Center\07-Learning\`

## API Keys Available
```
AIzaSyBl_lWBv86KeH4HnFaV0MoptSxMLaYgrSI
AIzaSyAY8QD37iUhiccdfmXqGcLdphJCMV_cr7I
AIzaSyBH06ztWeFjGYQLsT9URPSttTj8FqD3Wps
AIzaSyAzNEedSAv-WgTW6u5o_HhHKK6ZK-H8VS4
```

## Error Handling
- If IP blocked: Use web search for existing transcripts
- If no captions: Note in output, extract description instead
- If API quota exceeded: Rotate to next API key
