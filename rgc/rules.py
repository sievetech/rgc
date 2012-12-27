# -*- coding: utf-8 -*-
#TODO: set __name__ etc.

from datetime import datetime

AVAILABLE_RULES = {}

class Rule(object):
    """
    Base rule object. Binds the args and kwargs passed on instantiation to its
    rule function.
    """

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
        """
        Applies rule to cloudfile object with binded args and kwargs.
        """
        return self(obj, *self.args, **self.kwargs)


def rule(func):
    """
    Decorator that defines new rules based on existing functions.
    It accepts a function as its sole argument and returns a class that
    inherits from rule and whose rule is given by the decorated function.
    """

    class newr(Rule):

        def __call__(self, obj, *args, **kwargs):
            return func(obj, *args, **kwargs)

    AVAILABLE_RULES[func.__name__] = newr
    return newr


@rule
def olderthan(obj, ndays):
    """
    Returns True if obj's is older than ndays. False otherwise.
    """
    objdate = datetime.strptime(obj.last_modified, '%Y-%m-%dT%H:%M:%S.%f')
    return (datetime.now() - objdate).days > ndays


@rule
def newerthan(obj, ndays):
    """
    Returns True if obj's is newer than ndays. False otherwise.
    """
    objdate = datetime.strptime(obj.last_modified, '%Y-%m-%dT%H:%M:%S.%f')
    return (datetime.now() - objdate).days < ndays


@rule
def ageexact(obj, ndays):
    """
    Returns True if obj's age is exactly ndays.
    """
    objdate = datetime.strptime(obj.last_modified, '%Y-%m-%dT%H:%M:%S.%f')
    return (datetime.now() - objdate).days == ndays


@rule
def namehasprefix(obj, prefix):
    """
    Returns whether obj's name starts with prefix.
    """
    return obj.name.startswith(prefix)


@rule
def namehassuffix(obj, suffix):
    """
    Returns whether obj's name ends with suffix.
    """
    return obj.name.endswith(suffix)


@rule
def containerhasprefix(obj, prefix):
    """
    Returns whether obj's container starts with prefix.
    """
    return obj.container.name.startswith(prefix)


@rule
def containerhassuffix(obj, suffix):
    """
    Returns whether obj's container ends with suffix.
    """
    return obj.container.name.endswith(suffix)

