#!/usr/bin/env python
# coding: utf-8
"""
    apis.py
    ~~~~~~~~~~

"""
import os

from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route

from apps.core.responses import XResponse
from apps.core.viewsets import XListModelMixin
from apps.core.exceptions import XAPI404Error
from apps.user.permissions import login_required
from .services import PageService
from .permissions import validate_request
from helpers import get_client_ip


class ArticleViewSets(viewsets.GenericViewSet, XListModelMixin):
    lookup_field = "url"

    @login_required
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
    @login_required
    def retrieve(self, request, url):
        serializer = PageService.get_serializer(instance=request.page, name="page")
        return XResponse(data=serializer.data)

    @list_route()
    def preview(self, request):
        queryset = PageService.get_pages(allow_visit=True).order_by("-pk")
        return self.flexible_list(
            request,
            queryset,
            pagination=True,
            serializer_class=PageService.get_serializer_class("page_preview"),
        )

    @detail_route(methods=["get", "post"])
    @validate_request(target="page")
    def meta(self, request, url):
        if not request.page.allow_visit:
            return XResponse(data={})

        if request.method == "GET":
            serializer = PageService.get_serializer(name="page_meta", instance=request.page)
            data = serializer.data
            if request.page.need_key:
                data.pop("content", None)
            return XResponse(data=data)

        password = request.data.get("password")
        if request.page.password == password:
            serializer = PageService.get_serializer(name="page_meta", instance=request.page)
            return XResponse(data=serializer.data)
        return XResponse(success=False, message="密码错误")

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
            return XResponse(data=[])

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
    @login_required
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

    @list_route()
    def search(self, request):
        tagname = request.query_params.get("tagname", "")
        tagname = "," + tagname + ","

        pages = PageService.get_pages(allow_visit=True).filter(
            tags__icontains=tagname
        )
        return self.flexible_list(
            request,
            pages,
            pagination=True,
            serializer_class=PageService.get_serializer_class("page_preview")
        )


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


class LinkViewSets(viewsets.GenericViewSet, XListModelMixin):

    lookup_field = "pk"

    @login_required
    def list(self, request):
        queryset = PageService.get_links().order_by("-pk")
        return self.flexible_list(
            request,
            queryset,
            serializer_class=PageService.get_serializer_class("link"),
            pagination=True
        )

    @validate_request(target="link")
    @login_required
    def destroy(self, request, pk):
        request.link.delete()
        return XResponse()

    @validate_request(target="link")
    @login_required
    def update(self, request, pk):
        display = request.data.get("display", False)
        request.link.display = display
        request.link.save()
        return XResponse()

    @login_required
    def create(self, request):
        PageService.create_link(request.data)
        return XResponse()

class MediaViewSets(viewsets.GenericViewSet, XListModelMixin):

    @login_required
    def list(self, request):
        queryset = PageService.get_medias().order_by("-pk")
        return self.flexible_list(
            request,
            queryset,
            pagination=True,
            serializer_class=PageService.get_serializer_class("media")
        )

    @login_required
    @list_route(methods=["post"])
    def upload(self, request):
        file = request.FILES["file"]
        name = request.FILES["file"].name
        content_type = file.content_type
        PageService.create_media(file, name, content_type)
        return XResponse()

    @login_required
    def destroy(self, request, pk):
        media = PageService.get_media(pk=pk)
        if not media:
            raise XAPI404Error

        path = media.get_filepath()
        try:
            os.remove(path)
        except:
            pass

        media.delete()
        return XResponse()
