"""
Ingest video 6 (1qzTQLFR20s) - Microsoft Copilot: How AI Changed Excel Forever
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

video_id = '1qzTQLFR20s'
title = "Microsoft Copilot: How AI Changed Excel Forever"
channel = 'MyOnlineTrainingHub'
duration = '6:34'
topics = ['Microsoft Copilot', 'Excel Copilot', 'AI in Excel', 'Formulas', 'Conditional Formatting', 'Data Analysis', 'Python in Excel', 'ChatGPT']

transcript = """0:15 something similar, stick with me until the end.
I've got a great alternative to share with you.
0:20 To work with Copilot, your data must be
saved on OneDrive, and if you're working
0:25 in the desktop version of Excel, AutoSave must
be enabled. You'll find Copilot on the Home tab
0:31 over on the far right. It opens the task pane
in Excel for the desktop and Excel online. Now
0:37 you can left-click and drag the task pane to
undock it and resize it as required or leave
0:43 it docked. Now the second requirement is your
data must be stored in an Excel table so Copilot
0:49 can easily identify what data to work with. You
can either use the keyboard shortcut Ctrl+T or,
0:55 as Copilot suggests, via the Insert tab and then
Table. My table has headers, so I'll click okay.
1:03 Now when you first open Copilot, there's a prompt
guide at the top and some predefined prompts to
1:08 get you started. You can click the refresh button
to get some new ideas or simply type your request
1:14 in here. Interestingly, yesterday while I
was trying different prompts with Copilot,
1:19 I managed to get it to reveal something it
probably shouldn't have, which I'll share
1:23 with you soon. But first, let's say I want to
add a column that calculates the discounts as a
1:28 percentage of sales. I press Enter, and away it
goes. Now, notice I capitalize the column names
1:34 to help Copilot identify them. It comes back
with a suggestion that reiterates the request,
1:41 provides a formula which is okay. I probably would
have used "IFERROR" to handle errors rather than
1:46 "IF," but at least it's handling errors that will be returned
when the discount is zero, and I can click here to
1:53 see the formula explanation. If I'm happy with
the suggestion, I can insert it. Now, it gives
1:59 me a preview of where it's going to put it. I
click insert column to add it. Notice it's also
2:05 formatted the column with a percentage without
me having to ask it, which is a nice touch.
2:10 All right, let's look at some other things
it can do. I'll ask it to highlight the sales
2:14 greater than 100,000. And just like that,
it's applied a fill color. Better still,
2:23 if we look at the conditional formatting manager,
you can see it's used a conditional format,
2:29 so any updates to the table will automatically
be formatted without me having to ask Copilot
2:34 to do it again. It's thinking ahead
and saving itself some time. Similarly,
2:40 you can ask it to apply cell formats, styles, and
other formatting. For example, let's say I want to
2:46 remove the banded row effect from the table,
and then if we look at the table design tab,
2:50 you can see it's deselected banded rows. It can
also find and replace data. For example, let's
2:56 replace "United States of America" in the country
column with "USA." And there we go. Job done.
3:05 Let's see it sort and filter. Let's say I
want to sort the data by segment, country,
3:09 and product and filter for discount band 'high'.
And just like that, it's applied the sorting
3:15 to the first three columns I filtered the
table for discount band "High." Pretty cool.
3:20 Now it's all good and well having Copilot
do all this work for you. But some things
3:25 are still slower than doing it yourself
when you know how, so it would be good if
3:29 it would teach you. So I said, "How did you do
that?" and it revealed some information about
3:36 how it's working under the hood that, well,
it probably shouldn't have. It said, "I use
3:41 the edit document tool to perform the actions you
requested. It allows me to perform Excel commands,
3:47 including formatting, conditional formatting,
sorting, filtering, clearing formatting or
3:53 content, finding and replacing, and modifying
table structures such as inserting or deleting
3:59 rows or columns and adding or removing headers or
total rows." Okay. Well, not what I was expecting,
4:06 but at least we now have a list of things
we can use it for. That made me wonder,
4:10 what other tools does it have? So I asked it,
and Copilot replied, "I also have access to
4:16 the Get Insights tool, which allows me to return
analysis, query results, and insights obtained
4:21 from a given query. I also use my knowledge
and capabilities to generate imaginative and
4:27 innovative content such as poems, stories, code
essays, and songs to help with your request."
4:34 All right, well, I'm not sure I need a
poem or a song, but let's try out the
4:38 Insights tool. Let's say I'm not familiar with
this dataset. Perhaps Copilot can give me an
4:43 overview and identify any trends, patterns, and
outliers. So I'll ask it to show data insights,
4:51 and it returns a line chart for the cost
of goods sold by date and an explanation
4:57 of the data displayed in the chart. And
I can insert it into my file and then
5:02 work with it like any other pivot chart. If I
don't want to keep the pivot table and chart,
5:07 I can click undo or keep it and go back to the
table. And while this is a start, one insight
5:14 isn't enough. It appears this feature in Copilot
is currently throttled because I've seen demos
5:19 online of this where it returns a whole page of
insights. It's based on the original Analyze Data
5:24 tool that's been around since at least 2018. So if
you don't have Copilot, give Analyze Data a try.
5:30 So far, we've looked at how we can use Copilot to
make changes to our spreadsheets, but we can also
5:35 use it like ChatGPT to ask questions unrelated
to the data, specifically in the table. However,
5:40 for Copilot to work, I still need a cell in a
table selected. So let's say I want it to explain
5:47 this formula. It's from a file I inherited, and
then I can paste in the formula and press Enter
5:55 and be patient while it prepares a response. There
we go. Copilot has returned an explanation of how
6:01 the formula works. And this is a game-changer
for working with complex formulas. It's still
6:07 early days for Copilot, and while it has some
limitations, I'm sure they'll be ironed out in
6:11 due course, along with the release of new features
like the ability to write Python and insert it
6:22 check out this video right here for an accessible
tool that can elevate your Excel skills today.
6:28 Don't forget to like and subscribe, and I'll
see you in the next video. Thanks for watching."""

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

filename = f"{datetime.now().strftime('%Y-%m-%d')}_INTERMEDIATE_{video_id}_Copilot_Excel.txt"
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
