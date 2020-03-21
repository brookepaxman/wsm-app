from django import forms

class sleepQualityForm(forms.Form):
    tst = forms.TimeField()
    avgHR = forms.IntegerField()
    avgRR = forms.IntegerField()
    avgHRdip = forms.IntegerField()
    minHR = forms.IntegerField()
    maxHR = forms.IntegerField()
    minRR = forms.IntegerField()
    maxRR = forms.IntegerField()
    sleepQuality = forms.IntegerField()
    numSleepDisruptions = forms.IntegerField()
    sleepDisruptions = forms.CharField()
    sleepNotes = forms.CharField()
