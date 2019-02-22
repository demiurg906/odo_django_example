from django import forms


class QuestionForm(forms.Form):
    text = forms.CharField(label='Ask question', max_length=200)