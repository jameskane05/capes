from django.conf.urls import include, url
from django.contrib import admin
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^/[a-zA-Z0-9_]*$', views.work_sample, name='work_sample'),
    url(r'^/(?P<pk>[0-9]+)$', views.SingleWork.as_view()),
    url(r'^', views.WorkList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)