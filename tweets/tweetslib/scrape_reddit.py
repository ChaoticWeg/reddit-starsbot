import os

__CREDS_KEYS = [ "REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USERNAME", "REDDIT_PASSWORD", "REDDIT_USER_AGENT" ]

def __get_creds(user_agent=None):
    result = {}

    for name in __CREDS_KEYS:

        # get value from environ
        value = os.getenv(name)
        if value is None:
            raise Exception(f"missing value for credential env: {name}")

        # convert to PRAW kwargs-friendly dict
        name_key = name.lower()[7:]
        result[name_key] = value
    
    return result
    
def get_tweet_posts():
    creds = __get_creds()
    print(creds)
    return None
