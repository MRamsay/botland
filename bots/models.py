from django.db import models
from django.utils import timezone


class TweetRecord(models.Model):

    send_date = models.DateTimeField(default=timezone.now)
    series = models.IntegerField()

    SERIES_MAX = 34

    def create_next() -> 'TweetRecord':

        latest = TweetRecord.objects.order_by('-id').first()
        if not latest:
            return TweetRecord.objects.create(series=1)
        else:
            next_num = (latest.series % TweetRecord.SERIES_MAX) + 1
            return TweetRecord.objects.create(series=next_num)
