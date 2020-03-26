import datetime

from django.db import models
from django.utils import timezone

class Session(models.Model):
    startDate = models.DateField('date published')
    startTime = models.TimeField()

class User(models.Model):
    user_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.user_name

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Stat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sessionID = models.ForeignKey(Session, on_delete=models.CASCADE)
    time = models.IntegerField(default=0)
    hr = models.IntegerField(default=0)
    rr = models.IntegerField(default=0)

class Dummy(models.Model):
    time = models.IntegerField(default=0)
    hr = models.IntegerField(default=0)
    rr = models.IntegerField(default=0)
    sessionID = models.ForeignKey(Session, on_delete=models.CASCADE)
    
class UserInput(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField('date published')
    sleepQuality = models.IntegerField(default=0)
    sleepDisruptions = models.TextField()
    sleepNotes = models.TextField()

class Analysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    date = models.DateTimeField('date published')
    tst = models.TimeField()
    # tst = models.DurationField()
    avgHR = models.IntegerField(default=0)
    avgRR = models.IntegerField(default=0)
    avgHRdip = models.IntegerField(default=0)
    minHR = models.IntegerField(default=0)
    maxHR = models.IntegerField(default=0)
    minRR = models.IntegerField(default=0)
    maxRR = models.IntegerField(default=0)
    numSleepDisruptions = models.IntegerField(default=0)
