#from re import template
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Question


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
    return HttpResponse(f'Your\'re voting on {question_id}')
