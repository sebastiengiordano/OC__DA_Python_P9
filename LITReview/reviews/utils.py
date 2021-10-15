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
    return user_reviews


def get_users_viewable_tickets(user: User):
    # Get it own tickets
    user_tickets = Ticket.objects.filter(user__username=user.username)
    user_tickets = user_tickets.annotate(
        content_type=Value('TICKET', CharField()))
    return user_tickets


def get_followed_users_viewable_reviews(user: User):
    # Get reviews of followed users
    users_follow = UserFollows.objects.filter(user__username=user.username)
    followers_reviews = Review.objects.none()
    for user_follow in users_follow:
        user_follow_review = Review.objects.filter(
            user__username=user_follow.followed_user.username)
        user_follow_review = user_follow_review.annotate(
            content_type=Value('REVIEW', CharField()))
        followers_reviews = chain(followers_reviews, user_follow_review)
    return followers_reviews


def get_followed_users_viewable_tickets(user: User):
    # Get tickets of followed users
    users_follow = UserFollows.objects.filter(user__username=user.username)
    followers_tickets = Ticket.objects.none()
    for user_follow in users_follow:
        user_follow_ticket = Ticket.objects.filter(
            user__username=user_follow.followed_user.username)
        user_follow_ticket = user_follow_ticket.annotate(
            content_type=Value('TICKET', CharField()))
        followers_tickets = chain(followers_tickets, user_follow_ticket)
    return followers_tickets


def get_followed_users(user: User):
    # Get the list of all users followed by user
    users_follow = UserFollows.objects.filter(user=user)
    followed = []
    for user_follow in users_follow:
        followed.append(user_follow.followed_user)
    return followed


def get_users_subscriber(user: User):
    # Get the list of all users which follow the user
    users_follow = UserFollows.objects.filter(followed_user=user)
    followers = []
    for user_follow in users_follow:
        followers.append(user_follow.user)
    return followers


def get_user_by_id(id: str):
    return User.objects.filter(id=id)


def get_user_by_name(username: str):
    return User.objects.filter(username=username)


def get_users_by_name(username: str):
    return User.objects.filter(username__icontains=username)


def get_ticket_by_pk(pk: str):
    ticket = Ticket.objects.filter(pk=pk)
    ticket = ticket.annotate(
        content_type=Value('REVIEW', CharField()))
    return ticket


def get_review_by_pk(pk: str):
    review = Review.objects.filter(pk=pk)
    review = review.annotate(
        content_type=Value('REVIEW', CharField()))
    return review


def get_all_reviews():
    # Get all reviews
    reviews = Review.objects.all()
    reviews = reviews.annotate(
        content_type=Value('REVIEW', CharField()))
    return reviews


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
    if 'ticket_pk' in request.POST:
        review.ticket = get_ticket_by_pk(request.POST.get('ticket_pk'))[0]
        review.ticket.already_reviewed = True
    else:
        review.ticket = save_ticket(request, form)
    review.rating = form.cleaned_data["rating"]
    review.headline = form.cleaned_data["headline"]
    review.body = form.cleaned_data["body"]
    review.user = request.user
    review.save()


def save_subscribtion(user: User, followed_user: User):
    for user_follows in UserFollows.objects.all():
        # Check if this user is not always followed
        if (
                user_follows.user == user
                and
                user_follows.followed_user == followed_user):
            return
    user_follow = UserFollows()
    user_follow.user = user
    user_follow.followed_user = followed_user
    user_follow.save()


def delete_subscribtion(user: User, followed_user: User):
    # Get all users followed by user
    user_follow = UserFollows.objects.filter(user=user, followed_user=followed_user)
    user_follow.delete()
    # users_follow = UserFollows.objects.all()
    # for user_follow in users_follow:
    #     if (
    #             user_follow.user == user
    #             and
    #             user_follow.followed_user == followed_user):
    #         user_follow.delete()
    #         break


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
