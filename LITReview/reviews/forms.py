from django import forms


class ConnectionForm(forms.Form):
    user_name = forms.CharField(label='Nom d\'utilisateur', max_length=100)
    password = forms.CharField(
        label='Mot de passe', min_length=8, max_length=20)
