from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class sleepQualityForm(forms.Form):
    sleepQuality = forms.IntegerField(min_value=1,max_value=5)
    sleepDisruptions = forms.CharField(widget=forms.Textarea)
    sleepNotes = forms.CharField(widget=forms.Textarea)
    numDisruptions = forms.IntegerField(min_value = 0)


class calendarForm(forms.Form):
    inputDate = forms.DateField()

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )