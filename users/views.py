from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
import users.forms as UserForms


def logout_user(request):
    logout(request)
    return redirect('login')
def login_user(request):
    login_form = UserForms.LoginForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and login_form.is_valid():
        user_logged = authenticate(
            username=login_form.cleaned_data["username"],
            password=login_form.cleaned_data["password"],
        )
        if user_logged is not None:
            login(request, user_logged)
            return redirect('home')
        else:
            login_form.add_error("username", "ce compte n'existe pas")
            login_form.add_error("password", "bad password")
    return render(
        request,
        'login.html',
        {
            "login_form": login_form,
        },
    )

def signup(request):
    user_form = UserForms.SignupForm()
    return render(
        request,
        'signup.html',
        {'user_form': user_form},
    )