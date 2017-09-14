#!/usr/bin/python
import random
import os
import praw
from time import sleep
from slackclient import SlackClient

BOT_TOKEN = os.getenv('BOT_TOKEN')
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_CLIENT_USER_AGENT = os.getenv('REDDIT_CLIENT_USER_AGENT')

subreddits = [
  { 'c': 'funny', 's': 'funny' },
  { 'c': 'learnprogramming', 's': 'dailyprogrammer' },
  { 'c': 'hackernews', 's': 'hackernews' },
  { 'c': 'learnprogramming', 's': 'learnprogramming' },
  { 'c': 'todayilearned', 's': 'todayilearned' },
]

def get_posts(payload):
  r = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_CLIENT_USER_AGENT
  )
  try:
    subreddit = r.subreddit(payload)
    url_list = []
    for submission in subreddit.hot(limit=3):
      url_list.append(str(submission.url))
    return random.choice(url_list)
  except (praw.errors.PRAWException, praw.errors.HTTPException) as e:
    print(e)
    pass


def main():
  sc = SlackClient(BOT_TOKEN)
  if sc.rtm_connect():

    for subs in subreddits:
      sc.rtm_send_message(subs['c'], get_posts(subs['s']))


if __name__ == "__main__":
  main()
