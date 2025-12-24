"""
Ingest Playlist 3 video 18 (4hIxdFIaxLU) - DON'T Use Default Chart Labels, do This Instead!
"""

import os
from datetime import datetime
from supabase import create_client

def load_env():
    env_path = r'G:\My Drive\00 - Trajanus USA\00-Command-Center\.env'
    env_vars = {}
    with open(env_path, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if line and '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    return env_vars

env = load_env()
supabase = create_client(env['SUPABASE_URL'], env['SUPABASE_ANON_KEY'])

video_id = '4hIxdFIaxLU'
title = "DON'T Use Default Chart Labels, do This Instead!"
channel = 'MyOnlineTrainingHub'
duration = '3:50'
topics = ['Data Labels', 'Label Positioning', 'Text Boxes', 'Chart Formatting', 'White Fill Background', 'Color Matching', 'Legend Alternatives', 'Line Charts', 'Delete Axis', 'Remove Grid Lines', 'Series Labeling']

transcript = """0:00 labeling charts is useful if the reader
0:02 needs to know the exact value for each
0:05 point we can position labels left right
0:08 above below or centered however
0:10 centering line chart labels typically
0:12 looks messy so in this video I'm going
0:14 to show you how you can make them more
0:17 stylish here I have a regular line chart
0:20 first thing I want to do is add the data
0:23 labels and I want them
0:25 centered next I need to format each
0:28 series data labels so selecting the
0:30 labels just with one left click I'm
0:33 going to press control1 to open the
0:34 format data labels pane here I want the
0:37 paint bucket and I'm going to set the
0:40 fill to solid and I want it white that
0:43 way it hides the line behind the label
0:46 and we want to format the text it's a
0:48 good idea to match the text color to
0:50 that of the line now this is the line
0:52 color but notice with the font for the
0:55 text it looks a shade lighter so you can
0:58 always go one shade darker for your text
1:01 it will help the text be more readable
1:04 but the reader won't actually be able to
1:05 distinguish that it's a different shade
1:07 to the line let's rinse and repeat for
1:10 the orange series again we want solid
1:13 fill in white and for the text we want
1:17 it to be orange and we're going to go
1:19 one shade darker than the
1:21 line now that we have our data labeled
1:24 we don't need this vertical axis so I've
1:26 just selected it and I press the delete
1:28 key we also don't need the grid lines
1:31 they're just adding noise we have the
1:32 labels and that's enough so again left
1:35 click to select and press delete to
1:37 remove them now I have a legend but it's
1:40 at the bottom and with line charts it's
1:43 nice to have those lines labeled at the
1:45 end it just makes it quicker and easier
1:47 for our reader so we're going to remove
1:50 the legend I'm going to move the chart
1:52 body over to the left a little bit to
1:54 allow space for my Legend I'm going to
1:57 create this manually using text boxes so
2:00 in the shapes I want text box it's
2:03 actually down here in the basic shapes
2:05 but I use it regularly so it's up here
2:07 in my recently used shapes just going to
2:10 left click and drag to draw it on so
2:12 this is the south series and I want to
2:16 format my font to match the line so
2:18 let's choose the blue one shade darker
2:21 and the text box generally comes in with
2:24 a border and fill so let's just make
2:26 sure that isn't there so I want no fill
2:30 and no outline now if my chart resizes
2:34 my text box isn't going to cover the
2:37 Border or anything like that because it
2:39 has no fill so I just want to copy it so
2:42 I'm going to hold down control my mouse
2:44 cursor changes to show the plus symbol
2:46 going to left click and drag and hold
2:48 shift at the same time that keeps it
2:50 aligned to the text box above and let's
2:53 just change this to North and again
2:56 let's format the font to match the line
2:59 and there we have it our line chart with
3:02 our labels centered across the line and
3:05 we've labeled each of the
3:07 lines now an alternative to labeling
3:10 each point in the line is just to label
3:13 the first and last points and to do that
3:16 you simply left click once and then left
3:19 click again to select each Point's data
3:22 label and then press the delete key
3:24 rinse and repeat for each point after
3:26 that it's a little bit of manual work
3:28 but once it's set up it's done and
3:30 depending on the effect that you want
3:32 and how important seeing the value of
3:34 each point is you might find that the
3:35 first and last points are adequate I
3:38 hope you can make use of this technique
3:40 if you like this video please give it a
3:42 thumbs up and subscribe to my channel
3:44 for more thanks for
3:48 watching"""

# Save transcript
archive_dir = r'G:\My Drive\00 - Trajanus USA\00-Command-Center\Knowledge_Archive\Transcripts\Microsoft_Office'
os.makedirs(archive_dir, exist_ok=True)

header = f"""Title: {title}
Channel: {channel}
Video ID: {video_id}
URL: https://www.youtube.com/watch?v={video_id}
Duration: {duration}
Level: INTERMEDIATE
Application: Microsoft Excel
Topics: {', '.join(topics)}
Ingested: {datetime.now().strftime('%Y-%m-%d')}
Source: Playwright Browser Extraction
{'='*78}

"""

filename = f"{datetime.now().strftime('%Y-%m-%d')}_INTERMEDIATE_{video_id}_Custom_Chart_Labels.txt"
filepath = os.path.join(archive_dir, filename)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(header + transcript)

print(f'Transcript saved: {filename}')

# Chunk and ingest
def chunk_text(text, chunk_size=3000):
    chunks = []
    current = ''
    for line in text.split('\n'):
        if len(current) + len(line) + 1 <= chunk_size:
            current = current + '\n' + line if current else line
        else:
            if current:
                chunks.append(current.strip())
            current = line
    if current.strip():
        chunks.append(current.strip())
    return chunks

url = f'https://www.youtube.com/watch?v={video_id}'
chunks = chunk_text(transcript)

full_metadata = {
    'channel': channel,
    'video_id': video_id,
    'duration': duration,
    'level': 'INTERMEDIATE',
    'application': 'Microsoft Excel',
    'topics': topics,
    'source': 'YouTube Transcript',
    'ingested_date': datetime.now().strftime('%Y-%m-%d'),
    'content_type': 'youtube_tutorial',
    'category': 'Microsoft_Office'
}

inserted = 0
for i, chunk in enumerate(chunks):
    summary = chunk[:200].replace('\n', ' ').strip()
    if len(chunk) > 200:
        summary += '...'

    record = {
        'url': url,
        'chunk_number': i + 1,
        'title': title,
        'summary': summary,
        'content': chunk,
        'metadata': full_metadata
    }

    try:
        supabase.table('knowledge_base').insert(record).execute()
        inserted += 1
        print(f'  Chunk {i+1}/{len(chunks)} inserted')
    except Exception as e:
        print(f'  Error chunk {i+1}: {e}')

print(f'\nTotal: {inserted} chunks inserted to Supabase')
