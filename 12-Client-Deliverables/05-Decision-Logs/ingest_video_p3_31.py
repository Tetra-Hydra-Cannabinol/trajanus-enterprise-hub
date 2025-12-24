"""
Ingest Playlist 3 video 31 (2bXM18JWdLI) - Excel Burn Down & Burn Up Charts for Project Management
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

video_id = '2bXM18JWdLI'
title = "Excel Burn Down & Burn Up Charts for Project Management"
channel = 'MyOnlineTrainingHub'
duration = '8:40'
topics = ['Burn Down Charts', 'Burn Up Charts', 'Project Management', 'Agile Methodology', 'Progress Tracking', 'Line Charts', 'Scatter Charts', 'Forecasting', 'Cumulative Effort', 'SUM Function', 'COUNT Function', 'Absolute References', 'Chart Formatting', 'Scope Changes', 'Ideal vs Actual', 'Stakeholder Communication', 'Resource Planning']

transcript = """0:00 burn up and burn down charts are easy to
0:03 make in Excel now if you're familiar
0:05 with agile project management then
0:07 you'll know that these charts are useful
0:09 for monitoring the progress of a project
0:12 against expectations now while the
0:14 terminology is specific to Agile project
0:16 management the concept is relevant to
0:19 managing any project and it can be
0:21 applied to measures of time a number of
0:24 tasks costs Etc let's take a look a
0:28 burndown chart tracks the total expected
0:31 effort think tasks Milestones time costs
0:35 that type of thing versus the actual
0:37 effort over time for example let's say
0:40 we have 60 hours of effort to complete
0:42 10 tasks in a 10 workday period if we
0:45 work at a steady Pace we do 6 hours per
0:48 work day it's called a burnd down chart
0:50 because it starts with a total effort
0:51 available and over time that amount
0:53 reduces until all effort is used up in
0:56 this chart the expected effort is the
0:58 ideal burndown line line and the actual
1:01 effort is the remaining effort line now
1:04 if the remaining effort line is above
1:06 the ideal bur down line the project is
1:08 falling behind conversely if the
1:10 remaining effort line is below the ideal
1:12 burnd down line the project is ahead in
1:15 this example the team were initially
1:17 behind but by day four they pulled ahead
1:20 only to fall behind again on day six
1:22 however they managed to finish in line
1:24 with expectations now this isn't always
1:27 the case and these charts are used to
1:28 enable the team to adjust their original
1:31 targets and communicate with
1:32 stakeholders early on of any changes to
1:35 the original
1:36 plan for example in this chart we can
1:39 see that after 3 days of work the
1:41 average hours is closer to 4 hours per
1:43 day instead of six and if we extrapolate
1:45 that out the project will take 15 days
1:47 to complete rather than the planned 10
1:50 now at this point we can either add
1:51 resources to bring the project back in
1:53 line with the time deadline but at an
1:56 increased cost we can reduce the scope
1:58 of the project to bring it in on time
2:00 and budget or except it will just take
2:02 longer and cost more let's take a look
2:05 at how to build a band down chart in
2:08 Excel in this table we've got 10 tasks
2:12 and in column C we have the estimated
2:13 hours each task will take and as each
2:16 day passes the actual hours of work
2:18 completed are entered in columns D
2:20 through M now row 15 contains the
2:23 remaining effort and column C is simply
2:26 the sum of the estimated hours which is
2:29 60 that is the total hours we have
2:31 available to complete these 10 tasks
2:34 each day the cumulative hours of work
2:36 completed are subtracted from the total
2:38 estimated hours to show how many hours
2:41 are remaining so the formula in this
2:43 cell is equals our total remaining
2:46 effort F4 to Absolute minus the sum of
2:50 day one's time and I'm just going to
2:53 close parentheses I'm going to Absolute
2:55 the first reference F4 and press enter
2:59 and then I simply copy that
3:01 across until we get to the end when we
3:04 have zero hours left so in this case our
3:07 project has come in in line with our
3:09 planned effort now the ideal burndown is
3:12 simply the total estimated hours spread
3:15 evenly across the time the formula is
3:19 equals our total time F4 to Absolute
3:24 minus our total time F4 to Absolute / 10
3:29 because we have 10 days times the count
3:33 of the days we've completed so far so
3:35 I'm just going to Absolute the first
3:38 reference F4 and leave the second one
3:41 relative so that as I copy it across
3:44 it's going to count up by one day at a
3:46 time press enter there it's copied the
3:49 format from above so let's just copy
3:51 this format across and I'm going to copy
3:54 it and now I can create a chart that
3:56 plots these two lines now you can either
3:59 use a scatter chart or a line chart I'm
4:02 just going to go with the line chart
4:03 with markers let's make it a bit bigger
4:06 and I'll move it down below the table
4:08 I'll right click and edit the access
4:11 reference so that it's picking up this
4:14 data here click okay and
4:18 okay give the chart a title obviously
4:21 you'll give it a title that represents
4:23 the project that it's plotting I'm also
4:25 going to move the legend to the top and
4:29 that's is going to give the whole chart
4:31 a bit more space so I'll move the title
4:32 over there and the legend up there and
4:34 now I can make the plot area a bit
4:37 bigger so there you have a burn down
4:40 chart the burndown with forecast is the
4:42 same except we have an additional series
4:44 for the forecast values here you can see
4:46 we're only 3 days into the actual
4:48 Project work and based on those 3 days
4:50 we can forecast how long it will take to
4:52 complete the tasks at the current rate
4:55 the formula for the forecast is the
4:57 estimated effort absolute
5:00 minus the sum of the time taken so far
5:05 and I'm just going to Absolute that
5:07 close parentheses divided by three CU
5:09 there's three days times the count of
5:12 days so far so I'm just going to count
5:15 the dates up to column G cuz that's the
5:18 current position and F4 to Absolute the
5:21 first reference in count close
5:23 parentheses that way when I copy it
5:25 across this count is going to increment
5:27 by one column at a time and again it's
5:30 picked up the formatting cuz I've
5:31 referenced a date let's fix that and
5:35 left click and drag to copy it across so
5:37 now I have this forecast series just
5:40 going to copy it select the chart crl V
5:43 to paste and we can see the forecast
5:46 let's control one to open the formatting
5:48 pane we'll just drag the formatting pane
5:50 over here and we'll go in and instead of
5:54 using orange we're just going to
5:56 continue the blue but in a paler shade
5:59 and we'll give it a dash line we also
6:01 need to fix the marker so let's go in
6:03 and we'll just select none so it's just
6:05 a dash line that just helps to
6:08 illustrate that it's an estimate not an
6:11 actual B up charts plot the ideal effort
6:15 at a constant rate and display the
6:17 cumulative actual effort over time their
6:20 purpose is the same that is to identify
6:22 if a project is off track and unlikely
6:24 to meet its goals under agile project
6:26 management burnup charts typically
6:28 quantify Pro ress in points rather than
6:30 time hence the terminology here in the
6:33 chart however if you're not bound by
6:35 agile you can use them for costs hours
6:37 Milestones Etc let's take a look at how
6:40 to build burnup charts in
6:42 Excel you can use the same table for
6:45 burnup charts as you do for burnd down
6:46 charts here the cumulative effort in
6:49 cell D15 is simply the sum of day one
6:54 and I'm going to F4 to Absolute the
6:56 first cell reference that way when I
6:58 copy it across
7:00 it's going to increment by one column at
7:02 a
7:03 time now the ideal effort is typically
7:06 steady for the duration of the project
7:08 so you can simply reference the previous
7:09 cell and copy it
7:11 across however if the scope changes part
7:14 way you can override the formula so here
7:17 for example I might want to increase to
7:20 80 and by showing this step in the ideal
7:23 effort helps illustrate and explain to
7:26 your stakeholders that there was a
7:27 decision making change made at that
7:30 point in time fup charts also use line
7:34 or scatter chart however I don't want
7:36 this first value so I want the labels
7:38 and then the cumulative balances and
7:41 then we're going to insert either a line
7:44 or a scatter
7:46 chart and just like we did with the burn
7:49 down chart I'm going to go in and fix
7:52 the access labels so they pick up the
7:56 dates I can also move my lend to the top
7:59 top I prefer it at the top then I can
8:02 move it out of the
8:03 way and we'll give the chart a title
8:06 over here burn up chart and just like
8:10 with burn down charts you can forecast a
8:12 few days into the work to see if you're
8:14 on Target and make changes
8:17 accordingly I hope you found this
8:19 tutorial useful you can download the
8:21 Excel file for this lesson from the link
8:23 here and if you like this video please
8:25 give it a thumbs up and subscribe to our
8:27 channel for more and not share it with
8:29 your friends who might also find it
8:31 useful thanks for
8:34 [Music]
8:38 watching"""

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

filename = f"{datetime.now().strftime('%Y-%m-%d')}_INTERMEDIATE_{video_id}_Burn_Down_Up_Charts.txt"
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
