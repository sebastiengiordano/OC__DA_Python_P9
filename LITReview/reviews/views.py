from ast import IsNot
from itertools import chain
from django.db import reset_queries
from django.forms import PasswordInput

# from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
# from django.urls import reverse
from django.views import generic
from django.db.models import CharField, Value
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .models import Review, Ticket, UserFollows
from .forms import ConnectionForm, RegistrationForm
from .utils import (
    get_users_subscribers,
    get_users_subscriptions,
    get_users_viewable_reviews,
    get_users_viewable_tickets,
    get_users_by_name
)


def get_connection_data(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ConnectionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print(request.POST['username'])
            print(form.cleaned_data)
            if request.user.is_authenticated:
                login(request, request.user)
                # A backend authenticated the credentials
                return redirect('reviews:feed')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ConnectionForm()

    return render(request, 'reviews/home_page.html', {'form': form})


def get_registration_data(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegistrationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if get_users_by_name(form.cleaned_data.username):
                return redirect('reviews:feed')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegistrationForm()

    return render(request, 'reviews/registration.html', {'form': form})


@login_required
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


@login_required
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


@login_required
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
    return redirect('reviews')


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
