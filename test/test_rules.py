# -*- coding: utf-8 -*-

import mock
import unittest
import datetime

from rgc.rules import rule, Rule
from rgc.rules import olderthan, newerthan, ageexact
from rgc.rules import namehasprefix, namehassuffix, containerhasprefix, containerhassuffix
from rgc.rules import AVAILABLE_RULES


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

    def test_combination(self):
        @rule
        def maiorque(obj, value):
            return obj > value

        @rule
        def iguala(obj, value):
            return obj == value

        myrule = maiorque(10) | iguala(20)
        self.assertTrue(myrule.apply(30))
        self.assertFalse(myrule.apply(3))
        self.assertTrue(myrule.apply(20))

        rule_2 = maiorque(10) & maiorque(15)
        self.assertTrue(rule_2.apply(20))

        rule_2 = maiorque(10) & ~maiorque(15)
        self.assertTrue(rule_2.apply(12))
        self.assertFalse(rule_2.apply(16))

        rule_2 = maiorque(10) ^ iguala(15)
        self.assertTrue(rule_2.apply(30))
        self.assertFalse(rule_2.apply(8))


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

    def test_newerthan(self):
        obj = mock.MagicMock()
        dt = datetime.timedelta(days=31)
        objdate = (datetime.datetime.now() - dt)
        obj.last_modified = objdate.strftime('%Y-%m-%dT%H:%M:%S.%f')

        #returns False when obj is old
        self.assertFalse(newerthan(ndays=dt.days-1).apply(obj))
        #returns True when obj is new
        self.assertTrue(newerthan(ndays=dt.days+1).apply(obj))
        #returns False when obj has the same age
        self.assertFalse(newerthan(ndays=dt.days).apply(obj))

    def test_ageexact(self):
        obj = mock.MagicMock()
        dt = datetime.timedelta(days=31)
        objdate = (datetime.datetime.now() - dt)
        obj.last_modified = objdate.strftime('%Y-%m-%dT%H:%M:%S.%f')

        #returns False when obj is old
        self.assertFalse(ageexact(ndays=dt.days-1).apply(obj))
        #returns False when obj is new
        self.assertFalse(ageexact(ndays=dt.days+1).apply(obj))
        #returns True when obj has the same age
        self.assertTrue(ageexact(ndays=dt.days).apply(obj))

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

    def test_containerhasprefix(self):
        export = mock.MagicMock()
        export.container.name = 'export_frete'

        notexport = mock.MagicMock()
        notexport.container.name = 'blargh'

        isexport = containerhasprefix('export_')

        self.assertTrue(isexport.apply(export))
        self.assertFalse(isexport.apply(notexport))

    def test_containerhassuffix(self):
        odp = mock.MagicMock()
        odp.container.name = 'presentation.odp'

        notodp = mock.MagicMock()
        notodp.container.name = 'blargh'

        isodp = containerhassuffix('.odp')
        self.assertTrue(isodp.apply(odp))
        self.assertFalse(isodp.apply(notodp))


class RuleDecoratorTest(unittest.TestCase):

    def setUp(self):
        AVAILABLE_RULES = {}

    def test_register_rule(self):
        @rule
        def myrule(obj, param):
            return True

        self.assertTrue('myrule' in AVAILABLE_RULES)


if __name__ == '__main__':
    unittest.main()
