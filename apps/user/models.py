#!/usr/bin/env python
# coding: utf-8
"""
    models.py
    ~~~~~~~~~~

"""
import time

from django.utils import timezone
from django.utils.timezone import timedelta
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from settings import app_setting
from apps.core.models import XModel
from apps.core.managers import AccountManager, ActivatedUserManager
from helpers import generate_id, generate_user_id


class AuthToken(XModel):
    """
    The default authorization token model.
    """
    key = models.CharField(max_length=20, primary_key=True, unique=True)
    uid = models.CharField(max_length=12, unique=True)
    created = models.DateTimeField(auto_now=True)
    expired_at = models.DateTimeField()

    class Meta():
        db_table = "auth_token"

    @classmethod
    def generate_token_key(cls):
        return generate_id(20)

    @classmethod
    def get_or_create_token(cls, uid):
        token = cls.objects.filter(uid=uid).first()
        if not token:
            token = cls.objects.create(
                uid=uid,
                key=cls.generate_token_key(),
                expired_at=timezone.now()+timedelta(app_setting.DEFAULT_TOKEN_VALID_DAYS)
            )
        return token

    @property
    def user(self):
        if hasattr(self, "_user"):
            return self._user
        else:
            self._user = User.objects.filter(uid=self.uid).first()
            return self._user

    def is_going_to_expired(self):
        """如果token快要过期，自动更新token
        """
        return self.expired_at - timezone.now() <\
            timedelta(hours=app_setting.DEFAULT_TOKEN_VALID_DAYS)

    def is_expired(self):
        return self.expired_at < timezone.now()

    @property
    def expired_at_timestamp(self):
        return time.mktime(self.expired_at.timetuple())

    def extend_token_expired_at(self):
        if self.is_going_to_expired():
            self.expired_at = timezone.now() + timedelta(days=app_setting.DEFAULT_TOKEN_VALID_DAYS)
            self.save()


class User(AbstractBaseUser, XModel):
    """
    uid: 唯一ID， 生成后不允许修改
    username: 全局唯一，作为用户登录名或主页的标识，username可以更改
    password: r"[A-Za-z0-9@#$%^&!+=]{8,}",至少8位
    """

    ROLE_CHOICES = (
        ("admin", "admin"),
        ("reader", "reader"),
    )

    uid = models.CharField(max_length=12, unique=True, default=generate_user_id)
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=50)
    role = models.CharField(max_length=10, default="printer", choices=ROLE_CHOICES)
    avatar = models.CharField(max_length=200, default="")
    activated = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = AccountManager()
    activated_users = ActivatedUserManager()

    class Meta():
        db_table = "user"

    def is_admin(self):
        return self.role == "admin"

    def is_user(self):
        return self.role == "user"

    @property
    def is_staff(self):
        """compability layer for Django
        """
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name

    @property
    def token(self):
        if not hasattr(self, "_token"):
            self._token = AuthToken.get_or_create_token(uid=self.uid)
        if self._token.is_going_to_expired():
            self._token.extend_token_expired_at()
        return self._token
