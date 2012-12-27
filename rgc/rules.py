# -*- coding: utf-8 -*-

from datetime import datetime

#TODO: set docstrings, __name__ etc.

class Rule(object):

    def __init__(self, *args, **kwargs):
        self.args, self.kwargs = args, kwargs

    def __call__(self, *args, **kwargs):
        return True

    def __invert__(self):
        @rule
        def i(obj):
            return not self.apply(obj)
        return i(*self.args, **self.kwargs)

    def __and__(self, other):
        @rule
        def a(obj):
            return self.apply(obj) and other.apply(obj)
        return a(*self.args, **self.kwargs)

    def __or__(self, other):
        @rule
        def o(obj):
            return self.apply(obj) or other.apply(obj)
        return o(*self.args, **self.kwargs)

    def __xor__(self, other):
        @rule
        def x(obj):
            return self.apply(obj) != other.apply(obj)
        return x(*self.args, **self.kwargs)

    def apply(self, obj):
        return self(obj, *self.args, **self.kwargs)


def rule(func):

    class newr(Rule):

        def __call__(self, obj, *args, **kwargs):
            return func(obj, *args, **kwargs)

    return newr

@rule
def olderthan(obj, ndays):
    """
    Returns True if obj's is older than ndays. False otherwise.
    """
    objdate = datetime.strptime(obj.last_modified, '%Y-%m-%dT%H:%M:%S.%f')
    return (datetime.now() - objdate).days > ndays

@rule
def namehasprefix(obj, prefix):
    """
    Returns whether obj's name starts with prefix.
    """
    return obj.name.startswith(prefix)


