from django import forms
from users.models import User

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"

class LoginForm(forms.Form):
    username = forms.CharField(max_length=64, label="Username")
    password = forms.CharField(max_length=64, label="Password", widget=forms.PasswordInput)
