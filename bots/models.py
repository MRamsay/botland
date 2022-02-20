from typing import Text
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Language(models.TextChoices):

    ENGLISH = 'en'
    ITALIAN = 'it'


class TweetRecord(models.Model):

    language = models.CharField(max_length=2,
                                choices=Language.choices,
                                default=Language.ENGLISH)

    send_date = models.DateTimeField(default=timezone.now)
    series = models.IntegerField()

    SERIES_MAX = 34

    def create_next(language: Text) -> 'TweetRecord':
        '''
            :param language: one of 'en' or 'it'
        '''

        latest = TweetRecord.objects.filter(
            language=language).order_by('-id').first()
        if not latest:
            return TweetRecord.objects.create(series=1, language=language)
        else:
            next_num = (latest.series % TweetRecord.SERIES_MAX) + 1
            return TweetRecord.objects.create(series=next_num,
                                              language=language)

    def __str__(self):
        return f'{Language(self.language).label} Canto {self.series}'
