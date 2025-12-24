"""
Ingest Playlist 3 video 2 (46CGcyP4dbo) - Pro Excel Chart Tips for Rapid Report Creation!
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

video_id = '46CGcyP4dbo'
title = "Pro Excel Chart Tips for Rapid Report Creation!"
channel = 'MyOnlineTrainingHub'
duration = '11:52'
topics = ['Chart Formatting', 'Copy Charts', 'Paste Special Formats', 'Chart Properties', 'Select Objects', 'Selection Pane', 'Chart Alignment', 'Distribute Charts', 'Alt Key Snapping', 'Chart Templates', 'Pivot Charts', 'Color Themes', 'Dashboard Building']

transcript = """0:00 in this video I'm going to share some of
0:02 my favorite chart formatting tips to
0:04 help you build reports and dashboards
0:07 super fast at the end of the video let
0:09 me know in the comments which was your
0:11 favorite tip or if you have your own
0:13 favorite tip I'd love you to share
0:18 it when you're building a report or
0:21 dashboard it's important that the charts
0:22 have a consistent look and feel and
0:24 there's a couple of ways we can achieve
0:26 this the first is to build one chart and
0:28 then copy it and edit the range being
0:30 referenced for example let's say we want
0:33 a separate chart for each region I can
0:36 start by inserting a chart for Europe we
0:38 just insert a line chart let me bring it
0:41 over here and I'll make it a little
0:45 smaller now notice it's detected the
0:48 year as one of the series and it should
0:50 be on the axis so I'm going to right
0:52 click and select the data we'll remove
0:55 it and then we'll edit the access labels
0:58 to reference the years click okay and
1:02 okay let's say I also want this line to
1:05 be a different color so let's go with
1:09 blue and I don't need the legend because
1:11 the chart title already says what the
1:13 region is so we'll delete that that
1:16 chart's done now I can either insert
1:18 another chart and make all those changes
1:20 again from scratch or I can copy the
1:23 chart that's already nicely formatted so
1:25 with the outer edge selected crl D we'll
1:28 duplicate the chart let's bring over
1:30 here now all they need to do is change
1:32 the cells that it's referencing to pick
1:34 up the Americas but notice that the line
1:38 has changed back to the default green
1:39 color and this is due to a setting in
1:42 the options that's on by default so I'm
1:44 going to contrl zed undo that change and
1:47 we'll go into the
1:50 options and then on the advanced tab
1:52 going to scroll down to charts and here
1:56 properties follow chart data point for
1:58 the current workbook we're going to
2:00 uncheck that box click okay now when I
2:04 change it to Americas it keeps the
2:06 formatting so that's just going to save
2:08 me a little bit of time and big thanks
2:10 to fellow Microsoft MVP John Peltier for
2:13 teaching me that tip now I'm just going
2:16 to hold shift and select both of the
2:18 charts so I can copy both together
2:20 control D to duplicate let's drag them
2:23 down here and we'll just change one by
2:26 one so first of all this should be Asia
2:29 and and lastly this is Africa so there's
2:33 my four charts they're all consistently
2:35 formatted with blue lines and no
2:41 Legend now what happens if your boss
2:43 says they want all the lines to be a
2:45 different color so let's select a
2:47 different color I'm going to make this
2:50 one back to green they want the chart
2:53 title to be left aligned they want
2:55 labels on the data instead of the
2:58 vertical axis so just going to select
3:00 the vertical axis and delete that and
3:02 they don't want the grid lines now
3:05 that's a lot of changes to repeat for
3:07 each chart and a quick way we can copy
3:09 the formatting is to select the outer
3:11 edge of the chart crl C to copy it
3:14 select the next chart and on the Home
3:16 tab we're going to paste
3:18 special and here we just want formats so
3:22 you can see it's copied all the
3:23 formatting with one go so I can just
3:25 select the next chart and press the F4
3:28 key to repeat and likewise for Africa
3:31 now you'll notice that the three charts
3:33 that I copied the formatting to now have
3:35 this dark gray border around them and
3:38 that's an artifact of the copying and
3:40 pasting it's a bit of a bug in Excel so
3:42 let's go and fix that so we want the
3:44 outline to be this pale gray color and I
3:48 can't use F4 here to repeat that
3:50 formatting but I can just click the
3:52 shape outline button now that I've
3:55 selected the color once it's kept it
3:57 there so I can just click it once to use
3:59 it
4:00 again now just a word on pivot charts
4:03 copying the formatting of pivot charts
4:05 is slightly different we copy it and
4:08 then select the next chart you'll notice
4:10 there's no past special option here it's
4:12 there but when you click it nothing
4:14 happens with pivot charts you simply
4:16 paste so contrl + V to paste and that's
4:19 done and unlike the regular charts you
4:21 don't get the dark gray border around
4:23 the chart when you copy the
4:26 formatting now another way you can
4:28 quickly change the color is using a
4:30 color theme on the page layout tab and
4:33 then colors as you hover your mouse over
4:36 the color palettes you get a preview of
4:38 what it might look like now you can
4:40 choose from these default themes or you
4:43 can create your own custom theme maybe
4:45 based on your company branding just keep
4:48 in mind that these color changes are
4:50 applied to the color of shapes and cell
4:53 fill so this is not just for the
4:58 charts
5:01 charts are objects just like shapes
5:03 images and form controls you can select
5:07 multiple objects by holding down control
5:09 or shift to select them and then if you
5:13 want to deselect one just left click
5:15 again to deselect while holding down
5:18 shift or control you can also select all
5:21 objects by selecting one and then contrl
5:24 a to select them all you'll notice
5:26 though that this also selects objects
5:28 like shapes and image as you can see
5:30 here I can deselect that holding down
5:33 shift and left clicking it now sometimes
5:37 objects might be overlapping one another
5:39 or tricky to select you can display the
5:41 selection pane via the page layout tab
5:44 and then selection pane let me drag it
5:46 over here so it's closer to our
5:49 charts we can click on the I icon to
5:52 hide a
5:53 chart we can hide them all or show them
5:56 all notice the picture is also in this
5:59 list because it's an object you can also
6:02 click on the names of the objects to
6:04 select them and if you hold down control
6:07 you can select
6:08 multiple once they're selected you can
6:11 move them around and apply alignment
6:14 formatting and the like you can even
6:16 resize them if you're working with lots
6:18 of objects you can give them a better
6:20 name so double click type in the new
6:23 name and press enter another way to
6:26 quickly select multiple charts or
6:28 objects particularly object objects that
6:29 are layered on top of one another is by
6:32 turning on select objects so VI the Home
6:34 tab of the
6:35 ribbon find and select you want select
6:40 objects this turns your mouse cursor
6:42 into alasu you can left click and drag
6:45 to select multiple objects only those
6:48 objects that are entirely circled in
6:51 your lasso will be selected once the
6:54 chart or object is selected you can go
6:56 in and choose design options and
6:58 formatting
7:00 your mouse remains in the select object
7:02 State you can't select any other cells a
7:05 shortcut to turn off select objects is
7:07 to press escape and your mouse returns
7:10 to its original
7:15 state now that you know how to select
7:17 your charts quickly and easily you'll
7:19 want to make sure they're nicely aligned
7:21 so I'm going to hold down shift to
7:23 select multiple charts and then up on
7:26 the format tab under alignment I can
7:29 Center align these and I might want to
7:32 do the same for these
7:35 two align to the center we can also
7:39 align them
7:40 horizontally you can see there's lots of
7:43 options if you have three or more charts
7:46 horizontally or vertically aligned so
7:48 let me bring this on over here I like to
7:52 use the tool in the alignment that will
7:55 distribute them in this case
7:56 horizontally and what that's going to do
7:58 is just put an even space between each
8:00 of the charts if you hold down the ALT
8:03 key it's going to snap the chart to the
8:05 grid while you move it around and it
8:08 will also work when you're resizing it
8:11 so you can quickly align charts to the
8:13 grid and make sure they're all uniformly
8:16 sized using the ALT key once you get
8:19 them exactly as you want you can go to
8:22 the view Tab and turn off grid
8:26 lines another way you can copy charts is
8:29 by holding the control key while you
8:31 left click and drag so with the chart
8:32 selected and I hold down control and put
8:35 my mouse right on the edge of the chart
8:37 you can see I now have the plus sign if
8:40 I left click and drag you can see I'm
8:42 getting a copy of that and if I hold
8:44 down shift at the same time it will
8:46 remain aligned to that horizontal
8:49 axis of course you can also use the ALT
8:52 key with control while you snap the new
8:54 chart to the
8:55 grid if you want precise movements you
8:58 can use the arrow keys to just nudge the
9:01 chart up and down or left and right but
9:06 just note if you have XL 2013 then you
9:08 need to hold down control while you use
9:10 the arrow keys that's not relevant in XL
9:13 2016 onwards we have the luxury of just
9:16 being able to use the arrow keys without
9:23 control the most common way to select
9:26 chart elements is with the mouse but
9:28 sometimes an element might be tricky to
9:30 select like the series here for small
9:32 values it's very difficult to get my
9:35 mouse in exactly the right place an easy
9:38 way to select elements like this is via
9:40 the format Tab and then in the drop-
9:43 down here I can choose it from the list
9:45 you can see it's now selected because I
9:47 have the pull handles on those columns
9:50 and from here I can control one to open
9:52 the formatting let's drag it into view
9:54 and I can go about formatting that
9:56 series perhaps changing the color
9:59 another way you can cycle through
10:00 elements is by holding down the control
10:03 key while you use the arrow keys and you
10:05 can see it's cycling through the
10:07 different elements in the
10:13 chart one of the most annoying things
10:15 when building a dashboard is needing to
10:17 change column widths or row Heights and
10:19 as you do that your chart gets messed up
10:22 as well we can prevent this in the chart
10:25 properties so selecting the chart
10:28 control one to open in the formatting if
10:30 it's not already open and then in the
10:32 properties under the properties drop
10:35 down instead of move and size with cells
10:38 you can choose move but don't size with
10:40 cells or don't move or size with cells
10:43 with either of those selected your chart
10:45 isn't going to change the size as you
10:48 expand those row Heights or column
10:54 widths now if you regularly use the same
10:57 chart types and find yourself repeating
11:00 the same formatting over and over then
11:02 you can save time by saving the chart as
11:04 a template to do this select the chart
11:07 right click save as
11:10 template it's going to open up to the
11:13 location of your chart template give it
11:15 a name and click save to use the chart
11:19 simply select the data insert tab you
11:23 can either choose recommended charts or
11:25 click the chart dialog box launcher and
11:27 then under all charts
11:29 templates you'll find the templates that
11:32 you can choose
11:33 from I hope you found these tips useful
11:36 if you like this video please give it a
11:38 thumbs up and subscribe to our channel
11:40 for more and why not share it with your
11:42 friends who might also find it useful
11:45 thanks for
11:47 [Music]
11:51 watching"""

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

filename = f"{datetime.now().strftime('%Y-%m-%d')}_INTERMEDIATE_{video_id}_Chart_Tips.txt"
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
