# -*- coding: utf-8 -*-

class RuleDoesNotExistError(Exception):
    
    def __init__(self, rulename):
        self.value = rulename

    def __str__(self):
        return 'rule "{0}" is not implemented'.format(self.value)

    def __unicode__(self):
        return str(self).decode('utf-8')
    

class RuleSet(object):

    def __init__(self, *args, **kwargs):
        self.rules = kwargs 

    def apply(self, obj):
        """
        obj: A file inside a container (cloudfiles.Object)
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

