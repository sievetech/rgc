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
            return not self(obj)
        return i(*self.args, **self.kwargs)

    def apply(self, obj):
        return self(obj, *self.args, **self.kwargs)


def rule(func):

    class newr(Rule):

        def __call__(self, obj):
            return func(obj)

    return newr

