from django.http import HttpResponse, HttpResponseRedirect, JsonResponse # noqa: 401
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.views.generic.base import TemplateView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

#from chartjs.views.lines import BaseLineChartView
from rest_framework import viewsets

from .models import User, Stat, Dummy, UserInput, Analysis 

from .serializers import DummySerializer


def signup_view(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('logout')
    return render(request, 'signup.html', {'form': form})
    
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_stats'

    def get_queryset(self):
        name = None
        if self.request.user.is_authenticated:
            name = self.request.user.username
            accessor = User.objects.get(user_name=name)
            return Stat.objects.filter(user=accessor.id).order_by('time')
        else:
            return False


class DetailView(generic.DetailView):
    template_name = 'polls/detail.html'

class DummyView(viewsets.ModelViewSet):
    queryset = Dummy.objects.order_by('time')
    serializer_class = DummySerializer

class ChartView(generic.ListView):
    model = User
    template_name = 'polls/line-chart.html'
    
class UserInputView(generic.ListView):
    model = UserInput
    template_name = 'polls/user_input.html'

    def get(self,request):
        form = sleepQualityForm()
        return render(request, self.template_name, {'form': form})

    
    def post(self,request):
        form = sleepQualityForm(request.POST)
        if form.is_valid():
            name = self.request.user.username
            accessor = User.objects.get(user_name=name)

            sleepQuality = form.cleaned_data['sleepQuality']
            sleepDisruptions = form.cleaned_data['sleepDisruptions']
            sleepNotes = form.cleaned_data['sleepNotes']
            
            form = sleepQualityForm()
            data = UserInput()

            data.sleepQuality = sleepQuality
            data.sleepDisruptions = sleepDisruptions
            data.sleepNotes = sleepNotes
            data.user_id = accessor.id
            data.date = datetime.now()
            data.save()
            args = {'form':form,'sleepQuality':sleepQuality,'sleepDisruptions':sleepDisruptions,'sleepNotes':sleepNotes}
            # args = {'form':form, 'tst':tst, 'avgHR':avgHR, 'avgRR':avgRR, 'avgHRdip':avgHRdip,
            # 'minHR':minHR, 'maxHR':maxHR, 'minRR':minRR,'maxRR':maxRR,'sleepQuality':sleepQuality,
            # 'numSleepDisruptions':numSleepDisruptions, 'sleepDisruptions':sleepDisruptions,'sleepNotes':sleepNotes}
        return render(request, self.template_name, args)
    
class MultiView(TemplateView):
    template_name = 'polls/analysis.html'
    
    def get_context_data(self, **kwargs):
        name = self.request.user.username
        accessor = User.objects.get(user_name=name)
        context = super(MultiView, self).get_context_data(**kwargs)
        context['analysis'] = Analysis.objects.filter(user=accessor.id).order_by('date')
        context['userinput'] = UserInput.objects.filter(user=accessor.id).order_by('date')
        return context 
