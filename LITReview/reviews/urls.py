from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views


app_name = 'reviews'
urlpatterns = [
    path('', views.get_connection_data, name='home_page'),
    path('registration/', views.get_registration_data, name='registration'),
    path('feed/', views.feed, name='feed'),
    path('create_review/', views.create_review, name='create_review'),
    path('create_ticket/', views.create_ticket, name='create_ticket'),
    path('posts/', views.posts, name='posts'),
    path('update_ticket/', views.update_ticket, name='update_ticket'),
    path('update_review/', views.update_review, name='update_review'),
    path('subscription/', views.subscription, name='subscription'),
    path('disconnect/', views.disconnect, name='disconnect'),
    re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
]


urlpatterns += staticfiles_urlpatterns()
