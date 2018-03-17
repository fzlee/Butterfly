#!/usr/bin/env python
# coding: utf-8
"""
    apis.py
    ~~~~~~~~~~

"""
from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from django.http.response import HttpResponse

from apps.core.responses import XResponse, XResult
from apps.core.viewsets import XListModelMixin, XUpdateModelMixin
from apps.user.services import UserService
from apps.user.permissions import login_required
from .services import PageService
from .permissions import validate_request


class PageViewSets(viewsets.GenericViewSet, XListModelMixin):
    lookup_field = "url"

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

    @validate_request(target="page")
    def retrieve(self, request, url):
        serializer = PageService.get_serializer(instance=request.page, name="page")
        return XResponse(data=serializer.data)
