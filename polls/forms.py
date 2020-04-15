from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.forms.widgets import SelectDateWidget

from polls.models import Analysis


class sleepQualityForm(forms.Form):
    sleepQuality = forms.IntegerField(widget=forms.NumberInput(attrs={'style': 'width: 50px'}),label="Rate your sleep from 1-5",min_value=1,max_value=5)
    numDisruptions = forms.IntegerField(widget=forms.NumberInput(attrs={'style': 'width: 50px'}),label="Number of sleep disruptions",min_value = 0)
    sleepNotes = forms.CharField(label="Enter notes about your sleep:",widget=forms.Textarea(attrs={'rows':5, 'cols':40}))


class calendarForm(forms.ModelForm):
    # inputDate = forms.DateField(label="Date",widget=SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")))
    # inputDate = forms.DateField(label="Select a date", widget=forms.Select(choices = None))
    inputDate = forms.ModelChoiceField(label="Select a date", queryset = None, empty_label="No date selected")
    


    # def __init__(self, user, *args, **kwargs):
    #     super(calendarForm, self).__init__(*args, **kwargs)
    #     self.fields['inputDate'] = forms.ChoiceField(
    #         choices=[(o, str(o)) for o in Analysis.objects.filter(user=user).order_by('sessionID__startDate')]
    #     )

    # def __init__(self, user, *args, **kwargs):
    #         super(calendarForm, self).__init__(*args, **kwargs)
    #         qs = Analysis.objects.filter(user=user).order_by('sessionID__startDate')
    #         self.fields['inputDate'].queryset = qs

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['inputDate']
        if request:
            user = request.user
            self.fields['inputDate'].queryset = Analysis.objects.filter(user=user).order_by('sessionID__startDate')
        

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
    
