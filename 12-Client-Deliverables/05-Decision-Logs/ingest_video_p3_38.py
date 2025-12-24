"""
Ingest Playlist 3 video 38 (MYi966aU3fY) - Impress Your Boss with this Excel Actual v Target Chart Technique - Quick and Easy!
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

video_id = 'MYi966aU3fY'
title = "Impress Your Boss with this Excel Actual v Target Chart Technique - Quick and Easy!"
channel = 'MyOnlineTrainingHub'
duration = '3:16'
topics = ['Actual vs Target Charts', 'Thermometer Charts', 'Series Overlap', 'Column Charts', 'Combo Charts', 'Line Charts with Markers', 'Chart Formatting', 'Series Selection', 'Data Visualization', 'Format Data Series', 'Marker Formatting', 'Stretch Target']

transcript = """0:00 visualizing categorical actuals versus
0:03 Target data is often done in a column
0:04 chart but personally I find these slow
0:07 to interpret not to mention sometimes
0:09 you might want to also include a stretch
0:11 Target or a forecast and by then it's
0:13 just too tedious to read let's look at
0:16 some ways we can enhance the boring old
0:18 column chart and make it something
0:19 that's quick and easy to read you know
0:21 the way charts should
0:23 be let's start by transforming this two
0:26 series column chart into something more
0:28 like a thermometer chart I'm going to
0:30 duplicate this chart I've just selected
0:32 it and then contrl D to duplicate that
0:34 way we can compare the two charts side
0:36 by side first I want to select the
0:39 target series and then I'm going to
0:41 control one to open the format data
0:43 series pane the first thing I want to do
0:46 is set the series overlap to 100% And
0:49 then in the Paint Bucket tab I'm going
0:51 to set the fill to no fill and I want
0:55 the border to be a dark blue and let's
0:58 increase the width to 1 and A2 now
1:01 immediately we can see which managers
1:03 are above or below Target I think you'll
1:06 agree it's quicker and easier to
1:07 interpret than the regular column chart
1:09 on the
1:11 left but what happens if you have three
1:14 series like this chart with the actual
1:16 Target and stretch Target again I'll
1:19 duplicate the chart so we can compare
1:21 them side by side first I want to select
1:24 the target series and control1 to open
1:27 the format data series pane I'm going to
1:29 set the overlap to 100% And then let's
1:33 format it with no fill and we'll set the
1:36 border the same as the previous
1:39 one and I'll just select the actual
1:41 series now if you're having trouble
1:43 selecting series you can always go up to
1:45 the format Tab and then in the drop down
1:47 here you can select the series that you
1:49 want so I want to format the actual
1:51 series just with a lighter shade of blue
1:55 and we'll just to solid fill just to
1:58 help with the contrast next I want to
2:00 make the stretch series into a dash line
2:03 so I first need to select it let's use
2:06 this technique up here so we can be sure
2:08 we've got the right series and I want to
2:10 change the chart type so up in the
2:12 design tab we're going to change chart
2:14 type and in here we want the stretch
2:16 series to be the line with
2:19 markers and I'll click okay now all I
2:22 need to do is format the line so that
2:25 there's no line and then let's format
2:28 the marker in marker option we want the
2:30 built-in dashed line I'm going to
2:33 increase the size to 14 and then let's
2:37 set the fill to a darker shade so it
2:39 stands out I'm going to set it to the
2:41 same shade as the target let's do the
2:44 same for the border for the marker now
2:46 you could set the marker shade to a
2:49 different color if you prefer but since
2:51 they're both targets it makes sense to
2:53 leave them as the same color and let the
2:55 marker itself differentiate the series
2:58 so there's our new sh again we can more
3:01 easily compare the three series at a
3:04 glance I hope you can make use of this
3:06 technique if you like this video please
3:08 give it a thumbs up and subscribe to my
3:10 channel for more thanks for
3:15 watching"""

# Save transcript
archive_dir = r'G:\My Drive\00 - Trajanus USA\00-Command-Center\Knowledge_Archive\Transcripts\Microsoft_Office'
os.makedirs(archive_dir, exist_ok=True)

header = f"""Title: {title}
Channel: {channel}
Video ID: {video_id}
URL: https://www.youtube.com/watch?v={video_id}
Duration: {duration}
Level: BEGINNER
Application: Microsoft Excel
Topics: {', '.join(topics)}
Ingested: {datetime.now().strftime('%Y-%m-%d')}
Source: Playwright Browser Extraction
{'='*78}

"""

filename = f"{datetime.now().strftime('%Y-%m-%d')}_BEGINNER_{video_id}_Actual_vs_Target_Charts.txt"
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
    'level': 'BEGINNER',
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
