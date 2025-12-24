"""
Ingest Playlist 3 video 29 (_xh8YFToGGw) - Excel Dot Map Charts - Yes, this is Excel!
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

video_id = '_xh8YFToGGw'
title = "Excel Dot Map Charts - Yes, this is Excel!"
channel = 'MyOnlineTrainingHub'
duration = '14:58'
topics = ['Dot Map Charts', 'XY Coordinates', 'Scatter Charts', 'Geographic Visualization', 'PNG Images', 'Excel Tables', 'Pivot Tables', 'Chart Formatting', 'Shape Formatting', 'XLOOKUP', 'INDEX and MATCH', 'FILTER Function', 'Slicers', 'Custom Slicer Styles', 'Interactive Charts', 'Data Labels', 'Selection Pane', 'Format Painter', 'MAX Function', 'Gradient Fill']

transcript = """0:00 one of the things that makes XL stand
0:02 apart from other reporting tools is its
0:04 immense flexibility with some tinkering
0:07 you can make charts and Graphics that
0:09 don't look anything like excel in this
0:11 post I'm going to take you through the
0:13 steps to create this dot map chart now
0:16 there's no built-in map chart but don't
0:18 worry it's easier than it might appear
0:21 this data is going to form the basis of
0:23 what I want to visualize in my DOT map
0:25 it's sales data Group by segment and
0:27 market and the markets relate to regions
0:29 in Africa Asia Pacific Europe Latin
0:33 America and USA and Canada the first
0:35 thing I want to do is contrl T which is
0:37 a keyboard shortcut to format the data
0:39 in an Excel table and you'll see why
0:41 this is important later in the video if
0:44 we look at the table design tab we can
0:45 see the table name is table two next I
0:48 want to summarize it with a pivot table
0:50 and I've already got a worksheet set up
0:53 where I'm going to place a pivot table
0:55 so I want it there and in the field list
0:58 I just want the sales and and it
1:00 summarized by
1:01 market let's right click and apply some
1:04 number
1:05 formatting this is going to feed through
1:07 to my
1:08 chart now Excel can't visualize this
1:11 data in its built-in map chart it
1:14 doesn't recognize those regions so I'm
1:17 going to make my own map chart and I
1:19 found an image of a do map on PNG wi.com
1:22 I'm just going to insert it it's saved
1:24 on my PC there it is
1:27 there if you want to grab a copy of this
1:29 image you can download the file that's
1:31 linked to in the video description now
1:34 I'm going to set my Dimensions to 11.48
1:37 high because I know this works with my
1:39 coordinates that I've already figured
1:41 out but you can size it to whatever
1:42 suits you just be sure to choose the
1:44 size before you move on and don't
1:46 distort it too much next I want to use
1:49 the color tool and I'm going to recolor
1:51 it to just this gray accent color three
1:55 light the black dots are just a bit too
1:57 harsh now I need to Overlay the dot mat
1:59 app chart image with a scatter chart and
2:02 for that I need some XY coordinates so
2:04 I've got a little table here ready to go
2:07 it doesn't matter what you put in here
2:08 to start with it's just so that you have
2:11 something to insert the chart
2:13 on so any numbers between one and 100
2:17 will
2:18 do so select the data and then insert
2:22 and we want this scatter chart
2:25 here so you can see I've got three dots
2:27 based on these coordinates now I don't
2:30 need the chart title so let's turn that
2:33 off and I need to format the axis so
2:37 with it selected control1 and the
2:40 formatting pane opens and in here I want
2:42 to set the maximum to 100 and the major
2:46 unit two and then I want to repeat that
2:50 for the horizontal axis so I want 100
2:53 and the major unit is two and that just
2:56 gives me a nice grid that I can use to
2:59 to figure out what the coordinates are
3:01 of each of the dots so we need to resize
3:04 this chart to sit over top of the dot
3:06 map and to allow us to see through we're
3:09 going to format the chart with no fill
3:13 now in order to line it up with the dot
3:14 map I need an outline to that image it
3:17 doesn't have one so I'm just going to
3:18 give it a temporary outline doesn't
3:20 matter what color we'll just give it a
3:21 blue outline so now I can see my DOT map
3:25 I can left click and drag my scatter
3:28 chart so that the plot area matches the
3:32 blue line of the chart behind just line
3:35 it up by I okay that will do now I can
3:39 use the coordinates on the scatter chart
3:41 to match up the dots in the chart I'm
3:43 going to delete the data I have in here
3:46 and we'll add in some new values so
3:49 starting with Asia Pacific I want a DOT
3:51 at 88.5 and one at
3:53 51.3 now the AIS has readjusted its
3:57 starting point so it's currently 86 so
3:59 the dot isn't quite in the right
4:01 position let's go and change that so you
4:04 can see the effect we'll make the
4:06 minimum
4:08 zero so now you can see my DOT is over
4:11 here in as Pacific and it lines up with
4:14 the dot in the dot map image below the
4:16 scatter chart all you need to do now is
4:19 repeat this process until you have
4:20 enough dots if you can't see it clearly
4:23 enough you can zoom in to make it easier
4:25 the number of coordinates you enter here
4:27 will be dictated by the number of dots
4:28 you want for each
4:30 now I've got between 6 and 10 dots
4:32 depending on the size of the region I'm
4:34 going to paste in the coordinates I
4:35 prepared earlier so you don't need to
4:37 sit through watching me figure them all
4:38 out but it probably took me half an hour
4:40 or so to calculate them all so it's not
4:42 too
4:43 laborious so you can see I have multiple
4:45 coordinates for each region and I've
4:47 labeled them with the region names and
4:49 you'll see why that's important in a
4:50 moment the other thing I need to do is
4:53 resize the ranges so that it includes
4:55 all of the dots let's just zoom back out
4:58 and I'll left click and drag to include
5:02 all of the
5:03 regions now I can turn off the grid
5:05 lines because they're no longer required
5:07 so let's do that and I'm going to edit
5:10 my DOT format just select one of them
5:13 control one to open the formatting Pane
5:16 and under the paint bucket and marker
5:19 let's just make this a little bigger can
5:22 change the fill color so let's make it a
5:24 really bright blue and the same for the
5:27 Border bright blue and I'm just going to
5:29 increase the width of the border to
5:31 1.25 I'm going to add a shape to the
5:34 background so let's insert a shape and I
5:37 want this one here with the rounded
5:39 corners and we're just going to size it
5:43 same as the
5:45 map
5:46 behind let's change the radius on
5:49 that and I'm going to make it dark shade
5:53 of
5:55 gray and we'll get rid of the outline we
5:57 don't need that and we'll send it to the
6:00 back so it sits behind the chart now in
6:02 order to hide the axis labels you could
6:05 turn the axis labels off but if you do
6:07 that the chart will resize and then all
6:09 your dots will be in the wrong place so
6:11 I find it easier just to color them the
6:13 same color as the background and that's
6:15 that color and let's repeat it for the
6:18 horizontal axis so now we can't see the
6:20 axis we can still see the chart border
6:23 we don't need that anymore so selecting
6:26 one of the images on the formatting pane
6:28 I'm going to open the selection pain
6:30 let's drag it out and that's just going
6:32 to allow me to select the map cuz it's
6:34 currently sandwiched between the Round
6:36 the Corner rectangle in the background
6:39 and the scatter chart on the top so
6:41 let's go to the picture format and we no
6:43 longer need the border on that I also
6:45 don't need a border on my chart so let's
6:48 do that we'll get rid of that outline
6:51 and I don't need these vertical and
6:53 horizontal axis lines so let's go and
6:56 get rid of those no line for that one
6:59 and no line for that one okay it's
7:01 starting to come together now I want
7:04 some shapes to store the values from my
7:06 pivot table so I'll insert another shape
7:10 and again I'm going to use these rounded
7:11 corner shapes I'm just going to draw
7:13 them
7:15 in can set the fill colors for example I
7:18 could use this gradient fill let's set
7:21 it going left to right so dark to light
7:25 and perhaps we'll use a shade similar to
7:28 the background
7:30 [Music]
7:37 actually this one's redundant we'll get
7:39 rid of that and we'll just make it like
7:41 that this I might make a shade of gray
7:43 as well just so it's not so harsh with
7:45 the white and we'll get rid of the
7:49 border so that it's no line okay so
7:53 that's the placeholder for my value
7:55 labels with it's selected I'm just going
7:57 to put in equals and then this is USA
8:01 and Canada so it's this value here now a
8:04 shape cannot take a formula and that's
8:06 what's returned when you click on a cell
8:08 in a pivot table so what I actually want
8:10 is just the cell reference so USA and
8:12 Canada is in cell
8:15 B8 press enter we can make it a bit
8:18 bigger and format the font white so that
8:21 it's easy to read and Center it in the
8:24 label we also need a label to tell us
8:27 what region this is so let's
8:30 insert a text box
8:33 underneath and we'll just type in the
8:37 label and let's Center that now this
8:40 text box I don't want any formatting so
8:42 I don't want any fill and no outline
8:46 let's make the font white so it's easy
8:48 to see and we'll just line these two up
8:51 so shape format line
8:54 Center so that's our first label and we
8:57 need to just replicate it for the other
8:59 regions so with them selected holding
9:01 down shift to select them both I'm just
9:03 going to hold down control and left
9:05 click and drag so that will be Latin
9:09 America this will be Africa we need one
9:12 for
9:13 Europe and Asia Pacific so all we need
9:17 to do is edit the formula here so it's
9:20 currently picking up cell B8 but this is
9:24 Latin America so it's B7 we need to
9:26 change the label and rinson heat for the
9:30 other
9:32 [Music]
9:41 shapes now you notice that the
9:43 formatting has been lost when I edited
9:45 those formulas so just selecting one of
9:46 them I'm going to double click the
9:48 format painter and then paint the
9:50 formatting onto the other shapes so
9:53 there's my DOT map chart but wouldn't it
9:55 be nice to highlight the region with the
9:57 largest values to draw a attention and
9:59 make it quicker to interpret now I can
10:02 use the max function to find the highest
10:03 value select just select all the objects
10:05 CR a to select them all I'm going to
10:08 move them across so I've got some
10:10 space and I'll unhide these columns
10:13 where I've got my placeholders for the
10:15 maximum region and their coordinates so
10:19 finding the maximum of the sails and
10:23 then I need to find which region relates
10:25 to that max value so I'm looking up the
10:27 maximum in the sales and returning the
10:31 market if you don't have xook up you can
10:34 use index and match so now I know what
10:36 the maximum is and what region that
10:38 relates to I need to find all the XY
10:41 coordinates for that region and in XL
10:44 2021 or 365 or later we have the filter
10:48 function so I can filter this array so I
10:51 want both the X and Y values to
10:54 include where the region equals the
10:58 region return by xook up close
11:01 parentheses and filter spills now if you
11:04 don't have the filter function you'll
11:05 find an alternate array formula solution
11:08 in the file that's available to download
11:09 in the video description so now I have
11:12 these coordinates I can use them to add
11:14 another series to my scatter chart so
11:17 with the chart selected right click
11:19 select data and then I'm going to add a
11:22 series this series is just going to be
11:25 my Max series The X values are here and
11:29 the Y values are here now if you have
11:32 some regions that have more XY
11:35 coordinates than others then just make
11:37 sure you select more cells to allow for
11:39 them click okay and while we're here
11:42 let's just edit this one so this one's
11:45 series name isn't y it's actually all
11:47 regions not that it matters too much we
11:49 don't see it anywhere but just for
11:52 completeness we'll name them
11:54 appropriately I'll click okay and you
11:57 can see I've now got Orange dots in Asia
12:00 Pacific so let's go ahead and select
12:03 those dots they're sitting on top of the
12:05 blue dots you can see the blue dot
12:06 behind and that's because the orange dot
12:09 is smaller so let's first of all change
12:11 the color I'm going to go with this
12:13 bright pink and it doesn't matter what
12:16 color you choose just make sure it's
12:17 something that stands out and
12:19 contrasts let's make the outline bigger
12:23 so that it covers the blue dot so now we
12:25 have the maximum highlighted let's make
12:28 it interact acve and we'll add a slicer
12:31 for the market so with the pivot table
12:33 selected on the analyze tab I'm going to
12:36 insert a slicer and I want it for the
12:39 segment and click okay so we have three
12:42 segments as I choose a segment in the
12:45 slicer it's going to filter the values
12:47 in the pivot table which feed through to
12:49 the labels in my DOT chart
12:52 and depending on the segment I choose
12:54 the maximum could be different so here
12:57 for corporate the maximum segment is
12:59 Europe for home office it's USA and
13:02 Canada and for Consumer it's Asia
13:04 Pacific so now we have ourselves a nice
13:07 interactive dot map chart the icing on
13:10 the cake is to make the slicer match the
13:13 background and sit it on the chart so
13:16 I'm going to right click and go into
13:18 slicer settings and here I'm going to
13:21 turn off the
13:23 header we're going to give it three
13:25 columns and let's make it a bit wider so
13:29 they have space and I'm going to color
13:32 it the same as my background so let's
13:35 pop it on the chart now I've created a
13:37 custom style for my slicer so it matches
13:39 my chart and I'll put a link in the
13:41 video description to a video that covers
13:43 custom slicer Styles so I'll select this
13:45 style here which I created earlier and I
13:48 can make the buttons just a little
13:50 smaller and then they look like sheet
13:52 tabs so as I click on them it updates
13:56 and it looks like it belongs as part of
13:58 the the chart now because I stored The
14:01 Source data in an Excel table if I want
14:04 to update this chart all I need to do is
14:07 grab my new data which I happen to have
14:09 here some data for December
14:11 2022 and go back to my table that's
14:14 feeding my chart and on the very next
14:17 row crl + V to paste in my new data you
14:20 can see the table has grown to
14:21 incorporate that new data and then if I
14:24 go back to my chart sheet and go to the
14:27 data Tab and refresh all
14:29 if you keep your eye on the chart you'll
14:30 see the value labels update so there we
14:33 go I've updated my chart with one click
14:37 I hope you found this tutorial useful
14:38 you can download the Excel file for this
14:40 lesson from the link here and if you
14:42 like this video please give it a thumbs
14:44 up and subscribe to our channel for more
14:47 and why not share it with your friends
14:48 who might also find it useful thanks for
14:52 [Music]
14:57 watching"""

# Save transcript
archive_dir = r'G:\My Drive\00 - Trajanus USA\00-Command-Center\Knowledge_Archive\Transcripts\Microsoft_Office'
os.makedirs(archive_dir, exist_ok=True)

header = f"""Title: {title}
Channel: {channel}
Video ID: {video_id}
URL: https://www.youtube.com/watch?v={video_id}
Duration: {duration}
Level: ADVANCED
Application: Microsoft Excel
Topics: {', '.join(topics)}
Ingested: {datetime.now().strftime('%Y-%m-%d')}
Source: Playwright Browser Extraction
{'='*78}

"""

filename = f"{datetime.now().strftime('%Y-%m-%d')}_ADVANCED_{video_id}_Dot_Map_Charts.txt"
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
    'level': 'ADVANCED',
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
