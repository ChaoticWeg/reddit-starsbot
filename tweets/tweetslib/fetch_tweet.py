from . import creds as __creds
import twitter

## HELPERS

TWITTER_INSTANCE = None

def __create_twitter():
    global TWITTER_INSTANCE
    creds = __creds.get_twitter()
    TWITTER_INSTANCE = twitter.Api(**creds)

def __check_twitter():
    global TWITTER_INSTANCE
    if TWITTER_INSTANCE is None:
        __create_twitter()

## FETCH TWEETS

__FETCH_OPTIONS = {
    "include_entities": False
}

def fetch_tweet_by_id(id):
    """ Fetch a tweet, given its id """
    global TWITTER_INSTANCE
    __check_twitter()
    print(f"fetching tweet: {id}")
    return TWITTER_INSTANCE.GetStatus(id, **__FETCH_OPTIONS)

__FETCH_ALL_OPTIONS = {
    "include_entities": False,
    "map": True
}

def fetch_all_tweets_by_id(ids):
    """ Fetch multiple tweets, given ids """
    global TWITTER_INSTANCE
    __check_twitter()
    print(f"fetching {len(ids)} tweets")
    return TWITTER_INSTANCE.GetStatuses(ids, **__FETCH_ALL_OPTIONS)
