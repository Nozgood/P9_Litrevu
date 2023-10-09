from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from litrevu_management import forms
from litrevu_management.models import Ticket, Review


@login_required
def home(request):
    all_personal_tickets = Ticket.objects.filter(user=request.user)
    all_personal_reviews = Review.objects.filter(user=request.user)
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
def update_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    edit_ticket = forms.TicketForm(instance=ticket)
    return render(
        request,
        template_name='update_ticket.html',
        context={
            'edit_ticket_form': edit_ticket,
        }
    )


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.user != ticket.user:
        raise PermissionDenied

    ticket.delete()
    return redirect('litrevu:posts')


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
            "range": range,
        }
    )


@login_required
def update_review(request):
    return render(request)


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        raise PermissionDenied
    review.delete()
    return redirect('litrevu:posts')
