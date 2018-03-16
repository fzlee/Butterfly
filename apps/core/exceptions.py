#!/usr/bin/env python3
# coding: utf-8
"""

    exceptions.py
    ~~~~~~~~~~

"""
import logging
import json

from rest_framework import status
from rest_framework import exceptions

from . import codes


logger = logging.getLogger("apps.exception")


class XAPIError(exceptions.APIException):
    """
    Modified rest_framework's APIException to add errors in detail.
    Useage:
        raise XAPI404Error(code=0, message="")
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = codes.DEFAULT_ERROR_MESSAGE

    def __init__(self, code=0, message=None, status=status.HTTP_500_INTERNAL_SERVER_ERROR):
        """
        self.detail 会被exception_handler直接传递给response.data
        """
        self.detail = {}
        if code != 0:
            self.detail = {
                "message": codes.messages.get(code, codes.DEFAULT_ERROR_MESSAGE),
                "code": code
            }
        elif message:
            self.detail = {"message": message}

        XAPIError.status_code = status
        logger.error(json.dumps(self.detail))

    def __str__(self):
        return json.dumps(self.detail)


class XGeneralException(XAPIError):
    """返回消息为200的异常
    使用方法：
        raise XGeneralException(code=codes.xxxx))
    """
    def __init__(self, code, message):
        super(XGeneralException, self).__init__(code, message, 200)


class XAPI404Error(XAPIError):
    def __init__(self, code=0, message=u"您查看的资源不存在"):
        super(XAPI404Error, self).__init__(code, message, status=status.HTTP_404_NOT_FOUND)


class XAuthenticationFailed(XAPIError):
    def __init__(self, code=0, message=u"您没有登录或者登录状态过期"):
        super(XAuthenticationFailed, self).__init__(code, message, status.HTTP_401_UNAUTHORIZED)


class XPermissionDenied(XAPIError):
    def __init__(self, code=0, message=u"您没有足够权限执行此操作"):
        super(XPermissionDenied, self).__init__(code, message, status.HTTP_403_FORBIDDEN)


class XValidationError(XAPIError):
    def __init__(self, code=0, message=u"参数验证失败"):
        assert isinstance(code, int), "您传入的code不合法"
        super(XValidationError, self).__init__(code, message, status.HTTP_400_BAD_REQUEST)


class XMethodNotAllowed(XAPIError):
    def __init__(self, code=0, message=u"HTTP方法不受支持"):
        super(XMethodNotAllowed, self).__init__(code, message, status.HTTP_405_METHOD_NOT_ALLOWED)


class InvalidAttributeException(Exception):
    """ raised when assigning unknown attribute to jsonfield
    """
    pass
