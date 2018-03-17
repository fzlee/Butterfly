#!/usr/bin/env python
# coding: utf-8
"""
    filters.py
    ~~~~~~~~~~

"""
import django_filters
from .models import Page


class PageFilter(django_filters.FilterSet):

    class Meta:
        model = Page
        fields = [
            "title", "need_key", "editor", "allow_visit", "allow_comment"
        ]
