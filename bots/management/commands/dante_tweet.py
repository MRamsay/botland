from django.core.management.base import BaseCommand

from bots.twitter import assemble_tweets, send_tweet_thread
from pprint import pprint


class Command(BaseCommand):
    help = 'Send tweet'

    def add_arguments(self, parser):
        parser.add_argument('canto',
                            type=int,
                            help='The number of the canto, from 1 to 34')
        parser.add_argument(
            '--scratch',
            action='store_true',
            help='If True, send to test account instead of real one')

    def handle(self, *args, **options):

        current_canto: int = options['canto']
        is_fake: bool = options['scratch']

        tweets = assemble_tweets(current_canto)

        pprint(tweets)

        proceed: str = input('Proceed with sending tweet? [Y/N]: ')

        if proceed.lower() == 'y':
            print('Sending tweet thread')

            send_tweet_thread(tweets, is_fake=is_fake)

            print('Tweet thread sent')

        elif proceed.lower() == 'n':
            print('Tweet aborted')
        else:
            print('Invalid response, will not tweet')
