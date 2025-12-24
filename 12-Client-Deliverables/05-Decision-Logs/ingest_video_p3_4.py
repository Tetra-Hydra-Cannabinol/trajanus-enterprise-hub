"""
Ingest Playlist 3 video 4 (ANzRp-y-iW8) - Easy Excel Gantt Charts - Perfect for Project Management
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

video_id = 'ANzRp-y-iW8'
title = "Easy Excel Gantt Charts - Perfect for Project Management"
channel = 'MyOnlineTrainingHub'
duration = '8:28'
topics = ['Gantt Charts', 'Project Management', 'Conditional Formatting', 'WORKDAY.INTL', 'Overdue Tasks', 'Current Date Highlight', 'Task Tracking', 'Absolute Referencing']

transcript = """0:00 Gant charts are handy for planning and
0:02 managing project tasks over time they
0:04 give a visual representation of the
0:06 whole project displaying progress to
0:08 date and work to come in this video I'm
0:11 going to show you how to build Gant
0:12 charts in Excel using conditional
0:15 formatting we'll also look at how we can
0:17 highlight tasks that are overdue and the
0:19 current date so be sure to watch to the
0:22 end here I have a list of tasks the
0:25 start date estimated duration of the
0:28 task the completed day so far and the
0:31 remaining days and just note that my
0:33 dates are formatted day month year now I
0:36 often get asked how do you calculate the
0:38 completed days and the answer is well
0:40 that will be unique to your organization
0:43 for example it might Simply Be date
0:44 driven or you might review each task and
0:47 calculate how many days worth of the
0:48 project you've completed so far so for
0:51 the purpose of this example I've just
0:52 manually entered values and then the
0:55 remaining days is simply the difference
0:56 between the estimated days and the
0:58 completed days to calculate the
1:01 completion date I'm going to use the
1:02 work dat International function so that
1:04 I can ignore weekends and holidays but
1:06 I'm going to start with if is blank I
1:09 just want to check that this date is not
1:11 blank so if it equals blank then I'm
1:13 going to return blank otherwise we use
1:16 workday International if you don't have
1:18 workday International you can use
1:19 workday workday International simply
1:22 allows you to specify which days your
1:24 weekend falls on so my start date is
1:27 here and I'm just going to minus one so
1:29 that it doesn't assume that my first day
1:31 is already over and then how many days
1:33 am I adding well the estimated days and
1:37 then my weekend falls on a Saturday and
1:39 Sunday so I want number
1:40 one and then I can add a list of
1:43 holidays I'm going to leave that blank
1:45 but if you have a list of holiday dates
1:47 you can reference them here let's close
1:49 parenthesis on workday International and
1:52 close parentheses on if and there's my
1:55 completion date so I'll just double
1:57 click to copy that down so now I'm I'm
1:59 ready to apply my conditional formats
2:01 I'll start by selecting all the cells
2:03 that I want to format and then on the
2:05 hom tab of the ribbon conditional
2:07 formatting new rule and I want to use a
2:11 formula now there are two criteria so
2:13 I'm going to start with the and function
2:16 the first criteria simply checks whether
2:18 the start date is less than or equal to
2:22 the date in the First Column now I'm
2:25 just going to F4 to Absolute just the
2:28 row there and on on the start date I
2:31 want to Absolute the column so that's my
2:34 first logical test and then we're going
2:36 to use workday International again to
2:40 find the end date so we reference the
2:42 start date minus one and then we're
2:44 adding the estimated days and then our
2:48 weekend dates are type one let's just go
2:50 and fix the absolute referencing here so
2:52 we want absolute reference on the column
2:54 there and there I'm just using F4 to
2:57 toggle through so I'm comparing the end
3:01 date to see whether it's greater than or
3:04 equal to the date in the current column
3:08 and we're F4 to Absolute just the row
3:12 and I'll close parentheses on and let's
3:14 go and apply the format I want a cell
3:16 fill color in this bright
3:18 green I'll click okay and okay so you
3:22 can see it's highlighted more than just
3:24 the remaining days but as I keep adding
3:26 conditional formats those are going to
3:28 sit on top of this first formatting rule
3:31 the next rule is the completed days so
3:34 again conditional formatting new rule
3:37 and we want a formula now the formula is
3:39 the same almost so I'm just going to
3:41 copy in the previous one and instead of
3:44 C5 which is our estimated days I want my
3:48 completed days so I'm just going to
3:50 change that to D5 and then let's go and
3:53 set the format which will be this dark
3:55 green okay and okay so now I can see the
3:58 completed days
4:00 next I'll apply the rule for my
4:01 estimated
4:02 days and again it's with a formula and
4:06 I'm going to paste it in the formula
4:08 here is almost the same as well we just
4:11 need to add another criteria so I'm
4:14 going to check whether the estimated
4:17 days and f42 absolute just the column is
4:22 equal to the completed days and again
4:25 just absolu in the column so now we have
4:28 three criteria here I can apply the
4:30 formatting and the estimated days are
4:33 just going to be a paler shade of green
4:35 so this one here okay and okay you can
4:39 see the conditional formats layering on
4:41 top of each other to highlight the cells
4:43 accordingly the next thing I want to do
4:45 is highlight the overdue tasks and there
4:47 are a few ways we can do this so feel
4:49 free to make modifications for example
4:51 you could highlight the task name in
4:53 column A or you could highlight the days
4:55 where work should have been completed in
4:57 pink I'm going to do the latter notice
5:00 that I have a date up here this is
5:02 today's date for the purpose of this
5:04 tutorial so I would expect these two
5:07 cells here to be highlighted as overdue
5:10 so I'm just going to select the cells
5:13 again so new rule using a
5:17 formula now the beginning is the same so
5:20 I'm just going to paste that in and next
5:22 I need to check if the dates completed
5:24 so far are less than the current column
5:26 so we use the workday International
5:29 function for that and I'm starting with
5:32 the start date F4 to Absolute just the
5:34 column
5:36 minus1 plus the days completed so far
5:39 and my weekends are type one we're
5:42 checking whether this is less than the
5:46 current column F4 just to Absolute the
5:49 row and then I've got one more check and
5:51 that is whether the current column is
5:54 less than today's date now I could use
5:57 the today function here in place of the
5:59 cell reference but for the purpose of
6:01 this tutorial I've hard keyed my date in
6:03 the cell the today function will
6:05 dynamically update you won't need to
6:06 edit it so let's go and format this in
6:09 this pink color cck okay and you can see
6:12 there these two dates are overdue tasks
6:16 cuz we're currently on the 2nd of
6:18 December which leads me on to the last
6:21 format I want to apply and I want to
6:23 select the days at the top as well we're
6:26 just going to highlight the current date
6:28 using a new rule
6:30 which will be a formula and this one's
6:31 dead easy it's just WEA current column
6:35 date F4 to Absolute just the row is
6:39 equal
6:40 to today's date and again you could use
6:43 the today function here let's go and
6:45 format this I'm just going to put a
6:46 pattern in the cell that's going to
6:48 allow the colors to shine through click
6:51 okay and okay so you can see that is
6:55 today's date we could change the date
6:58 here let's just see the effect of the
7:00 conditional format can see now we're on
7:03 Monday the 12th of December so all of
7:05 these tasks are
7:07 overdue now if you have trouble with the
7:10 conditional formats not displaying
7:11 correctly one reason may be their order
7:14 you can modify it by the conditional
7:16 formatting manage rules dialogue box and
7:19 you can see the order they're in here
7:20 and as I set them up the first format I
7:23 set up is at the bottom and so on so if
7:26 I rearrange these for example put this
7:28 on at the bottom and then click apply
7:31 you can see this rule is being
7:32 overridden by the rules above it so it
7:34 needs to be up here towards the top so
7:37 that it shines through another reason
7:39 you might have problems with conditional
7:41 formats is if you don't get your
7:43 absolute referencing correct and I've
7:46 created a video that shows you behind
7:48 the scenes of conditional formats and
7:50 how they're evaluated I put a link to
7:52 that in the video description so you can
7:54 troubleshoot your conditional formatting
7:57 formulas I hope you found this tutorial
7:59 useful be sure to check out my project
8:01 management dashboard video where I use
8:03 this technique along with others to
8:05 create an interactive dashboard you can
8:08 download the Excel file containing the
8:09 completed Gant chart for this lesson
8:11 from the link here and if you like this
8:13 video please give it a thumbs up and
8:15 subscribe to our channel for more and
8:18 why not share it with your friends who
8:19 might also find it useful thanks for
8:22 [Music]
8:27 watching"""

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

filename = f"{datetime.now().strftime('%Y-%m-%d')}_INTERMEDIATE_{video_id}_Gantt_Charts.txt"
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
