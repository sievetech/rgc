# -*- coding: utf-8 -*-

import mock
import unittest
import datetime

from rgc.rules import rule, Rule

class TestRule(unittest.TestCase):

    def test_rule_decorator(self):

        @rule
        def foo(obj, *args, **kwargs):
            pass

        self.assertTrue(Rule, isinstance(foo, Rule))

    def test_base_class_returns_true(self):
        self.assertTrue(Rule().apply(object()))

    def test_unary_negation(self):
        rule = ~Rule()
        self.assertFalse(rule.apply(object))

    def test_and_operator(self):
        true = Rule()
        false = ~Rule()
        self.assertFalse((true & false).apply(object()))

    def test_or_operator(self):
        true = Rule()
        false = ~Rule()
        self.assertTrue((true | false).apply(object()))

    def test_xor_operator(self):
        true = Rule()
        false = ~Rule()
        self.assertTrue((true ^ false).apply(object()))


if __name__ == '__main__':
    unittest.main()

