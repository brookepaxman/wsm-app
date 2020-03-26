from django.http import HttpResponse, HttpResponseRedirect, JsonResponse # noqa: 401
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from datetime import datetime
# from chartjs.views.lines import BaseLineChartView
from rest_framework import viewsets

from .models import User, Stat, Dummy, UserInput, Analysis
from .forms import sleepQualityForm, calendarForm

from .serializers import DummySerializer


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
        return render(request, self.template_name, args)
    
class MultiView(generic.TemplateView):
    template_name = 'polls/analysis.html'
    
    def get(self,request):
        form = calendarForm()
        name = self.request.user.username
        accessor = User.objects.get(user_name=name)

        return render(request, self.template_name, {'form': form,'analysis':Analysis.objects.filter(user=accessor.id).order_by('date'),
        'userinput':UserInput.objects.filter(user=accessor.id).order_by('date')})

    
    def post(self,request):
        form = calendarForm(request.POST)
        name = self.request.user.username
        accessor = User.objects.get(user_name=name)
        if form.is_valid():
            txt = form.cleaned_data['inputDate']
            args = {'form':form,'txt':txt,'analysis':Analysis.objects.filter(user=accessor.id),
        'userinput':UserInput.objects.filter(user=accessor.id).order_by('date')}
        return render(request, self.template_name, args)

    def get_context_data(self, **kwargs):
        name = self.request.user.username
        accessor = User.objects.get(user_name=name)
        context = super(MultiView, self).get_context_data(**kwargs)
        context['analysis'] = Analysis.objects.filter(user=accessor.id).order_by('date')
        context['userinput'] = UserInput.objects.filter(user=accessor.id).order_by('date')
        return context 
