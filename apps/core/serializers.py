#!/usr/bin/env python3
# coding: utf-8
"""

    serialziers.py
    ~~~~~~~~~~

"""
from rest_framework.serializers import (
    ModelSerializer
)


class XRoleSerializer(ModelSerializer):
    """ 根据role决定哪些需要被序列化
    """
    def __init__(self, *args, **kwargs):
        role = kwargs.pop("role", "anonymous")
        super(XRoleSerializer, self).__init__(*args, **kwargs)

        # 将不合理的字段pop出来
        assert role in ("admin", "user", "anonymous"),\
            "{} is not a valid role".format(role)

        if role != "admin":
            for forbidden_field in self.get_forbidden_fields(role):
                self.fields.pop(forbidden_field, None)

    def get_forbidden_fields(self, role):
        key = role + "_forbidden_fields"
        if hasattr(self.Meta, key):
            return getattr(self.Meta, key)
        else:
            return getattr(self.Meta, "anonymous_forbidden_fields")

