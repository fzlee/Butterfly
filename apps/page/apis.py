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
from helpers import cached, parse_size_and_page


class ArticleViewSets(viewsets.GenericViewSet, XListModelMixin):
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

    @list_route()
    def sidebar(self, request):
        return XResponse(
            data=PageService.generate_sidebar()
        )

    @list_route()
    def preview(self, request):
        pages = PageService.get_pages().order_by("-pk")

        size, page = parse_size_and_page(request)
        pages = pages[(page - 1) * size: page * size]

        serializer = PageService.get_serializer(name="page", instance=pages, many=True)
        pages = serializer.data
        for page in pages:
            page["content"] = page["content"][:200]

        return XResponse(data=pages)

    @list_route(methods=["post"])
    def in_place(self, request):
        pk = request.data.get("id", None)
        url = request.data.get("url", None)
        article = PageService.get_page(url=url)

        if article and article.pk != pk:
            return XResponse(data={"in_place": True})

        return XResponse(data={"in_place": False})

    @list_route(methods=["put"])
    def save(self, request):
        data = request.data
        if "id" not in data:
            page = PageService.create_page(data)
            serializer = PageService.get_serializer(name="page", instance=page)
            return XResponse(data=serializer.data)

        page = PageService.get_page(pk=data["id"])
        data.pop("id")
        page = PageService.update_page(page, data)

        serializer = PageService.get_serializer(name="page", instance=page)
        return XResponse(data=serializer.data)
