#!/usr/bin/env python
# coding: utf-8
"""
    models.py
    ~~~~~~~~~~

"""
from django.db import models
from apps.core.models import XModel


class Page(XModel):
    url = models.CharField(max_length=128, unique=True)
    title = models.CharField(max_length=256)
    raw_content = models.TextField()
    content = models.TextField()
    keywords = models.CharField(max_length=256, default="")
    metacontent = models.CharField(max_length=256, default="")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    # access control
    need_key = models.BooleanField(default=False)
    password = models.CharField(max_length=20, default="")

    # tag seperated by comma
    tags = models.CharField(max_length=256, default="")
    # editor html or markdown
    editor = models.CharField(max_length=10, choices=(("html", "html"), ("markdown", "markdown")))

    allow_visit = models.BooleanField(default=False)
    allow_comment = models.BooleanField(default=True)
    is_original = models.BooleanField(default=True)
    num_lookup = models.IntegerField(default=0)

    class Meta:
        db_table = "page"


class Link(XModel):

    name = models.CharField(max_length=64)
    href = models.CharField(max_length=1024)
    description = models.CharField(max_length=64)
    create_time = models.DateTimeField(auto_now_add=True)
    display = models.BooleanField()

    class Meta:
        db_table = "link"


class Comment(XModel):

    page = models.ForeignKey(Page, related_name="comments", on_delete=models.CASCADE)
    email = models.CharField(max_length=64)
    nickname = models.CharField(max_length=20)
    content = models.CharField(max_length=1024)
    parent_comment = models.ForeignKey(
        'self',
        null=True,
        related_name="sub_comments",
        on_delete=models.CASCADE
    )
    to = models.CharField(max_length=20, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=64)
    website = models.CharField(max_length=64)

    class Meta:
        db_table = "comment"


class Tag(XModel):

    name = models.CharField(max_length=64)
    post = models.ForeignKey(Page, related_name="sub_tags", on_delete=models.CASCADE)

    class Meta:
        db_table = "tag"
