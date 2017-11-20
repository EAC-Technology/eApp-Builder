"""
"""

import cgi
import time


class CachedProperty(object):

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls=None):
        result = instance.__dict__[self.func.__name__] = self.func(instance)
        return result


def to_list(data):
    """
    """
    if not isinstance(data, (list, tuple)):
        data = [data]

    return data


def escape_w_quote(data):
    """
    """
    return cgi.escape(data, True)


def ensure_https(url):
    return '://'.join(['https', url.split('://')[-1]])


class Timer:

    def __init__(self):
        self.reset()

    def reset(self):
        self.__t = time.clock()

    def get(self):
        return time.clock() - self.__t
