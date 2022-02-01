from django_cron import CronJobBase, Schedule
from bots.models import TweetRecord
from bots.twitter import post_canto


class DanteTweet(CronJobBase):
    RUN_AT_TIMES = ['14:00': '22:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'bots.dante_tweet'  # a unique code

    def do(self):
        try:
            rec: TweetRecord = TweetRecord.create_next()
            post_canto(rec.series)
        except Exception as e:
            print(str(e))
