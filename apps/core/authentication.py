#!/usr/bin/env python3
# coding: utf-8
"""

    authentication.py
    ~~~~~~~~~~

"""
import logging

from rest_framework.authentication import (BaseAuthentication, get_authorization_header)

from apps.user.models import AuthToken
from apps.core.globals import g
from . import codes
from .exceptions import XAuthenticationFailed

logger = logging.getLogger('auth')


class XTokenAuthentication(BaseAuthentication):
    auth_model = AuthToken
    keyword = "Token"

    def authenticate(self, request):
        header = get_authorization_header(request)
        auth = header.split()

        # 请求不包含token，那么使用下一个认证方式
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) != 2:
            raise XAuthenticationFailed(code=codes.INVALID_TOKEN)
        return self.authenticate_credentials(auth[1])

    def authenticate_credentials(self, key):
        token = self.auth_model.objects.filter(key=key).first()
        if token is None or token.is_expired():
            raise XAuthenticationFailed(code=codes.INVALID_TOKEN)
        elif not token.user.activated:
            raise XAuthenticationFailed(code=codes.INVALID_ACCOUNT)

        # 注入user
        g.user = token.user
        return token.user, token


class XCookieAuthentication(BaseAuthentication):
    """ Authenticate via user.token
    """
    auth_model = AuthToken

    def authenticate(self, request, cookie_name="g.token"):
        key = request.COOKIES.get(cookie_name, None)
        if not key:
            return None

        token = self.auth_model.objects.filter(key=key).first()
        if token is None or token.is_expired():
            raise XAuthenticationFailed(code=codes.INVALID_TOKEN)
        elif not token.user.activated:
            raise XAuthenticationFailed(code=codes.INACTIVE_ACCOUNT)

        g.user = token.user
        return token.user, token
