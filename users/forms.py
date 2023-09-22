from django import forms
from users.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ["email", "username", "first_name", "last_name"]


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=64,
        label="Username",
    )
    password = forms.CharField(
        max_length=64,
        label="Password",
        widget=forms.PasswordInput
    )
