from itertools import chain

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import (
    ConnectionForm,
    RegistrationForm,
    CreateReviewForm,
    AskForReviewForm,
    SubscriptionForm)
from .utils import (
    get_user_by_id,
    get_user_by_name,
    get_users_by_name,
    get_users_subscribers,
    get_all_reviews,
    get_users_subscriptions,
    get_users_viewable_reviews,
    get_users_viewable_tickets,
    get_followed_users_viewable_reviews,
    get_followed_users_viewable_tickets,
    username_exists,
    check_password_confirmation,
    get_ticket_by_pk,
    save_ticket,
    save_review,
    save_subscribtion,
    delete_subscribtion
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
    # Get queryset of reviews
    reviews = get_users_viewable_reviews(request.user)
    followed_users_reviews = get_followed_users_viewable_reviews(request.user)

    # Get queryset of tickets
    tickets = get_users_viewable_tickets(request.user)
    followers_tickets = get_followed_users_viewable_tickets(request.user)
    tickets = list(chain(tickets, followers_tickets))
    # For each ticket, check if it has been reviewed by user
    for ticket in tickets:
        ticket.already_reviewed = False
        for review in get_all_reviews():
            if review.ticket == ticket:
                ticket.already_reviewed = True
                break

    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets, followed_users_reviews, followers_tickets),
        key=lambda post: post.time_created,
        reverse=True
    )

    # Update context
    context = {}
    context['posts'] = posts

    # Check if there is message to display
    message_to_display = request.session.get('message_to_display')
    if message_to_display:
        if message_to_display == 'save_new_ticket':
            context['message'] = 'save_new_ticket'
        elif message_to_display == 'save_new_review':
            context['message'] = 'save_new_review'

        del request.session['message_to_display']
    return render(request, 'reviews/feed.html', context=context)


@login_required(login_url='reviews:home_page')
def create_review(request, ticket=None):
    '''View used to write a new review.'''

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and
        # populate it with data from the request:
        form = CreateReviewForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            save_review(request, form)
            # Ask to display a message
            request.session['message_to_display'] = 'save_new_review'
            return redirect('reviews:feed')

    # if a GET (or any other method) we'll create a blank form
    else:
        # check if this request come from a response to a ticket
        if 'ticket_pk' in request.GET:
            pk = request.GET.get('ticket_pk')
            ticket = get_ticket_by_pk(pk)[0]
            ticket.already_reviewed = True
        # create a form instance
        form = CreateReviewForm()

    # Update context
    context = {}
    context['form'] = form
    context['ticket'] = ticket

    return render(request, 'reviews/create_review.html', context=context)


@login_required(login_url='reviews:home_page')
def ask_for_review(request):
    '''View used to ask for a review.'''
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AskForReviewForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            save_ticket(request, form)
            # Ask to display a message
            request.session['message_to_display'] = 'save_new_ticket'
            return redirect('reviews:feed')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AskForReviewForm()

    return render(request, 'reviews/ask_for_review.html', {'form': form})


##############
# Posts page #
##############
@login_required(login_url='reviews:home_page')
def posts(request):
    '''View which manage the posts page.'''
    # Get queryset of reviews
    reviews = get_users_viewable_reviews(request.user)

    # Get queryset of tickets
    tickets = get_users_viewable_tickets(request.user)

    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(
        request,
        'reviews/posts.html',
        context={
            'posts': posts,
            'update': 'tickets_and_reviews'})


#####################
# Subscription page #
#####################
@login_required(login_url='reviews:home_page')
def subscription(request):
    '''View which managed the subscription page.'''
    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # Check if the request is a users research
        if request.POST.get('users_search'):
            users = get_users_by_name(request.POST.get('username', ''))
            # Removed all users already followed
            users_follows = get_users_subscriptions(request.user)
            users_to_removed = []
            for user_follows in users_follows:
                for user in users:
                    if user_follows == user:
                        users_to_removed.append(user)
                        break
            for user in users_to_removed:
                users = users.exclude(username=user)
            if request.user in users:
                users = users.exclude(username=request.user)
            if get_user_by_name('admin')[0] in users:
                users = users.exclude(username='admin')
            # create a form instance and
            # populate it with data from the request:
            form = SubscriptionForm(request.POST)
        # Or if its a subscribing request
        elif request.POST.get('subscribing'):
            user_follows = get_user_by_id(
                request.POST.get('subscribing'))
            save_subscribtion(
                request.user,
                user_follows[0])
            # create a form instance
            form = SubscriptionForm()
            # Ask to display a message
            request.session['message_to_display'] = \
                f'Vous suivez à présent {user_follows[0].username}.'
        # Or if its an unsubscribing request
        elif request.POST.get('unsubscribing'):
            user_follows = get_user_by_id(
                request.POST.get('unsubscribing'))
            delete_subscribtion(
                request.user,
                user_follows[0])
            # create a form instance
            form = SubscriptionForm()
            # Ask to display a message
            request.session['message_to_display'] = \
                f'Vous ne suivez plus {user_follows[0].username}.'
        else:
            form = SubscriptionForm(request.POST)

    # if a GET (or any other method) we'll create a blank form
    else:
        # create a form instance
        form = SubscriptionForm()

    # returns queryset of subscribtions
    subscribtions = get_users_subscriptions(request.user)

    # returns queryset of subscribers
    subscribers = get_users_subscribers(request.user)

    # Update context
    context = {}
    context['form'] = form
    context['users_search'] = users if 'users' in locals() else None
    context['subscribtions'] = subscribtions
    context['subscribers'] = subscribers

    # Check if there is message to display
    message_to_display = request.session.get('message_to_display')
    if message_to_display:
        context['message_to_display'] = message_to_display
        del request.session['message_to_display']

    return render(
        request,
        'reviews/subscription.html',
        context=context)


#################
# Disconnection #
#################
def disconnect(request):
    '''Function used to log out the current user.'''
    logout(request)
    return redirect('reviews:home_page')


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
