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
    # path('review_response', views.review_in_response_to_ticket, name='review_response'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
    # re_path(r'^media/(?P<path>.*)$', serve, {
    #         'document_root': settings.MEDIA_ROOT,
    #     }),
]
# Serving the media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()
