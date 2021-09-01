from django import forms

from django.contrib.auth.models import User


class ConnectionForm(forms.Form):
    username = forms.CharField(label='Nom d\'utilisateur', max_length=100)
    password = forms.CharField(
        label='Mot de passe', min_length=8, max_length=20)


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Nom d\'utilisateur', max_length=100)
    password = forms.CharField(
        label='Mot de passe', min_length=8, max_length=20)
    confirm_password = forms.CharField(
        label='Confirmer mot de passe', min_length=8, max_length=20)
