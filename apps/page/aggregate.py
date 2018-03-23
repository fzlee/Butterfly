#!/usr/bin/env python
# coding: utf-8
"""
    aggregate.py
    ~~~~~~~~~~

"""
from apps.core.aggregate import BaseAggregator
from apps.page.base_services import BasePageService


class CommentAggregator(BaseAggregator):

    @classmethod
    def update_comments(cls, comments):

        return cls.aggregate_items(
            comments,
            BasePageService.get_pages(),
            "page",
            "page_id",
            "pk"
        )
