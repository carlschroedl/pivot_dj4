from django.http import HttpResponse
from django.template import loader

from .models import Question

def index(request):
    latest_questions = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_questions': latest_questions,
    }
    content = template.render(context, request)
    response = HttpResponse(content)
    return response

def detail(request, question_id):
    response = f"You're viewing question {question_id}"
    return HttpResponse(response)

def results(request, question_id):
    response = f"You're view the results of question {question_id}"
    return HttpResponse(response)

def vote(request, question_id):
    response = f"You're voting on question {question_id}"
    return HttpResponse(response)
