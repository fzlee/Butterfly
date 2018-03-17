#!/usr/bin/env python
# coding: utf-8
"""
    apis.py
    ~~~~~~~~~~

"""
import io
import urllib

from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from django.http.response import HttpResponse

from apps.core.responses import XResponse, XResult
from apps.core.exceptions import XAPI404Error
from apps.core.viewsets import XListModelMixin, XUpdateModelMixin
from apps.user.services import UserService
from apps.user.permissions import login_required
from .services import PageService


class PageViewSets(viewsets.GenericViewSet, XListModelMixin):

    # @login_required
    def list(self, request):
        queryset = PageService.get_pages().order_by("-pk")
        return self.flexible_list(
            request,
            queryset,
            pagination=True,
            serializer_class=PageService.get_serializer_class("page"),
            filter_class=PageService.get_filter_class("page")
        )
