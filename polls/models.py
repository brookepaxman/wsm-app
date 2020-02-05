import datetime

from django.db import models
from django.utils import timezone


class User(models.Model):
    user_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.user_name

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Stat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField('date published')
    hr = models.IntegerField(default=0)
    rr = models.IntegerField(default=0)
