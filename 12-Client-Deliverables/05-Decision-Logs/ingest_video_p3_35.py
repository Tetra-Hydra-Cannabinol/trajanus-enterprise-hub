"""
Ingest Playlist 3 video 35 (nGDBFuG9srE) - Excel Chart Mistakes That Make Data Experts Cringe
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

video_id = 'nGDBFuG9srE'
title = "Excel Chart Mistakes That Make Data Experts Cringe"
channel = 'MyOnlineTrainingHub'
duration = '3:40'
topics = ['Chart Best Practices', '3D Charts', 'Chart Styles', 'Axis Starting Point', 'Axis Labels', 'Data Sorting', 'Chart Selection', 'Data Labels', 'Legends', 'Titles', 'Gridlines', 'Data Visualization', 'Chart Formatting', 'Column Charts', 'Line Charts', 'Bar Charts', 'Stacked Charts']

transcript = """0:00 a lot of people send me their Excel
0:02 files asking for help or feedback on
0:04 their reports and in those files I see a
0:07 lot of bad charts it's enough to drive a
0:10 person to
0:11 [Music]
0:13 drink so I decided to compile a dossier
0:17 of the 10 telltale signs that you're a
0:19 chart amateur and the techniques you
0:21 should use instead so you can up your
0:24 chart game to Pro level now before we
0:26 start just so we're all on the same page
0:29 remember the the purpose of a chart is
0:31 to provide visual representation of data
0:33 making it quicker and easier to
0:35 interpret now the key words are quicker
0:38 and easier okay grab your drink let's
0:41 get started at number one are 3D effects
0:45 which add zero value and at worst they
0:47 can distort the results and mislead the
0:50 pie chart here illustrates this with the
0:52 red segment falsely appearing far bigger
0:55 than the yellow segment just don't use
0:57 3D charts ever chart amateurs love using
1:01 excel's built-in chart Styles
1:03 particularly the ones with the dark
1:04 backgrounds and the gradient fills just
1:07 back away from the style gallery and let
1:10 the data be the star of the show
1:13 amateurs think they can make charts look
1:15 more dramatic by starting the vertical
1:17 axis above zero but this is a big no no
1:19 for column charts just take this chart
1:22 from Air Wallock illustrating their fees
1:25 compared to other companies they've
1:28 purposely hidden the vertical ax
1:30 so you can't see that it starts way
1:32 above zero the difference between the
1:34 column Heights makes air wocks appear
1:37 75% cheaper than their nearest
1:39 competitor when in reality it's only 31%
1:43 cheaper this is a common marketing
1:45 employee to distort the truth and it's
1:47 effective because we subconsciously
1:49 compare the height of the columns and
1:51 make judgments this is how the chart
1:54 should
1:55 look now I should point out that the
1:57 axis starting at zero is less important
1:59 important with line charts because we
2:01 tend to refer to the access labels to
2:03 interpret one Line's position in
2:05 relation to others don't make people
2:08 turn their head to read your chart
2:09 labels if your access labels don't fit
2:12 horizontally then use a different chart
2:14 like a bar chart sorting data takes the
2:17 work out of ranking making your charts
2:19 quicker and easier to interpret stack
2:22 charts make all but the first series
2:24 difficult to compare it's better to use
2:26 a line chart if the point of the chart
2:28 is to compare the different series
2:30 excessive labeling clutters and
2:32 distracts dial back the labels by only
2:35 labeling key data points Legends slow
2:38 down interpretation because we have to
2:40 flip between the data points and the
2:41 legend and back and forth It's better to
2:44 directly label the data if you're not
2:46 expecting the chart to update titles are
2:49 often wasted on stating the obvious
2:52 instead use this Prime real estate to
2:54 communicate the key message by the way
2:57 notice the alignment of the title is
2:59 left in line with the AIS and this makes
3:01 the chart appear tidier than a centered
3:03 title when you have data labels and
3:06 vertical access labels the vertical
3:08 access labels and grid lines can often
3:10 be redundant you probably don't need
3:12 both you've made it to the end cheers to
3:15 you now go forth and make professional
3:18 looking charts by avoiding these 10
3:19 mistakes and if I missed any please
3:21 share them in the comments I hope you
3:23 like this video please give it a thumbs
3:25 up and subscribe to our channel for more
3:28 and if you know any chart amateurs
3:30 please share this video with them thanks
3:33 for
3:34 [Music]
3:38 watching"""

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

filename = f"{datetime.now().strftime('%Y-%m-%d')}_BEGINNER_{video_id}_Chart_Mistakes.txt"
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
