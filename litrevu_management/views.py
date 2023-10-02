from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return render(
        request,
        'home.html',
    )


@login_required
def posts(request):
    return render(
        request,
        'posts.html',
    )


@login_required
def create_ticket(request):
    return render(
        request,
        'ticket.html',
    )


@login_required
def create_review(request):
    return render(
        request,
        'review.html',
    )
