from dotenv import load_dotenv
import os

__KEYS = [
    "REDDIT_CLIENT_ID",
    "REDDIT_CLIENT_SECRET",
    "REDDIT_USERNAME",
    "REDDIT_PASSWORD",
    "REDDIT_USER_AGENT"
]

def get():
    load_dotenv()
    result = {}

    for name in __KEYS:
        value = os.getenv(name)
        if value is None:
            raise Exception(f"missing env for cred: {name}")
        name_key = name.lower()[7:]
        result[name_key] = value
    
    return result

