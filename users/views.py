from django.db import IntegrityError

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
import users.forms
from users.models import User, UserFollows, UserBlocked
from litrevu import settings


def user_login(request):
    login_form = users.forms.LoginForm(request.POST if request.method == "POST" else None)
    login_message = ""
    if request.method == "POST" and login_form.is_valid():
        user = authenticate(
            username=login_form.cleaned_data["username"],
            password=login_form.cleaned_data["password"]
        )
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
    return redirect('users:login')


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
    follow_form = users.forms.FollowUserForm()
    block_form = users.forms.BlockUserForm()
    followers_relation = UserFollows.objects.filter(followed_user=request.user.id)
    followers_users = []
    for follower in followers_relation:
        follower_user = User.objects.get(id=follower.user_id)
        followers_users.append(follower_user)
    return render(
        request,
        template_name='following.html',
        context={
            'follow_form': follow_form,
            'block_form': block_form,
            'followers': followers_users,
        }
    )


@login_required
def follow_user(request, unfollow=False):
    user_to_follow_form = users.forms.FollowUserForm(
        request.POST if request.method == "POST" and not unfollow else None)
    if request.method == "POST":
        if unfollow:
            try:
                UserFollows.objects.get(user=request.user, followed_user=request.POST.get("user_id")).delete()
                return redirect("users:following")
            except UserFollows.DoesNotExist:
                pass
        else:
            if user_to_follow_form.is_valid():
                try:
                    user_to_follow = User.objects.get(username=user_to_follow_form.cleaned_data["username"])
                    if user_to_follow == request.user:
                        messages.error(
                            request,
                            message="Vous ne pouvez pas vous suivre vous-même.",
                            extra_tags="follow_error")
                        return redirect("users:following")

                    UserFollows.objects.create(
                        followed_user=user_to_follow,
                        user=request.user,
                    )
                except User.DoesNotExist:
                    messages.error(request, message="Utilisateur introuvable.", extra_tags="follow_error")
                    return redirect("users:following")
                except IntegrityError:
                    messages.error(request, message="Vous suivez déjà cet utilisateur.", extra_tags="follow_error")
                    return redirect("users:following")
                return redirect("users:following")
    return redirect('users:following')


@login_required
def block_user(request, unblock=False):
    user_to_block_form = users.forms.BlockUserForm(
        request.POST if request.method == "POST" and not unblock else None)
    if request.method == "POST":
        if unblock:
            try:
                UserBlocked.objects.get(user=request.user, blocked_user=request.POST.get("user_id")).delete()
                return redirect("users:following")
            except UserBlocked.DoesNotExist:
                pass
        else:
            if user_to_block_form.is_valid():
                try:
                    user_to_block = User.objects.get(username=user_to_block_form.cleaned_data["username"])
                    if user_to_block == request.user:
                        messages.error(
                            request,
                            message="Vous ne pouvez pas vous bloquer vous-même.",
                            extra_tags="block_error")
                        return redirect("users:following")
                    UserBlocked.objects.create(user=request.user, blocked_user=user_to_block)
                except User.DoesNotExist:
                    messages.error(request, message="utilisateur introuvable.", extra_tags="block_error")
                    return redirect("users:following")
                except IntegrityError:
                    messages.error(request, message="Vous bloquez déjà cet utilisateur.", extra_tags="block_error")
                    return redirect("users:following")
                return redirect("users:following")
    return redirect('users:following')
