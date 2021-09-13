from itertools import chain

# from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
# from django.urls import reverse
from django.views import generic
from django.db.models import CharField, Value
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Review, Ticket, UserFollows
from .forms import ConnectionForm, RegistrationForm
from .utils import (
    get_users_subscribers,
    get_users_subscriptions,
    get_users_viewable_reviews,
    get_users_viewable_tickets,
    username_exists,
    check_password_confirmation
)


def get_connection_data(request):
    '''View used to manage user's log in.'''
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ConnectionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'])
            if user:
                login(request, user)
                # A backend authenticated the credentials
                return redirect('reviews:feed')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ConnectionForm()

    return render(request, 'reviews/home_page.html', {'form': form})


def get_registration_data(request):
    '''View used to append new user.'''
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegistrationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # If the username is not already used
            if not username_exists(username):
                # Check if the password has been correctly set twice
                if check_password_confirmation(form):
                    # This user could be append to DB.
                    user = User.objects.create_user(username, '', password)
                    # And we could log in it
                    login(request, user)
                    return redirect('reviews:feed')
            else:
                # This username already exist,
                # we need to informed the user to choose another name.
                form.add_error(
                    'username',
                    f'Le nom d\'utilisateur "{username}" est déjà utilisé.')
                check_password_confirmation(form)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegistrationForm()

    return render(request, 'reviews/registration.html', {'form': form})


@login_required(login_url='reviews:home_page')
def feed(request):
    reviews = get_users_viewable_reviews(request.user)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = get_users_viewable_tickets(request.user)
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, 'reviews/feed.html', context={'posts': posts})


@login_required(login_url='reviews:home_page')
def posts(request):
    reviews = get_users_viewable_reviews(request.user)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = get_users_viewable_tickets(request.user)
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, 'reviews/posts.html', context={'posts': posts})


@login_required(login_url='reviews:home_page')
def subscription(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        followed_user_to_removed = request.POST['submit']
        user_Follows_object = UserFollows.objects.filter(id=followed_user_to_removed)
        if user_Follows_object is not None:
            user_Follows_object.delete()
            return subscription(request)

    # returns queryset of subscribtions
    subscribtions = get_users_subscriptions(request.user)

    # returns queryset of subscribers
    subscribers = get_users_subscribers(request.user)

    return render(
        request,
        'reviews/subscription.html',
        context={
            'subscribtions': subscribtions,
            'subscribers': subscribers
            })


def disconnect(request):
    logout(request)
    return redirect('reviews:home_page')


class FeedView(generic.ListView):
    model = [Review, Ticket]
    template_name = 'reviews/feed.html'
    context_object_name = 'latest_review_list'

    def get_queryset(self):
        """Return the last five published reviews."""
        return Review.objects.order_by('-pub_date')[:5]


# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'polls/detail.html'


# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = 'polls/results.html'
