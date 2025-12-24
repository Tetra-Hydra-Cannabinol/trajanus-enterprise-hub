"""
Ingest Playlist 3 video 37 (IuqE6uh2Z9w) - Microsoft said it couldn't be done - Interactive Python Charts in Excel
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

video_id = 'IuqE6uh2Z9w'
title = "Microsoft said it couldn't be done - Interactive Python Charts in Excel"
channel = 'MyOnlineTrainingHub'
duration = '13:57'
topics = ['Python in Excel', 'Interactive Charts', 'Slicers', 'Power Query', 'DataFrames', 'Seaborn Charts', 'Pivot Tables', 'Pivot Charts', 'Dashboard Design', 'xl Function', 'Python Formulas', 'Data Filtering', 'Referenced Pictures', 'External Data Sources', 'Calculation Options']

transcript = """0:00 The first thing I asked Microsoft after trying out Python in Excel was, can I connect Python formulas
0:06 in Excel to Slicers? The answer I got was, no. But I've never been one to take no for an answer. In
0:13 this video I'm going to show you how you can create interactive python charts connected to
0:18 Excel Slicers, which will enable you to build interactive dashboards containing both Python
0:23 and Excel charts side by side, controlled by the same slicer. For this example, I'll connect python
0:30 to power query data, which is currently only supported for external data sources. That is,
0:35 you can't connect python to a query that's connected to an Excel table in the same file, yet.
0:42 My data's in a CSV file so let's go and grab it. This is one of them. I'll import,
0:48 and I'll go ahead and transform the data. This is just going to give me an opportunity to rename the
0:53 query. And I just want to put 'qry' at the front of the name. Now, one of the fields I want to work
1:00 with is the education field, and if we scroll across you can see it only contains numbers,
1:06 which aren't very helpful. But I've got another table and a CSV file, so let's go and grab
1:12 that. That's going to allow me to translate those education level numbers into labels,
1:17 so let's get that table. You can see there it's got the level and then the label.
1:23 Again, I'll just prefix this with 'qry' to differentiate the names. So what I'm going
1:28 to do is bring this data into my original table, and we'll do that using a merge.
1:35 And the matching columns are education, and then in my other table, the level.
1:42 So let's click ok to bring that in. There's my new column, but we need to expand the columns
1:48 just to bring label in. And we'll rename this, "education level name". Another option instead
1:56 of merging is to load the two tables to Power Pivot and create relationships between the tables,
2:01 but I'm going to keep this example simple. Let's go ahead and "close and load to",
2:07 and here I just want to create a connection, and click ok. And we can see in the queries
2:15 and connections pane I've got two queries. Next, I need to create a python data frame
2:21 connected to power query. And I want to connect it to my employee data, so in this cell here,
2:27 I need to activate python mode. So I can type in equals py, and then TAB, or I can use the keyboard
2:34 shortcut CTRL+ALT+SHIFT+P, that also jumps me into the formula bar to type my python. so I'm
2:40 going to call this data frame df1, and it's going to equal my query. Now, I can't select
2:46 it using the mouse but I can use the new Excel function "xl" and then type in the query name,
2:52 or use the autocomplete to select it from the list. There it is there, I'll just tab to select
2:58 it. Then I need to specify that headers are true, that is, my data table and my query has headers.
3:05 And close parentheses. Now I should point out that python formulas are case sensitive, just like
3:10 power query. So to complete the formula CTRL and ENTER, and there's my first data frame now. I like
3:18 to just put a note to the left of the data frame, it tells me what this data frame represents,
3:24 because they can get out of hand quite quickly. so this is df1, and it's the query employee data. now
3:32 because this is a data type, I can click on the icon here and get a preview of the data in the
3:39 data frame. it shows me some of the columns. I've got a massive table so it just gives me some of
3:44 them and it shows me the first five and last five rows of the data. I can see here I've got 1469
3:51 rows. actually it's 1470 because the first row is zero based, so it starts numbering from zero.
3:59 I can also click on the widget here and bring in data into my worksheet. Either a preview or some
4:06 of this other information. I'm going to leave it in the data frame collapsed for the purpose
4:10 of this tutorial. Now, the chart I want to build enables the user to filter employee data using
4:16 a Slicer for the Education Level, so I need a pivot table for the slicer to connect to,
4:22 and to return the selections made in the slicer. So let's go ahead and do that. I'm going to use
4:28 the query data for my pivot table, so I'm going to right click and change the load to setting to
4:34 a pivot table report. And I'm just going to pop it in this cell here, click OK. Let's move that
4:40 out of the way and we'll bring the pivot table fields over beside the pivot table.
4:47 Let's make it a bit bigger. So, here I want the education level name in the row labels.
4:53 I don't need the grand total, so right click remove that. Let's rename the column header
4:58 "Education Level", and we'll make the column a bit wider. Now, I also need a slicer for this field,
5:04 so right click, add a slicer, and let's just bring it over here for now. I'll right click
5:10 the slicer and go into the slicer settings, and let's rename the display header "Education Level".
5:17 Next, I need to capture the selections made in the slicer from the pivot table, so as I select
5:22 something in the slicer, the pivot table reflects that. It's kind of a cheating way to capture what
5:28 the user has selected in the slicer. So let's do that here, and I'm going to CTRL+ALT+SHIFT+P to
5:35 go into python mode. This is going to be called "df2". It's my second data frame. And it's simply
5:41 going to reference these cells here. So if I press CTRL+ENTER we can see the data frame, and
5:48 we can see the list. However, if I select only two items in my slicer the pivot table filters, now if
5:56 I click on the data frame, we've got these empty cells. That's going to cause problems later on.
6:00 So, what I want to do is filter this data frame. Let's just expand the formula bar CTRL+SHIFT+U,
6:07 and we'll go down onto the next line, and I want to filter df2. So, df2 filtering the column
6:15 called "Education Level", even though there's only one, t dropna and convert it to a list.
6:23 CTRL+ENTER, and now it's a list. Let's just make a note of what we've got in this cell. It's data
6:30 frame number two education level pivot. Next, I need a data set for my chart that contains the
6:37 employee data in data frame one, filtered based on the selections made in the slicer. So I'm going to
6:43 create another data frame, again going into python mode, CTRL+ALT+SHIFT+P. This one's going to be
6:49 called filtered_df, and it's going to equal df1. You can tap to select it. Open square bracket,
6:56 filtering df1 column called "Education Level" name. Where the education name is in,
7:04 not quite correct English but let's go with it, is in this list. So, where the education levels are
7:12 in that list it's going to filter the data frame one. Close my square bracket and CTRL+ENTER to
7:19 complete the formula. So let's make a note of what this cell contains. So it's filtered_df,
7:25 which is df1 filtered for the education level. Let's just make that column a bit wider,
7:31 and now I'm ready to create my chart. I've got my data here that's filtered based on this list,
7:36 which reflects the selections made in the slicer that are displayed in the pivot table here.
7:43 Now let's rename this sheet "Workings" and I'm going to insert a new sheet for my charts.
7:49 Now let's just take a look at the chart that we're building again. Here we can see it
7:54 contains the monthly income, age, job level, and education, in a scatter chart. You can see this
8:02 one is currently filtered for "below college" and "master" education levels. The job levels
8:08 are color coded and the bubble size represents the education. Now, I've already written some code,
8:14 so I'm just going to copy it because it's quite a lot. And then we'll go back to our
8:17 file and in this empty cell I'll use the keyboard shortcut CTRL+ALT+SHIFT+P to go
8:24 into python mode. And then I'm going to copy the code that I've already written because
8:28 there's quite a lot and I'll paste it in. Let's make the formula bar bigger CTRL+SHFIT+U. Let's
8:35 move that out of the way so we can see. It's using the Seaborn chart, setting the theme,
8:41 and then we're getting the filtered data that's in a data frame on the working sheet in cell B4.
8:47 Let's just delete that and we'll check. So, I'll click on the working sheet and it's this one here,
8:53 and it puts in the reference. Then I'm going to rename the column for the education level
8:59 name because it's a bit of a mouthful. I'm just changing it to education, Notice it's
9:03 got a space on the end to differentiate it from the actual column called education. And then we
9:08 plot the data. So, we're using the age column on the x-axis, monthly income on the y-axis,
9:14 the hue or color is the job level, and the size of the bubbles is education. And it's using the
9:21 data in the data frame called filtered df1. So, let's CTRL and ENTER to commit that. CTRL+SHIFT+U
9:29 to reduce the formula bar. And it's put it in as an image because I forgot to change it to an
9:34 Excel value, so let's do that from the drop down. And now there's a tiny chart. Let's right click
9:39 and create a referenced picture. So there's our picture. The original one is still in the cell
9:46 and they're linked, so if anything changes in the python code or the query that it's connected to,
9:51 it's going to update automatically and pick up the changes. It's pretty big. Let's just make it a bit
9:58 smaller and we can go ahead and grab the slicer. So I'll CTRL+X to cut it out and then I'll paste
10:05 it on this sheet. Let's apply some formatting to the slicer. So I'm just going to give it a gray
10:10 color. I'm going to make it five columns wide and we'll just sit it above the chart up here.
10:19 Okay let's test that the slicer works. So, we'll choose "below college" and "master".
10:26 And that looks great! Now, let's build an Excel pivot chart and connect it to the same slicer so,
10:32 we'll have a python chart and a native Excel chart running side by side both controlled
10:37 by the same slicer. So, what I'm going to do to start that chart is copy this pivot table,
10:42 and the reason I do that is because that way this pivot table is already connected to the
10:48 same slicer, so don't need to mess about with slicer settings. Now, this pivot table contains
10:53 the average monthly sales by education field, so let's change it bring the education field down,
10:59 and take the education level out. And we want the monthly income down here,
11:05 and instead of Sum I'm just going to change it to Average. And let's apply some number formatting.
11:13 So we'll put in the comma separator and no decimal places. And let's sort it from
11:20 smallest to largest. Okay, now I can go ahead and insert a regular pivot chart. I'm just going
11:27 to go with this 2D bar chart. Let's apply some formatting quickly. I'll get rid of the field
11:32 buttons. Let's get rid of the horizontal axis because I'm going to add data labels. In fact I'm
11:39 going to add data labels inside the base. Let's also get rid of the grid lines and the legend.
11:46 I'll format these labels in white font and make them a bit bigger and bold. And then we'll make
11:52 these bars bigger so CTRL+1 to open the formatting pane. Let's bring it over and we'll change the gap
11:58 width to 50. And let's get rid of the border on the chart itself because that will be more in
12:07 keeping with the python chart. And before I move it I'm just going to change the fill color for
12:13 these bars to a shade of gray. All right. Let's CTRL X to cut the chart out and we'll pop it here
12:21 beside the python chart. And let's just resize it a little and we'll center the slicer. Let's get
12:27 rid of the grid lines and now we have something that looks a bit more like a report. Now,
12:33 I nearly forgot to give the chart a proper name so let's put that in. "Average monthly salary by
12:38 education". And lastly, let's test if the slicer works. So we'll look at "College" and "Bachelor".
12:48 And there we go! Awesome! Now, there are a couple of limitations you should be aware of. First,
12:54 refreshing python formulas also triggers a full refresh of the query it's connected to,
12:59 so you might find it helpful to go into the formulas tab and change your calculation option
13:04 to partial. Partial is a new setting which puts Python and Excel data tables into manual calc
13:11 mode. To manually trigger a calculation just press the F9 key or set it back to automatic.
13:19 And lastly, python charts like these ones, that are interactive using python code,
13:25 are not supported in Exce, yet. Hopefully they'll come but I don't have any promises for Microsoft
13:31 that they will, so I'm just hoping and crossing my fingers that we'll get them in Excel as well. I
13:37 hope you'll find these techniques useful. You can download the file for this tutorial from the link
13:41 here and if you like this video please give it a thumbs up and subscribe to our channel for more,
13:47 and why not share with your friends who might also find it useful. Thanks for watching.
13:52 [Music]"""

# Save transcript
archive_dir = r'G:\My Drive\00 - Trajanus USA\00-Command-Center\Knowledge_Archive\Transcripts\Microsoft_Office'
os.makedirs(archive_dir, exist_ok=True)

header = f"""Title: {title}
Channel: {channel}
Video ID: {video_id}
URL: https://www.youtube.com/watch?v={video_id}
Duration: {duration}
Level: ADVANCED
Application: Microsoft Excel
Topics: {', '.join(topics)}
Ingested: {datetime.now().strftime('%Y-%m-%d')}
Source: Playwright Browser Extraction
{'='*78}

"""

filename = f"{datetime.now().strftime('%Y-%m-%d')}_ADVANCED_{video_id}_Python_Interactive_Charts.txt"
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
    'level': 'ADVANCED',
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
