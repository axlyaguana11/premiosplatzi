#from re import template
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Choice, Question


def index(request):
    template = 'polls/index.html'
    latest_question_list = Question.objects.all()
    context = {
        'latest_question_list': latest_question_list
    }
    return render(request, template, context)


def detail(request, question_id):
    template = 'polls/detail.html'
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, template, context)


def results(request, question_id):
    return HttpResponse(f'Your\'re looking at the results {question_id}')


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
