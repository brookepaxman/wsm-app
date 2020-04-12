from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.forms.widgets import SelectDateWidget
from django.contrib.admin.widgets import AdminDateWidget

class sleepQualityForm(forms.Form):
    sleepQuality = forms.IntegerField(label="Rate your sleep from 1-5",min_value=1,max_value=5)
    numDisruptions = forms.IntegerField(label="Number of sleep disruptions",min_value = 0)
    sleepNotes = forms.CharField(label="Enter notes about your sleep:",widget=forms.Textarea)
    # inputDate = forms.DateField(widget=forms.SelectDateWidget(years=[1990,1991,1992]))
    # sleepNotes = forms.CharField(widget=forms.TextInput(attrs={'size': 50}))


class calendarForm(forms.Form):
    inputDate = forms.DateField(label="Date",widget=SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")))

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
    
