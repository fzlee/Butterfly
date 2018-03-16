#!/usr/bin/env python
# coding: utf-8
"""
    __init__.py
    ~~~~~~~~~~

"""
import random
import string


def generate_id(total_size=6, chars=string.ascii_lowercase + string.digits, header=""):
    return header + ''.join(
        random.SystemRandom().choice(chars) for _ in range(total_size - len(header))
    )


def generate_user_id():
    return generate_id(8, header="u")
