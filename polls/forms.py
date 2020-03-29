from django import forms

class sleepQualityForm(forms.Form):
    sleepQuality = forms.IntegerField(min_value=1,max_value=5)
    sleepDisruptions = forms.CharField(widget=forms.Textarea)
    sleepNotes = forms.CharField(widget=forms.Textarea)
    numDisruptions = forms.IntegerField(min_value = 0)


class calendarForm(forms.Form):
    inputDate = forms.DateField()