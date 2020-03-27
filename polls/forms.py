from django import forms

class sleepQualityForm(forms.Form):
    sleepQuality = forms.IntegerField(min_value=1,max_value=5)
    sleepDisruptions = forms.CharField(widget=forms.Textarea)
    sleepNotes = forms.CharField(widget=forms.Textarea)


class calendarForm(forms.Form):
    inputDate = forms.DateField()