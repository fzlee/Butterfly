#!/usr/bin/env python
# coding: utf-8
"""
    base_services.py
    ~~~~~~~~~~

"""
from apps.core.services import BaseService
from .models import Page, Comment, Link, Tag
from .serializers import PageSerializer, LinkSerializer, CommentSerializer
from .filters import PageFilter


class BasePageService(BaseService):

    _INTERNAL_SERIALIZERS = {
        "page": PageSerializer,
        "link": LinkSerializer,
        "comment": CommentSerializer
    }
    _INTERNAL_MODELS = {
        "page": Page,
        "tag": Tag,
        "link": Link,
        "comment": Comment
    }
    _INTERNAL_FILTERS = {
        "page": PageFilter
    }
