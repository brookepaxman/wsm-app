import datetime

from django.db import models
from django.utils import timezone
from django.conf import settings


class Session(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    startDate = models.DateField('date published')
    startTime = models.TimeField()
    status = models.TextField(default="")

class Stat(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sessionID = models.ForeignKey(Session, on_delete=models.CASCADE)
    time = models.IntegerField(default=0)
    hr = models.IntegerField(default=0)
    rr = models.IntegerField(default=0)

class Dummy(models.Model):
    time = models.IntegerField(default=0)
    hr = models.IntegerField(default=0)
    rr = models.IntegerField(default=0)
 

class Analysis(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sessionID = models.ForeignKey(Session, on_delete=models.CASCADE)
    tst = models.TimeField()
    # tst = models.DurationField()
    avgHR = models.IntegerField(default=0)
    avgRR = models.IntegerField(default=0)
    avgHRdip = models.IntegerField(default=0)
    minHR = models.IntegerField(default=0)
    maxHR = models.IntegerField(default=0)
    minRR = models.IntegerField(default=0)
    maxRR = models.IntegerField(default=0)
    sleepQuality = models.IntegerField(default=0)
    sleepDisruptions = models.TextField(default="")
    sleepNotes = models.TextField(default="")
    numSleepDisruptions = models.IntegerField(default=0)
    dailyHR = models.IntegerField(default=0)
    dailyRR = models.IntegerField(default=0)

