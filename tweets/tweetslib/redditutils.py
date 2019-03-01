from . import creds as __creds
from . import regexutils as regex
import praw

## GET POSTS WITH TWEETS IN EM

def get_tweet_posts(subreddit):
    """ Scrape the target subreddit for link posts to Twitter """
    creds = __creds.get_reddit()

    reddit = praw.Reddit(**creds)
    print(f"scraping posts from r/{subreddit} as u/{reddit.user.me()}")

    submissions = reddit.subreddit(subreddit).new()
    tweet_posts = [s for s in submissions if regex.match_tweet(s.url) is not None]

    return tweet_posts

## POST UNFURLED TWEET TO REDDIT

def post_and_sticky(parent, comment_text):
    """ Post an unfurled tweet as a top-level comment and sticky it """
    parent.reply(comment_text).mod.distinguish(how='yes', sticky=True)

## HELPERS

def get_target_subreddit():
    """ Read target subreddit from env """
    return __creds.get_subreddit()

def format_tweet_text(tweet):
    """ Format tweet text for insertion into reddit comment """
    lines = tweet.full_text.splitlines()
    lines.append(f"— {tweet.user.name} (@{tweet.user.screen_name})")
    quoted_lines = ["> " + line for line in lines]
    blockquote = "\n> \n".join(quoted_lines)
    return f"&nbsp;\n\n{blockquote}\n\n&nbsp;"

def reddit_footer():
    return f"""I'm a bot. [Source code here](https://github.com/ChaoticWeg/reddit-starsbot).  
    Issue? Request? [Let me know](https://github.com/ChaoticWeg/reddit-starsbot/issues)."""
