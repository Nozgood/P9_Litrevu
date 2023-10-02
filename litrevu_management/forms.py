from django import forms


class TicketForm(forms.Form):
    title = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(max_length=2048, widget=forms.TextInput(attrs={"class": "form-control"}))
    image = forms.ImageField
