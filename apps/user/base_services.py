#!/usr/bin/env python
# coding: utf-8
"""
    base_services.py
    ~~~~~~~~~~

"""
import time
import json
import urllib

from apps.core.services import BaseService
from .models import User


class BaseUserService(BaseService):
    _INTERNAL_MODELS = {
        "user": User,
    }
    _INTERNAL_FILTERS = {
    }

    @classmethod
    def set_login_credential_to_cookie(cls, response, user):
        max_age = user.token.expired_at_timestamp - int(time.time())
        response.set_cookie("g.token", user.token.key, max_age=max_age, httponly=False)
        user = {
            "uid": user.uid,
            "nickname": user.nickname,
            "role": user.role
        }
        data = json.dumps(user)
        data = urllib.parse.quote_plus(data, safe=" ")
        data = data.replace("+", "%20")
        response.set_cookie("g.user", data, max_age=max_age)
        return response

    @classmethod
    def generate_login_credential(cls, user):
        return {
            "g.user": {
                "uid": user.uid,
                "nickname": user.nickname,
                "role": user.role
            },
            "g.token": user.token.key
        }

    @classmethod
    def clear_login_credential(cls, request, response):
        response.delete_cookie("g.token")
        response.delete_cookie("g.user")
        for item in request.COOKIES:
            response.delete_cookie(item)
        return response
