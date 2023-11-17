from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from litrevu_management import forms
from litrevu_management.models import Ticket, Review
from users.models import UserFollows


@login_required
def home(request):
    items_to_display = []
    following_relations = UserFollows.objects.filter(user=request.user)
    for following in following_relations:
        items_to_display.extend(
            Ticket.objects.filter(user=following.followed_user))
        items_to_display.extend(
            Review.objects.filter(user=following.followed_user))
    personal_tickets = Ticket.objects.filter(user=request.user)
    personal_reviews = Review.objects.filter(user=request.user)
    for personal_ticket in personal_tickets:
        review_associated = personal_ticket.review_set.all()
        items_to_display.extend(review_associated)
    items_to_display.extend(personal_tickets)
    items_to_display.extend(personal_reviews)
    items_to_display = list(set(items_to_display))
    sorted_items = sorted(
        items_to_display,
        key=lambda item: item.time_created,
        reverse=True
    )
    return render(
        request,
        'home.html',
        context={
            "items": sorted_items
        }
    )


@login_required
def posts(request):
    items_to_display = []
    items_to_display.extend(Ticket.objects.filter(user=request.user))
    items_to_display.extend(Review.objects.filter(user=request.user))
    sorted_items = sorted(
        items_to_display,
        key=lambda item: item.time_created,
        reverse=True
    )
    return render(
        request,
        'posts.html',
        context={
            'items': sorted_items,
        }
    )


@login_required
def create_ticket(request, ticket_id=None):
    is_updating = ticket_id is not None
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        ticket = None
    ticket_form = forms.TicketForm(
        request.POST if request.method == "POST" else None,
        request.FILES if request.method == "POST" else None,
        instance=ticket if ticket else None,
    )
    if request.method == "POST" and ticket_form.is_valid():
        ticket = ticket_form.save(commit=False)
        ticket.user = request.user
        ticket.save()
        return redirect('litrevu:posts')
    return render(
        request,
        'create_ticket.html',
        context={
            "is_updating": is_updating,
            "ticket_form": ticket_form,
        },
    )


@login_required
def update_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    edit_ticket = forms.TicketForm(instance=ticket)
    if request.method == "POST":
        edit_ticket = forms.TicketForm(
            request.POST,
            request.FILES,
            instance=ticket,
        )
        if edit_ticket.is_valid():
            edit_ticket.save()
            return redirect('litrevu:home')
    return render(
        request,
        template_name='update_ticket.html',
        context={
            'edit_ticket_form': edit_ticket,
            'ticket': ticket,
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
    ticket_form = forms.TicketForm(
        request.POST if request.method == "POST" else None,
        request.FILES if request.method == "POST" else None
    )
    review_form = forms.ReviewForm(
        request.POST if request.method == "POST" else None)
    if (request.method == "POST" and ticket_form.is_valid() and
            review_form.is_valid()):
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
        'create_review.html',
        context={
            "ticket_form": ticket_form,
            "review_form": review_form,
        }
    )


@login_required
def create_review_from_ticket(request, ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id)
    review_form = forms.ReviewForm(
        request.POST if request.method == "POST" else None)
    if request.method == "POST" and review_form.is_valid():
        review = review_form.save(commit=False)
        review.ticket = ticket
        review.user = request.user
        review.save()
        return redirect('litrevu:home')
    return render(
        request,
        template_name='review_from_ticket.html',
        context={
            'ticket': ticket,
            'review_form': review_form,
        }
    )


@login_required
def update_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        raise PermissionDenied
    update_review_form = forms.ReviewForm(instance=review)
    if request.method == "POST":
        update_review_form = forms.ReviewForm(request.POST, instance=review)
        if update_review_form.is_valid():
            update_review_form.save()
            return redirect('litrevu:posts')
    return render(
        request,
        template_name='update_review.html',
        context={
            'update_review_form': update_review_form,
            'review': review,
        }
    )


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        raise PermissionDenied
    review.delete()
    return redirect('litrevu:posts')
