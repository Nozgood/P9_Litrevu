from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ["email", "username"]


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    username = forms.CharField(
        max_length=64,
        label="Username",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        max_length=64,
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
