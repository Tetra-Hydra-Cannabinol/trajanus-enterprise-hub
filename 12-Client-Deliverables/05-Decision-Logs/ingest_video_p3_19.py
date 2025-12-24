"""
Ingest Playlist 3 video 19 (i4jk1Hwga80) - Communicate Clearly - 3 Easy Tips for Better Excel Chart Titles
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

video_id = 'i4jk1Hwga80'
title = "Communicate Clearly - 3 Easy Tips for Better Excel Chart Titles"
channel = 'MyOnlineTrainingHub'
duration = '4:11'
topics = ['Chart Titles', 'Subtitles', 'Text Boxes', 'Color Coding', 'Legend Alternatives', 'Data Communication', 'Font Formatting', 'Accessibility', 'Color Blindness', 'Audience Awareness', 'Plot Area Adjustment']

transcript = """0:00 chart titles are often a wasted
0:02 opportunity to connect with your
0:03 audience and drive home your message
0:06 instead of a boring title make the title
0:08 short and snappy to introduce the chart
0:10 and then add a subtitle to expand the
0:13 story or findings in the data let's look
0:16 at some ideas for how we can leverage
0:17 this prime chart real estate to help
0:19 your audience get the most from the
0:21 chart here I have a typical cluster
0:24 column chart which shows the annual
0:26 percentage of B colonies lost in gray
0:29 orange is a percentage Lost In Summer
0:32 and blue is a percentage lost in Winter
0:34 now there's a lot of information in this
0:36 chart and we can see fairly easily that
0:38 winter losses are increasing while
0:40 summer losses are declining but your
0:42 audience might not notice or might not
0:45 even be bothered to look long enough to
0:47 notice so we can help them out by
0:49 including a subtitle simply insert a
0:52 text box at the top of your chart now
0:56 I'll just make the plot area a little
0:57 bit smaller so we have more room for the
0:59 text box
1:00 and in here we can type in our
1:03 message let's format the font in a shade
1:06 of
1:07 gray and then I'm going to color code
1:09 the keywords in the subtitle to match
1:13 the columns in the chart so winter is
1:15 blue and I'm going to make it bold just
1:17 to make it easier to read and summer is
1:20 orange now I'm going to go a shade
1:22 darker than the columns that just makes
1:24 the font easier to read now all I need
1:27 to do is Center the text and hide the
1:31 outline of the text box I'll set it to
1:33 no outline and I'll just drag it across
1:36 to the left so that it's in line with
1:38 the chart Title by color coding the
1:40 legend items in the subtitle we simply
1:43 make it quicker to interpret and relate
1:45 back to the Chart now with the subtitle
1:47 we have a better chance of conveying our
1:49 message plus our audience will thank us
1:51 for making their job
1:54 easy we can also use subtitles in place
1:56 of Legends Again by using the color
1:59 coding we saw in the previous example so
2:02 here I can insert a text box at the top
2:04 of the
2:08 chart let's make the text box a bit
2:10 bigger and I'll format the font in a
2:13 shade of gray now we can highlight
2:16 winter losses including losses and
2:19 format the font to match the
2:24 columns make this a shade of orange and
2:28 bold let's sent the text and hide the
2:31 shape outline I'll just move it slightly
2:34 to the
2:35 left and a little bit smaller so it's
2:38 not overlapping the title so you can see
2:41 there I haven't needed a legend as well
2:43 as my
2:44 subtitle now when you remove the legend
2:47 and rely on the title or subtitle color
2:50 coding keep in mind those with color
2:52 blindness and be sure to use colors that
2:54 are easily distinguished making colored
2:56 font bold will also help differentiate
2:59 them from the rest of the
3:01 text another use for subtitles is to add
3:05 context or detail not present in the
3:08 chart for example here beekeeper numbers
3:10 are down 34% since they peak in
3:14 20134 but you can't easily work that out
3:17 at a glance so we can insert a text
3:25 box and I'm going to color code down 34%
3:29 sent to match the highlighted column in
3:32 the
3:34 chart let's make the outline go away and
3:39 we'll just align it slightly over to the
3:42 left now when writing chart titles and
3:45 subtitles keep your audience in mind
3:47 remember just because something is clear
3:49 to you doesn't mean it will be clear to
3:51 your
3:52 audience I hope you found this tip
3:54 useful if you like this video please
3:56 give it a thumbs up and subscribe to my
3:58 channel for more and don't forget to
4:00 share it with your friends who might
4:01 also find it useful thanks for
4:04 [Music]
4:10 watching"""

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

filename = f"{datetime.now().strftime('%Y-%m-%d')}_BEGINNER_{video_id}_Chart_Titles_Tips.txt"
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
