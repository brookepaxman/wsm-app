from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from polls.models import Analysis


class SleepQualityForm(forms.Form):
    sleepQuality = forms.IntegerField(widget=forms.NumberInput(attrs={'style': 'width: 50px'}),label="Rate your sleep from 1-5",min_value=1,max_value=5)
    numDisruptions = forms.IntegerField(widget=forms.NumberInput(attrs={'style': 'width: 50px'}),label="Number of sleep disruptions",min_value = 0)
    sleepNotes = forms.CharField(label="Enter notes about your sleep:",widget=forms.Textarea(attrs={'rows':5, 'cols':40}))


class CalendarForm(forms.Form):
    inputDate = forms.ModelChoiceField(label="Select a date", queryset = Analysis.objects.none(),empty_label="No date selected")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CalendarForm, self).__init__(*args, **kwargs)
        qs = Analysis.objects.filter(user=user).order_by('-sessionID__startDate')
        self.fields['inputDate'].queryset = qs


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class StatGeneratorForm(forms.Form):
    startDate = forms.DateField()
    startTime = forms.TimeField()
    numberofEntries = forms.IntegerField(min_value=1)
    
