from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views


app_name = 'reviews'
urlpatterns = [
    path('', views.get_connection_data, name='home_page'),
    path('feed/', views.feed, name='feed'),
    path('ask_for_review/', views.ask_for_review, name='ask_for_review'),
    path('create_review/', views.create_review, name='create_review'),
    path('registration/', views.get_registration_data, name='registration'),
    path('posts/', views.posts, name='posts'),
    path('subscription/', views.subscription, name='subscription'),
    path('disconnect/', views.disconnect, name='disconnect'),
    re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
]


urlpatterns += staticfiles_urlpatterns()
