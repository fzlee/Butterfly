#!/usr/bin/env python
# coding: utf-8
"""
    permissions.py
    ~~~~~~~~~~

"""
import functools

from apps.core.exceptions import XAPI404Error
from apps.core import codes
from .base_services import BasePageService


def validate_request(target):
    def wrapper_func(func):
        @functools.wraps(func)
        def new_func(self, request, *args, **kwargs):
            if target == "page":
                url = kwargs.get("url")
                request.page = BasePageService.get_page(url=url)
                if not request.page:
                    raise XAPI404Error(code=codes.UNKNOWN_RESOURCE)

            elif target == "comment":
                pk = kwargs.get("pk")
                request.comment = BasePageService.get_comment(pk=pk)
                if not request.comment:
                    raise XAPI404Error
            elif target == "link":
                pk = kwargs.get("pk")
                request.link = BasePageService.get_link(pk=pk)
                if not request.link:
                    raise XAPI404Error
            else:
                raise Exception("Unhandled permission check")
            return func(self, request, *args, **kwargs)
        return new_func
    return wrapper_func
