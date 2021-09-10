from django import forms

from django.contrib.auth.models import User


class ConnectionForm(forms.Form):
    username = forms.CharField(
        label="",
        max_length=30,
        widget=forms.TextInput(
            attrs={'placeholder': 'Nom d\'utilisateur'})
        )
    password = forms.CharField(
        label="",
        min_length=8, max_length=20,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Mot de passe'})
        )


class RegistrationForm(forms.Form):
    username = forms.CharField(
        label="",
        max_length=30,
        widget=forms.TextInput(
            attrs={'placeholder': 'Nom d\'utilisateur'})
        )
    password = forms.CharField(
        label="",
        min_length=8, max_length=20,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Mot de passe'})
        )
    password_confirmation = forms.CharField(
        label="",
        min_length=8, max_length=20,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Confirmer mot de passe'})
        )
