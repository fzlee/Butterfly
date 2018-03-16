#!/usr/bin/env python3
# coding: utf-8
"""

    codes.py
    ~~~~~~~~~~

"""

# 常用的错误
DEFAULT_ERROR = 100
DEFAULT_ERROR_MESSAGE = "未知错误"
HAS_NO_PERMISSION = 102
HAS_NO_PERMISSION_MESSAGE = "您没有权限执行这个操作"
TOO_MANY_REQUESTS = 103
TOO_MANY_REQUESTS_MESSAGE = "您的请求过于频繁"
UNKNOWN_RESOURCE = 104
UNKNOWN_RESOURCE_MESSAGE = "资源不存在"
UNKNOWN_USER = 105
UNKNOWN_USER_MESSAGE = "用户不存在"
UNKNOWN_USER_PASSWORD = 106
UNKNOWN_USER_PASSWORD_MESSAGE = "用户名密码错误"


# 用户验证相关
INVALID_TOKEN = 111
INVALID_TOKEN_MESSAGE = "无效token"
INVALID_ACCOUNT = 112
INVALID_ACCOUNT_MESSAGE = "无效帐户"


messages = {}
for name in dir():
    if not name.startswith('__') and name != 'messages' and not name.endswith('_MESSAGE'):
        messages[globals()[name]] = globals()[name + '_MESSAGE']


def errors(code):
    return {
        "message": messages.get(code, ""),
        "code": code
    }
