from dotenv import load_dotenv
import os

## HELPERS

DOTENV_LOADED = False

def check_env():
    """ Load values from .env, if they have not already been loaded """
    global DOTENV_LOADED
    if not DOTENV_LOADED:
        try:
            load_dotenv()
        except:
            pass

def load_list(names, raise_on_missing=True):
    """ Read environment variables """
    check_env()

    result = {}
    for name in names:
        value = os.getenv(name)
        if value is None and raise_on_missing:
            raise Exception(f"missing env for cred: {name}")
        prefix_length = name.find('_') + 1
        name_key = name.lower()[prefix_length:]
        result[name_key] = value
    return result

## REDDIT

__REDDIT_KEYS = [
    "REDDIT_CLIENT_ID",
    "REDDIT_CLIENT_SECRET",
    "REDDIT_USERNAME",
    "REDDIT_PASSWORD",
    "REDDIT_USER_AGENT"
]

def get_reddit():
    """ Read reddit credentials from environment """
    global __REDDIT_KEYS
    return load_list(__REDDIT_KEYS)

def get_subreddit():
    """ Read target subreddit from environment """
    check_env()
    
    prod = os.getenv("REDDIT_PROD_SUBREDDIT", None)
    dev = os.getenv("REDDIT_DEV_SUBREDDIT", None)
    assert prod is not None and dev is not None, f"please specify prod and dev subreddits: prod = {prod}, dev = {dev}"

    environ = os.getenv("REDDIT_ENVIRONMENT", None)
    assert environ is not None, "please specify either dev or prod environment"

    assert environ == "dev" or environ == "prod", f"unknown environ: {environ}, expected 'prod' or 'dev'"
    return prod if environ == "prod" else dev

## TWITTER

__TWITTER_KEYS = [
    "TWITTER_CONSUMER_KEY",
    "TWITTER_CONSUMER_SECRET",
    "TWITTER_ACCESS_TOKEN_KEY",
    "TWITTER_ACCESS_TOKEN_SECRET",
    "TWITTER_TWEET_MODE"
]

def get_twitter():
    """ Read Twitter credentials from environment """
    global __TWITTER_KEYS
    return load_list(__TWITTER_KEYS)
