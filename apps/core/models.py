#!/usr/bin/env python3
# coding: utf-8
"""

    models.py
    ~~~~~~~~~~

"""
import functools

from django.db import models
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist


class CacheManager(models.Manager):
    pass


def get_or_none(old_func):
    """
    get one from database and
        1. return None if nothing returned
        2. raise Exception if multiple recortds returned
    """
    @functools.wraps(old_func)
    def new_func(*args, **kwargs):
        try:
            return old_func(*args, **kwargs)
        except ObjectDoesNotExist:
            return None
    return new_func


class XModel(models.Model):
    """
    全局的model类
    """
    objects = CacheManager()

    @classmethod
    @get_or_none
    def get_one(cls, **kwargs):
        return cls.objects.get(**kwargs)

    @classmethod
    def get_list(cls, **kwargs):
        return cls.objects.filter(**kwargs)

    class Meta():
        abstract = True


class XAnonymousUser(AnonymousUser):
    """
    定义匿名用户
    """
    def __init__(self):
        self.role = "anonymous"
        self.uid = None

    def is_anonymous(self):
        return True

    def is_admin(self):
        return False

    def is_user(self):
        return False


class BaseUniqueIDModel(models.Model):
    """ A model does nothing but help to generate unique increasing unique numbers
    """
    class Meta:
        abstract = True

    @classmethod
    def generate_id(cls):
        instance = cls.objects.create()
        return instance.pk
