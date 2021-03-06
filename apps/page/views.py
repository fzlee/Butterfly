#!/usr/bin/env python
# coding: utf-8
"""
    views.py
    ~~~~~~~~~~

"""
from datetime import datetime

from django.conf import settings
from django.contrib.syndication.views import Feed
from django.shortcuts import render
from rest_framework.views import APIView

from helpers import generate_external_url
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
        if article.need_key:
            return "需要输入密码访问"
        return article.html_content

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, article):
        return generate_external_url(article.url)


class SiteMapView(APIView):

    def get(self, request):
        """Generate sitemap.xml. Makes a list of urls and date modified.
        """
        # user model postlist
        records = []
        pages = PageService.get_pages(allow_visit=True, need_key=False).order_by("-pk")

        url = settings.BASE_URL
        if pages:
            modified_time = pages[0].update_time.date().isoformat()
        else:
            modified_time = datetime.now().date().isoformat()
        records.append({
            "url": url,
            "time": modified_time,
            "priority": 1.0
        })

        for page in pages:
            url = generate_external_url(page.url)
            modified_time = page.update_time.date().isoformat()
            records.append({
                "url": url,
                "time": modified_time,
                "priority": 0.7
            })

        return render(
            request,
            "sitemap.xml",
            context={"pages": records},
            content_type="application/xml"
        )
