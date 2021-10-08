from itertools import chain

from django.contrib.auth.models import User
from django import forms
from django.db.models import CharField, Value

from .models import Review, Ticket, UserFollows


def get_users_viewable_reviews(user: User):
    # Get it own reviews
    user_reviews = Review.objects.filter(user__username=user.username)
    user_reviews = user_reviews.annotate(
        content_type=Value('REVIEW', CharField()))
    # Get reviews of followed users
    users_follows = UserFollows.objects.filter(user__username=user.username)
    followers_reviews = Review.objects.none()
    for user_follows in users_follows:
        user_follows_review = Review.objects.filter(
            user__username=user_follows.followed_user.username)
        followers_reviews = chain(followers_reviews, user_follows_review)
        user_follows_review = user_follows_review.annotate(
            content_type=Value('REVIEW', CharField()))
    # Merge all reviews
    reviews = list(chain(user_reviews, followers_reviews))

    return reviews


def get_users_viewable_tickets(user: User):
    # Get it own tickets
    user_tickets = Ticket.objects.filter(user__username=user.username)
    user_tickets = user_tickets.annotate(
        content_type=Value('TICKET', CharField()))
    # Get tickets of followed users
    users_follows = UserFollows.objects.filter(user__username=user.username)
    followers_tickets = Ticket.objects.none()
    for user_follows in users_follows:
        user_follows_ticket = Ticket.objects.filter(
            user__username=user_follows.followed_user.username)
        followers_tickets = chain(followers_tickets, user_follows_ticket)
        user_follows_ticket = user_follows_ticket.annotate(
            content_type=Value('TICKET', CharField()))
    # Merge all tickets
    tickets = list(chain(user_tickets, followers_tickets))

    return tickets


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
    if (
            form.cleaned_data['password']
            ==
            form.cleaned_data['password_confirmation']):
        return True
    else:
        # The password confirmation doesn't correspond to the
        # password, we need to informed the user to its mistake.
        form.add_error(
            'password_confirmation',
            'Vous n\'avez pas renseigné '
            'deux fois le même mot de passe.')
        return False



def save_ticket(request, form: forms):
    ticket = Ticket()
    ticket.title = form.cleaned_data["title"]
    ticket.description = form.cleaned_data["description"]
    ticket.user = request.user
    ticket.image = request.FILES.get('image_download', None)
    ticket.save()
    return ticket


def save_review(request, form: forms):
    review = Review()
    if hasattr(form, 'ticket_pk'):
        review.ticket = get_ticket_by_pk(form.ticket_pk)[0]
        review.ticket.already_reviewed = True
    else:
        review.ticket = save_ticket(request, form)
    review.rating = form.cleaned_data["rating"]
    review.headline = form.cleaned_data["headline"]
    review.body = form.cleaned_data["body"]
    review.user = request.user
    review.save()
