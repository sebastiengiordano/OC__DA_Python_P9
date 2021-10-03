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
    title = forms.CharField(
        label="Titre",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'review_page_form_title'}),
        error_messages={'required': 'Merci de renseigner un titre.'}
        )
    description = forms.CharField(
        label="Description",
        min_length=10, max_length=2500,
        widget=forms.Textarea(),
        error_messages={
            'required': 'Merci de renseigner '
            'la description de votre livre ou article.'}
        )
    image_download = forms.ImageField(
        label="Image",
        required=False
        )
    headline = forms.CharField(
        label="Titre",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'review_page_form_title'}),
        error_messages={'required': 'Merci de renseigner un titre.'}
        )
    rating = forms.ChoiceField(
        label="Note",
        widget=forms.RadioSelect(attrs={'class': 'rating'}),
        choices=[(str(x), x) for x in range(6)],
        error_messages={
            'required': 'Merci de donner une note.'
            }
        )
    body = forms.CharField(
        label="Commentaire",        
        min_length=10, max_length=2500,
        widget=forms.Textarea(),
        error_messages={'required': 'Merci de mettre un commentaire.'}
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove colons on all field labels
        self.label_suffix = ""


class AskForReview(forms.Form):
    title = forms.CharField(
        label="Titre",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'review_page_form_title'}),
        error_messages={'required': 'Merci de renseigner un titre.'}
        )
    description = forms.CharField(
        label="",
        min_length=10, max_length=2500,
        widget=forms.Textarea(),
        required=False,
        error_messages={
            'required': 'Merci de renseigner '
            'la description de votre ticket.'}
        )
    image_download = forms.ImageField(
        label="Image",
        required=False
        )
