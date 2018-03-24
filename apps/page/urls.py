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
router.register("articles", apis.ArticleViewSets, base_name="articles")
router.register("comments", apis.CommentViewSets, base_name="comments")
router.register("links", apis.LinkViewSets, base_name="links")

urlpatterns = [
    url(r"^", include(router.urls)),
]
