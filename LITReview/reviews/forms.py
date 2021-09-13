from django import forms


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


class CreateReview(forms.Form):
    review_title = forms.CharField(
        label="Titre",
        max_length=100,
        widget=forms.TextInput()
        )
    description = forms.CharField(
        label="",
        min_length=8, max_length=20,
        widget=forms.TextInput()
        )


class AskForReview(forms.Form):
    book_article_title = forms.CharField(
        label="Titre",
        max_length=100,
        widget=forms.TextInput()
        )
    description = forms.CharField(
        label="",
        min_length=8, max_length=20,
        widget=forms.TextInput()
        )
    password_confirmation = forms.CharField(
        label="",
        min_length=8, max_length=20,
        widget=forms.TextInput(
            attrs={'placeholder': 'Confirmer mot de passe'})
        )
    review_title = forms.CharField(
        label="Titre",
        max_length=100,
        widget=forms.TextInput()
        )
    rating = forms.ChoiceField(
        label = "Note",
        widget=forms.CheckboxInput,
        choices=[x for x in range(6)]
        )
    commentary = forms.CharField(
        label="Commentaire",
        max_length=100,
        widget=forms.TextInput()
        )
