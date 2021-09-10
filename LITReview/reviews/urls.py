from django.urls import path

from . import views

app_name = 'reviews'
urlpatterns = [
    path('', views.get_connection_data, name='home_page'),
    path('feed/', views.feed, name='feed'),
    path('registration/', views.get_registration_data, name='registration'),
    path('posts/', views.posts, name='posts'),
    path('subscription/', views.subscription, name='subscription'),
    path('disconnect/', views.disconnect, name='disconnect'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]
