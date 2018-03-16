#!/usr/bin/env python3
# coding: utf-8
"""

    serialziers.py
    ~~~~~~~~~~

"""
from rest_framework.serializers import (
    Serializer
)


class EmptySerializer(Serializer):
    """Serializer class which used to serialize empty list
    """
    def __init__(self, *args, **kwargs):
        """ serializer有时会被传入role参数，将这个参数忽略掉
        """
        kwargs.pop("role", "user")
        super(EmptySerializer, self).__init__(*args, **kwargs)
