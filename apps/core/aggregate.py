#!/usr/bin/env python
# coding: utf-8
"""
    aggregate.py
    ~~~~~~~~~~

"""

class BaseAggregator():

    @classmethod
    def aggregate_items(cls, instances, queryset, attribute, keyword1, keyword2=None):
        """
        如果 instances[i].keyword1 == model.keyword2
        则instances[i].attribute = model
        """
        keyword2 = keyword2 or keyword1

        query_items = set([getattr(i, keyword1) for i in instances])
        arg_name = keyword2 + "__in"
        queryset = queryset.filter(**{
            arg_name: query_items
        })

        for instance in instances:
            for i in queryset:
                if getattr(instance, keyword1) == getattr(i, keyword2):
                    setattr(instance, attribute, i)
                    break

        return instances



