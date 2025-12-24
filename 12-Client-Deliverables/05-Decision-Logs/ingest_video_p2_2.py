"""
Ingest Playlist 2 video 2 (ce1Nf-H3h2Q) - 5 HIDDEN Excel Tools Almost Nobody Is Talking About
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

video_id = 'ce1Nf-H3h2Q'
title = "5 HIDDEN Excel Tools Almost Nobody Is Talking About"
channel = 'MyOnlineTrainingHub'
duration = '8:59'
topics = ['Quick Analysis Tool', 'Ctrl+Q', 'Flash Fill', 'Ctrl+E', 'Fill Without Formatting', 'Menu Key Filtering', 'Navigation Pane', 'Data Bars', 'Sparklines', 'Productivity']

transcript = """0:00 Excel is full of hidden tools that can completely
transform the way you work, but most people will
0:05 never discover them. Today, I'm revealing five
hidden tools that will improve productivity and
0:10 make your life easier. By the end of this video,
you'll be wondering how you ever managed without
0:14 them. My favorite is number four. Let me know
in the comments which is your favorite at the
0:18 end of the video. Okay, let's dive in and unlock
these secret tools. If you've ever received a new
0:24 dataset and not been sure where to start, in the
Quick Analysis tool you have a load of shortcuts
0:29 to help you make sense of it at your fingertips.
Here I've got a table of sales by year, category,
0:34 and product, and I can simply press Ctrl + Q,
and up pops a load of tools I can access with
0:41 one click. For example, under charts,
I can quickly see my sales by category.
0:47 I'll click on it and it inserts a new sheet
including a pivot table and chart. From here,
0:52 I can continue to work with the pivot table and
chart to further customize them to my liking.
0:57 Here I have some data on the daily intake of
fruit and vegetables, and this sea of numbers is
1:02 a bit difficult to make sense of. Let's see what
Quick Analysis can do. I'll start by selecting the
1:09 numbers, Ctrl + Q, and under Formatting, we've got
data bars, color scales, and icon sets. Hovering
1:17 over them, I get a preview of how it's going to
look. The data bars look pretty good. With one
1:22 click, I've now got data bars to help me interpret
my data. It would also be useful to know what the
1:27 average is. I can do that with Ctrl + Q, and then
under Totals, scroll across and choose Average.
1:36 This inserts a new column for me, and all I need
to do is delete a few cells that have the #DIV!
1:41 errors and give it a heading. I'll insert another
column because another cool feature is sparklines.
1:48 Ctrl + Q on the Sparklines tab. I think the
columns will be best. Let's add those. Let's give
1:56 them a different color. Now I can easily see at
a glance that the younger generations are not big
2:02 fruit and vegetable consumers compared to older
generations, which was really difficult to see
2:07 without these tools to help visualize the data.
Now, if I select the data again and Ctrl + Q,
2:13 you'll notice there are loads more tools
available and you can try these for homework.
2:18 So be sure to download the practice file
from the link in the video description.
2:22 This next tool can clean all kinds of
messy data with a keyboard shortcut.
2:26 Here I've got a list of names and I want
to separate them into first name and
2:29 last name. So I'll just enter an example for
the first row and then Ctrl + E for Flash Fill,
2:35 and it extracts all the first names.
Let's repeat for the last names, Ctrl + E,
2:40 and it's inserted the last names, but it's got
a couple wrong. So we can see here this should
2:45 be a Jones-Barnley. By just correcting one of
them, it now knows how to treat the rest. Now
2:54 notice the Flash Fill menu appears and I can
click on the drop-down to undo the revision,
3:00 accept the suggestions, or select all three
changed cells. Or I can just continue on,
3:07 and it will assume I've accepted the suggestions.
Now there are tons of patterns you can have Flash
3:12 Fill work with. For example, here I can have it
construct an email address from the first and
3:17 last names, then Ctrl + E, and it completes the
rest for me. Now there are loads of other ways
3:23 that you can use Flash Fill, and I've got some
different examples here in the file that you
3:27 can try for homework. Remember you can download
the file from the link in the video description.
3:33 If you're looking to take your Excel expertise
to the next level, I highly recommend checking
3:37 out my Excel Expert course. Whether you're aiming
to enhance your resume with advanced Excel skills,
3:43 or you need to get quickly up to speed
for a new job, this course has got you
3:46 covered with tutorials ranging from beginner
to advanced. You can pick and choose exactly
3:51 what you need to learn. Plus, you get hands-on
practice with downloadable Excel files and a
3:56 certificate of completion to showcase your
new skills. Click the course link in the
4:01 video description to find out more and start
your journey to becoming an Excel pro today.
4:06 This might sound crazy, but you should stop
using copy and paste because this can be more
4:10 time-consuming than what I'm about to share with
you. Here I have some formulas that calculate the
4:15 sales, the cost of goods sold, and the profit.
I want to copy these formulas down, so I can
4:21 double-click the bottom right corner and it fills
down. But notice it messed up my formatting. So
4:27 let's Ctrl + Z to undo that. Another way I could
copy it down is to copy it and then paste special,
4:35 formulas. That does the job, but it's a load of
clicks. So let's Ctrl + Z to undo that. Instead
4:43 of copying and pasting, I can right-click the
fill handle and drag down. When I release,
4:50 I get a menu that allows me to choose Fill
Without Formatting. Now if we look in the cells,
4:56 you can see it's copied down my formulas
and my formatting isn't messed up. At first,
5:01 it'll feel weird right-clicking and dragging,
but you get used to it after a while.
5:06 This next shortcut is my favorite. It's
great for working with large data sets,
5:10 enabling you to cut through the noise and find
exactly what you need. For example, let's say I
5:15 wanted to focus on data for France. I can press
the menu key. This brings up the right-click
5:21 menu. Here I want to filter. So you can see 'e' in
Filter is underlined. So I need to press E. Then I
5:28 want to filter by the selected cell's value. So
that's V. Now my table is filtered for France.
5:35 I have filter buttons for every column. Now I can
continue applying filters. For example, let's say
5:39 I want to only see data for government. So again,
the menu key, E, V. And maybe I only want to see
5:48 the Montana product. So menu key, E, V, and you'll
get quicker and quicker at it the more you use it.
5:54 Now I have much less data to focus on, making
it easier to find what I need. And of course,
5:59 I can use the filter buttons to apply further
filtering. Or I can click the menu key and access
6:05 the other filter options here. If you want to
clear filters, you can do it one by one via
6:10 this menu. Or you can go to the Data tab of the
ribbon and click the Clear Filter button. Now
6:15 for homework, check out the other shortcuts
in the menu key. For example, 'O' for Sort.
6:22 Navigating through a workbook with countless
sheets, tables, and charts can be like looking for
6:26 a needle in a haystack. With the Navigation pane,
we can get an instant overview of our workbook
6:31 so we can quickly and easily find and access
different elements. To access the Navigation pane,
6:37 go to the View tab and then click on Navigation.
This opens the pane on the right-hand side. You
6:44 can unlock it by left-clicking and dragging.
Now it's mobile. Alternatively, you can dock
6:49 it to the left-hand side if you prefer. Clicking
on one of the sheets takes you to that sheet and
6:54 exposes the elements available there. You can
select the elements from the Navigation pane,
6:59 and you can see the chart is now selected in the
worksheet. If I expose one of the other sheets,
7:04 you'll notice it also makes ranges that contain
data available. So I can click on this, and it
7:09 takes me to that sheet. It also selects the table
of data. Now the search bar at the top of the
7:15 Navigation pane allows you to type and filter for
specific tables or charts, for example. You can
7:20 see now I've got all the charts available. It also
shows me the chart titles so I can easily select
7:26 the correct chart. This is especially useful in
large workbooks with numerous items. By default,
7:32 all charts start with the name Chart, so they're
easy to find. But this also applies to pivot
7:36 tables, tables, shapes, and other objects, so you
can search for them by their default name. Or you
7:41 can name elements in line with how you want to
search for them. For example, let's say I want to
7:46 rename these charts based on the intake of fruit
and vegetables. Instead of calling it Chart 1,
7:52 I can right-click and rename it. The options you
have in the right-click menu here will differ
7:57 depending on the type of element. So I can rename
this Intake 1 and click OK, then repeat for each
8:05 chart. Now I can simply type in Intake to filter
my list of elements based on that name. You can
8:21 see I have charts and ranges named accordingly.
So I've got all of my objects and elements in one
8:28 succinct list, making it super quick and easy to
jump to them. If I want to navigate to a range,
8:33 I can click on it, and it selects it. All
this is the range of cells that I've named
8:38 in the name box up here, so they're super quick
and easy to jump to from the Navigation pane.
8:44 Now if you feel like you're not doing things as
quickly as you could be in Excel, here's a video
8:49 that I highly recommend you watch next on the
top ten productivity tips for work. You'll learn
8:54 quick and easy ways to solve some of the most
common problems in Excel. I'll see you there."""

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

filename = f"{datetime.now().strftime('%Y-%m-%d')}_BEGINNER_{video_id}_Hidden_Excel_Tools.txt"
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
