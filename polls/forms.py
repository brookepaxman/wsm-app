from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.forms.widgets import SelectDateWidget
from django.contrib.admin.widgets import AdminDateWidget

from polls.models import Analysis

FRUIT_CHOICES= [
    ('03/25/2020', 'March 25, 2020'),
    ('03/26/2020', 'March 26, 2020'),
    ('03/27/2020', 'March 27, 2020'),
    ('03/28/2020', 'March 28, 2020'),
    ('03/29/2020', 'March 29, 2020'),
    ('03/30/2020', 'March 30, 2020'),
    ('03/31/2020', 'March 31, 2020')
    ]


class sleepQualityForm(forms.Form):
    sleepQuality = forms.IntegerField(widget=forms.NumberInput(attrs={'style': 'width: 50px'}),label="Rate your sleep from 1-5",min_value=1,max_value=5)
    numDisruptions = forms.IntegerField(widget=forms.NumberInput(attrs={'style': 'width: 50px'}),label="Number of sleep disruptions",min_value = 0)
    sleepNotes = forms.CharField(label="Enter notes about your sleep:",widget=forms.Textarea(attrs={'rows':5, 'cols':40}))


class calendarForm(forms.Form):
    # inputDate = forms.DateField(label="Date",widget=SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")))
    
    inputDate = forms.DateField(label="Select a date", widget=forms.Select(choices=FRUIT_CHOICES))
    
    # inputDate = forms.ModelChoiceField(queryset=Analysis.objects.none())

    # def __init__(self, user, *args, **kwargs):
    #     super(calendarForm, self).__init__(*args, **kwargs)
    #     qs = Analysis.objects.filter(user=user)
    #     self.fields['inputDate'].queryset = qs



class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class statGeneratorForm(forms.Form):
    startDate = forms.DateField()
    startTime = forms.TimeField()
    numberofEntries = forms.IntegerField(min_value=1)
    
