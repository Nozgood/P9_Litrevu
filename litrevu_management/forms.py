from django import forms
from litrevu_management.models import Ticket, Review

RATING_CHOICES = [(value, str(value)) for value in range(6)]


class TicketForm(forms.ModelForm):
    """
    TicketForm is used to manage the creation of a ticket received from
    the front in our django application.
    """

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        labels = {
            'title': 'Titre',
            'description': 'Description',
            'image': 'Image',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ReviewForm(forms.ModelForm):
    """
    ReviewForm is used to manage the creation of a ticket received from the
    front in our Django Application.
    """

    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        labels = {
            'headline': 'Titre',
            'rating': 'Note',
            'body': 'Description',
        }
        widgets = {
            'rating': forms.RadioSelect(choices=RATING_CHOICES),
            'headline': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.TextInput(attrs={'class': 'form-control'}),
        }
