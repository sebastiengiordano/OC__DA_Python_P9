from itertools import chain
from django.http.request import RAISE_ERROR

# from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
# from django.urls import reverse
from django.views import generic
from django.db.models import CharField, Value
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.views.generic.base import TemplateView

from .models import Review, Ticket, UserFollows
from .forms import (
    ConnectionForm,
    RegistrationForm,
    CreateReview,
    AskForReview)
from .utils import (
    get_users_subscribers,
    get_users_subscriptions,
    get_users_viewable_reviews,
    get_users_viewable_tickets,
    username_exists,
    check_password_confirmation,
    get_ticket_by_pk
)


#############
# Home page #
#############
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


#####################
# Registration page #
#####################
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


#############
# Feed page #
#############
@login_required(login_url='reviews:home_page')
def feed(request):
    '''View which manage the feed page.'''
    reviews = get_users_viewable_reviews(request.user)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = get_users_viewable_tickets(request.user)
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    for ticket in tickets:
        ticket.already_reviewed = False
        for review in reviews:
            if review.ticket == ticket:
                ticket.already_reviewed = True
                break

    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )

    # Update context
    context = {}
    context['posts'] = posts
    # Check if there is message to display
    if request.session.get('ask_for_review') == 'save_new_ticket':
        context['message']= 'save_new_ticket'
    return render(request, 'reviews/feed.html', context=context)


@login_required(login_url='reviews:home_page')
def create_review(request):
    '''View used to write a new review.'''

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CreateReview(request.POST)
        # check whether it's valid:
        if form.is_valid():
            return redirect('reviews:feed')
        else:
            form = CreateReview()


    # if a GET (or any other method) we'll create a blank form
    else:
        form = CreateReview()

    return render(request, 'reviews/create_review.html', {'form': form})


@login_required(login_url='reviews:home_page')
def ask_for_review(request):
    '''View used to ask for a review.'''
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AskForReview(request.POST)
        # check whether it's valid:
        if form.is_valid():
            ticket = Ticket()
            ticket.title = form.cleaned_data["title"]
            ticket.description = form.cleaned_data["description"]
            ticket.user = request.user
            ticket.image = request.FILES.get('image_download', None)
            ticket.save()
            # if image_download == "Télécharger fichier":
            #     # Add image file management
            #     RAISE_ERROR
            # else:
                # Save the review request
            request.session['ask_for_review'] = 'save_new_ticket'
            return redirect('reviews:feed')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AskForReview()

    return render(request, 'reviews/ask_for_review.html', {'form': form})


@login_required(login_url='reviews:home_page')
def review_in_response_to_ticket(request):
    '''View which managed a review created from a ticket.'''
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        if 'post_pk' in request.POST:
            pk = request.POST.get('post_pk')
            ticket = get_ticket_by_pk(pk)

    else:
        feed(request)


##############
# Posts page #
##############
@login_required(login_url='reviews:home_page')
def posts(request):
    '''View which manage the posts page.'''
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


#####################
# Subscription page #
#####################
@login_required(login_url='reviews:home_page')
def subscription(request):
    '''View which managed the subscription page.'''
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        followed_user_to_removed = request.POST['submit']
        user_Follows_object = UserFollows.objects.filter(
            id=followed_user_to_removed
            )
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


#################
# Disconnection #
#################
def disconnect(request):
    '''Function used to log out the current user.'''
    logout(request)
    return redirect('reviews:home_page')




# class ReviewInResponseToTicket(TemplateView):
#     template_name = 'review/response_review.html'
#     def get_context_data(self,*args, **kwargs):
#         context = super(
#             ReviewInResponseToTicket,
#             self).get_context_data(*args,**kwargs)
#         reviews = get_users_viewable_reviews(self.request.user)
#         context['reviews'] = reviews
#         return context


# class FeedView(generic.ListView):
#     model = [Review, Ticket]
#     template_name = 'reviews/feed.html'
#     context_object_name = 'latest_review_list'

#     def get_queryset(self):
#         """Return the last five published reviews."""
#         return Review.objects.order_by('-pub_date')[:5]


# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'polls/detail.html'


# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = 'polls/results.html'
