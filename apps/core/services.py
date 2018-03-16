#!/usr/bin/env python3
# coding: utf-8
"""

    services.py
    ~~~~~~~~~~

"""
import json

from rest_framework.fields import empty


class SelectDBMetaClass(type):

    def __getattr__(cls, name):
        # 获取model的参数
        if name.startswith("get_"):
            model_name = name.split("get_", 1)[1]
            get_list = False
            if model_name.endswith("s"):
                model_name = model_name[:-1]
                get_list = True

            model_class = cls._INTERNAL_MODELS.get(model_name, None)
            if not model_class:
                raise AttributeError("'{}' has no model '{}'".format(cls.__name__, model_name))

            return model_class.get_list if get_list else model_class.get_one
        raise AttributeError("'{}' has no attribute '{}'".format(cls.__name__, name))


class BaseService(object, metaclass=SelectDBMetaClass):
    _INTERNAL_MODELS = {}
    _INTERNAL_SERIALIZERS = {}
    _INTERNAL_FILTERS = {}

    @classmethod
    def get_model_class(cls, name):
        assert name in cls._INTERNAL_MODELS, "{} is not in internal models".format(name)
        return cls._INTERNAL_MODELS[name]

    @classmethod
    def get_serializer_class(cls, name):
        assert name in cls._INTERNAL_SERIALIZERS, "{} is not in internal serializers".format(name)
        return cls._INTERNAL_SERIALIZERS[name]

    @classmethod
    def get_serializer(cls, name, instance=None, data=empty, body=empty, **kwargs):
        """
        instance: django model instance
        data: request.data
        body: request.body
        """
        # 如果传入了body，将body反序列化，传给data
        if body != empty:
            data = json.loads(body.decode("utf8"))

        serializer_class = None

        # 如果传入了name， 使用name对应的serializer，否则自动判定
        serializer_class = cls.get_serializer_class(name=name)
        return serializer_class(instance=instance, data=data, **kwargs)

    @classmethod
    def get_filter_class(cls, name):
        assert name in cls._INTERNAL_FILTERS, "{} is not in internal filters".format(name)
        return cls._INTERNAL_FILTERS[name]
