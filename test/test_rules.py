# -*- coding: utf-8 -*-

import mock
import unittest
import datetime

from rgc.rules import rule, Rule
from rgc.rules import olderthan, namehasprefix, namehassuffix

class TestRule(unittest.TestCase):

    def setUp(self):
        self.obj = object()

    def test_rule_decorator(self):

        @rule
        def foo(obj, *args, **kwargs):
            pass

        self.assertTrue(Rule, isinstance(foo, Rule))

    def test_base_class_returns_true(self):
        self.assertTrue(Rule().apply(self.obj))

    def test_unary_negation(self):
        rule = ~Rule()
        self.assertFalse(rule.apply(object))
        self.assertTrue((~rule).apply(object))

    def test_and_operator(self):
        true = Rule()
        false = ~Rule()
        self.assertTrue((true & true).apply(self.obj))
        self.assertFalse((true & false).apply(self.obj))
        self.assertFalse((false & true).apply(self.obj))
        self.assertFalse((false & false).apply(self.obj))

    def test_or_operator(self):
        true = Rule()
        false = ~Rule()
        self.assertTrue((true | true).apply(self.obj))
        self.assertTrue((true | false).apply(self.obj))
        self.assertTrue((false | true).apply(self.obj))
        self.assertFalse((false | false).apply(self.obj))

    def test_xor_operator(self):
        true = Rule()
        false = ~Rule()
        self.assertFalse((true ^ true).apply(self.obj))
        self.assertTrue((true ^ false).apply(self.obj))
        self.assertTrue((false ^ true).apply(self.obj))
        self.assertFalse((false ^ false).apply(self.obj))


class TestBaseRules(unittest.TestCase):

    def test_olderthan(self):
        obj = mock.MagicMock()
        dt = datetime.timedelta(days=31)
        objdate = (datetime.datetime.now() - dt)
        obj.last_modified = objdate.strftime('%Y-%m-%dT%H:%M:%S.%f')

        #returns True when obj is old
        self.assertTrue(olderthan(ndays=dt.days-1).apply(obj))
        #returns False when obj is new
        self.assertFalse(olderthan(ndays=dt.days+1).apply(obj))
        #returns False when obj has the same age
        self.assertFalse(olderthan(ndays=dt.days).apply(obj))

    def test_namehasprefix(self):
        export = mock.MagicMock()
        export.name = 'export_frete'

        notexport = mock.MagicMock()
        notexport.name = 'blargh'

        isexport = namehasprefix('export_')

        self.assertTrue(isexport.apply(export))
        self.assertFalse(isexport.apply(notexport))

    def test_namehassuffix(self):
        odp = mock.MagicMock()
        odp.name = 'presentation.odp'

        notodp = mock.MagicMock()
        notodp.name = 'blargh'

        isodp = namehassuffix('.odp')
        self.assertTrue(isodp.apply(odp))
        self.assertFalse(isodp.apply(notodp))


if __name__ == '__main__':
    unittest.main()

