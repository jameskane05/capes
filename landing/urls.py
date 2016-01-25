from django.conf.urls import include, url
from django.contrib import admin
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.capes, name='capes'),
    url(r'^clients$', views.ClientList.as_view()),
    url(r'^clients/(?P<pk>[0-9]+)$', views.SingleClient.as_view()),
    url(r'^users$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)$', views.SingleUser.as_view()),
    url(r'^email_client$', views.email_client, name='email_client')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns = format_suffix_patterns(urlpatterns)