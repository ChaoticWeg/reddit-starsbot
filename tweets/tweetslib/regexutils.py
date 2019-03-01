import re

TWEET_RE="^https?:\/\/(?P<sub>(?:www)|(?:mobile)\.)?twitter\.com\/(?P<user>\w+)\/status\/(?P<tweet_id>[0-9]+)\/?(?P<params>\?.*)?$"
TWEET_PROG = None

def check_progs():
    global TWEET_PROG
    if TWEET_PROG is None:
        TWEET_PROG = re.compile(TWEET_RE)

def match_tweet(url):
    global TWEET_PROG
    check_progs()

    return TWEET_PROG.match(url)

def get_tweet_user(url):
    match = match_tweet(url)
    return match.group('user') if match is not None else None

def get_tweet_id(url):
    match = match_tweet(url)
    return match.group('tweet_id') if match is not None else None
