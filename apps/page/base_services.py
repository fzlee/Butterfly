#!/usr/bin/env python
# coding: utf-8
"""
    base_services.py
    ~~~~~~~~~~

"""
import smtplib
import threading
from email.mime.text import MIMEText

from apps.core.services import BaseService
from settings import app_setting
from .models import Page, Comment, Link, Tag, Media
from .serializers import (
    PageSerializer, LinkSerializer, CommentSerializer,
    MediaSerializer, PagePreviewSerializer, PageMetaSerializer
)
from .filters import PageFilter


class BasePageService(BaseService):

    _INTERNAL_SERIALIZERS = {
        "page": PageSerializer,
        "page_preview": PagePreviewSerializer,
        "page_meta": PageMetaSerializer,
        "link": LinkSerializer,
        "comment": CommentSerializer,
        "media": MediaSerializer
    }
    _INTERNAL_MODELS = {
        "page": Page,
        "tag": Tag,
        "link": Link,
        "comment": Comment,
        "media": Media
    }
    _INTERNAL_FILTERS = {
        "page": PageFilter
    }

    @classmethod
    def get_email_client(cls):
        if not app_setting.SMTP_ENABLED:
            return None

        client = smtplib.SMTP_SSL(
            host=app_setting.SMTP_HOST,
            port=app_setting.SMTP_PORT
        )
        client.login(app_setting.SMTP_USERNAME, app_setting.SMTP_PASSWORD)
        return client

    @classmethod
    def send_email(cls, client, to_user, title, content):
        """
        sendemail with subprocesses, this is not recommaneded on high concurrent webservices though
        """
        message = MIMEText(content)
        message["Subject"] = title
        message["To"] = to_user
        message["From"] = app_setting.SMTP_USERNAME
        client = cls.get_email_client()
        client.send_message(message)

    @classmethod
    def send_email_async(cls, to_user, title, content):
        t = threading.Thread(target=cls.send_email, args=(cls, to_user, title, content))
        t.start()
