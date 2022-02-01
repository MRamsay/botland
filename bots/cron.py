from django_cron import CronJobBase, Schedule
from bots.models import TweetRecord
from bots.twitter import post_canto


class DanteTweet(CronJobBase):
    RUN_EVERY_MINS = 60 * 24  # Once Daily

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bots.dante_tweet'  # a unique code

    def do(self):
        try:
            rec: TweetRecord = TweetRecord.create_next()
            post_canto(rec.series)
        except Exception as e:
            print(str(e))
