"""
Ingest video 9 (ITjl7J7zJro) - NEW Excel COPILOT Function Will Replace Half of What You Do
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

video_id = 'ITjl7J7zJro'
title = "NEW Excel COPILOT Function Will Replace Half of What You Do"
channel = 'MyOnlineTrainingHub'
duration = '6:18'
topics = ['COPILOT Function', 'Excel AI', 'Data Classification', 'Data Cleaning', 'Formula Explanations', 'Data Analysis', 'Financial Statements', 'Microsoft 365', 'TEXTJOIN', 'FORMULATEXT']

transcript = """0:00 Stop scrolling, because Excel just got an update that changes everything. Forget
0:05 writing formulas. Forget Googling syntax. You can literally talk to your data with
0:10 the new COPILOT function. Type plain English into a cell, and Excel does
0:14 the work. Categorize hundreds of transactions, clean messy addresses, explain scary formulas,
0:22 even analyze financial statements without you lifting a finger. Sounds impossible, right? I've
0:28 got five jaw-dropping ways to use the new COPILOT function inside Excel that will blow your mind.
0:33 The COPILOT function lets you pass a prompt, point at your data, and get back the answer
0:39 instantly. And once you see how it works, you'll never go back to doing things the old way. It's
0:44 currently available on the Beta Channel for Microsoft 365 users with a Copilot license.
0:50 Got a messy list of expenses? Normally, you could waste hours categorizing them,
0:55 but with the new COPILOT function, simply tell it to analyze the Australian credit
0:59 card descriptions and come up with a short list of categories I can use to group the expenses. Close
1:05 parenthesis. And in seconds, COPILOT scans the list and proposes the categories to suit my data.
1:12 And notice, I didn't even tell it which cells the expenses are in. The COPILOT function is
1:16 aware of the data around it, so it infers that I'm referring to the descriptions in
1:21 column B. And to help it out, I told it the transactions are Australian,
1:25 so it has some context of the business names it'll find in those descriptions.
1:30 And now I can have it apply those categories to the transactions.
1:34 This time, I'm going to tell it where those descriptions are and the categories
1:39 that I want to use, which are in these cells here. And it's a spilled array,
1:44 so it puts in the hash for the spilled array operator. Press Enter. And just like that,
1:49 my transactions are categorized. And with a quick scan of them,
1:52 it looks like it's got them all right. Imagine scaling this to thousands of rows.
1:58 But wait until you see how COPILOT cleans messy addresses just as easily. Data cleaning used
2:03 to be a nightmare. Watch COPILOT extract ZIP codes from chaos. Here I have a list
2:08 of inconsistently formatted addresses, and I want to extract the ZIP code from column
2:14 B. So these are the cells containing my addresses. Close parenthesis. Job done.
2:21 And in the next step, I'm going to have COPILOT fix the formatting so
2:24 these addresses are actually useful. I'll tell it the cells the addresses
2:28 are in. Close parenthesis. Done. It feels like magic, right?
2:32 But what if you stumble on a monster formula you don't understand? COPILOT can explain
2:37 it in plain English. Now, most of us have seen a formula that makes our brain melt,
2:42 like this one. With COPILOT, simply ask it to explain in plain English what this
2:47 formula is doing. And to pass it the formula, I'll use the FORMULATEXT function. Refer to
2:53 the cell containing the formula. Close FORMULATEXT. Close COPILOT. Press Enter.
2:59 And now we have no more formula guesswork, just clear explanations in plain English.
3:05 If COPILOT can explain formulas, imagine what happens when we ask it to analyze an entire
3:10 profit and loss statement. Instead of manually scanning rows of figures, let COPILOT highlight
3:16 what matters. I'm going to ask it to analyze the profit and loss statement and give me a summary of
3:21 notable points. I'll reference the entire table. Close parenthesis. And let's see how it goes.
3:29 So, you can see it's given me a spilled array. It's analyzed revenue, cost of goods sold,
3:34 gross profit, expenses, and net profit. But it's a bit hard to read, and the text is quite long. So,
3:40 let's edit the formula. And I'm going to use the TEXTJOIN function to join the five
3:44 points together. And I'm going to use the CHAR function to insert a carriage return.
3:50 Now, character 10 is a line break or carriage return. Let's insert two of them between each
3:57 paragraph. So that's going to be my delimiter. Two carriage returns. Comma. I'm going to ignore
4:02 empty cells — that's fine. We don't have any, but let's go with TRUE anyway. And then the
4:06 text is returned by COPILOT. So let's just go and close parenthesis on the TEXTJOIN function.
4:13 And now we have one string of text. I'm going to actually link this to a shape.
4:19 I'm going to insert this rectangle here. I'll move it down a little bit. And then I'm going
4:24 to reference the cell containing my COPILOT formula. It's now in my shape. Let's change
4:29 the text to white so it's easier to read. And I can resize the text box a little bit.
4:35 Let's move this out of the way. And then we can move our text box up beside the
4:40 profit and loss statement. It's like having a financial analyst built right into Excel.
4:45 If you're excited about what AI can do in Excel, just imagine combining it with advanced Excel
4:50 skills. That's what my Excel Expert course is all about — mastering the formulas,
4:55 automation, and pro techniques that set you apart. The link's in the video description
4:59 and pinned comment if you're ready to take your skills to the next level.
5:03 Okay, here's where it gets crazy. You can even ask it to generate data it
5:08 doesn't already have in your sheet. Let's ask COPILOT to list the English
5:12 Premier League teams for the 25/26 season and rank them based on their
5:17 likelihood of taking out the Premiership. Close parenthesis. Let's see how it goes.
5:23 Controversial. It's got Man City first. Liverpool fans won't be impressed. Arsenal,
5:28 Chelsea, Manchester United, and so on. It's also got some teams
5:32 in this list that are no longer in the Premier League, including
5:35 Leicester City and Sheffield United. And it's missing Sunderland and Leeds,
5:40 which is why you need to validate information COPILOT returns. Like any AI, prompts matter,
5:46 so be clear, structure your data in a tabular layout, and iterate until you get what you want.
5:52 Remember, COPILOT is best for interpretation, classification,
5:55 and insights, not precision math. The COPILOT function isn't the future — it's
6:01 here now. Type what you want, point at your data, and let Excel do the heavy lifting.
6:06 And if you're impressed by what COPILOT can do with prompts,
6:09 wait until you see how AI can scrape data from the web and drop it straight
6:13 into Excel with just a few clicks in this video. I'll see you there."""

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

filename = f"{datetime.now().strftime('%Y-%m-%d')}_INTERMEDIATE_{video_id}_Excel_COPILOT_Function.txt"
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
