from . import creds as __creds
import praw

def get_tweet_posts():
    creds = __creds.get()

    reddit = praw.Reddit(**creds)
    print(f"scraping posts as u/{reddit.user.me()}")

    return None
