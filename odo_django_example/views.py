from django.http import HttpRequest, Http404
from django.shortcuts import render

from odo_django_example.models import Question, Answer


def index(request: HttpRequest):
    return render(request, 'index.html')


def hello(request: HttpRequest, name: str = None):
    if name is None:
        name = 'Anonymous'
    return render(request,'hello.html', {'name': name})


def get_question(request: HttpRequest, question_id: int):
    try:
        question = Question.objects.get(pk=question_id)
        return render(request, 'question.html', {'question': question})
    except Question.DoesNotExist:
        raise Http404(f'Question {question_id} does not exists')


def get_answer(request: HttpRequest, answer_id: int):
    try:
        answer = Answer.objects.get(pk=answer_id)
        return render(request, 'answer.html', {'answer': answer})
    except Answer.DoesNotExist:
        raise Http404(f'Answer {answer_id} does not exists')


def get_questions(request: HttpRequest):
    questions = Question.objects.order_by('pk').all()
    return render(request, 'questions.html', {'questions': questions})
