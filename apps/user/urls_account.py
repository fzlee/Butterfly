#!/usr/bin/env python
# coding: utf-8
"""
    account_urls.py
    ~~~~~~~~~~

"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^login", views.LoginView.as_view()),
    url(r"^logout", views.LogoutView.as_view()),
]
