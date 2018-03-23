#!/usr/bin/env python
# coding: utf-8
"""
    views.py
    ~~~~~~~~~~

"""
from django.shortcuts import redirect
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.renderers import StaticHTMLRenderer

from apps.core.responses import XResponse, XResult
from apps.core.views import LazyAuthView
from apps.core import codes
from .services import UserService


class LoginView(APIView):

    permission_classes = []

    def post(self, request):
        username = request.data.get("username", None)
        password = request.data.get("password", None)

        user = UserService.get_users().filter(Q(username=username) | Q(email=username)).first()
        if not user or not user.check_password(password):
            return XResponse(result=XResult(code=codes.UNKNOWN_USER_PASSWORD))

        response = XResponse(success=True, data={})
        UserService.set_login_credential_to_cookie(response, user)
        return response


class LogoutView(LazyAuthView):
    renderer_classes = [StaticHTMLRenderer]
    permission_classes = []

    def get(self, request):
        return self.logout(request)

    def post(self, request):
        return self.logout(request)

    def logout(self, request):
        """
        """
        url = request.GET.get("url", "/")
        response = redirect(url)
        return UserService.clear_login_credential(request, response)
