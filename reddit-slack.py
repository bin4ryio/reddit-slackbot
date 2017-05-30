#!/usr/bin/python
import praw
import os
from slackclient import SlackClient

token = 'xoxb-189120246384-cfVhYNqRvRut3pe3bSYmXRvO'
sc = SlackClient(token)

reddit = praw.Reddit(client_id='7ht41_-pPRbe2Q',
                     client_secret='DKehB69dNr-TgBxQov58eD3ZjhQ',
                     user_agent='reddit-slackbot:v1.0 (by /u/welcome-2-reddit)')

if not os.path.isfile('posted_id.txt'):
    posted_id = []
else:
    with open('posted_id.txt', 'r') as f:
        posted_id = f.read()
        posted_id = posted_id.split('\n')
        posted_id = filter(None, posted_id)

subreddit = reddit.subreddit('funny')

for submission in subreddit.hot(limit=5):
    if submission.id not in posted_id:
        sc.api_call(
            'chat.postMessage',
            username='Digibear',
            channel='#funny',
            text=submission.url,
            unfurl_links='true',
            unfurl_media='true',
            icon_emoji='chart_with_upwards_trend')
        #posted_id.append(submission.id)

with open('posted_id.txt', 'w') as f:
    for post_id in posted_id:
        f.write(post_id + '\n')
