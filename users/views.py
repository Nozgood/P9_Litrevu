from django.shortcuts import render
from users.forms import UserForm

def login(request):
    return render(
        request,
        'login.html',
    )

def signup(request):
    user_form = UserForm()
    return render(
        request,
        'signup.html',
        {'user_form': user_form},
    )