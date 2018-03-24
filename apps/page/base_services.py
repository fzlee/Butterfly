#!/usr/bin/env python
# coding: utf-8
"""
    base_services.py
    ~~~~~~~~~~

"""
from apps.core.services import BaseService
from .models import Page, Comment, Link, Tag, Media
from .serializers import (
    PageSerializer, LinkSerializer, CommentSerializer,
    MediaSerializer, PagePreviewSerializer, PageMetaSerializer
)
from .filters import PageFilter


class BasePageService(BaseService):

    _INTERNAL_SERIALIZERS = {
        "page": PageSerializer,
        "page_preview": PagePreviewSerializer,
        "page_meta": PageMetaSerializer,
        "link": LinkSerializer,
        "comment": CommentSerializer,
        "media": MediaSerializer
    }
    _INTERNAL_MODELS = {
        "page": Page,
        "tag": Tag,
        "link": Link,
        "comment": Comment,
        "media": Media
    }
    _INTERNAL_FILTERS = {
        "page": PageFilter
    }
