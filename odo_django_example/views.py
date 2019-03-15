from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpRequest, Http404, HttpResponseRedirect
from django.shortcuts import render

from odo_django_example.forms import QuestionForm, LoginForm, RegistrationForm
from odo_django_example.models import Question, Answer

POST = 'POST'


def index(request: HttpRequest):
    return render(request, 'index.html', {'user': request.user})


def hello(request: HttpRequest, name: str = None):
    if name is None:
        name = 'Anonymous'
    return render(request, 'hello.html', {'name': name})


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


def ask_question(request: HttpRequest):
    if request.method == POST:
        form = QuestionForm(request.POST)
        if form.is_valid():
            current_user = request.user
            if current_user.is_authenticated :
                current_user = get_guest_user()
            question = Question.objects.create(
                question_text=form.cleaned_data['text'],
                author=current_user
            )
            question.save()
            return HttpResponseRedirect('/question/{}'.format(question.pk))
    else:
        form = QuestionForm()

    return render(request, 'ask-question.html', {'form': form})


def login_view(request: HttpRequest):
    if request.method == POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # найти подходящего пользователя в базе данных
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
    else:
        form = LoginForm()

    return render(request, 'login_register.html', {
        'form': form,
        'header': 'Login',
        'button_label': 'Login'
    })


def register_view(request: HttpRequest):
    if request.method == POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = User.objects.create_user(username, email, password)
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = RegistrationForm()

    return render(request, 'login_register.html', {
        'form': form,
        'header': 'Registration',
        'button_label': 'Register'
    })


def get_guest_user():
    return User.objects.get(username='Guest')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')