#!/usr/bin/python
import datetime
import os
import sys

from random import randint
import praw
from slackclient import SlackClient

BOT_TOKEN = os.getenv('BOT_TOKEN')
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_CLIENT_USER_AGENT = os.getenv('REDDIT_CLIENT_USER_AGENT')

// FIXME: File writes do not persist when this script is run inside a scheduler

subreddits = [
  # {'c': 'funny', 's': 'funny'},
  # {'c': 'hackernews', 's': 'hackernews'},
  # {'c': 'design', 's': 'web_design'},
  # {'c': 'funny', 's': 'programmerhumor'},
  # {'c': 'learnprogramming', 's': 'dailyprogrammer'},
  # {'c': 'hackernews', 's': 'technology'},
  # {'c': 'learnprogramming', 's': 'ProgrammerTIL'},
  # {'c': 'todayilearned', 's': 'todayilearned'},
  # {'c': 'design', 's': 'art'},
  {'c': 'reddit', 's': 'funny'},
  {'c': 'reddit', 's': 'dailyprogrammer'},
  {'c': 'reddit', 's': 'programmerhumor'},
  {'c': 'reddit', 's': 'hackernews'},
  {'c': 'reddit', 's': 'technology'},
  {'c': 'reddit', 's': 'ProgrammerTIL'},
  {'c': 'reddit', 's': 'todayilearned'},
  {'c': 'reddit', 's': 'web_design'},
  {'c': 'reddit', 's': 'art'},
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
    i = randint(0, len(url_list) - 1)
    return '{} {}'.format(title_list[i], url_list[i])

  except (praw.errors.PRAWException, praw.errors.HTTPException) as e:
    print(e)
    pass


def getLastRead():
  try:
    f = open('lastRead', 'r')
    lastRead = f.readline()
    lastRead = lastRead if len(lastRead) else 0
    f.close()
    lastRead = int(lastRead)

  except(FileNotFoundError, ValueError):
    lastRead = 0
  return lastRead

def getUpdatedLastRead(val):
  return val + 1 if (val + 1) <= len(subreddits) - 1 else 0


def main():
  hour = datetime.datetime.today().hour
  if (hour >= 2 & hour <= 14) & hour % 2 == 0:
    sc = SlackClient(BOT_TOKEN)
    if sc.rtm_connect():
      lastRead = getLastRead()
      updatedLastRead = getUpdatedLastRead(lastRead)

      sc.api_call(
        "chat.postMessage",
        username="Digibear",
        channel=subreddits[updatedLastRead]['c'],
        text=get_posts(subreddits[updatedLastRead]['s']),
        unfurl_links="true"
      )
      # sc.rtm_send_message(subs['c'], get_posts(subs['s']))

      wr = open('lastRead', 'w')
      wr.write(str(updatedLastRead))
      wr.close()
  else:
    print('The time is not ripe!')

if __name__ == "__main__":
  main()
