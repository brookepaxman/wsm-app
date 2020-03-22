from django.http import HttpResponse, HttpResponseRedirect # noqa: 401
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import Permission, User 
from django.contrib.contenttypes.models import ContentType
from django.views.generic import TemplateView

from datetime import datetime
from .models import User, Stat, Dummy, Analysis, UserInput
from .forms import sleepQualityForm

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


# class AnalysisView(generic.ListView):
#     model = Analysis
#     template_name = 'polls/analysis.html'
#     context_object_name = 'latest_stats'

#     def get_queryset(self):
#         name = None
#         form = sleepQualityForm()
#         if self.request.user.is_authenticated:
#             name = self.request.user.username
#             accessor = User.objects.get(user_name=name)
#             return Analysis.objects.filter(user=accessor.id).order_by('date')
#         else:
#             return False 



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
