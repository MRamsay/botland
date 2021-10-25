from django.core.management.base import BaseCommand

from bots.helpers import unmark, strip_footnotes, readfile

from urllib.parse import parse_qs
from typing import Dict, Text, Pattern
import tweepy
import re

class Command(BaseCommand):
    help = 'Send tweet'

    def handle(self, *args, **options):

        canto = 1

        path = 'bots/content/dantebot'
        english_file = f'{path}/canto_{canto}_en.md'
        english: Text = readfile(english_file)

        # Add a newline to each verse triplet
        # NOTE: Every verse triplet starts without indenting
        start_of_english_triplet_re: Pattern = re.compile(r'\n\s\s(\S)')
        an_extra_newline_re = r'\n\n\g<1>'
        english = re.sub(start_of_english_triplet_re, an_extra_newline_re, english)

        line_number_marker_re: Pattern = re.compile('\d{2,3}(\n|$)')
        english = re.sub(line_number_marker_re, '\n', english)

        english = unmark(strip_footnotes(english))
        english = re.sub('   ', '', english)
        english = re.sub('\n ', '\n', english)

        twitter_api_key =           readfile('twitter_api_key')
        twitter_api_key_secret =    readfile('twitter_api_key_secret')
        cantobot_credentials =      readfile('cantobot_credentials')

        params: Dict = parse_qs(cantobot_credentials)

        # parsed as list of length 1, so do ['my-cool-string'] -> 'my-cool-string'
        oauth_token, = params['oauth_token']
        oauth_token_secret, = params['oauth_token_secret']

        auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_key_secret)
        # auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_key_secret)
        auth.set_access_token(oauth_token, oauth_token_secret)

        api: tweepy.API = tweepy.API(auth)

        lines = english.split('\n')
        tweets = []
        current_tweet = ''
        for line in lines:
            if len(current_tweet) + len(line) > 280-2: # including newlines
                tweets.append(current_tweet)
                current_tweet = ''
            else:
                current_tweet += '\n' + line
        tweets.append(current_tweet)

        try:
            api.verify_credentials()
            print("Authentication OK")
        # TODO: catch specific error
        except:
            print("Error during authentication")
        else:

            # in_reply_to_status_id = None
            # for tweet in tweets:
            #     ret = api.update_status(tweet, in_reply_to_status_id=in_reply_to_status_id, auto_populate_reply_metadata=True)
            #     in_reply_to_status_id = ret.id

            # ret = api.update_status(tweet[:280])
            print(english)
