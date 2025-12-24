"""
Ingest video 5 (hfAwUhQOaVw) - 4 x AI Dashboard Designs in 60 SECONDS!
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

video_id = 'hfAwUhQOaVw'
title = "4 x AI Dashboard Designs in 60 SECONDS!"
channel = 'MyOnlineTrainingHub'
duration = '6:08'
topics = ['AI Dashboard Design', 'DALL-E', 'Midjourney', 'ChatGPT', 'Excel Dashboards', 'Power BI', 'Dashboard Best Practices', 'Data Visualization']

transcript = """0:00 designing dashboards and reports can be
0:02 a timec consuming task particularly if
0:05 you're not artistically inclined so when
0:08 AI designed these four dashboards you
0:09 see behind me in just 60 seconds from a
0:12 sentence worth of instructions I was
0:15 super excited I think you'll agree
0:17 they're eye-catching and they make you
0:19 want to take a closer look which is half
0:21 the battle in getting your audience to
0:22 read your report we'll talk about the
0:25 more important other half of the battle
0:27 later first let me take you through the
0:30 AI tool I used and the process at the
0:33 end I'll also share the cons of using AI
0:36 to design your reports so you don't end
0:37 up with something that's all style and
0:40 no substance so be sure to stay tuned
0:43 everyone is talking about chat GPT which
0:46 provides text based AI answers to
0:48 questions so I started by trying out
0:51 chat gpt's sister service for generating
0:53 images called darly I asked it to create
0:57 a Microsoft Excel dashboard containing
1:00 displaying quarterly sales data over a
1:02 2-year period and unfortunately it's
1:05 generated dashboard images that look
1:07 like they were made in
1:08 1985 thankfully there's another service
1:12 called mid Journey which is more up to
1:14 the task although not without its own
1:16 limitations and I'll talk more about
1:18 that later after signing up for an
1:20 account with mid Journey you use Discord
1:22 to request the images which seems a
1:24 little odd especially if you've never
1:26 used Discord before my teenage Sons will
1:28 be rolling their ey should they ever
1:30 watch this video now you start by
1:32 selecting a newcomer room for new bees
1:35 and then in the message you enter SL
1:39 imagine press enter and it opens the
1:42 prompt field and here you simply
1:44 describe in words what you'd like and it
1:46 spits out four ideas from there you can
1:48 ask for variations of a design or simply
1:51 ask another question tweaking the
1:53 instructions to get the desired result
1:55 now these are public rooms so you can
1:57 see what others have requested and they
2:00 can see what you've requested if you
2:02 sign up for a paid account and you get
2:05 access to a member's gallery and with
2:07 the Pro Plan there's also an option to
2:08 opt out of your images being public by
2:11 the way I'm not affiliated with mid
2:13 Journey so if you sign up for a plan I
2:14 don't make any money now it stores your
2:17 designs in your homepage and my first
2:20 attempts were okay I started by asking
2:23 it to create a Microsoft Excel dashboard
2:26 report for coffee company displaying
2:29 monthly sales data over one year with
2:31 six different charts and in 60 seconds I
2:34 got these four Images which are okay but
2:36 they're not amazing notice it's used
2:39 shades of brown in keeping with the
2:40 coffee theme but most of the dashboard
2:42 images have ignored the instructions to
2:44 include six different charts so I
2:47 thought maybe powerbi dashboard designs
2:49 will be better so I asked it for a
2:51 powerbi dashboard for tracking Global
2:53 clothing company sales and distribution
2:55 data and I got this it's better than the
2:58 Excel dashboards and in the the absence
3:00 of anything specific in my request it
3:02 appears to have taken inspiration from
3:04 the powerbi logo for the color theme I
3:07 then asked it to upscale one of the
3:09 designs so I could see it better notice
3:11 the text is elgible so don't expect help
3:14 with knowing what metrics to include I
3:16 then asked for some variations on one of
3:18 the designs but there's not a lot of
3:20 difference between them and then I
3:22 thought I could emit the application
3:24 name altoe from my request and see if I
3:26 can get something more eye-catching by
3:28 specifying a color scheme so I asked it
3:30 for a dashboard report displaying
3:32 different types of charts and visuals
3:34 for a bicycle company's sales and
3:36 distribution data kpis using a dark
3:38 color theme including bright blue and
3:41 pink and I got this you can see the more
3:44 descriptive you can be the more likely
3:46 you'll get something elaborate and
3:47 closer to what you're after no doubt
3:50 you're excited to give AI a try for
3:52 designing your dashboards and reports
3:54 but before you go all in let's
3:56 understand the limitations the good news
3:59 is there's nothing in these designs that
4:01 can't be achieved in XL or powerbi
4:04 however if we take a closer look at one
4:06 of the dashboard designs you can see
4:09 it's very light on details it contains a
4:12 load of pretty visuals that have no
4:14 substance as well as what appears to be
4:17 piles of bike parts that will serve no
4:19 purpose in a business report also the
4:22 bike in the middle is taking up some
4:24 prime dashboard real estate so you
4:26 probably wouldn't keep this at best we
4:28 can use this design for color
4:30 inspiration assuming your audience
4:32 aren't color blind the contrasting boxes
4:35 behind each visual nicely segregate the
4:37 data and the blue and pink font for the
4:40 chart titles with gray labels complement
4:42 the color scheme don't be tempted to
4:45 create charts to match those in the
4:47 design the prime driver of the visuals
4:49 you include in your report should meet
4:51 the business purpose of the dashboard if
4:54 you're displaying data over time then
4:56 use a line or column chart if you're
4:58 showing parts a whole with three or less
5:01 segments use a pie or donut chart if
5:04 your categories have long labels use a
5:06 bar chart Etc now I cover more on chart
5:10 best practices in my Excel dashboard
5:12 course which you can find at the link in
5:14 the video description so the bottom line
5:17 is have some fun getting ideas for your
5:19 reports from Ai and mid Journey but
5:22 don't use it to inform decisions on what
5:24 charts to include in your dashboard and
5:26 certainly don't include charts for the
5:28 sake of Art or piles of bike parts for
5:31 that matter and keep in mind as defined
5:34 by Steven Fu the objective of a
5:36 dashboard report is to provide a visual
5:38 display of the most important
5:40 information needed to achieve one or
5:42 more objectives displayed on a single
5:45 screen so it can be monitored at a
5:47 glance well I hope you found this
5:50 tutorial useful if you like this video
5:52 please give it a thumbs up and subscribe
5:54 to our channel for more and why not
5:56 share it with your friends who might
5:57 also find it useful thanks for watching
6:02 [Music]"""

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

filename = f"{datetime.now().strftime('%Y-%m-%d')}_INTERMEDIATE_{video_id}_AI_Dashboard_Designs.txt"
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
