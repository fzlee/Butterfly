#!/usr/bin/env python3
# coding: utf-8
"""

    response.py
    ~~~~~~~~~~

"""
from rest_framework.response import Response
from . import codes


class XResponse(Response):
    """
    初始方法：
        XResponse(result=result)
        XResponse(success=False/True, data=data)
        XResponse(success=Fales/True, message="")

    返回的数据：
        {
            "success": truye/false
            "data" = {} # success
            "error" = {} # fail
        }
    """
    def __init__(self, data=None, outer=None, result=None, success=True, message="", **kwargs):
        self._response_data = {
            "success": None,
        }

        #  传入数据检测
        if result and (data or message):
            error_message = "XReponse mustn't be initialized with result and data at the same time"
            raise Exception(error_message)
        if result and not isinstance(result, XResult):
            raise Exception("result must be instance of XResult")

        # 构建响应内容
        if result:
            self.update_result(result)
        else:
            self.update_response(success, data, message)

        if outer:
            self.update_outer(outer)

        super(XResponse, self).__init__(data=self._response_data, **kwargs)

    def update_result(self, result):
        if result.success:
            self._response_data["success"] = True
            self._response_data["data"] = result.data
        else:
            self._response_data["success"] = False
            self._response_data["error"] = result.error

    def update_response(self, success, data=None, message=""):
        if data and message:
            raise Exception("data and message are both set")

        if success:
            self._response_data["success"] = True
            self._response_data["data"] = data or {}
            # 注意data可以为 空list，[]
            if data is not None:
                self._response_data["data"] = data
            else:
                self._response_data["data"] = {}
        else:
            self._response_data["success"] = False
            self._response_data["error"] = {"message": message}

    def update_outer(self, outer):
        self._response_data.update(outer)

    @classmethod
    def success_or_fail_response(cls, result, key=None,
                                 serializer_class=None,
                                 serializer_params=None):
        """
        if failed, return response with code
        if succeeded
            return serialized data or empty response
        """
        if not result.success:
            return cls(result=result)
        # success response only
        elif result.success and key is None:
            return cls(success=True)
        # serialized response
        else:
            serializer_params = serializer_params or {}
            serializer = serializer_class(result.data[key], **serializer_params)
            return cls(data=serializer.data)


class XResult():
    """ 新式Result类
    XResult 可以使用code初始化，或者手动设定data以及message。如果需要对result进行修改，
    请使用set_code, set_success, set_fail方法
        result = XResult(success=True, data=data)
        result = XResult(code=1234)

        result.set_success(data)

    result里面总是有四个属性，success，code, message and data：
        success为True时，data有效
        success为False时，message有效
        调用set_code方法时，code有效

    """
    def __init__(self, code=0, success=True, data={}, message="", params=None):
        """
        :param params:传入的code对应有message，用params里面的参数format code的message
        """
        if code != 0 and (data or message):
            raise Exception("XResult must not be initialized with code and data at the same time")

        if code:
            self.set_code(code, params)
        else:
            if success:
                self.set_success(data)
            else:
                self.set_fail(message)

    def set_code(self, code, params=None):
        self.success = False
        self.error = {}
        self.error["code"] = code
        self.error["message"] = codes.messages.get(code, codes.DEFAULT_ERROR_MESSAGE)
        if params:
            self.error["message"] = self.error["message"].format(*params)
        self.data = None
        return self

    def set_success(self, data):
        assert isinstance(data, dict) or isinstance(data, list)
        self.success = True
        self.error = None
        self.data = data
        return self

    def set_fail(self, message):
        self.success = False
        self.error = {}
        self.error["code"] = 0
        self.error["message"] = message
        self.data = None
        return self

    @property
    def code(self):
        if self.success:
            return 0
        else:
            return self.error.get("code", 0)

    def __unicode__(self):
        if self.success:
            return "<XResult object, success:{}, {}>".format(self.success, self.data)
        else:
            return "<XResult object, success:{}, {}>".format(self.success, self.error)

    def __repr__(self):
        if self.success:
            return "<XResult object, success:{}, {}>".format(self.success, self.data)
        else:
            return "<XResult object, success:{}, {}>".format(self.success, self.error)

    def as_json_response(self):
        if self.success:
            return {
                "success": True,
                "data": self.data
            }

        else:
            return {
                "success": False,
                "error": self.error
            }
