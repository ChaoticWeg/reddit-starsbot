import tweetslib
from os import path, getenv

## HELPERS

def get_data_file(filename):
    """ Get a fully-qualified path to a file in the data folder """
    return path.join(path.dirname(path.abspath(__file__)), 'data', filename)

def post_unfurled_tweet(submission, tweet):
    """ Post an unfurled tweet """
    print(f"posting unfurled tweet '{tweet.id}' as comment on submission '{submission.id}'")
    formatted_text = tweetslib.format_tweet_text(tweet)
    footer = tweetslib.reddit_footer()
    comment_text = f"Linked tweet:\n\n{formatted_text}\n\n{footer}\n"
    tweetslib.post_and_sticky(submission, comment_text)

def post_unfurled_retweet(submission, tweet, retweeted):
    """ Post an unfurled retweet """
    print(f"posting unfurled retweet '{retweeted.id}' as comment on submission '{submission.id}'")
    formatted_text = tweetslib.format_tweet_text(retweeted)
    footer = tweetslib.reddit_footer()
    comment_text = f"Retweeted by {tweet.user.name} (@{tweet.user.screen_name}):\n\n{formatted_text}\n\n{footer}\n"
    tweetslib.post_and_sticky(submission, comment_text)

## MAIN EXECUTION GO

def run():
    """ Main executing function """
    # read subreddit from env
    subreddit = tweetslib.get_target_subreddit()
    tweet_posts = tweetslib.get_tweet_posts(subreddit)

    # read known post ids from data folder
    known_post_ids = tweetslib.read(get_data_file('known_posts.json'), default=[])

    # filter out known posts
    unknown_posts = [post for post in tweet_posts if not post.id in known_post_ids]
    unknown_tweet_ids = [tweetslib.get_tweet_id(post.url) for post in unknown_posts]
    unknown_tweet_ids = [t_id for t_id in unknown_tweet_ids if t_id is not None]

    # fetch tweets from unknown posts
    tweets = tweetslib.fetch_all_tweets_by_id(unknown_tweet_ids)

    # handle posts
    for post in unknown_posts:
        # pull tweet from recently fetched
        tweet_id = tweetslib.get_tweet_id(post.url)
        print(f"post {post.id} needs unfurled || tweet id: {tweet_id}")

        # handle tweet or retweet
        tweet = tweets[int(tweet_id)]
        if tweet.retweeted_status is None:
            post_unfurled_tweet(post, tweet)
        else:
            post_unfurled_retweet(post, tweet, tweet.retweeted_status)
    
    # add previously-unknown posts to list of now-known posts and write to disk
    unknown_post_ids = [post.id for post in unknown_posts]
    known_post_ids.extend(unknown_post_ids)
    tweetslib.write(known_post_ids, get_data_file('known_posts.json'))

## EXECUTION GUARD

if __name__ == "__main__":
    run()
