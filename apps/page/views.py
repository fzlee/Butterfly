#!/usr/bin/env python
# coding: utf-8
"""
    views.py
    ~~~~~~~~~~

"""
from django.conf import settings
from django.contrib.syndication.views import Feed

from apps.page.services import PageService


class LatestEntriesFeed(Feed):
    title = settings.BLOG_NAME
    link = "/rss"
    description = "偶尔会更新"

    def items(self):
        return PageService.get_pages(allow_visit=True).order_by("-pk")[:20]

    def item_title(self, article):
        return article.title

    def item_description(self, article):
        return article.html_content

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, article):
        return settings.BASE_URL + "pages/" + article.url

