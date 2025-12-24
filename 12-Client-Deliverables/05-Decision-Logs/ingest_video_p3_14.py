"""
Ingest Playlist 3 video 14 (i-nOqUTzEX0) - Custom Excel Chart Label Positions | GHOST Trick
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

video_id = 'i-nOqUTzEX0'
title = "Custom Excel Chart Label Positions | GHOST Trick"
channel = 'MyOnlineTrainingHub'
duration = '2:51'
topics = ['Ghost Series', 'Custom Labels', 'Label Positioning', 'Column Charts', 'Data Labels', 'No Fill', 'Chart Formatting', 'Legend Editing', 'Color Coding', 'Axis Scale']

transcript = """0:00 when you plot multiple Series in a chart
0:02 the labels can end up overlapping other
0:05 data which is less than ideal now we can
0:08 avoid this with custom chart label
0:10 positions assigned to a ghost series it
0:12 sounds scary but it's dead easy okay
0:15 well that was two puns in one sentence
0:18 anyhow let's take a
0:20 look first I need to delete these labels
0:23 because they're assigned to the actual
0:25 Series so just selecting them and press
0:27 the delete key now all I need to do is
0:30 is add a column to my table for the
0:32 labels and we want to find the maximum
0:36 of the Target and the actual now because
0:39 my chart is linked to this table it's
0:42 automatically included this new series
0:44 so that saves me a step I'm going to
0:47 select this new series and add labels
0:51 but I want to click on the arrow and go
0:53 down to more options now I want to
0:56 deselect show leader lines and value and
0:59 and I want to select a value from CES
1:01 now when I check this it opens the
1:04 dialogue box asking me to select the
1:06 data range so I want the labels for the
1:08 actual Series so I'm going to select the
1:11 actual in the table and click okay so
1:14 now we have the labels for the actual
1:18 assigned to this new series called
1:20 labels all I need to do now is make this
1:22 new series a ghost so I'm going to
1:24 select the columns and on the paint
1:27 bucket in the format data series pane
1:29 I'm going to choose no fill and no line
1:32 for the border now we have a little bit
1:34 more tidying up to do I've now got an
1:37 extra item in my legend for the labels
1:40 so I'm going to left click once and left
1:42 click again to select the labels item
1:45 and press delete we don't need that now
1:48 my readers might be confused about which
1:50 series these labels relate to so I'm
1:53 going to color code them to match the
1:55 column color for the actual so up on the
1:58 Home tab this is the color for my column
2:01 but it's a bit pale when it's in a font
2:03 which is quite fine so I'm going to
2:05 select this color up here it's a little
2:07 bit darker but you can't really tell
2:09 looking at it on the face of the chart
2:12 and it's just going to make it that bit
2:13 easier for my reader so there you have
2:16 your own custom chart label positions
2:18 assigned to a ghost series now you can
2:20 also use ghost series to fix the axis
2:23 height which is handy when you have
2:25 multiple charts that you want plotted
2:27 based on the same vertical axis scale
2:30 okay take a moment to download the EXL
2:33 file for this lesson from the link here
2:34 or in the video description I hope you
2:37 can make use of this technique if you
2:39 like this video please give it a thumbs
2:41 up and subscribe to my channel for more
2:43 and why not share it with your friends
2:44 who might also find it useful thanks for
2:50 watching"""

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

filename = f"{datetime.now().strftime('%Y-%m-%d')}_INTERMEDIATE_{video_id}_Ghost_Series_Labels.txt"
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
