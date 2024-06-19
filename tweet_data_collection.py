import tweepy
from dotenv import load_dotenv
import os
import json
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Retrieve API keys and tokens from environment variables
API_KEY = os.getenv('API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Authenticate to Twitter
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Create an API object
api = tweepy.API(auth, wait_on_rate_limit=True)

# Verify authentication
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

# Create a client object for API v2
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Function to get a user by username
def get_user_by_username(username):
    user = client.get_user(username=username)
    return user.data

# Function to get a user's tweets and convert them to a DataFrame
def get_user_tweets_v2(username, max_results=5):
    user = client.get_user(username=username)
    user_id = user.data.id
    tweets = client.get_users_tweets(id=user_id, max_results=max_results, tweet_fields=['created_at', 'public_metrics', 'lang', 'source'])

    if tweets.data is None:
        print(f"No tweets found for user {username}.")
        return None

    # Collect tweet data
    tweet_data = []
    for tweet in tweets.data:
        tweet_info = {
            'Tweet': tweet.text,
            'Created at': tweet.created_at,
            'Retweet count': tweet.public_metrics['retweet_count'],
            'Reply count': tweet.public_metrics['reply_count'],
            'Like count': tweet.public_metrics['like_count'],
            'Quote count': tweet.public_metrics['quote_count'],
            'Bookmark count': tweet.public_metrics['bookmark_count'],
            'Impression count': tweet.public_metrics['impression_count'],
            'Language': tweet.lang,
            'Source': tweet.source
        }
        tweet_data.append(tweet_info)

    # Convert to DataFrame
    df = pd.DataFrame(tweet_data)
    return df

# Get user details (optional, if you need user information)
user = get_user_by_username('elonmusk')
print(f"User: {user.name}, Username: {user.username}, ID: {user.id}")

# Get user tweets and convert them to a DataFrame
df = get_user_tweets_v2('elonmusk', max_results=5)

# Display the DataFrame
print(df)
