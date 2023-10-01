from django.shortcuts import render, redirect
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
    follow_message, block_message = "", ""
    connected_user = request.user
    following_users = get_following_users(request, connected_user)
    followers = get_followers(request, connected_user)
    blocked_users = get_blocked_users(request, connected_user)
    user_to_follow_form = users.forms.FollowUserForm(
        request.POST if request.method == "POST" and 'is_follow_form' in request.POST else None)
    user_to_block_form = users.forms.BlockUserForm(
        request.POST if request.method == "POST" and 'is_block_form' in request.POST else None)
    if request.method == "POST":
        if 'is_follow_form' in request.POST and user_to_follow_form.is_valid():
            follow_message = follow_user(request, user_to_follow_form, connected_user)
            if follow_message == "":
                return redirect(settings.UNFOLLOW_REDIRECT_URL)
        if 'is_block_form' in request.POST and user_to_block_form.is_valid():
            block_message = block_user(request, connected_user, user_to_block_form)
            if block_message == "":
                return redirect(settings.UNFOLLOW_REDIRECT_URL)
    return render(
        request,
        template_name="following.html",
        context={
            'follow_form': user_to_follow_form,
            'block_form': user_to_block_form,
            'follow_message': follow_message,
            'block_message': block_message,
            'following_users': following_users,
            'followers': followers,
            'blocked_users': blocked_users,
        },
    )


def get_following_users(request, connected_user):
    following_relations = connected_user.following.all()
    following_users = [relation.followed_user for relation in following_relations]
    return following_users


def get_followers(request, connected_user):
    followers_relations = connected_user.followed_by.all()
    followers = [relation.user for relation in followers_relations]
    return followers


def get_blocked_users(request, connected_user):
    blocked_relations = connected_user.user.all()
    blocked_users = [relation.blocked_user for relation in blocked_relations]
    return blocked_users


@login_required
def follow_user(request, user_to_follow_form, connected_user):
    try:
        user_to_follow = User.objects.get(username=user_to_follow_form.cleaned_data["username"])
        UserFollows.objects.create(
            followed_user=user_to_follow,
            user_id=connected_user.id,
        )
    except User.DoesNotExist:
        return "cet utilisateur n'existe pas"
    return ""


@login_required
def block_user(request, connected_user, user_to_block_form):
    try:
        user_to_block = User.objects.get(username=user_to_block_form.cleaned_data["username"])
        UserBlocked.objects.create(
            blocked_user=user_to_block,
            user_id=connected_user.id,
        )
    except User.DoesNotExist:
        return "cet utilisateur n'existe pas"
    return ""


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


@login_required
def unblock_user(request, user_to_unblock_id):
    print(f'user to unblock id: {user_to_unblock_id}')
    connected_user = request.user
    user_to_unblock = User.objects.get(id=user_to_unblock_id)
    blocked_relation = UserBlocked.objects.get(
        blocked_user=user_to_unblock,
        user_id=connected_user.id,
    )

    blocked_relation.delete()
    return redirect(settings.UNFOLLOW_REDIRECT_URL)
