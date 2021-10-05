from itertools import chain

from django.contrib.auth.models import User
from django import forms

from .models import Review, Ticket, UserFollows


def get_users_viewable_reviews(user: User):
    # Get it own reviews
    user_reviews = Review.objects.filter(user__username=user.username)
    # Get reviews of followed users
    users_follows = UserFollows.objects.filter(user__username=user.username)
    followers_reviews = Review.objects.none()
    for user_follows in users_follows:
        user_follows_review = Review.objects.filter(
            user__username=user_follows.followed_user.username)
        followers_reviews = chain(followers_reviews, user_follows_review)
    # Merge all reviews
    reviews = chain(user_reviews, followers_reviews)

    return reviews


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


def create_ticket(request, form: forms):
    ticket = Ticket()
    ticket.title = form.cleaned_data["title"]
    ticket.description = form.cleaned_data["description"]
    ticket.user = request.user
    ticket.image = request.FILES.get('image_download', None)
    return ticket


def save_ticket(request, form: forms):
    ticket = create_ticket(request, form)
    ticket.save()


def save_review(request, form: forms):
    review = Review()
    if hasattr(form, 'ticket_pk'):
        ticket = get_ticket_by_pk(pk)[0]
        ticket.already_reviewed = True
    else:
        review.ticket = create_ticket(request, form)
        review.ticket.save()
    review.rating = form.cleaned_data["rating"]
    review.headline = form.cleaned_data["headline"]
    review.body = form.cleaned_data["body"]
    review.user = request.user
    review.save()
