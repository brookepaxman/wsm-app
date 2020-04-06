from django.http import HttpResponse, HttpResponseRedirect, JsonResponse # noqa: 401
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from datetime import datetime
from datetime import timedelta
# from chartjs.views.lines import BaseLineChartView
from rest_framework import viewsets
from .models import User, Stat, Dummy, Analysis, Session
from .forms import sleepQualityForm, calendarForm
from .serializers import StatSerializer, AnalysisSerializer
from numpy import abs
from .serializers import StatSerializer, AnalysisSerializer, StrippedAnalysisSerializer


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
            #name = self.request.user.username
            userid = self.request.user.id 
            #accessor = User.objects.get(user_name=name)
            return Stat.objects.filter(user=userid).order_by('time')
        else:
            return False


class DetailView(generic.DetailView):
    template_name = 'polls/detail.html'

class StatView(viewsets.ModelViewSet):

    def get_queryset(self):         # this returns most recent session of the user that is logged in
        name = None
        if self.request.user.is_authenticated:  # if user is logged in
            userid = self.request.user.id
            #name = self.request.user.username
            #accessor = User.objects.get(user_name=name) # grab all of user's stat objects
            user_allstats = Stat.objects.filter(user=userid).order_by('sessionID__id') # and filter by sessionID
            recent = user_allstats.last()       # grab the most recent sessionID
            recent_Sid = recent.sessionID
            queryset = user_allstats.filter(sessionID=recent_Sid.id).order_by('time')       # filter to only have that sessionID
            return queryset
        else:
            queryset = Stat.objects.order_by('time')
            return queryset

    # queryset = get_queryset()
    # access = User.objects.get(user_name='David')
    # queryset = Stat.objects.filter(user=access.id).order_by('time')
    serializer_class = StatSerializer

class AnalysisSetView(viewsets.ModelViewSet):
    def get_queryset(self):
        #accessor = User.objects.get(user_name="David")
        userid = self.request.user.id
        return Analysis.objects.filter(user=userid).order_by('sessionID')
    serializer_class = AnalysisSerializer

class MonthAnalysisViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        if self.request.user.is_authenticated:
            #name = self.request.user.username
            #accessor = User.objects.get(user_name=name)
            userid = self.request.user.id
        return Analysis.objects.filter(user=userid).order_by('sessionID')[:30]
    serializer_class = StrippedAnalysisSerializer

class ChartView(generic.ListView):
    model = User
    template_name = 'polls/line-chart.html'
    context_object_name = 'queryset'

    def get_queryset(self):     # this is here mostly for debugging purposes
        name = None
        if self.request.user.is_authenticated:
            #name = self.request.user.username
            #accessor = User.objects.get(user_name=name)
            userid = self.request.user.id
            queryset = Stat.objects.filter(user=userid).order_by('time')
            return queryset
        else:
            queryset = Stat.objects.order_by('time')
            return queryset

class UserInputView(generic.ListView):
    model = Analysis
    template_name = 'polls/user_input.html'

    def get(self,request,session_id):
        form = sleepQualityForm()
        if self.request.user.is_authenticated:
            #name = self.request.user.username
            #accessor = User.objects.get(user_name=name)
            userid = self.request.user.id
            s = Session.objects.get(id=session_id)
            args = {'form': form,'s':s,'analysis':Analysis.objects.filter(user=userid,sessionID=s)}
        else:
            args = {'form': form}
        return render(request, self.template_name,args)


    def post(self,request,session_id):
        form = sleepQualityForm(request.POST)
        if form.is_valid():
            #name = self.request.user.username
            #accessor = User.objects.get(user_name=name)
            userid = self.request.user.id

            s = Session.objects.get(id = session_id)

            try:
                data = Analysis.objects.get(sessionID = s)

                data.sleepQuality = form.cleaned_data['sleepQuality']
                data.sleepDisruptions = form.cleaned_data['sleepDisruptions']
                data.sleepNotes = form.cleaned_data['sleepNotes']
                data.numSleepDisruptions = form.cleaned_data['numDisruptions']

                data.save()
                form = sleepQualityForm()
                args = {'form':form,'s':s,'analysis':Analysis.objects.filter(user=userid,sessionID=s)}
            except Analysis.DoesNotExist:
                args = {'form':form}
        return render(request, self.template_name, args)

class MultiView(generic.TemplateView):
    template_name = 'polls/analysis.html'

    def get(self,request):
        form = calendarForm()
        if self.request.user.is_authenticated:
            #name = self.request.user.username
            #accessor = User.objects.get(user_name=name)
            userid = self.request.user.id
            # sess = Session.objects.filter(user=accessor.id)
            args = {'form': form,'analysis':Analysis.objects.filter(user=userid).order_by('id')}
        else:
            args = {'form': form}
        return render(request, self.template_name,args)


    def post(self,request):
        form = calendarForm(request.POST)
        if self.request.user.is_authenticated:
            #name = self.request.user.username
            #accessor = User.objects.get(user_name=name)
            userid = self.request.user.id
            if form.is_valid():
                date = form.cleaned_data['inputDate']
                if not Session.objects.filter(startDate = date).exists():
                    args = {'form':form}
                else:
                    analysisList = Analysis.objects.none()
                    # anal = Analysis.objects.filter(user=accessor.id)
                    # sess = Session.objects.filter(anal__user=accessor.id,startDate = date).distinct()
                    sess = Session.objects.filter(user=userid,startDate = date)
                    for s in sess:
                        a = Analysis.objects.filter(user=userid,sessionID=s)
                        analysisList = a | analysisList
                    analysisList.order_by('sessionID')
                    form = calendarForm()
                    args = {'form':form,'date':date,'analysis':analysisList}
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

    def avgmaxtime(self,data):
        HRsum, RRsum, maxHR, maxRR = 0, 0, 0, 0
        minHR, minRR = 1000, 1000
        skipcount = 0
        datasize = len(data)
        sec = data[datasize-1].time
        if sec > 600:
            sleepindex = 300//4  # approx 5 minute delay
            while sleepindex < datasize:
                if data[sleepindex].hr < 48:
                    skipcount += 1
                    RRsum += data[datasize].rr
                    if maxRR < data[sleepindex].rr:
                        maxRR = data[sleepindex].rr
                    if minRR > data[sleepindex].rr:
                        minRR = data[sleepindex].rr
                    sleepindex += 1
                else:
                    HRsum += data[sleepindex].hr
                    RRsum += data[sleepindex].rr
                    if maxHR < data[sleepindex].hr:
                        maxHR = data[sleepindex].hr
                    if maxRR < data[sleepindex].rr:
                        maxRR = data[sleepindex].rr
                    if minHR > data[sleepindex].hr:
                        minHR = data[sleepindex].hr
                    if minRR > data[sleepindex].rr:
                        minRR = data[sleepindex].rr
                    sleepindex += 1
            HRavg = HRsum/(datasize - sleepindex - skipcount)
            RRavg = RRsum/(datasize - sleepindex)
        else:
            for d in data:
                if d.hr < 48:
                    skipcount += 1
                    RRsum += d.rr
                    if maxRR < d.rr:
                        maxRR = d.rr
                    if minRR > d.rr:
                        minRR = d.rr
                else:
                    HRsum += d.hr
                    RRsum += d.rr
                    if maxHR < d.hr:
                        maxHR = d.hr
                    if maxRR < d.rr:
                        maxRR = d.rr
                    if minHR > d.hr:
                        minHR = d.hr
                    if minRR > d.rr:
                        minRR = d.rr
            HRavg = HRsum/(datasize - skipcount)
            RRavg = RRsum/datasize
        tst = str(timedelta(seconds=sec))
        return HRavg, RRavg, maxHR, minHR, maxRR, minRR, tst

    def dipHR(self, data):
        dipsum = 0
        skipcount = 0
        datasize = len(data)
        sec = data[datasize - 1].time
        if sec > 600:
            sleepindex = 300//4  # approx 5 minute delay
            awake_ref = data[sleepindex].hr
            while sleepindex < datasize:
                if data[sleepindex].hr >= 48:
                    dipsum += abs(awake_ref - data[sleepindex].hr)
                    sleepindex += 1
                else:
                    skipcount += 1
                    sleepindex += 1
            HRdip = dipsum/(datasize - sleepindex - skipcount)
        else:
            try:
                awake_ref = data[10].hr  # close to 75% of 1 minute delay
            except IndexError:
                print("less than 40 seconds of stats data, not enough to accurately calculate heart rate dip")
                return -1
            for d in data:
                if d.hr >= 48:
                    dipsum += abs(awake_ref - d.hr)
                else:
                    skipcount += 1
            HRdip = dipsum/(datasize - skipcount)
        return HRdip

    def get(self, request, session_id):
        if self.request.user.is_authenticated:
            userid = self.request.user
            try:
                session = Session.objects.get(id = session_id)
                if(session.user == userid):
                    if(session.status == "calculate"):
                        try:
                            stat = Analysis.objects.get(sessionID = session)
                        except Analysis.DoesNotExist:
                            stat = Analysis()
                            stat.sessionID = session
                            stat.user = userid
                        if Stat.objects.filter(sessionID = session).exists():
                            stats = Stat.objects.filter(sessionID = session)
                            stat.avgHR, stat.avgRR, stat.maxHR, stat.minHR, stat.maxRR, stat.minRR, stat.tst = AnalysisView.avgmaxtime(self, stats)
                            stat.avgHRdip = AnalysisView.dipHR(self, stats)
                            stat.save()
                            args = {'stat':stat, 'stats':stats}
                        else:
                            args = {'error':"no stats for this session"}
                    elif(session.status == "done"):
                        try:
                            stat = Analysis.objects.get(sessionID = session)
                            args = {'stat':stat}
                        except Analysis.DoesNotExist:
                            args = {'error':"sessions status indicated done, but analysis object doesn't exist, so calc not done"}
                    elif(session.status == "running"):
                        args = {"error": "session is running, please stop device before calculating"}
                    else:
                        args = {'error':"invalid session status"}
                else: 
                    args = {'error':"session doesn't belong to this user"}
            except Session.DoesNotExist:
                args = {'error':"session doesn't exist"}
        else:
            args = {'error':"user not authorized"}
        return render(request, self.template_name, args)
