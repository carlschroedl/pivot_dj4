from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404

from .models import Question

def index(request):
    context = {
        'latest_questions': Question.objects.order_by('-pub_date')[:5],
    }
    
    response = render(request, 'polls/index.html', context)
    return response

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    response = render(request, 'polls/detail.html', {'question': question})
    return response

def results(request, question_id):
    response = f"You're view the results of question {question_id}"
    return HttpResponse(response)

def vote(request, question_id):
    response = f"You're voting on question {question_id}"
    return HttpResponse(response)

