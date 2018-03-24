#!/usr/bin/env python
# coding: utf-8
"""
    apis.py
    ~~~~~~~~~~

"""
from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route

from apps.core.responses import XResponse
from apps.core.viewsets import XListModelMixin
from apps.core.exceptions import XPermissionDenied
from apps.user.permissions import login_required
from .services import PageService
from .permissions import validate_request
from helpers import parse_size_and_page, get_client_ip


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

    @validate_request(target="page")
    @login_required
    def destroy(self, request, url):
        request.page.delete()
        return XResponse()

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
    @login_required
    def in_place(self, request):
        pk = request.data.get("id", None)
        url = request.data.get("url", None)
        article = PageService.get_page(url=url)

        if article and article.pk != pk:
            return XResponse(data={"in_place": True})

        return XResponse(data={"in_place": False})

    @detail_route(methods=["get", "post"])
    @validate_request(target="page")
    def comments(self, request, url):

        if not request.page.allow_visit:
            raise XPermissionDenied

        if request.method == "GET":
            if request.page.allow_comment:
                comments = PageService.get_comments(page_id=request.page.pk).order_by("pk")
                serializer = PageService.get_serializer("comment", instance=comments, many=True)
                return XResponse(data=serializer.data)
            else:
                return XResponse(data=[])

        if request.page.allow_comment:
            PageService.create_comment(request.page, request.data, get_client_ip(request))
        return XResponse()

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


class CommentViewSets(viewsets.GenericViewSet, XListModelMixin):
    lookup_fiels = "pk"

    @login_required
    def list(self, request):
        queryset = PageService.get_comments().order_by("-pk")
        return self.flexible_list(
            request,
            queryset,
            pagination=True,
            serializer_class=PageService.get_serializer_class("comment"),
        )

    @validate_request("comment")
    @login_required
    def destroy(self, request, pk):
        request.comment.delete()
        return XResponse()
