#!/usr/bin/env python
# coding: utf-8
"""
    serializers.py
    ~~~~~~~~~~

"""
from rest_framework import serializers
from apps.core.serializers import XRoleSerializer


from .models import Page, Link, Comment, Media


class PageSerializer(XRoleSerializer):

    class Meta:
        model = Page
        fields = "__all__"
        anonymous_forbidden_fields = []


class PagePreviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = [
            "url", "title", "tags", "preview", "need_key"
        ]


class NestedPageSerializer(serializers.Serializer):
    url = serializers.CharField()
    title = serializers.CharField()


class LinkSerializer(XRoleSerializer):

    class Meta:
        model = Link
        fields = "__all__"
        anonymous_forbidden_fields = []


class CommentSerializer(XRoleSerializer):
    page =  NestedPageSerializer(required=False)

    class Meta:
        model = Comment
        fields = [
            "id", "page", "email", "nickname", "content", "to", "create_time"
        ]
        anonymous_forbidden_fields = [
            "email"
        ]


class MediaSerializer(XRoleSerializer):

    class Meta:
        model = Media
        fields = "__all__"
        anonymous_forbidden_fields = []
