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
