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
    follow_error_message = ""
    user_to_follow_form = users.forms.FollowUserForm(request.POST if request.method == "POST" else None)
    connected_user = request.user
    following_relations = connected_user.following.all()
    followed_relations = connected_user.followed_by.all()
    followed_by_users = [relation.user for relation in followed_relations]
    followed_users = [relation.followed_user for relation in following_relations]
    if request.method == "POST" and user_to_follow_form.is_valid():
        follow_error_message = follow_user(request, user_to_follow_form, connected_user)
        if follow_error_message == "":
            return redirect(settings.UNFOLLOW_REDIRECT_URL)

    return render(
        request,
        template_name="following.html",
        context={
            'form': user_to_follow_form,
            'message': follow_error_message,
            'following_users': followed_users,
            'followed_by_users': followed_by_users,
        },
    )


@login_required
def follow_user(request, user_to_follow_form, connected_user):
    message = ""
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
    return message


@login_required
def unfollow_user(request, user_to_unfollow_id):
    connected_user = request.user
    user_to_unfollow = User.objects.get(id=user_to_unfollow_id)

    if user_to_unfollow is None:
        print("error during unfollow user: user not found")
        return

    following_relation = UserFollows.objects.get(
        followed_user=user_to_unfollow,
        user_id=connected_user.id,
    )
    if following_relation is None:
        print(f'error during unfollow : it seems that you dont follow this person')

    following_relation.delete()

    print(f'following relation: {following_relation}')
    return redirect(settings.UNFOLLOW_REDIRECT_URL)
