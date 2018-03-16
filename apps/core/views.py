#!/usr/bin/env python3
# coding: utf-8
"""

    views.py
    ~~~~~~~~~~

"""
from rest_framework.views import exception_handler, APIView


def xexception_handler(exc, context):
    """
    exception_handler 可以处理三种exception，并返回response
    对于不能处理的 exception，返回None
    """
    response = exception_handler(exc, context)
    if response:
        response.data = {"success": False,  "error": response.data}
    return response


class LazyAuthView(APIView):
    def perform_authentication(self, request):
        """
        不执行授权操作，首次调用request.user时才会触发
        """
        pass
