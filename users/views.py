from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
import users.forms
from litrevu import settings


def user_login(request):
    login_form = users.forms.LoginForm(request.POST if request.method == "POST" else None)
    login_message = ""
    if request.method == "POST" and login_form.is_valid():
        user = authenticate(
            username=login_form.cleaned_data["username"],
            password=login_form.cleaned_data["password"]
        )
        print(f"user: {user}")
        if user is not None:
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            login_message = "identifiants invalides"
    return render(
        request,
        template_name='login.html',
        context={
            "form": login_form,
            "message": login_message,
        }
    )


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
