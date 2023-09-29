from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
import users.forms
from users.models import User, UserFollows
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


@login_required
def following(request):
    message = ""
    user_to_follow_form = users.forms.FollowUserForm(request.POST if request.method == "POST" else None)
    connected_user = request.user
    following_relations = connected_user.following.all()
    print(f'following relations: {following_relations}')
    followed_users = [relation.followed_user for relation in following_relations]
    print(f'test: {followed_users}')
    if request.method == "POST" and user_to_follow_form.is_valid():
        try:
            user_to_follow = User.objects.get(username=user_to_follow_form.cleaned_data["username"])
            print(f'connected user: {connected_user.username}')
            print(f'test: {user_to_follow}, {user_to_follow.id}')
            UserFollows.objects.create(
                followed_user=user_to_follow,
                user_id=connected_user.id,
            )
        except User.DoesNotExist:
            message = "cet utilisateur n'existe pas"

    return render(
        request,
        template_name="following.html",
        context={
            'form': user_to_follow_form,
            'message': message,
            'following_users': followed_users,
        },
    )

    # TODO: create the view to get who is following me (GET)
