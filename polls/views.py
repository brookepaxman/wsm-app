from django.http import HttpResponse, HttpResponseRedirect, JsonResponse # noqa: 401
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import login, authenticate

from datetime import datetime
from datetime import date
from datetime import timedelta
# from chartjs.views.lines import BaseLineChartView
from rest_framework import viewsets
from .models import User, Stat, Dummy, Analysis, Session
from .forms import sleepQualityForm, calendarForm, statGeneratorForm, SignUpForm
from numpy import abs
from .serializers import StatSerializer, AnalysisSerializer, StrippedAnalysisSerializer, SessionSerializer
import random

def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('logout')
    else:
        form = SignUpForm()
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

class GenerateView(generic.FormView):
    template_name = 'polls/generate.html'
    def get(self,request):
        form = statGeneratorForm()
        userid = self.request.user.id
        args = {'form': form}
        return render(request, self.template_name, args)


    def post(self,request):
        form = statGeneratorForm(request.POST)
        test = 'a'
        if self.request.user.is_authenticated:
            userid = self.request.user.id
            test = 'ab'
            if form.is_valid():
                new_sess = Session()
                new_sess.startDate = form.cleaned_data['startDate']
                new_sess.startTime = form.cleaned_data['startTime']
                # c_user = User.objects.get(id=userid)
                new_sess.user = self.request.user
                new_sess.save()
                entries = form.cleaned_data['numberofEntries']
                time = random.randint(0, 4)
                test = 'abc'
                new_sess.status = 'running'
                oldhr = random.randint(48, 84)
                oldrr = random.randint(5, 25)
                for e in range(0, entries):
                    new_stat = Stat()
                    new_stat.sessionID = new_sess
                    new_stat.user = self.request.user
                    new_stat.time = 72*e + time
                    if (oldhr < 49) | (oldhr > 83):
                        new_stat.hr = random.randint(48, 84)
                    else:
                        new_stat.hr = oldhr + random.randint(-3, 3)
                    if (oldrr < 6) | (oldrr > 24):
                        new_stat.rr = random.randint(5, 25)
                    else:
                        new_stat.rr = oldrr + random.randint(-2, 2)
                    oldhr = new_stat.hr
                    oldrr = new_stat.rr
                    new_stat.save()
                    if e == entries-1:
                        test = 'Success!'
                        new_sess.status = 'calculate'
                new_sess.save()
                args = {'form':form, 'test':test}
        return render(request, self.template_name, args)

class DetailView(generic.DetailView):
    template_name = 'polls/detail.html'

class StatView(viewsets.ModelViewSet):
    def get_queryset(self):         # this returns most recent session of the user that is logged in
        if self.request.user.is_authenticated:  # if user is logged in
            userid = self.request.user.id
            user_allstats = Stat.objects.filter(user=userid).order_by('sessionID__startDate') # and filter by sessionID
            recent = user_allstats.last()       # grab the most recent sessionID
            recent_Sid = recent.sessionID
            queryset = user_allstats.filter(sessionID=recent_Sid.id).order_by('time')       # filter to only have that sessionID
            return queryset
        else:
            return False

    # queryset = get_queryset()
    # access = User.objects.get(user_name='David')
    # queryset = Stat.objects.filter(user=access.id).order_by('time')
    serializer_class = StatSerializer

class AnalysisSetView(viewsets.ModelViewSet):
    def get_queryset(self):
        if self.request.user.is_authenticated:
            userid = self.request.user.id
        userAnalysisAll = Analysis.objects.filter(user=userid).order_by('sessionID__startDate')
        dateCutoff = date.today() - timedelta(days=7)
        userAnalysisWeek = userAnalysisAll.filter(sessionID__startDate__gte=dateCutoff).order_by('-sessionID')
        week_set = {} # ^^ assumes that sessions are being calculated in order

        for analysis in userAnalysisWeek:
            print(analysis.sessionID)
            if week_set.get(analysis.sessionID.startDate, False):
                print("excluded: "+ str(analysis.sessionID))
                userAnalysisWeek = userAnalysisWeek.exclude(id=analysis.id)
            else:
                week_set[analysis.sessionID.startDate] = True
        # theset = userAnalysisWeek.distinct("sessionID__startDate")
        userAnalysisWeek = userAnalysisWeek.reverse()
        print(week_set)
        return userAnalysisWeek
    serializer_class = AnalysisSerializer

class MonthAnalysisViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        month = self.request.query_params.get('month')
        if self.request.user.is_authenticated:
            userid = self.request.user.id
            queryset = Analysis.objects.filter(user=userid).filter(sessionID__startDate__month=month).order_by('-sessionID')
            month_set = {}

            for analysis in queryset:
                print(analysis.sessionID)
                if month_set.get(analysis.sessionID.startDate, False):
                    print("excluded: "+ str(analysis.sessionID))
                    queryset = queryset.exclude(id=analysis.id)
                else:
                    month_set[analysis.sessionID.startDate] = True
            # theset = userAnalysisWeek.distinct("sessionID__startDate")
            queryset = queryset.order_by('sessionID__startDate')
            # print(month_set)
            return queryset
    serializer_class = StrippedAnalysisSerializer

class ChartView(generic.ListView):
    model = User
    template_name = 'polls/graphs.html'
    context_object_name = 'queryset'

    def get_queryset(self):# this is here mostly for debugging purposes
        name = None
        if self.request.user.is_authenticated:
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
            args = {'form': form,'s':s,'stat':Analysis.objects.get(user=userid,sessionID=s)}
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
                data.sleepNotes = form.cleaned_data['sleepNotes']
                data.numSleepDisruptions = form.cleaned_data['numDisruptions']

                data.save()
                form = sleepQualityForm()
                args = {'form':form,'s':s,'stat':Analysis.objects.get(user=userid,sessionID=s)}
            except Analysis.DoesNotExist:
                args = {'form':form}
        return render(request, self.template_name, args)

class MultiView(generic.TemplateView):
    template_name = 'polls/analysis.html'


    def get(self,request):
        if self.request.user.is_authenticated:
            form = calendarForm()
            #name = self.request.user.username
            #accessor = User.objects.get(user_name=name)
            userid = self.request.user.id
            # sess = Session.objects.filter(user=accessor.id)
        
            args = {'form': form,'stats':Analysis.objects.filter(user=userid).order_by('-id')}
            # args = {'form': form,'stats':Analysis.objects.filter(user=userid).order_by('id').last()}
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
                    args = {'form':form,'date':date,'stats':analysisList}
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
                    RRsum += data[sleepindex].rr
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
            HRavg = HRsum/(datasize - 75 - skipcount)
            RRavg = RRsum/(datasize - 75)
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
            HRdip = dipsum/(datasize - 75 - skipcount)
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
                        daily_date = session.startDate
                        try:
                            stat = Analysis.objects.get(sessionID = session)
                        except Analysis.DoesNotExist:
                            stat = Analysis()
                            stat.sessionID = session
                            stat.user = userid

                        if Stat.objects.filter(sessionID = session).exists():
                            stats = Stat.objects.filter(sessionID = session).order_by('time')
                            stats_day = Stat.objects.filter(sessionID__startDate=daily_date, user=userid)
                            stat.avgHR, stat.avgRR, stat.maxHR, stat.minHR, stat.maxRR, stat.minRR, stat.tst = AnalysisView.avgmaxtime(self, stats)
                            stat.dailyHR, stat.dailyRR, e1, e2, e3, e4, e5 = AnalysisView.avgmaxtime(self, stats_day)
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

class RealtimeView(generic.ListView):
    template_name = 'polls/realtime.html'
    context_object_name = 'latest_stat'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            userid = self.request.user.id
            latestSession = Session.objects.filter(user=userid).latest('id')
            print(latestSession.id)
            print(latestSession.status)
            latestStat = Stat.objects.filter(user=userid, sessionID=latestSession.id).latest('time')
            print(latestStat.hr)
            print(latestStat.rr)
            print(latestStat.sessionID)
            if latestSession.status == "running":
                return Stat.objects.filter(user=userid, sessionID=latestSession.id).latest('time')
            else:
                return False
        else:
            return False
