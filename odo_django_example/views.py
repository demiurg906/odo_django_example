from django.http import HttpRequest, Http404
from django.shortcuts import render

from odo_django_example.models import Question


def index(request: HttpRequest):
    return render(request, 'index.html')


def hello(request: HttpRequest, name: str = None):
    if name is None:
        name = 'Anonymous'
    return render(request,'hello.html', {'name': name})


def get_question(request: HttpRequest, question_id: int):
    try:
        question = Question.objects.get(pk=question_id)
        next_id = question_id + 1
        previous_id = question_id - 1
        if not Question.objects.filter(pk=next_id).exists():
            next_id = None
        if not Question.objects.filter(pk=previous_id).exists():
            previous_id = None
        Question.objects.filter()
        return render(request, 'question.html', {'question': question, 'next_id': next_id, 'previous_id': previous_id})
    except Question.DoesNotExist:
        raise Http404(f'Question {question_id} does not exists')
