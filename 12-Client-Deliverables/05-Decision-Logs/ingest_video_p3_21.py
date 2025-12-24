"""
Ingest Playlist 3 video 21 (SKzEyK7bvco) - Stacked Bar Excel Waffle Charts - Quick and Easy!
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

video_id = 'SKzEyK7bvco'
title = "Stacked Bar Excel Waffle Charts - Quick and Easy!"
channel = 'MyOnlineTrainingHub'
duration = '5:31'
topics = ['Stacked Bar Waffle Charts', 'Error Bars', 'XY Scatter Charts', 'Axis Configuration', 'Gap Width', 'Grid Lines', 'Precise Proportions', 'Chart Formatting', 'Secondary Axis', 'Legend Formatting', 'Plot Area Fill', 'Chart Types']

transcript = """0:00 last week we looked at how to build
0:02 Excel waffle charts using conditional
0:03 formatting and this week I'm going to
0:05 show you how to build them using a
0:07 stacked bar chart stacked bar waffle
0:09 charts enable you to show precise
0:12 proportions for example fractions of a
0:14 segment as opposed to conditional
0:16 formatting segments which are rounded to
0:18 a whole percentage point now you might
0:20 also find this approach easier than
0:22 using the conditional formatting
0:24 technique let's take a look here's the
0:27 data for my Waffle chart at the top I've
0:30 got a list of my series and their
0:32 proportions now you notice they don't
0:34 add up to 100% in this example but they
0:37 can do in yours then in column D I've
0:40 got the cumulative total of values and
0:43 here is my chart data now the First
0:46 Column just contains the values for the
0:48 error bars it's simply the numbers 1
0:51 through 10 and typically error bars are
0:53 used to show margins of error and
0:55 standard deviations but in this chart
0:57 we're going to use them to create the
0:59 waffle line Lines by hard keying a
1:01 specific value for the errors which
1:03 you'll see shortly in the next three
1:05 columns I have the series now each
1:08 column here has a slightly different Max
1:10 and Min formula that calculates the
1:12 number of segments on each row of the
1:14 chart that will be filled I'm not going
1:17 to explain them here because you can
1:18 download the file and see for yourself
1:20 however if you want to add more series
1:23 you can copy the formula in column e and
1:26 make sure you just modify it to follow
1:28 the pattern so you know is here that
1:31 it's 10 - C10 and then it's 10 - C10 -
1:35 d10 so you'll simply have to add minus
1:38 E10 to that formula that said I don't
1:41 recommend having more than three
1:43 segments okay to insert the chart select
1:46 the data insert and here we're going to
1:49 use the Stacked 2D bar chart let me
1:52 bring it over here into view the first
1:55 thing we want to do is rightclick this
1:57 series which is the error bar series and
2:00 change the series chart type what we
2:03 want here is the XY scatter with
2:06 straight lines notice it automatically
2:09 puts it on the secondary axis now click
2:12 okay and now we have a line for the
2:14 error bar series next I want to format
2:17 These Bars the Stacked bars so that
2:20 there's less Gap so I'm going to select
2:22 one and then control one to open the
2:24 formatting pane let me bring it over
2:26 here into view and we'll actually move
2:29 everything you can see it in a smaller
2:32 area so with one of the bars selected in
2:35 the series options I want to change the
2:37 Gap width to
2:39 0% next I want to modify the secondary
2:41 vertical axis so that the maximum and
2:44 minimum are fixed so you want a minimum
2:46 of zero and a maximum of 10 let's do the
2:50 same for the horizontal axis and
2:52 although it's defaulting to zero we want
2:54 to fix it so that it doesn't alter when
2:56 we add the error bars next I'm going to
2:59 to select my arrow bar series and in the
3:02 plus menu we're going to go to Arrow
3:05 bars more
3:07 options and in here I want the direction
3:09 both no cap and the fixed value is going
3:12 to be 10 and you can see they now
3:15 continue all the way up to the top of
3:17 the chart now that's modified my
3:19 vertical Arrow bar and you can see that
3:21 that's what's selected here I need to do
3:23 the same for the X Arrow bar so you can
3:26 select it from the list and now you can
3:28 see it's selected the horizontal errow
3:30 bar so we want both directions no cap
3:33 and a fixed value of 10 now that we've
3:36 added our errow bars let's format them
3:38 so that they have a solid white
3:40 line and then repeat that for the
3:43 vertical ones just select them solid
3:45 line and white now that we've done that
3:48 we don't need this line visible in the
3:50 chart so select it and on the formatting
3:53 we simply want no
3:55 line next I'm going to hide the axes and
3:59 the chart title in this case I don't
4:01 need a chart title but you can leave it
4:02 on if you want one and let's make the
4:06 chart more Square so that my Waffle
4:08 segments appear
4:10 Square now you can see the Arab bar
4:13 series is still showing in the legend so
4:15 let me select that and press delete now
4:18 you can see there's still a vertical
4:19 line on the left hand side of the chart
4:22 this is the major grid line and it can
4:23 be tricky to select it so what I tend to
4:26 do is use control and then my arrow keys
4:29 to toggle through the different chart
4:31 elements you can see now major grid line
4:34 is selected and here I want to format it
4:37 with no line the last thing we want to
4:40 do is color the rest of the waffle
4:41 segments so selecting the plot area I
4:45 can select a fill color in a pale shade
4:48 of gray it's defaulted to the one I used
4:51 earlier and there you have the waffle
4:53 chart using a stacked bar chart and
4:56 errow bars for the vertical and
4:57 horizontal white lines that give it that
4:59 that waffle
5:01 effect I hope you found this technique
5:03 useful a special thanks to Nick hman
5:06 associate professor at University
5:08 Wisconsin Madison who shared his
5:10 template for Waffle charts you can
5:12 download the Excel file for this lesson
5:14 from the link here and if you like this
5:16 video please give it a thumbs up and
5:18 subscribe to my channel for more and why
5:21 not share it with your friends who might
5:22 also find it useful thanks for
5:26 [Music]
5:28 watching"""

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

filename = f"{datetime.now().strftime('%Y-%m-%d')}_INTERMEDIATE_{video_id}_Stacked_Bar_Waffle_Charts.txt"
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
