"""
Ingest video 8 (1b4gDSodMwo) - AI Tool That Creates Dashboards in Minutes for Free
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

video_id = '1b4gDSodMwo'
title = "AI Tool That Creates Dashboards in Minutes for Free"
channel = 'MyOnlineTrainingHub'
duration = '9:43'
topics = ['Claude AI', 'Dashboard Creation', 'Data Visualization', 'Chart.js', 'HTML CSS', 'Power BI', 'Excel Dashboards', 'AI Tools', 'Artifacts']

transcript = """0:00 In this video, we're going to turn this boring table of data into this
0:04 interactive dashboard. Actually, I'm not going to do much at all. I'm going to use
0:09 AI to do it all for me. And unlike ChatGPT, with this tool, it's free to upload files,
0:16 and it creates the dashboard for you. However, it does come with some limitations. So stick
0:20 around to the end where I cover them and the alternatives. And if you'd like to
0:24 try it yourself, you can download the example file from the link in the video description.
0:29 First, let me quickly introduce you to our AI assistant, Claude. Claude is created by
0:34 Anthropic with backing from Google and Amazon, and it's designed to assist with a wide range
0:40 of tasks from data analysis to coding and beyond. What's great about Claude is that
0:45 it's free to use, and you can access it from your web browser. Unlike ChatGPT,
0:50 Claude can generate and display complex content like charts and even entire dashboards in its
0:56 artifacts window. This preview feature is free to use. You just need to turn it on in your settings,
1:03 which you'll find by clicking on your initials in the bottom left and then going to feature
1:08 preview and here make sure you've toggled artifacts on. And you can see with artifacts,
1:14 you can ask Claude to generate content like code snippets, text documents, or website designs.
1:20 So now that we have artifacts enabled, let's see Claude, create a dashboard for our data. Here I
1:27 have a table of fictional data by date, region, product, and sales channel with units sold,
1:33 unit price, total revenue, total cost, and profit. It's a lot to get your head around in this format.
1:39 So I'm going to close the file, and we're going to drag it in and drop it into the chat. And
1:45 then in the prompt field, I'm just going to paste my prompt in, which is, "Analyze this
1:50 data and suggest six key visualizations or metrics that would be most effective for a comprehensive
1:55 sales performance dashboard and explain why each would be valuable." This way, we're not
2:00 just getting a dashboard; we're gaining insights into what makes an effective data visualization.
2:06 So we can see, Claude has come back and it's suggested total revenue by region bar chart,
2:12 which will show us which regions are generating the most revenue. We've got a sales channel
2:17 performance pie chart, which is going to compare offline versus online. Then we've
2:22 got a product category performance stacked bar chart. Not sure about the stacked bar chart,
2:26 so we'll come back to that. Then we've got a monthly revenue trend line chart,
2:30 which is great for seeing how our revenue tracks over time. We've got a profit margin by product
2:35 scatter plot, which is going to plot units sold against profit margin, revealing which items
2:41 are most profitable. And then we've got average order value, which we might leave out because we
2:46 don't have individual orders in our dataset, so it can't actually calculate the average order value.
2:52 So we can see Claude has given us some great suggestions, and these visualizations cover
2:57 different aspects of our sales data: geographic performance, time trends, product analysis,
3:03 and sales channel split, giving us a comprehensive overview. So now that we have these ideas,
3:09 let's ask Claude to help us create our dashboard. I'm going to paste in my prompt, which says,
3:15 "Based on the visualizations you've suggested, create a visual representation of our complete
3:20 dashboard with interactive elements, excluding chart number six, which is the average order value
3:26 and doesn't make sense. Make the line chart span the width of the dashboard, use the data from the
3:32 CSV file I uploaded to populate the chart. If you don't say this, Claude might make up its own data.
3:38 Then we want it to provide this as an HTML/CSS artifact that represents how our dashboard should
3:44 look and use Chart.js, which is a JavaScript chart library for creating the charts, and make sure to
3:51 include the necessary JavaScript to process the CSV data and create the visualizations."
3:57 Let's click send and see what we get.
4:02 And you can see on the right, Claude is writing the HTML for the web page to display the dashboard
4:07 as well as the CSS for the styling and the JavaScript to generate the charts. And there's our
4:15 dashboard. So we've got our monthly revenue trend, we've got our revenue by region, our sales channel
4:22 performance, and if I hover over the different elements in the charts, you can see it gives me
4:27 the tooltips; it's completely interactive. At the bottom, we've got a product category performance
4:33 stacked column chart and profit margin by product scatter chart. So some of the charts are
4:39 a bit questionable. I probably wouldn't use this stacked column chart, and the scatter chart is not
4:45 really very effective for this dataset, but overall, it's a pretty good first attempt.
4:51 What is impressive is how Claude has taken our raw data and transformed it into meaningful insights.
4:57 For example, we can easily see which regions are performing the best, and we can see the breakdown
5:02 of our sales by online and offline. And down here, we can see which product category performs
5:08 the best in terms of revenue, cost, and profit. Now I can also click on the publish button at the
5:13 bottom to publish it or click the download button to download the HTML file that I can then share
5:19 with others. And because it's HTML, the file size is super small, so with it downloaded, let me open
5:25 the file in a new tab. We can see there's our line chart at the top. I can hover over the elements.
5:31 It's fully functional, just as an HTML file, and you can see it's saved on my C drive. So I
5:37 could share this file with others over email or in Teams for them to open in their own web browser.
5:43 Claude has not only created the visualizations, but if I click on the code button, you can see
5:48 it's written all the code that is the HTML, CSS, and JavaScript code to process our CSV
5:56 data and populate the charts. Now, if you have JavaScript skills, you can connect
6:01 this dashboard to a larger dataset and have it automatically update the report. But of course,
6:07 this is just the starting point. Let's see if we can get Claude to up the design quality. So I'll
6:12 add another prompt asking it to make the dashboard color scheme more impressive. And let's click send
6:19 and see what it comes up with this time. So you can see it's gone for a dark theme. We've
6:25 got a curved line on our line chart. We've got a donut instead of a pie, we've got a bubble chart
6:32 indicating the size of the profit margin, and our stacked column chart looks very similar just in a
6:39 different color scheme. And of course, you could give Claude specific instructions on the color
6:43 theme, for example, have it in keeping with your brand colors and design best practices to follow.
6:49 Because although this is eye-catching, the colors don't really aid interpretation as they should.
6:54 As impressive as Claude's dashboard creation capabilities are, it's important to understand
6:59 the limitations of using AI for this task. First, there's the data volume limit. According
7:05 to the documentation, Claude can only handle datasets up to 30 megabytes, but in testing,
7:10 it wouldn't even accept files containing more than a thousand rows and a handful of columns. Second,
7:16 customization can be challenging. While we can ask Claude to make changes, it doesn't always do what
7:22 you ask of it. It's not as flexible as creating a dashboard manually, especially when it comes
7:28 to complex custom visualizations or layouts. Third, there are data security considerations.
7:35 When using AI tools, you need to be cautious about uploading sensitive business data. Fourth,
7:41 integration with other systems is limited. Claude can't directly connect to your
7:45 company's databases or automatically update with new data. You need JavaScript and Python
7:51 skills to take the code that Claude gives you and connect it to your source data. Lastly,
7:57 as with all AI, you must check the output and not blindly rely on its accuracy.
8:03 Given these limitations, what are some alternatives? One option is to use Excel
8:08 with AI's assistance. For example, you can use Claude to get ideas and formulas and then
8:14 implement them yourself in Excel. Another option is to use professional business intelligence tools
8:20 like Power BI, which offer more flexible and robust features for large datasets and
8:25 complex visualizations. If you're interested in mastering Power BI, I've got a course designed
8:30 to quickly take you from novice to expert in creating professional interactive dashboards.
8:35 In my comprehensive course, you'll learn how to transform raw data into stunning visual reports
8:41 with more functionality and customization options. You'll discover how to use advanced features,
8:47 create dynamic charts, and design user-friendly interfaces that make data analysis a breeze.
8:54 The link to the course is in the description below and the pinned comment. Check it out
8:58 if you want to take your Excel and data visualization skills to the next level.
9:03 We've seen how Claude AI can be a powerful tool in streamlining the dashboard creation process,
9:08 making complex data analysis more accessible, and it's an excellent starting point,
9:13 especially if you're new to data visualization or you need quick insights. But remember,
9:19 while AI is a fantastic assistant, there's immense value in understanding the process
9:24 yourself, and that's why I've prepared something special for you. In this video,
9:29 I'll show you how to create an interactive Power BI dashboard in just 12 minutes. No AI
9:34 assistance required. It's a perfect follow-up to what we've learned today, and you'll be
9:39 amazed at how quickly you can create stunning dashboards on your own. I'll see you there."""

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

filename = f"{datetime.now().strftime('%Y-%m-%d')}_INTERMEDIATE_{video_id}_Claude_AI_Dashboards.txt"
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
