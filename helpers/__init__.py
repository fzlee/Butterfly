#!/usr/bin/env python
# coding: utf-8
"""
    __init__.py
    ~~~~~~~~~~

"""
import random
import string
from datetime import datetime, timedelta


def generate_id(total_size=6, chars=string.ascii_lowercase + string.digits, header=""):
    return header + ''.join(
        random.SystemRandom().choice(chars) for _ in range(total_size - len(header))
    )


def generate_user_id():
    return generate_id(8, header="u")


class cached(object):
    def __init__(self, *args, **kwargs):
        self.cached_function_responses = {}
        self.default_max_age = timedelta(seconds=kwargs.get("default_cache_max_age", 0))

    def __call__(self, func):
        def inner(*args, **kwargs):
            max_age = kwargs.get('max_age', self.default_max_age)
            if not max_age or func not in self.cached_function_responses or (datetime.now() - self.cached_function_responses[func]['fetch_time'] > max_age):
                if 'max_age' in kwargs: del kwargs['max_age']
                res = func(*args, **kwargs)
                self.cached_function_responses[func] = {'data': res, 'fetch_time': datetime.now()}
            return self.cached_function_responses[func]['data']
        return inner
