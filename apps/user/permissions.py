#!/usr/bin/env python
# coding: utf-8
"""
    permissions.py
    ~~~~~~~~~~

"""
import functools
from apps.core.exceptions import XAuthenticationFailed


def login_required(func):
    @functools.wraps(func)
    def new_func(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise XAuthenticationFailed
        return func(self, request, *args, **kwargs)

    return new_func
