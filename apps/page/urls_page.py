#!/usr/bin/env python
# coding: utf-8
"""
    urls_page.py
    ~~~~~~~~~~

"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^rss", views.LatestEntriesFeed())
]
