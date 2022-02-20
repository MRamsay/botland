import os

from bots.helpers import format_english_canto_for_twitter, readfile
from botland.settings import (TWITTER_API_KEY, TWITTER_API_KEY_SECRET,
                              CANTOBOT_OAUTH_TOKEN,
                              CANTOBOT_OAUTH_TOKEN_SECRET,
                              TWITTER_ACCESS_TOKEN,
                              TWITTER_ACCESS_TOKEN_SECRET)

from typing import List, Text
from bots.helpers import RomanNumeral
import tweepy

# Tweepy login


def tweepy_connect(is_fake: bool) -> tweepy.API:

    if is_fake:
        token = TWITTER_ACCESS_TOKEN
        secret = TWITTER_ACCESS_TOKEN_SECRET
    else:
        token = CANTOBOT_OAUTH_TOKEN
        secret = CANTOBOT_OAUTH_TOKEN_SECRET

    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
    # auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_key_secret)
    auth.set_access_token(token, secret)

    api: tweepy.API = tweepy.API(auth)

    # might fail
    api.verify_credentials()

    return api


def get_canto(canto: int = 1, language: Text = 'en') -> Text:

    if canto > 34 or canto < 1:
        raise ValueError('Invalid canto detected')

    path = 'bots/content/dantebot'
    filepath = f'{path}/canto_{canto}_{language}.md'
    text: Text = readfile(filepath)

    return text


def chunk_for_twitter(content: str) -> List[str]:
    '''
        Break a long piece of text into a series of tweets on newline.
    '''

    TWEET_SIZE = 280  # characters

    lines = content.split('\n')
    tweets = []
    current_tweet = ''
    for line in lines:
        if len(current_tweet) + len(
                line) > TWEET_SIZE - 2:  # including newlines
            tweets.append(current_tweet)
            current_tweet = ''
        current_tweet += '\n' + line
    tweets.append(current_tweet)

    return tweets


def assemble_tweets(number: int, language) -> List[Text]:

    canto = get_canto(number, language)
    if language == 'en':
        canto = format_english_canto_for_twitter(canto)
    tweets = chunk_for_twitter(canto)

    header = ''

    if language == 'en':
        header = f'DANTE\'S INFERNO: CANTO {RomanNumeral(number)}\n#Poetry #Dante #Inferno'
    elif language == 'it':
        header = f'LA DIVINA COMMEDIA: INFERNO, CANTO {RomanNumeral(number)}\n#Poesia #Poetry #Dante #Inferno'

    tweets = [header] + tweets

    return tweets


def send_tweet_thread(number: int, tweets: List[Text], is_fake=False):

    api = tweepy_connect(is_fake)

    in_reply_to_status_id = None
    for idx, tweet in enumerate(tweets):

        filepath = f'bots/images/dantebot/canto_{number}.{idx}.jpg'
        if os.path.isfile(filepath):
            ret = api.update_status_with_media(
                tweet, filepath, in_reply_to_status_id=in_reply_to_status_id)
        else:
            ret = api.update_status(
                tweet,
                in_reply_to_status_id=in_reply_to_status_id,
                auto_populate_reply_metadata=True)
        in_reply_to_status_id = ret.id


def post_canto(number: int, is_fake=True, language='en'):
    tweets = assemble_tweets(number, language)
    send_tweet_thread(number, tweets, is_fake=is_fake)
