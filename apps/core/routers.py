#!/usr/bin/env python3
# coding: utf-8
"""

    routers.py
    ~~~~~~~~~~

"""
from rest_framework.routers import SimpleRouter


class RestRouter(SimpleRouter):
    """A more RESTFul router which ignore trailing_slash based on resource types
    """
    def __init__(self, trailing_slash=True):
        self.trailing_slash = trailing_slash and '/?' or ''
        super(SimpleRouter, self).__init__()
