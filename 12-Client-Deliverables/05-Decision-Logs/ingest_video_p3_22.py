"""
Ingest Playlist 3 video 22 (xlwaqO9knLo) - Highlight Periods in Excel Charts - Focus Readers' Attention!
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

video_id = 'xlwaqO9knLo'
title = "Highlight Periods in Excel Charts - Focus Readers' Attention!"
channel = 'MyOnlineTrainingHub'
duration = '6:36'
topics = ['Chart Highlighting', 'Shaded Periods', 'Secondary Axis', 'Combo Charts', 'Clustered Columns', 'Gap Width', 'Helper Columns', 'Nested Axis', 'Date Formulas', 'MOD Function', 'IF Function', 'NA Error Handling', 'Marker Formatting', 'Data Labels', 'Legend Customization']

transcript = """0:00 shading or highlighting periods in Excel
0:02 charts can help users more quickly
0:04 interpret them and identify patterns in
0:07 this chart I've highlighted every second
0:09 month to give a quick visual indication
0:11 of each period and this allows the user
0:14 to focus on the line instead of having
0:16 to refer back and forth to the
0:17 horizontal axis or you can use this
0:20 technique to focus their attention on a
0:22 specific period like the winter months
0:24 in this chart and we can use this same
0:27 technique to highlight a single date or
0:29 even several points and the good news is
0:32 it's super easy let's take a
0:34 look here I have my chart Source data
0:38 starting in column B are the dates now
0:40 this column isn't actually plotted in
0:42 the chart instead I have two helper
0:45 columns C and D for the month and day
0:47 and they'll form a nested axis the
0:50 formula in column C uses if to identify
0:53 the first date in each month and the
0:56 formula in column D uses if with Mod to
0:58 list every seventh date this avoids the
1:01 axis getting cluttered and makes it
1:03 easier to read a whole Year's worth of
1:05 data now the secret to these techniques
1:08 is to plot another series on the
1:09 secondary axis for highlighting or
1:12 shading and that's what I have here in
1:14 column F in my example the even months
1:17 are shaded and you can see the formula
1:19 returns true if the month number is even
1:22 and when you plot true in a chart it's
1:25 the equivalent of one and you'll see
1:26 that in a moment I'll start by selecting
1:29 the chart data remember I don't want
1:32 column B that contains the dates we're
1:35 just going to insert a line
1:38 chart bring it up here and make it a bit
1:42 bigger now I need to change the chart
1:45 type for the shade month series to a
1:47 clustered column so I'm going to right
1:49 click change chart type down here I want
1:53 combo the temperature values I want as a
1:56 line and the shade month I want as the
1:59 cluster column and we're going to pop
2:01 that on the secondary axis you can see
2:03 in the preview it's already taking
2:06 shape next we need to format these
2:09 columns so I'm going to select one of
2:10 them control one that opens the format
2:13 data series here I want the Gap width to
2:16 be
2:17 zero and we're just going to tone down
2:19 the color to make it something more
2:21 subtle let's go with a pale shade of
2:23 gray next I want to modify the secondary
2:27 axis so that the maximum is is one that
2:30 will just take the column to the top of
2:32 the chart now I've done that I want to
2:34 hide the secondary axis so we're going
2:36 to go into tick marks and set the major
2:39 Type To None and with labels we also
2:42 want
2:44 none lastly I can put some finishing
2:46 touches on like perhaps getting rid of
2:48 the grid lines let's move the legend up
2:52 to the top and we'll get rid of the
2:55 shade month Legend we don't need that
2:58 self-explanatory let's give it the chart
3:01 title and we're good to go so there you
3:04 have a shaded months which may help your
3:06 reader interpret the chart more quickly
3:09 now A variation on this technique is to
3:11 shade period so let's take a look here
3:14 I've simply changed the formula for the
3:16 Shaded area to check if the dates fall
3:18 within our winter period of June to
3:20 August and instead of gray shading I've
3:22 used blue to represent winter otherwise
3:25 everything else is the same in terms of
3:27 the way the chart is built and you can
3:29 obviously modify this technique to suit
3:31 your business needs you might want to
3:33 highlight quarters or there might be a
3:35 specific period in your sales calendar
3:37 that you want to focus
3:39 on an alternative to shading areas is to
3:42 highlight just one date either with a
3:45 vertical line or a marker here in column
3:48 F the formula checks if the temperature
3:50 is equal to the maximum for the year if
3:52 it is the temperature is returned as we
3:55 can see down here in February if not we
3:57 get the na error now I'm I'm using na
4:00 here to hide the line in the chart which
4:03 is required for the second example I'm
4:04 going to show you in a moment so I'm
4:07 just going to select the data and scroll
4:10 to the
4:11 top insert a line chart let's bring it
4:16 up here and we'll make it a bit
4:18 bigger I need to change the chart type
4:22 down here in combo the temperature needs
4:24 to be a line chart and the maximum
4:27 temperature is going to be the cluster
4:28 column here I I'm going to leave them
4:30 both on the primary axxis so I'll click
4:33 okay and you can see the line now for
4:35 the maximum temperature in the chart now
4:38 an alternative is to use a DOT marker
4:41 instead of the line so I'm just going to
4:43 contrl D to duplicate that chart and
4:46 we'll modify it so here I want to right
4:49 click and change the chart type for the
4:51 maximum temperature I want the line
4:53 chart with markers again they both stay
4:56 on the primary axis now click okay you
4:59 can see now the maximum temperature is
5:01 highlighted with the dot now with this
5:04 example it's important that the values
5:07 you don't want plotted in the line are
5:09 returning the na error that will prevent
5:12 the line dipping down to the zero and
5:14 drawing a straight line along the bottom
5:16 of the chart now I just want to select
5:19 that dot and format it because if we
5:23 look at the legend you can see it's
5:25 showing a line with the dot marker and I
5:28 want to just remove that line so I'm
5:30 going to select the series maximum
5:34 temperature in here in the formatting
5:36 which is already open but if it's not
5:38 for you you can control one to open it I
5:40 want to say no line you can see now the
5:43 legend correctly matches the dot marker
5:45 in the chart and with that series
5:48 selected I can also add things like a
5:51 data label just to that series and
5:53 that's going to highlight the maximum
5:56 for the year let's get rid of the grid
5:58 lines and our chart is done can
6:01 obviously add the title and move the LGE
6:04 to the Top If that's where you prefer to
6:06 have it that's typically where I like to
6:07 put my Legend it just takes up a bit
6:09 less space in my
6:13 chart well I hope you found this
6:15 technique useful you can download the
6:17 Excel file for this lesson from the link
6:19 here and if you like this video please
6:21 give it a thumbs up and subscribe to my
6:23 channel for more and why not share it
6:25 with your friends who might also find it
6:27 useful thanks for watching"""

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

filename = f"{datetime.now().strftime('%Y-%m-%d')}_INTERMEDIATE_{video_id}_Highlight_Chart_Periods.txt"
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
