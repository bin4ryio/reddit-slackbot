#!/usr/bin/python
import os
import praw
from random import randint
from slackclient import SlackClient

BOT_TOKEN = os.getenv('BOT_TOKEN')
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_CLIENT_USER_AGENT = os.getenv('REDDIT_CLIENT_USER_AGENT')

subreddits = [
  # { 'c': 'reddit', 's': 'funny' },
  # { 'c': 'reddit', 's': 'dailyprogrammer' },
  # { 'c': 'reddit', 's': 'programmerhumor' },
  # { 'c': 'reddit', 's': 'hackernews' },
  # { 'c': 'reddit', 's': 'technology' },
  # { 'c': 'reddit', 's': 'learnprogramming' },
  # { 'c': 'reddit', 's': 'todayilearned' },
  { 'c': 'funny', 's': 'funny' },
  { 'c': 'funny', 's': 'programmerhumor' },
  { 'c': 'learnprogramming', 's': 'dailyprogrammer' },
  { 'c': 'hackernews', 's': 'hackernews' },
  { 'c': 'hackernews', 's': 'technology' },
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
    title_list = []
    url_list = []
    for submission in subreddit.hot(limit=3):
      title_list.append(str(submission.title))
      url_list.append(str(submission.url))
    # return random.choice(url_list)
    i = randint(0, len(url_list)-1)
    return '{} {}'.format(title_list[i], url_list[i])

  except (praw.errors.PRAWException, praw.errors.HTTPException) as e:
    print(e)
    pass


def main():
  sc = SlackClient(BOT_TOKEN)
  if sc.rtm_connect():

    for subs in subreddits:
      sc.api_call(
        "chat.postMessage",
        username="Digibear",
        channel=subs['c'],
        text=get_posts(subs['s']),
        unfurl_links="true"
      )
      # sc.rtm_send_message(subs['c'], get_posts(subs['s']))


if __name__ == "__main__":
  main()
