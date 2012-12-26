# -*- coding: utf-8 -*-

from datetime import datetime


class RuleDoesNotExistError(Exception):
    
    def __init__(self, rulename):
        self.value = rulename

    def __str__(self):
        return 'rule "{0}" is not implemented.'.format(self.value)

    def __unicode__(self):
        return str(self).decode('utf-8')


class RuleSet(object):
    """
    Implements each rule that is applied to a cloudfile object.
    """

    def __init__(self, *args, **kwargs):
        """
        Accepts arguments in the form rulename=param.
        """

        self.rules = kwargs 

    def apply(self, obj):
        """
        Applies and ANDs each rule received as kwargs on object instantiation.
        obj: A file inside a container (cloudfiles.Object)
        retval: the AND of each rule applied to obj
        """
        ret_val = False
        for rulename, arg in self.rules.iteritems():
            try:
                rule = getattr(self, rulename+'_rule')
            except AttributeError:
                raise RuleDoesNotExistError(rulename)
            else:
                ret_val &= rule(obj, arg)

        return ret_val

    def days_rule(self, obj, ndays):
        """
        retval: True if obj's last modification is older than ndays. False otherwise.
        """
        objdate = datetime.strptime(obj.last_modified, '%Y-%m-%dT%H:%M:%S.%f')
        return (datetime.now() - objdate).days > ndays

