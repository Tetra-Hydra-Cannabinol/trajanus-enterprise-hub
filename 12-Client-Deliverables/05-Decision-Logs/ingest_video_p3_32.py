"""
Ingest Playlist 3 video 32 (-uONzlicrnU) - Excel Speedometer Charts - How to build them and why YOU SHOULDN'T!
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

video_id = '-uONzlicrnU'
title = "Excel Speedometer Charts - How to build them and why YOU SHOULDN'T!"
channel = 'MyOnlineTrainingHub'
duration = '10:24'
topics = ['Speedometer Charts', 'Gauge Charts', 'Donut Charts', 'Pie Charts', 'Data Visualization Best Practices', 'Secondary Axis', 'Stacked Column Charts', 'Line Charts', 'Data Labels', 'Qualitative Scale', 'Dashboard Design', 'Cognitive Load', 'Chart Formatting', 'Chart Rotation', 'Marker Formatting']

transcript = """0:00 speedometer charts or gauge charts as
0:02 they're also known have a worse
0:03 reputation in data visualization circles
0:06 than the disdained pie chart in this
0:08 tutorial we're going to learn how to
0:10 build Excel speed oper charts because I
0:12 know you're going to ask me anyway then
0:14 I'll explain why they're bad and what to
0:17 use
0:18 instead Excel speedometer charts
0:20 actually consist of three charts two
0:22 donuts and Pi the color bands represent
0:26 a qualitative scale my qualitative scale
0:30 for this example is generic but they're
0:31 typically aligned to Performance for
0:34 example red is poor orange adequate
0:36 yellow good and green excellent and
0:39 obviously you can modify that scale to
0:41 suit your needs the first donut with the
0:43 colored bands is supported by its own
0:45 table of data so let's take a look at
0:47 that we'll delete this chart and you can
0:50 see it here behind note that the
0:52 qualitative bands add up to 100 and the
0:55 omitted line is for the bottom half of
0:58 the chart which You Don't See and we'll
1:00 cover more on that in a moment so to
1:02 create the chart we simply select the
1:03 data through to the emitted row and then
1:06 on the insert tab we want under Pi a
1:10 donut let's bring it up here closer to
1:13 the data now I need to rotate the chart
1:15 so selecting the donut control1 to open
1:18 the formatting pane let's bring it over
1:20 closer and I need to change the angle of
1:23 the First Slice to 270 that just puts
1:26 the omitted piece on the bottom so that
1:28 the top half represents our speedometer
1:32 okay let's move that across and we'll go
1:33 ahead and insert the next chart and that
1:37 is the donut that contains the scale
1:40 notice that the scale values also add up
1:42 to 100 and that's for the top half so to
1:46 insert this chart we're going to select
1:47 the label right through to row 16 contrl
1:51 C to copy select the outer edge of the
1:54 chart crl + V to paste now you can see
1:57 the scale is on the Outer Edge and my
1:59 qualitative scale is the inner donut now
2:02 I want to change the colors of the outer
2:05 donut so I'm going to go to chart design
2:07 change colors and I want this
2:10 monochromatic palette with the gray
2:12 gradient going from light to dark
2:15 applies it to the whole chart that's
2:17 fine we're going to tidy that up in a
2:19 moment next I want to hide the bottom
2:22 segments of each dut so selecting it
2:25 twice so left clicking twice not a
2:27 double click just two left clicks with
2:30 the first segment I'm going to set it to
2:31 no fill and then repeat for the second
2:34 donut and no fill next I can set the
2:37 colors for my inner segments for my
2:40 qualitative scale so let's go ahead and
2:42 the first one is red and then we have
2:47 orange
2:50 yellow and lastly
2:53 green now if you want to make the dut a
2:55 bit thicker we can go into the series of
2:58 options and change the whole size
3:00 perhaps to
3:02 50% and while we're here let's turn off
3:04 the legend cuz it's
3:07 redundant okay we're ready to insert the
3:09 needle chart and that's a pie chart
3:12 that's supported by this data here
3:15 notice it's total adds up to 200 which
3:18 is actually the total values of the
3:20 whole Donuts the actual is the position
3:23 of my needle the one is the thickness of
3:26 my needle and the balance creates the
3:29 complete Pi you can see it's just a
3:31 formula that subtracts the total less
3:34 the actual and the needle thickness so
3:37 to insert my pie chart I'm going to
3:39 select the table and then copy it
3:42 selecting the chart contrl V to paste it
3:45 inserts it as another donut so with that
3:48 selected I'm going to right click and
3:50 change the series chart
3:52 type and it's the last one here we're
3:55 going to make it a pi on the secondary
3:57 axis I click okay and let's select the
4:00 pi and we also need to rotate it so it
4:03 needs to be 270 for the first slice and
4:07 then we'll go back to formatting and
4:09 we're going to set the border to no line
4:12 and then the big segments we want to
4:14 hide them so let's select them one at a
4:16 time no fill and no fill and then the
4:20 tiny segment if it's difficult to select
4:22 you can make the needle thickness bigger
4:24 so let's make it five then you can
4:26 select that segment and go ahead and
4:29 form mat it in black and then we can go
4:32 back and change the value to one next I
4:35 want to apply labels to my outer donut
4:38 so selecting that and it might be
4:40 difficult to select because the p is
4:41 sitting on top of it so you can use
4:43 control and your arrow keys to select
4:46 the right chart and then we're going to
4:49 add data labels but I want to go into
4:51 more options because I don't want values
4:54 of 10 I want this label scale here so
4:58 I'm going to deselect lead lines and
5:00 value and choose value from cells and
5:03 then in the dialogue here I can select
5:05 the cells right through to the zero
5:07 click okay now it places the labels on
5:09 top of the donut I actually need them
5:11 and they're correct to be at the gaps
5:14 between each
5:15 segment so you have to manually left
5:18 click and drag them unfortunately one by
5:20 one so let me fast forward while I do
5:22 that and lastly the zero needs to go up
5:27 here now my chart still has a big border
5:30 around it which shows the size of the
5:32 actual dut it is a space hog so
5:34 selecting the outer edge I'm going to go
5:36 to formatting and set the outline to no
5:39 outline and the shape fill to no fill
5:42 that's just going to allow you to
5:44 position the donut closer to other
5:46 charts and data and for bonus points we
5:49 can insert a text box that's going to
5:52 contain the value of the needle just to
5:55 help our users interpret the data even
5:57 more quickly so selecting the outer edge
5:59 of the text box in the formula bar enter
6:02 equals and then select the value of the
6:05 actual press enter and there it is let's
6:09 Center that in the text box and we'll
6:12 make it a bit bigger we can make it bold
6:15 you might also like to add some text in
6:17 there that tells us what this data
6:19 represents or you could give it a header
6:22 let's also hide the fill and outline
6:25 from that and we'll just move it down a
6:27 little bit okay
6:30 and there you have a speedometer or a
6:32 gauge chart while speedometer charts
6:35 require a load of fiddling about to
6:37 create the main issue data visualization
6:39 experts have with them is that they take
6:41 up a huge amount of space relative to
6:43 the information they convey taking the
6:46 chart in this example it's reporting on
6:48 a single value it places that metric in
6:51 the context of qualitative scale which
6:53 gives it perspective and it's visually
6:55 easy to interpret so that's good however
6:58 when you're using using these charts in
7:00 a dashboard that's limited for space
7:02 they become expensive plus all the extra
7:05 embellishments like color access labels
7:07 Etc add to the cognitive load we can
7:10 simplify this chart and still convey the
7:12 same information in less space and
7:15 reduce cognitive load with simple column
7:17 charts and a marker and unlike
7:19 speedometer charts column charts require
7:22 very little work and data to create so
7:25 let's look at how we create this one all
7:27 we need to do is select the table
7:30 insert column chart this one here
7:33 stacked column now it doesn't look like
7:35 a stacked column chart at the moment
7:37 that's fine let's bring it up closer I'm
7:39 going to right click and select the data
7:41 and all I need to do is switch row and
7:43 column and now we have our stacked
7:45 column chart the top segment is our
7:48 actual and that needs to be a line chart
7:51 with marker so we're going to right
7:52 click change series chart type it's the
7:56 last one here and we want line with
7:59 markers click okay now it's looking
8:03 better let's delete the horizontal axis
8:06 label and we'll resize it let's go in
8:10 here control1 to format the axis and
8:14 here we just want the vertical axis
8:16 maximum to be 100 and then I'll select
8:18 the column and in here let's change the
8:21 Gap width to be zero now we get a better
8:24 idea of how small it can get all right
8:27 let's go ahead and set the fill color
8:29 for these qualitate bands so this one's
8:31 red orange this one's yellow and the top
8:35 one is
8:37 green and now for the marker this is a
8:40 line chart but because it only has one
8:42 point there's no line to draw so we can
8:45 set the marker to behave a bit more like
8:48 a line by selecting this type here and
8:51 making it wider until it spans the width
8:54 of our column let's fix the color of the
8:56 marker so we'll set it to solid fill and
8:58 I'll make make it
9:00 black and I'll just take the Border off
9:03 it right let's see how that looks it
9:05 could probably be slightly wider so
9:07 let's go and fix
9:09 that make it
9:11 16 select the chart border and we'll get
9:14 rid of
9:16 that and lastly let's add a data label
9:20 for the marker it pops it to the right
9:23 so let's just reposition it make it
9:26 bigger and drag it across
9:29 I can also make it bold font and easier
9:33 to read and that's it job done only one
9:36 table of data one very small chart takes
9:39 up far less space there's less noise
9:42 it's quicker to interpret you could also
9:44 make it look more professional by
9:46 turning down the colors to bring them in
9:48 line with your dashboards color theme
9:50 don't feel that you need to stick with
9:51 the generic traffic light
9:54 approach next time your boss asks for a
9:56 gauge chart or speedometer chart show
9:58 your data visualization expertise and
10:00 try to convince them otherwise I hope
10:03 you found this tutorial useful you can
10:05 download the Excel file for the lesson
10:07 from the link here if you like this
10:08 video please give it a thumbs up and
10:11 subscribe to our channel for more and
10:13 why not share it with your friends who
10:14 might also find a useful thanks for
10:17 [Music]
10:23 watching"""

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

filename = f"{datetime.now().strftime('%Y-%m-%d')}_INTERMEDIATE_{video_id}_Speedometer_Charts.txt"
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
