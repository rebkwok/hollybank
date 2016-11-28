# -*- coding: utf-8 -*-

from django.conf.urls import url
from web.views import home_view


urlpatterns = [
    url(r'^', home_view, name='home'),
]