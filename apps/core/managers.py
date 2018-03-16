# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import UserManager


class ActivatedUserManager(models.Manager):

    def get_queryset(self):
        return super(ActivatedUserManager, self).get_queryset().filter(activated=True)


class AccountManager(UserManager):

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):

        extra_fields["role"] = "admin"

        return self._create_user(username, email, password, **extra_fields)
