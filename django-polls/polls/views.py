#from re import template
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone 

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    #latest_question_list = Question.objects.all()
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        #return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any question that is not published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        template = 'polls/detail.html'
        context = {
            'question': question,
            'error_message': 'You didn\'t select a choice.'
        }
        return render(request, template, context)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


# def index(request):
#     template = 'polls/index.html'
#     latest_question_list = Question.objects.all()
#     context = {
#         'latest_question_list': latest_question_list
#     }
#     return render(request, template, context)


# def detail(request, question_id):
#     template = 'polls/detail.html'
#     question = get_object_or_404(Question, pk=question_id)
#     context = {'question': question}
#     return render(request, template, context)


# def results(request, question_id):
#     template = 'polls/results.html'
#     question = get_object_or_404(Question, pk=question_id)
#     context = {'question': question}
#     return render(request, template, context)



