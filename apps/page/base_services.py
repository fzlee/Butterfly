#!/usr/bin/env python
# coding: utf-8
"""
    base_services.py
    ~~~~~~~~~~

"""
from apps.core.services import BaseService
from .models import Page
from .serializers import PageSerializer
from .filters import PageFilter


class BasePageService(BaseService):

    _INTERNAL_SERIALIZERS = {
        "page": PageSerializer
    }
    _INTERNAL_MODELS = {
        "page": Page
    }
    _INTERNAL_FILTERS = {
        "page": PageFilter
    }
