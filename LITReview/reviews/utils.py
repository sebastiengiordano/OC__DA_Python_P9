from .models import Review, Ticket
from django.contrib.auth.models import User


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
