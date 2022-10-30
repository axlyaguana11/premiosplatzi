from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def index(request):
    return HttpResponse('Ola, estou criando aplicacoes com Django')


def detail(request, question_id):
    return HttpResponse(f'Your\'re looking at question {question_id}')


def results(request, question_id):
    return HttpResponse(f'Your\'re looking at the results {question_id}')


def vote(request, question_id):
    return HttpResponse(f'Your\'re voting on {question_id}')
