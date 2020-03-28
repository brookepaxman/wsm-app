from django.http import HttpResponse, HttpResponseRedirect, JsonResponse # noqa: 401
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from datetime import datetime
# from chartjs.views.lines import BaseLineChartView
from rest_framework import viewsets

from .models import User, Stat, Dummy, UserInput, Analysis, Session
from .forms import sleepQualityForm, calendarForm

from .serializers import StatSerializer


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

class StatView(viewsets.ModelViewSet):
    queryset = Stat.objects.order_by('time')
    serializer_class = StatSerializer

class ChartView(generic.ListView):
    model = User
    template_name = 'polls/line-chart.html'
    
class UserInputView(generic.ListView):
    model = UserInput
    template_name = 'polls/user_input.html'

    def get(self,request,session_id):
        form = sleepQualityForm()
        if self.request.user.is_authenticated:
            name = self.request.user.username
            accessor = User.objects.get(user_name=name)
            s = Session.objects.get(id=session_id)
            args = {'form': form,'analysis':Analysis.objects.filter(user=accessor.id,sessionID=s).order_by('date'),
            'userinput':UserInput.objects.filter(user=accessor.id,sessionID=s).order_by('date')}
        else:
            args = {'form': form}
        return render(request, self.template_name,args)

    
    def post(self,request,session_id):
        form = sleepQualityForm(request.POST)
        if form.is_valid():
            name = self.request.user.username
            accessor = User.objects.get(user_name=name)

            form = sleepQualityForm()
            s = Session.objects.get(id = session_id)

            try:
                data = UserInput.objects.get(sessionID = s)
            except UserInput.DoesNotExist:
                data = UserInput()
                data.sessionID = s

            data.sleepQuality = form.cleaned_data['sleepQuality']
            data.sleepDisruptions = form.cleaned_data['sleepDisruptions']
            data.sleepNotes = form.cleaned_data['sleepNotes']
            data.user_id = accessor.id
            data.date = datetime.now()
            data.save()
            args = {'form':form,'analysis':Analysis.objects.filter(user=accessor.id,sessionID=s).order_by('date'),
            'userinput':UserInput.objects.filter(user=accessor.id,sessionID=s).order_by('date')}
        return render(request, self.template_name, args)
    
class MultiView(generic.TemplateView):
    template_name = 'polls/analysis.html'
    
    def get(self,request):
        form = calendarForm()
        if self.request.user.is_authenticated:
            name = self.request.user.username
            accessor = User.objects.get(user_name=name)
            args = {'form': form,'analysis':Analysis.objects.filter(user=accessor.id).order_by('date'),
            'userinput':UserInput.objects.filter(user=accessor.id).order_by('date')}
            
        else:
            args = {'form': form}
        return render(request, self.template_name,args)

    
    def post(self,request):
        form = calendarForm(request.POST)
        if self.request.user.is_authenticated:
            name = self.request.user.username
            accessor = User.objects.get(user_name=name)
            if form.is_valid():
                txt = form.cleaned_data['inputDate']
                if(not Session.objects.filter(startDate = txt).exists()):
                    args = {'form':form}
                else: 
                    q = Analysis.objects.none()
                    a = UserInput.objects.none()
                    sess = Session.objects.filter(user=accessor.id,startDate = txt)
                    for s in sess:
                        obj = Analysis.objects.filter(user=accessor.id,sessionID=s).order_by('date')
                        objs = UserInput.objects.filter(user=accessor.id,sessionID=s).order_by('date')
                        q = obj | q
                        a = objs | a
                    args = {'form':form,'txt':txt,'analysis':q,'userinput':a}
        else:
            form = calendarForm()
            args = {'form':form}
        return render(request, self.template_name, args)

        
    # def get_context_data(self, **kwargs):
    #     name = self.request.user.username
    #     accessor = User.objects.get(user_name=name)
    #     context = super(MultiView, self).get_context_data(**kwargs)
    #     context['analysis'] = Analysis.objects.filter(user=accessor.id).order_by('date')
    #     context['userinput'] = UserInput.objects.filter(user=accessor.id).order_by('date')
    #     return context 
