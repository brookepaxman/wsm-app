from django.http import HttpResponse, HttpResponseRedirect, JsonResponse # noqa: 401
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from datetime import datetime
from datetime import timedelta
# from chartjs.views.lines import BaseLineChartView
from rest_framework import viewsets

from .models import User, Stat, Dummy, UserInput, Analysis, Session
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

    def get(self,request,session_id):
        form = sleepQualityForm()
        if self.request.user.is_authenticated:
            name = self.request.user.username
            accessor = User.objects.get(user_name=name)
            s = Session.objects.get(id=session_id)
            args = {'form': form,'s':s,'analysis':Analysis.objects.filter(user=accessor.id,sessionID=s).order_by('date'),
            'userinput':UserInput.objects.filter(user=accessor.id,sessionID=s).order_by('date')}
        else:
            args = {'form': form}
        return render(request, self.template_name,args)

    
    def post(self,request,session_id):
        form = sleepQualityForm(request.POST)
        if form.is_valid():
            name = self.request.user.username
            accessor = User.objects.get(user_name=name)

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
            form = sleepQualityForm()
            args = {'form':form,'s':s,'analysis':Analysis.objects.filter(user=accessor.id,sessionID=s).order_by('date'),
            'userinput':UserInput.objects.filter(user=accessor.id,sessionID=s).order_by('date')}
        return render(request, self.template_name, args)
    
class MultiView(generic.TemplateView):
    template_name = 'polls/analysis.html'
    
    def get(self,request):
        form = calendarForm()
        if self.request.user.is_authenticated:
            name = self.request.user.username
            accessor = User.objects.get(user_name=name)
            sess = Session.objects.filter(user=accessor.id)
            args = {'form': form,'sess':sess,'analysis':Analysis.objects.filter(user=accessor.id).order_by('date'),
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
                date = form.cleaned_data['inputDate']
                if(not Session.objects.filter(startDate = date).exists()):
                    args = {'form':form}
                else: 
                    analysisList = Analysis.objects.none()
                    userInputList = UserInput.objects.none()
                    sess = Session.objects.filter(user=accessor.id,startDate = date)
                    for s in sess:
                        a = Analysis.objects.filter(user=accessor.id,sessionID=s)
                        u = UserInput.objects.filter(user=accessor.id,sessionID=s)
                        analysisList = a | analysisList
                        userInputList = u | userInputList
                    analysisList.order_by('sessionID')
                    userInputList.order_by('sessionID')
                    form = calendarForm()
                    args = {'form':form,'date':date,'analysis':analysisList,'userinput':userInputList}
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


class AnalysisView(generic.ListView):
    model = Analysis
    template_name = 'polls/calculate.html'

    def avg(self,data):
        HRsum = 0
        RRsum = 0
        maxHR = 0
        maxRR = 0
        minHR = 1000
        minRR = 1000
        datasize = len(data)
        for d in data:
            HRsum += d.hr
            RRsum += d.rr
            if(maxHR < d.hr):
                maxHR = d.hr
            if(maxRR < d.rr):
                maxRR = d.rr
            if(minHR > d.hr):
                minHR = d.hr
            if(minRR > d.rr): 
                minRR = d.rr
        HRavg = HRsum/datasize
        RRavg = RRsum/datasize
        sec = data[datasize-1].time
        tst = str(timedelta(seconds=sec))
        return HRavg,RRavg, maxHR, minHR, maxRR, minRR, tst

    def get(self,request,session_id):
        if self.request.user.is_authenticated:
            name = self.request.user.username
            accessor = User.objects.get(user_name=name)
            session = Session.objects.get(id = session_id)
            stats = Stat.objects.filter(sessionID = session)

            try:
                calc = Analysis.objects.get(sessionID_id = session_id)
            except UserInput.DoesNotExist:
                calc = Analysis()
                calc.sessionID_id = session_id

            calc.avgHR, calc.avgRR, calc.maxHR, calc.minHR, calc.maxRR, calc.minRR, calc.tst = AnalysisView.avg(self,stats)

            calc.user_id = accessor.id
            calc.date = datetime.now()
            calc.numSleepDisruptions = 1
            calc.avgHRdip = 2
            calc.save()
            
        return render(request,self.template_name, {'stat':calc})
