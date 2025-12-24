"""
Ingest Playlist 3 video 11 (jYomlz0e-yE) - TRICKS for Labeling Events in Excel Charts - Focus Attention & Explain Blips
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

video_id = 'jYomlz0e-yE'
title = "TRICKS for Labeling Events in Excel Charts - Focus Attention & Explain Blips"
channel = 'MyOnlineTrainingHub'
duration = '9:47'
topics = ['Event Labeling', 'Chart Annotations', 'Line Charts', 'Column Charts', 'Data Labels', 'IF Formula', 'NA Function', 'Chart Formatting', 'Custom Labels', 'Series Overlap', 'Gap Width', 'Chart Title', 'Legend', 'Value from Cells']

transcript = """0:01 plotting data over time can reveal
0:03 patterns and Trends but often blips in
0:06 the data require further explanation now
0:08 we can help our user by labeling events
0:10 in our charts to highlight key points in
0:12 time that might explain those blips or
0:14 patterns that are revealed in the data
0:17 let's take a look for example this chart
0:19 monitors average running pace per
0:21 kilometer for the month of December now
0:24 December is a busy social month and
0:26 there were a few shall we say occasions
0:29 plus an injury that derailed the
0:31 training routine the timing of which is
0:33 indicated by the blue markers now these
0:36 events help explain the patterns and
0:38 blips in the data without the user
0:40 having to ask further questions so let's
0:42 take a look at how we build it on this
0:45 sheet I've got the data column B and C
0:48 tracks the date and you can see it's
0:50 actually a date I've just formatted just
0:52 to show the day and the average pace so
0:56 this is what the user enters we've also
0:59 got column e here with the events and
1:02 when they enter an event in column e the
1:06 formula in column D returns a value for
1:09 that event and that value just positions
1:12 the marker above all of the columns and
1:15 we use a formula to determine what that
1:18 value should be and when to enter it
1:20 it's an if formula and what it says is
1:24 if the event type cell is not
1:27 blank then find the maximum of the
1:31 average pace and add 5% to
1:35 it if the event field is blank so if
1:39 this logical test is false then return
1:42 the na error now the reason we use the
1:45 na error is because Nas don't get
1:49 plotted in the line chart if we returned
1:52 a blank in here or a zero instead of the
1:54 na error then what we' have is a load of
1:57 blue dots along the horizontal axis down
2:01 here so what we just want are the dots
2:03 where the events occurred and we're just
2:06 using a placeholder value and that
2:08 forces the blue dot to sit up above the
2:12 columns the other thing I've done is
2:15 I've extracted the day letter just with
2:18 a text function that picks up the date
2:22 converts it into text that Returns the
2:24 day and then I've used the left function
2:26 just to return the first letter of that
2:29 date so if I evaluate this I get
2:33 Friday and then left just Returns the F
2:36 so I press Escape so that's my data for
2:39 my chart let's insert the chart now I'm
2:42 going to start by selecting just the
2:44 date and the average paste columns now
2:47 my version of excel doesn't like this
2:49 layout of the data what happens is when
2:52 you format your data in an Excel table
2:54 which this is and you go and insert a
2:56 chart Excel tries to determine what type
2:59 of chart chart you might want based on
3:01 the T the data in the table and you can
3:04 see here it's going to give me a load of
3:06 nonsense this is my chart and you can
3:09 see the range has gone a bit crazy so
3:12 let me fix that up I'm going to right
3:13 click select data and we're just going
3:15 to edit the ranges so first of all we're
3:18 going to pick up the series
3:20 name and the values are these ones
3:24 here now there's lots of ways you could
3:27 fix this but I'm just going about it in
3:29 this way if you know a different way
3:30 that's fine as well now my access labels
3:34 are both of these columns just the data
3:38 not the headers so I'll click okay and
3:41 okay again and our chart's looking
3:45 better the next thing I need to do is
3:47 add in the event data and there's lots
3:50 of ways to do that as well since I've
3:52 got the chart selected I can simply grab
3:55 the pull handles and drag across and now
3:57 I have the event information as well
4:00 so I need to plot these
4:02 events as a line chart so I'm going to
4:05 select any column and right click change
4:08 series chart type now in here I want to
4:12 change the event to a line chart with
4:16 markers and we'll click
4:18 okay so there are my markers for the
4:21 events now I need to do a little bit of
4:22 formatting for this line so with it
4:25 selected I can click control1 and that
4:27 opens my formatting options
4:30 and I'll remove the line so I'm just
4:32 left with the markers now let's make the
4:34 markers a bit more to our liking I'm
4:37 going to go with the built-in Dot and
4:39 I'm going to make it a bit bigger we'll
4:40 make it a size seven and I'll make it a
4:44 blue color this til color will do and I
4:47 need to change the Border as well so
4:49 they're my markers now I need to add
4:53 actually before we move on we'll change
4:54 the color of these columns I'm going to
4:57 go with a gray
5:00 and we'll make it a bit wider we'll do a
5:03 little bit of formatting while we're
5:04 here so one of the things I want to do
5:06 is make sure that the series both
5:08 overlap so the columns are a series and
5:10 so are the dots and I want them to
5:12 overlap so that they're both aligned
5:15 correctly to the days below these days
5:18 down here so you can see there was an
5:19 event on this day and there was also
5:22 some run training done on this day so
5:25 they line up I'm going to reduce my Gap
5:28 width to about 30 30% that just makes my
5:31 columns fatter I want to add some labels
5:33 to those columns but I also want to
5:35 label my line chart or these markers and
5:39 there's a few ways you can do that you
5:40 can rightclick add data labels or if
5:44 you've got Excel 2013 onwards you can go
5:46 in here and add data labels I'm going to
5:48 go to more options cuz I don't want the
5:50 standard
5:51 labels and in the label
5:54 options I have this choice to add a
5:58 label that is a value from a Cale if you
6:01 have Excel 2013 onwards then you have
6:03 this option if you have earlier versions
6:06 of excel then in the materials that you
6:08 can download with this video I'll link
6:11 you to a tutorial that tells you how to
6:13 achieve it in Excel 207 or 2010 but if
6:17 you got Excel 2013 or 2016 or even Excel
6:20 2018 then you can use this value from
6:22 sales I'm going to check that and a
6:25 dialogue box pops up and these are my
6:28 labels in this event type column so
6:30 we're going to grab those and click okay
6:33 now my label has the event type and the
6:36 time I don't want the value and I don't
6:39 want any leader lines and I'm going to
6:41 pop the label above the
6:43 marker so there our labels while I'm
6:47 here I'm just going to click on the grid
6:49 lines and press the delete key and get
6:51 rid of those I'm also going to label my
6:54 columns so I'm careful just to select
6:56 the columns you can see that's what's
6:58 selected based on the data in the table
7:00 here and I'm going to add data labels I
7:04 want to format
7:06 them I want the labels to sit inside the
7:11 end and let's make the font white
7:14 there's a few places you can format the
7:16 font I tend to do it on the Home tab
7:18 it's just a habit now I think we need to
7:21 make our column Gap width smaller so
7:23 let's reduce that down to 10% and see
7:26 how that looks I don't want the columns
7:27 to touch each other I make my chart a
7:29 bit wider there we go so now our times
7:32 are in the columns because the times
7:35 from one column to the next are quite
7:38 close together that information is
7:40 really important and this vertical axis
7:42 isn't going to do it for us so since
7:44 I've labeled The Columns I'm just going
7:45 to delete the vertical axis I don't need
7:48 it it's just adding more noise I've got
7:50 the times in
7:52 here now let's add a title to my chart
7:55 and we'll add a legend and I'll put that
7:57 Legend at the top now I'm just going to
8:00 move the legend to the top right and the
8:03 chart title to the top left and that
8:05 gives me more room for my actual
8:09 chart let's give it a a chart
8:15 name December run training if you wanted
8:19 to you could add some commentary to the
8:21 to the Chart title as well and if we
8:24 look at my original one you can see I've
8:26 said went completely off the rails at
8:29 Christmas so this just draws your
8:31 readers attention to Christmas being one
8:33 of the key anomalies to draw their
8:35 attention to so the key to building a
8:40 chart that has markers or labels events
8:44 is primarily in how you structure your
8:47 Source data we plot the event with its
8:50 own series we've used custom labels and
8:54 we've nested our AIS so that we have the
8:57 day and then the day label
8:59 that gives context to those dates we can
9:02 see where the weekends are and the other
9:04 thing that I've done here is because I'm
9:06 plotting data over time I've made sure
9:09 I've included those dates where no
9:11 running happened because that's part of
9:14 the information even though there was no
9:16 training on that day that's a key piece
9:19 of information so when you're plotting
9:20 data over time it is important in some
9:24 cases to actually include those days
9:26 where there was no
9:28 data
9:29 well I hope you found this useful please
9:31 take a moment to click the thumbs up and
9:33 don't forget there's a link in the
9:34 description where you can download the
9:36 workbook and if you'd like to be
9:37 notified when I publish more videos like
9:39 this please subscribe to my channel
9:41 thanks for
9:45 watching"""

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

filename = f"{datetime.now().strftime('%Y-%m-%d')}_INTERMEDIATE_{video_id}_Event_Labeling_Charts.txt"
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
