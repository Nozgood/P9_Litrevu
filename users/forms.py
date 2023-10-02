from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from users.models import User

USERNAME_VALIDATION_TEXT = "15 caractères maximum."
PASSWORD_VALIDATION_TEXT = "Votre mot de passe doit contenir 8 caractères minimum."
PASSWORD_2_VALIDATION_TEXT = "Ressaisissez le même mot de passe."


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = "Email"
        self.fields["password1"].label = "Mot de passe"
        self.fields["password2"].label = 'Confirmer mot de passe'
        self.fields["username"].help_text = USERNAME_VALIDATION_TEXT
        self.fields["password1"].help_text = PASSWORD_VALIDATION_TEXT
        self.fields["password2"].help_text = PASSWORD_2_VALIDATION_TEXT
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) > 15:
            raise forms.ValidationError("le nom d'utilisateur ne peut pas contenir plus de 15 caractères")
        return username

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
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class FollowUserForm(forms.Form):
    username = forms.CharField(
        label='',
        max_length=64,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "nom d'utilisateur"})
    )

    def clean(self):
        cleaned_data = super().clean()
        if not User.objects.filter(username=cleaned_data["username"]).exists():
            self.add_error("username", "cet utilisateur n'existe pas")


class BlockUserForm(forms.Form):
    is_block_form = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    username = forms.CharField(
        max_length=64,
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "nom d'utilisateur"})
    )


class UnfollowUserForm(forms.Form):
    is_unfollow_form = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    username = forms.CharField(
        label='',
        max_length=64,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


class UnblockUserForm(forms.Form):
    is_unblock_form = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    username = forms.CharField(
        label='',
        max_length=64,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
