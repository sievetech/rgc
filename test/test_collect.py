# -*- coding: utf-8 -*-
import pyrax
import os

import mock
import unittest

from rgc.rules import Rule, namehasprefix, namehassuffix
from rgc import collect


class TestCollect(unittest.TestCase):

    def setUp(self):
        os.environ['user'] = 'john'
        os.environ['key'] = '12345abcd'

    def test_dryrun_no_rule_true_collects_everything(self):
        mock_obj = mock.MagicMock()
        mock_obj.name = 'blargh'
        mock_cont = mock.MagicMock()
        mock_cont.get_objects.side_effect = [[mock_obj], []]

        mock_conn = mock.MagicMock()
        mock_conn.get_all_containers.return_value = [mock_cont]
        mock_conn.get_container.return_value = mock_cont

        with mock.patch('pyrax.connect_to_cloudfiles', return_value=mock_conn),\
             mock.patch.object(pyrax, "set_credentials"):
            deleted = collect(rule=Rule(), user=mock.ANY, key=mock.ANY)

        self.assertIn(mock.call.delete_object(mock_obj.name), mock_cont.method_calls)
        self.assertItemsEqual(['blargh'], deleted)

    def test_dryrun_yes_rule_true_does_not_collect(self):
        mock_obj = mock.MagicMock()
        mock_obj.name = 'blargh'
        mock_cont = mock.MagicMock()
        mock_cont.get_objects.side_effect = [[mock_obj], []]

        mock_conn = mock.MagicMock()
        mock_conn.get_all_containers.return_value = [mock_cont]
        mock_conn.get_container.return_value = mock_cont

        with mock.patch('pyrax.connect_to_cloudfiles', return_value=mock_conn),\
             mock.patch.object(pyrax, "set_credentials"):
            deleted = collect(rule=Rule(), dryrun=True, user=mock.ANY, key=mock.ANY)

        self.assertNotIn(mock.call.delete_object(mock_obj.name), mock_cont.method_calls)
        self.assertItemsEqual([mock_obj.name], deleted)

    def test_collect_applies_rule(self):
        mock_obj1 = mock.MagicMock()
        mock_obj1.name = 'pref_name_suf'

        mock_obj2 = mock.MagicMock()
        mock_obj2.name = 'noprefnosuf'

        mock_cont = mock.MagicMock()
        mock_cont.get_objects.side_effect = [[mock_obj1, mock_obj2], [mock_obj1], []]

        mock_conn = mock.MagicMock()
        mock_conn.get_all_containers.return_value = [mock_cont]
        mock_conn.get_container.return_value = mock_cont

        with mock.patch('pyrax.connect_to_cloudfiles', return_value=mock_conn),\
             mock.patch.object(pyrax, "set_credentials"):
            deleted = collect(rule=namehasprefix('pref') & namehassuffix('suf'), user=mock.ANY, key=mock.ANY)

        self.assertIn(mock.call.delete_object(mock_obj1.name), mock_cont.method_calls)
        self.assertNotIn(mock.call.delete_object(mock_obj2.name), mock_cont.method_calls)
        self.assertItemsEqual([mock_obj1.name], deleted)

    def test_specific_container(self):
        mock_obj1 = mock.MagicMock()
        mock_obj1.name = 'mock1'

        mock_cont1 = mock.MagicMock()
        mock_cont1.name = 'container1'
        mock_cont1.get_objects.side_effect = [[mock_obj1], []]

        mock_obj2 = mock.MagicMock()
        mock_obj2.name = 'mock2'

        mock_cont2 = mock.MagicMock()
        mock_cont2.name = 'container2'
        mock_cont2.get_objects.side_effect = [[mock_obj2], []]

        mock_conn = mock.MagicMock()
        mock_conn.get_all_containers.return_value = [mock_cont1, mock_cont2]
        mock_conn.get_container.return_value = mock_cont1

        with mock.patch('pyrax.connect_to_cloudfiles', return_value=mock_conn),\
             mock.patch.object(pyrax, "set_credentials"):
            deleted = collect(rule=Rule(), container='container1', user=mock.ANY, key=mock.ANY)

        self.assertIn(mock.call.delete_object(mock_obj1.name), mock_cont1.method_calls)
        self.assertNotIn(mock.call.delete_object(mock_obj2.name), mock_cont2.method_calls)
        self.assertItemsEqual([mock_obj1.name], deleted)

    def test_specific_region(self):
        mock_obj = mock.MagicMock()
        mock_obj.name = 'object_1'
        mock_cont = mock.MagicMock()
        mock_cont.get_objects.side_effect = [[mock_obj], []]

        mock_conn = mock.MagicMock()
        mock_conn.get_all_containers.return_value = [mock_cont]
        mock_conn.get_container.return_value = mock_cont

        with mock.patch('pyrax.connect_to_cloudfiles', return_value=mock_conn) as mock_cloud,\
             mock.patch.object(pyrax, "set_credentials"):
            collect(rule=Rule(), user=mock.ANY, key=mock.ANY, region="REGION_1")

        self.assertEqual([mock.call(region="REGION_1")], mock_cloud.call_args_list)


if __name__ == '__main__':
    unittest.main()
