# -*- coding: utf-8 -*-

import mock
import unittest
import datetime

from rgc.rules import RuleSet, RuleDoesNotExistError


class TestRules(unittest.TestCase):

    def test_vacuous_truth(self):
        self.assertEqual(True, RuleSet().apply(object()))

    def test_bad_rule_raises_error(self):
        rset = RuleSet(badrule='blargh')
        self.assertRaises(RuleDoesNotExistError, rset.apply, object())

    def test_valid_rule_should_be_applied(self):
        rset = RuleSet(mockrule='mockarg')
        obj = object()
        mockrule_result = False
        with mock.patch.object(rset, 'mockrule_rule',create=True, return_value=mockrule_result) as mockrule:
            self.assertEqual(mockrule_result, rset.apply(obj))
            self.assertEqual(mock.call(obj, 'mockarg'), mockrule.call_args)

    def test_multiple_rules_should_be_applied(self):
        rset = RuleSet(mockrule1='mockarg1', mockrule2='mockarg2')
        obj = object()
        with mock.patch.object(rset, 'mockrule1_rule', create=True, return_value=False) as mockrule1,\
             mock.patch.object(rset, 'mockrule2_rule', create=True, return_value=False) as mockrule2:

            self.assertEqual(False, rset.apply(obj))
            self.assertEqual(mock.call(obj, 'mockarg1'), mockrule1.call_args)
            self.assertEqual(mock.call(obj, 'mockarg2'), mockrule2.call_args)

    def test_days_rule(self):
        obj = mock.MagicMock()
        dt = datetime.timedelta(days=31)
        objdate = (datetime.datetime.now() - dt)
        obj.last_modified = objdate.strftime('%Y-%m-%dT%H:%M:%S.%f')

        #returns True when obj is old
        self.assertEqual(True, RuleSet(days=dt.days-1).apply(obj))
        #returns False when obj is new
        self.assertEqual(False, RuleSet(days=dt.days+1).apply(obj))
        #returns False when obj has the same age
        self.assertEqual(False, RuleSet(days=dt.days).apply(obj))

    def test_is_export_rule(self):
        export = mock.MagicMock()
        export.container.name = 'export_frete'

        notexport = mock.MagicMock()
        notexport.container.name = 'blargh'

        self.assertEqual(True, RuleSet(is_export=True).apply(export))
        self.assertEqual(False, RuleSet(is_export=True).apply(notexport))

        self.assertEqual(False, RuleSet(is_export=False).apply(export))
        self.assertEqual(True, RuleSet(is_export=False).apply(notexport))

if __name__ == '__main__':
    unittest.main()

