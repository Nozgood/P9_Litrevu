from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
import users.forms
from litrevu import settings

def logout_user(request):
    logout(request)
    return redirect('login')

def signup(request):
    user_form = users.forms.SignupForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and user_form.is_valid():
        new_user = user_form.save()
        login(request, new_user)
        return redirect(settings.LOGIN_REDIRECT_URL)
    return render(
        request,
        'signup.html',
        {'user_form': user_form},
    )