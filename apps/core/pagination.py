#!/usr/bin/env python3
# coding: utf-8
"""

    pagination.py
    ~~~~~~~~~~

"""
from django.conf import settings
from rest_framework import pagination

from .responses import XResponse


class XPagination(pagination.BasePagination):
    """
    比django还要简单的分页器，主要是为了避免count(*)的sql操作
    """
    page_size = settings.PAGE_SIZE

    # Client can control the page using this query parameter.
    page_query_param = 'page'

    # Client can control the page size using this query parameter.
    # Default is 'None'. Set to eg 'page_size' to enable usage.
    page_size_query_param = None

    # Set to an integer to limit the maximum page size the client may request.
    # Only relevant if 'page_size_query_param' has also been set.

    last_page_strings = ('last',)

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        page_number = int(request.query_params.get(self.page_query_param, 1))

        self.page = queryset[page_size * (page_number - 1): page_size * page_number]
        self.request = request
        if getattr(request, "return_count") is True:
            self.count = queryset.count()
        return list(self.page)

    def get_paginated_response(self, data):
        if getattr(self.request, "return_count", False) is True:
            outer = {"count": self.count}
        else:
            outer = {}
        return XResponse(data=data, outer=outer)

    def get_page_size(self, request):
        size = request.query_params.get("size", "")
        if size.isdigit():
            size = int(size)
            if size <= 100:
                return size
            else:
                return 100
        return self.page_size
