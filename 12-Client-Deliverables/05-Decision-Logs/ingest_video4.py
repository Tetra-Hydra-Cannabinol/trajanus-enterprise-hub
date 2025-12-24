"""
Ingest video 4 (lRqCd2eL2gA) - I Don't Write Formulas Anymore, Excel Does It For Me!
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

video_id = 'lRqCd2eL2gA'
title = "I Don't Write Formulas Anymore, Excel Does It For Me!"
channel = 'MyOnlineTrainingHub'
duration = '6:14'
topics = ['Formula by Example', 'Flash Fill', 'Text Split', 'Text Rearrange', 'Text Join', 'Calculations', 'Dates', 'Row Numbering', 'Forward Filling']

transcript = """0:00 remember how amazing Flash Fill was when
0:02 you saw it for the first time well
0:04 there's a new feature that's 10 times
0:06 better it's called formula by example
0:09 simply give Excel an example or two and
0:12 it will suggest a formula to complete
0:13 the task it's 10 times better than
0:16 flashfill because it isn't a one time
0:18 and done solution being a formula it
0:20 automatically picks up any changes in
0:22 the data now it's still in the early
0:25 stages of development and only available
0:27 in Excel online for us English users of
0:30 Microsoft 365 with a personal or family
0:33 subscription this also means that the
0:35 functionality I'm going to show you in
0:37 this video may change before it's
0:39 generally available now don't worry if
0:41 you don't have one of those
0:42 subscriptions because there's a link in
0:44 the video description where you can try
0:46 it out let's take a look at some
0:49 examples extracting text from a sale is
0:51 now easy to do with formula by example
0:54 just give it an example or two click on
0:57 show formula there's the formula it's
0:59 proposing if I'm happy with it I can
1:01 click apply and you can see it's split
1:04 the text after the
1:06 period here we can split text into first
1:09 name and last name columns again give it
1:11 a few
1:13 examples if you think it's going to get
1:15 the formula right you can take a Gamble
1:17 and click apply notice it also corrects
1:21 the case since it's detected that I
1:23 wanted upper case first initial and it's
1:26 also applied it for Miles we can see
1:28 it's built into the formula with the of
1:30 the proper function let's see how it
1:32 handles the
1:33 surname let's have a look at the formula
1:36 it's a bit more complicated this formula
1:38 because it's realized that some names
1:40 have a middle initial so it needs to
1:42 allow for that it hasn't quite fixed the
1:45 case sensitivity here and that's
1:47 probably because I didn't get to give it
1:49 the example for this name we can go
1:52 ahead and fix the ones that it got wrong
1:55 it's detected that I wanted to correct
1:56 the formula and we can now see it's
1:59 wrapped in the proper function and if we
2:01 take a look you can see it's being
2:03 applied to all the cells in the column
2:05 so it autoc corrects
2:08 itself it can also rearrange data for
2:11 example here I might want my phone
2:13 numbers separated with a hyphone between
2:15 each set of three digits let's give it
2:18 some
2:20 examples let's see formulas quite long
2:24 it's a bit much to try and get my head
2:25 around so I'm just going to click apply
2:27 and see if it looks correct and we can
2:29 see it's correctly split each of the
2:32 numbers with a hyphen between the first
2:34 and second set of three
2:37 digits joining text is similar we've got
2:40 a few names with some case issues so
2:43 let's see how it handles that let's have
2:46 a look at the formula it's wrapped it
2:48 iner so it looks like it's detected that
2:50 we need to correct some of the names
2:52 we'll click apply and that looks
2:55 perfect formula by example can also
2:58 handle math equations it's triggered
3:00 when it detects the manual entry of data
3:02 that could be derived with a formula
3:05 it's detected that I appear to be
3:06 multiplying the quantity times the price
3:09 let's click apply and there we go it's
3:11 replaced my hard key values with the
3:14 formula and that way if I make a change
3:16 to this it's going to feed through and
3:19 update
3:20 automatically extracting date
3:22 information from a list of dates is also
3:24 super easy let's take a look here I want
3:27 the
3:28 year let's see what it gives me pretty
3:31 straightforward just the year
3:33 function and there we go what if I want
3:36 the month
3:37 name so it's going to convert the date
3:40 into a text formula and format it to
3:43 just show the month name and there we go
3:46 perfect let see how it goes with the
3:48 month end it's 31 days in May as is
3:51 March 30 in September it's detected that
3:55 a formula could do the job and it's
3:58 going to use the end of month function
4:00 to find the last day and then just
4:02 extract the day let's apply it and
4:05 perfect but what if we wanted to see the
4:08 actual month date not just the day so
4:10 let's see and you'll notice it's not
4:13 coming up with a suggestion despite the
4:16 previous example correctly using the end
4:18 of month function obviously something
4:21 that needs to be
4:23 developed Dynamic row numbering is super
4:25 easy just start to enter consecutive
4:28 numbers and it detects that we're
4:32 numbering the column it's going to use
4:34 the row function let's apply it now the
4:37 cool thing about this is if I add a row
4:40 notice that the numbering has
4:42 automatically adjusted and likewise if I
4:45 delete a row it correctly
4:49 updates like row numbering you can give
4:51 Excel a set of examples and it will
4:53 detect the pattern and suggest a formula
4:55 to complete the column so let's say I
4:57 want these to be skew num numers that
5:00 start with E 0 0 and then a number let's
5:05 have a look at the formula and we'll
5:07 apply problem is it hasn't correctly
5:10 numbered once it gets to 10 let's fix
5:13 that and it's going to correct the
5:16 formula now click apply and you can see
5:20 they're all
5:21 updated now this formula will work until
5:23 we get to 100 and then it's going to
5:26 have the same problem as we had with 10
5:28 that's because it's pretty fixing
5:30 everything with e- Z so what we really
5:32 need is e Dash so we'll remove the zero
5:36 and we'll make this three digits long
5:40 and you'll notice it still Returns the
5:41 same result but if we got to e 100 it
5:45 would correctly format it as a
5:47 three-digit
5:48 number I hope you found this tutorial
5:51 useful check out the link in the video
5:53 description where you can try out
5:54 formula by example if you don't have a
5:56 suitable 365 subscription if you like
5:59 this video please give it a thumbs up
6:01 and subscribe to our channel for more
6:03 and why not share it with your friends
6:05 who might also find it useful thanks for
6:08 watching"""

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

filename = f"{datetime.now().strftime('%Y-%m-%d')}_INTERMEDIATE_{video_id}_Formula_By_Example.txt"
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
