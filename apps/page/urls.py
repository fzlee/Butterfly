#!/usr/bin/env python
# coding: utf-8
"""
    urls.py
    ~~~~~~~~~~

"""
from . import apis

from django.conf.urls import url, include
from rest_framework import routers


router = routers.SimpleRouter(trailing_slash=False)
router.register("pages", apis.PageViewSets, base_name="pages")

urlpatterns = [
    url(r"^", include(router.urls)),
]
