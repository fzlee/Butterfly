#!/usr/bin/env python
# coding: utf-8
"""
    fields.py
    ~~~~~~~~~~

"""
import json
from jsonfield import JSONField

from django.db import models

from .exceptions import InvalidAttributeException


class StaticJSON(object):
    def __init__(self, default, value):
        self.__dict__["_default"] = default
        self.__dict__["_value"] = value
        for k, v in self._default.items():
            self.__dict__["_value"].setdefault(k, v)

    def __getattr__(self, name):
        if name in self.__dict__.get("_default", {}):
            return self.__dict__["_value"][name]
        else:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        if name == "_default" or name == "_value":
            setattr(self.__dict__[name], name, value)

        if name not in self.__dict__["_default"]:
            raise InvalidAttributeException("{} is not a valid attribute, try {} instead".format(
                name, ", ".join(self.__dict__["_default"].keys())
            ))
        self.__dict__["_value"][name] = value

    @property
    def internal_value(self):
        return self._value

    def items(self):
        """ used for serializer.to_representation
        """
        return self._value.items()

    def __iter__(self):
        """ for i in StaticJSON:
                pass
        """
        for item in self._value:
            yield item

    def __unicode__(self):
        return "<StaticJSON instance: {}>".format(json.dumps(self._value))

    def __repr__(self):
        return "<StaticJSON instance: {}>".format(json.dumps(self._value))


class StaticJSONField(JSONField):
    """
    a JSONField that accepts attributes based on pre-defined styles
    """
    def __init__(self, *args, **kwargs):
        super(StaticJSONField, self).__init__(*args, **kwargs)
        self._default = kwargs.get("default")

    def pre_init(self, value, obj):
        value = super(StaticJSONField, self).pre_init(value, obj)
        if isinstance(value, StaticJSON):
            return value
        return StaticJSON(self._default, value)

    def get_db_prep_value(self, value, connection, prepared=False):
        """Convert JSON object to a string"""
        if self.null and value is None:
            return None

        if isinstance(value, StaticJSON):
            return json.dumps(value.internal_value, **self.dump_kwargs)
        else:
            return json.dumps(value)


class TruncatingCharField(models.CharField):
    def get_prep_value(self, value):
        value = super(TruncatingCharField, self).get_prep_value(value)
        if value:
            return value[:self.max_length]
        return value
