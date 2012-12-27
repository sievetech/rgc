# -*- coding: utf-8 -*-

from datetime import datetime


class Rule(object):

    def __init__(self, *args, **kwargs):
        self.args, self.kwargs = args, kwargs

    def __call__(self, *args, **kwargs):
        return True

    def apply(self, obj):
        return self(obj, *self.args, **self.kwargs)


def rule(func):

    class newr(Rule):

        def __call__(self, obj):
            return func(obj)
        #set docstring, name etc.

    return newr

