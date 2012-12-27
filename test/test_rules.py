# -*- coding: utf-8 -*-

import mock
import unittest
import datetime

from rgc.rules import rule, Rule

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


if __name__ == '__main__':
    unittest.main()

