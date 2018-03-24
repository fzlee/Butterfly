#!/usr/bin/env python



# coding: utf-8
"""
    services.py
    ~~~~~~~~~~

"""
from django.db import connection

from .base_services import BasePageService
from .models import Page, Comment
from settings import app_setting
from helpers import cached


class PageService(BasePageService):
    pass

    @classmethod
    def generate_sidebar(cls):
        return {
            "announcement": cls.generate_sidebar_announcement(),
            "links": cls.generate_sidebar_links(),
            "comments": cls.generate_sidebar_comments(),
            "tags": cls.generate_sidebar_tags()
        }

    @classmethod
    @cached(default_max_age=1 * 60 * 60)
    def generate_sidebar_announcement(cls):
        url = app_setting.BLOG_ANNOUNCEMENT_URL
        page = cls.get_page(url=url)
        if not page:
            return {}

        return {
            "url": url,
            "content": page.content[:200]
        }

    @classmethod
    @cached(default_max_age=1 * 60 * 60)
    def generate_sidebar_links(cls):
        links = PageService.get_links(display=True).order_by("-pk")[:12]
        return cls.get_serializer(name="link", instance=links, many=True).data

    @classmethod
    @cached(default_max_age=1 * 60 * 60)
    def generate_sidebar_comments(cls):
        comments = PageService.get_comments(
            page__allow_visit=True,
            page__allow_comment=True
        ).order_by("-pk")[:8]
        return cls.get_serializer(name="comment", instance=comments, many=True).data

    @classmethod
    @cached(default_max_age=1 * 60 * 60)
    def generate_sidebar_tags(cls):
        with connection.cursor() as cursor:
            cursor.execute("select name from tag group by name order by count(name) desc")
            records = cursor.fetchall()
            return [i[0] for i in records]

    @classmethod
    def update_page(cls, page, data):
        """
        """
        data.pop("id", None)

        for key, value in data.items():
            setattr(page, key, value)

        if not page.tags.startswith(","):
            page.tags = "," + page.tags
        if not page.tags.endswith(","):
            page.tags = page.tags + ","

        page.save()
        return page

    @classmethod
    def create_page(cls, data):
        page = Page.objects.create(**data)
        if not page.tags.startswith(","):
            page.tags = "," + page.tags
        if not page.tags.endswith(","):
            page.tags = page.tags + ","

        page.save()
        return page

    @classmethod
    def create_comment(cls, page, data, ip=""):
        """
        data = {
            "nickname": "",
            "comment_id": None,
            "website": "",
            "email": ""
        }
        """
        if data.get("comment_id", None):
            comment = cls.get_comment(pk=data["comment_id"])
            to = comment.nickname
        else:
            comment = None
            to = ""

        Comment.objects.create(
            page=page,
            email=data.get("email", "").strip(),
            nickname=data.get("nickname").strip(),
            website=data.get("website", ""),
            content=data.get("content"),
            parent_comment=comment,
            ip=ip,
            to=to
        )
