from django import forms
from django.forms.widgets import SelectDateWidget
from django.contrib.admin.widgets import AdminDateWidget

class sleepQualityForm(forms.Form):
    sleepQuality = forms.IntegerField(label="Rate your sleep from 1-5",min_value=1,max_value=5)
    sleepDisruptions = forms.CharField(label="Log any sleep disruptions",widget=forms.Textarea)
    sleepNotes = forms.CharField(label="Log any general notes about your sleep",widget=forms.Textarea)
    numDisruptions = forms.IntegerField(label="Log the number of sleep disruptions",min_value = 0)


class calendarForm(forms.Form):
    inputDate = forms.DateField(label="Date",widget=SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")))
