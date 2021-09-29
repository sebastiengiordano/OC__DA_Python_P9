from django.contrib.auth.models import User
from django import forms

from .models import Review, Ticket



def get_users_viewable_reviews(user: User):
    return Review.objects.filter(user__username=user.username)


def get_users_viewable_tickets(user: User):
    return Ticket.objects.filter(user__username=user.username)


def get_users_subscriptions(user: User):
    return user.following.all()


def get_users_subscribers(user: User):
    return user.followed_by.all()


def get_users_by_name(username: str):
    return User.objects.filter(username=username)



def get_ticket_by_pk(pk: str):
    return Ticket.objects.filter(pk=pk)


def username_exists(username):
    if User.objects.filter(username=username).exists():
        return True

    return False


def check_password_confirmation(form: forms):
    if (form.cleaned_data['password'] == form.cleaned_data['password_confirmation']):
        return True
    else:
        # The password confirmation doesn't correspond to the
        # password, we need to informed the user to its mistake.
        form.add_error(
            'password_confirmation',
            'Vous n\'avez pas renseigné '
            'deux fois le même mot de passe.')
        return False
