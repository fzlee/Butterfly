#!/usr/bin/env python
# coding: utf-8
"""
    models.py
    ~~~~~~~~~~

"""
import os
import re

import markdown2
from django.db import models
from django.conf import settings

from apps.core.models import XModel


class Page(XModel):
    url = models.CharField(max_length=128, unique=True)
    title = models.CharField(max_length=256)
    content = models.TextField()
    content_digest = models.TextField()
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
    html = models.TextField(default="")

    cleaner = re.compile("<.*?>")

    class Meta:
        db_table = "page"

    @property
    def html_content(self):
        if self.editor == "html":
            return self.content

        return markdown2.markdown(self.content, extras=["febced-code-blocks", "tables", "cuddled-lists"])

    def preview(self):
        if self.need_key:
            return ""
        else:
            return self.content_digest

    def save_digest(self):
        content = re.sub(self.cleaner, '', self.html)
        self.content_digest = content[:200]
        self.save(update_fields=["content_digest"])


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
    page = models.ForeignKey(Page, related_name="sub_tags", on_delete=models.CASCADE)

    class Meta:
        db_table = "tag"


class Media(XModel):

    fileid = models.CharField(max_length=64, unique=True)
    filename = models.CharField(max_length=64)
    # For a give filename , there could be multi file exits
    version = models.IntegerField(default=0)
    content_type = models.CharField(max_length=32)
    size = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    display = models.BooleanField(default=True)

    class Meta:
        db_table = "media"

    def get_filepath(self):
        return os.path.join(settings.MEDIA_ROOT, self.local_filename)

    @property
    def local_filename(self):
        return self.filename
