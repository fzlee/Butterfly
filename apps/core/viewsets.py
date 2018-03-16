#!/usr/bin/env python3
# coding: utf-8
"""

    viewsets.py
    ~~~~~~~~~~

"""
from .responses import XResponse


class XListModelMixin(object):
    """
    传入自定义的queryset，serializer_class以及filter_class 返回分页并序列化后的数据。
    目前只支持djanog-filter
    """
    def flexible_list(self, request,
                      queryset,
                      serializer_class=None,
                      filter_class=None,
                      pagination=True,
                      return_count=False,
                      aggregate_function=None,
                      aggregate_kwargs=None,
                      *args, **kwargs):
        aggregate_kwargs = aggregate_kwargs or {}

        # 应用filter
        if filter_class:
            queryset = self.flexible_filter_queryset(queryset, filter_class)

        # 如果是登录用户， 根据用户角色返回数据
        serialize_kwargs = {"many": True}
        # 应用pagination, 且有分页信息， 返回分页结果
        if pagination:
            request.return_count = return_count
            page = self.paginate_queryset(queryset)
            if page is not None:
                # 向数据里面填充数据
                if aggregate_function:
                    page = aggregate_function(page, **aggregate_kwargs)
                serializer = serializer_class(page, **serialize_kwargs)
                return self.get_paginated_response(serializer.data)

        serializer = serializer_class(queryset, **serialize_kwargs)
        return XResponse(data=serializer.data)

    def flexible_filter_queryset(self, queryset, filter_class):
        return filter_class(self.request.query_params, queryset=queryset).qs


class XUpdateModelMixin(object):
    """
    1. no PATCH method
    2. return whole resource if request succeeded
    """
    def update(self, request, *args, **kwargs):
        instance = kwargs.get("instance") or self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return XResponse(data=serializer.data)

    def perform_update(self, serializer):
        serializer.save()
