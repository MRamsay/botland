from django.core.management.base import BaseCommand

from bots.helpers import format_english_canto_for_twitter, readfile
from botland.settings import TWITTER_API_KEY, TWITTER_API_KEY_SECRET, CANTOBOT_OAUTH_TOKEN, CANTOBOT_OAUTH_TOKEN_SECRET

from urllib.parse import parse_qs
from typing import Dict, List, Text, Tuple
import tweepy

# Tweepy login

def tweepy_connect() -> tweepy.API:

    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
    # auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_key_secret)
    auth.set_access_token(CANTOBOT_OAUTH_TOKEN, CANTOBOT_OAUTH_TOKEN_SECRET)

    api: tweepy.API = tweepy.API(auth)

    # might fail
    api.verify_credentials()

    return api


def get_canto(canto: int = 1) -> Text:

    if canto > 34 or canto < 1:
        raise ValueError('Invalid canto detected')

    path = 'bots/content/dantebot'
    english_file = f'{path}/canto_{canto}_en.md'
    english: Text = readfile(english_file)

    return english


def chunk_for_twitter(content: str) -> List[str]:
    '''
        Break a long piece of text into a series of tweets on newline.
    '''

    TWEET_SIZE = 280 # characters

    lines = content.split('\n')
    tweets = []
    current_tweet = ''
    for line in lines:
        if len(current_tweet) + len(line) > TWEET_SIZE-2: # including newlines
            tweets.append(current_tweet)
            current_tweet = ''
        current_tweet += '\n' + line
    tweets.append(current_tweet)

    return tweets

class Command(BaseCommand):
    help = 'Send tweet'

    def handle(self, *args, **options):

        current_canto = 5

        canto = get_canto(current_canto)
        canto = format_english_canto_for_twitter(canto)
        tweets = chunk_for_twitter(canto)

        print(tweets)

        api = tweepy_connect()

        # in_reply_to_status_id = None
        # for tweet in tweets:
        #     ret = api.update_status(tweet, in_reply_to_status_id=in_reply_to_status_id, auto_populate_reply_metadata=True)
        #     in_reply_to_status_id = ret.id

        print(canto)
