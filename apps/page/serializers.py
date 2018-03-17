#!/usr/bin/env python
# coding: utf-8
"""
    serializers.py
    ~~~~~~~~~~

"""
from rest_framework import serializers
from apps.core.serializers import XRoleSerializer


from .models import Page


class PageSerializer(XRoleSerializer):

    class Meta:
        model = Page
        fields = "__all__"
        anonymous_forbidden_fields = [
            "need_key", "password", "allow_visit", "allow_comment"
        ]