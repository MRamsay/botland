from django.core.management.base import BaseCommand

from bots.helpers import format_english_canto_for_twitter, unmark, strip_footnotes, readfile

from urllib.parse import parse_qs
from typing import Dict, List, Text, Pattern, Tuple
import tweepy
import re

# Tweepy login

def get_twitter_credentials() -> Dict:
    '''
        Get twitter credentials
    '''
    twitter_api_key =           readfile('twitter_api_key')
    twitter_api_key_secret =    readfile('twitter_api_key_secret')
    cantobot_credentials =      readfile('cantobot_credentials')

    params: Dict = parse_qs(cantobot_credentials)

    # parsed as list of length 1, so do ['my-cool-string'] -> 'my-cool-string'
    oauth_token, = params['oauth_token']
    oauth_token_secret, = params['oauth_token_secret']

    return twitter_api_key, twitter_api_key_secret, oauth_token, oauth_token_secret,


def get_tweepy_api(twitter_api_key: str, twitter_api_key_secret: str, oauth_token: str, oauth_token_secret: str) -> tweepy.API:

    auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_key_secret)
    # auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_key_secret)
    auth.set_access_token(oauth_token, oauth_token_secret)

    api: tweepy.API = tweepy.API(auth)

    # might fail
    api.verify_credentials()

    return api


def tweepy_connect() -> tweepy.API:

    credentials: Tuple[str, str, str, str] = get_twitter_credentials()
    api = get_tweepy_api(*credentials)

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

        in_reply_to_status_id = None
        for tweet in tweets:
            ret = api.update_status(tweet, in_reply_to_status_id=in_reply_to_status_id, auto_populate_reply_metadata=True)
            in_reply_to_status_id = ret.id

        print(canto)
