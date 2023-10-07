from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from litrevu_management import forms
from litrevu_management.models import Ticket, Review


@login_required
def home(request):
    return render(
        request,
        'home.html',
    )


@login_required
def posts(request):
    all_tickets = Ticket.objects.filter(user=request.user)
    all_reviews = Review.objects.filter(user=request.user)
    return render(
        request,
        'posts.html',
        context={
            'tickets': all_tickets,
            'reviews': all_reviews,
        }
    )


@login_required
def create_ticket(request):
    ticket_form = forms.TicketForm(request.POST if request.method == "POST" else None,
                                   request.FILES if request.method == "POST" else None)
    if request.method == "POST" and ticket_form.is_valid():
        ticket = ticket_form.save(commit=False)
        ticket.user = request.user
        ticket.save()
        return redirect('litrevu:home')
    return render(
        request,
        'ticket.html',
        context={
            "ticket_form": ticket_form,
        },
    )


@login_required
def create_review(request):
    ticket_form = forms.TicketForm(request.POST if request.method == "POST" else None,
                                   request.FILES if request.method == "POST" else None)
    review_form = forms.ReviewForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and ticket_form.is_valid() and review_form.is_valid():
        ticket = ticket_form.save(commit=False)
        ticket.user = request.user
        review = review_form.save(commit=False)
        review.ticket = ticket
        review.user = request.user
        ticket.save()
        review.save()
        return redirect('litrevu:home')
    return render(
        request,
        'review.html',
        context={
            "ticket_form": ticket_form,
            "review_form": review_form,
        }
    )
