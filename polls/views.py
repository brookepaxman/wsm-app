from django.http import HttpResponse, HttpResponseRedirect # noqa: 401
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import Permission, User 
from django.contrib.contenttypes.models import ContentType

from .models import User, Stat, Dummy, Analysis

def get_sleepQuality(request):
    if request.method == 'POST':
        if request.POST.get('sleepQuality'):
            post = Analysis()
            post.sleepQuality=request.POST.get('sleepQuality')
            post.save()

            return render(request,'/analysis/')
    else:
        return render(request, 'analysis.html')

class SleepForm(generic.ListView):
    template_name = 'polls/saveForm.html'
    model = Analysis
def get_sleepQuality(request):
    if request.method == 'POST':
        if request.POST.get('sleepQuality'):
            post = Post()
            post.sleepQuality=request.POST.get('sleepQuality')
            post.save()

            return render(request,'/analysis/')
    else:
        return render(request, 'analysis.html')

class AnalysisView(generic.ListView):
    model = Analysis
    template_name = 'polls/analysis.html'
    context_object_name = 'latest_stats'

    def get_queryset(self):
        name = None
        if self.request.user.is_authenticated:
            name = self.request.user.username
            accessor = User.objects.get(user_name=name)
            return Analysis.objects.filter(user=accessor.id).order_by('date')
        else:
            return False  


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
    model = User
    template_name = 'polls/detail.html'

class DummyView(generic.ListView):
    model = Dummy
    template_name = 'polls/dummy.html'
    context_object_name = 'latest_stats'

    def get_queryset(self):
        return Dummy.objects.order_by('time')


# class ResultsView(generic.DetailView):
#     model = User
#     template_name = 'polls/results.html'

#
# def vote(request, user_id):
#     question = get_object_or_404(Question, pk=user_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Stats.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'polls/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(
#             reverse('polls:results', args=(question.id,))
#         )
