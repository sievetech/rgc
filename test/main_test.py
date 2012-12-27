# coding=utf-8

import sys
import unittest
import mock
import os

from rgc.main import main, _impossible_to_authenticate, _show_help, _validate_params


class MainTest(unittest.TestCase):

    def test_help_command(self):
        with mock.patch('sys.stderr'),\
             mock.patch('rgc.main.collect'),\
             mock.patch('sys.exit'):
            os.environ['user'] = 'sieve'
            os.environ['key'] = 'sieve-key'
            sys.argv = ['rgc', '--help']

            _validate_params({'help': True})
            self.assertTrue(sys.stderr.write.call_count > 1)

            del os.environ['user']
            del os.environ['key']

    def test_impossible_to_authenticate(self):
        os.environ['user'] = 'sieve'
        self.assertTrue(_impossible_to_authenticate(), 'Nao deveria ser possivel autenticar apenas com user')

        os.environ['key'] = 'sieve'
        del os.environ['user']
        self.assertTrue(_impossible_to_authenticate(), 'Nao deveria ser possivel autenticar apenas com key')

        os.environ['key'] = 'sieve'
        os.environ['user'] = 'sieve'
        self.assertFalse(_impossible_to_authenticate())

        del os.environ['key']
        del os.environ['user']
        self.assertTrue(_impossible_to_authenticate())

    def test_no_environ_vars(self):
        """
        Deveos mostrar a mensagem de "help" caso falte alguma informação
        para o rgc poder rodar
        """
        with mock.patch('sys.stderr'),\
             mock.patch('sys.exit'):

            if 'user' in os.environ:
                del os.environ['user']
            if 'key' in os.environ:
                del os.environ['key']

            sys.argv = ['rgc']
            _validate_params({})
            self.assertTrue(sys.stderr.write.call_count > 1)
            self.assertEquals(mock.call("Authentication tokens not present, please verify that you have os.environ['user'] and os.environ['key']"), sys.stderr.write.call_args_list[0])

    def test_rule_validation(self):
        """
        Devemos mostrar a mensagem de "help" caso falte alguma informação
        para o rgc poder rodar
        """
        with mock.patch('sys.stderr'),\
             mock.patch('sys.exit'),\
             mock.patch('rgc.main._impossible_to_authenticate', return_value=False):

            sys.argv = ['rgc']
            _validate_params({})
            self.assertTrue(sys.stderr.write.call_count > 1)
            self.assertEquals(mock.call("No rule selected."), sys.stderr.write.call_args_list[0])

    def test_params_collect(self):
        rule_instance_class = mock.Mock()
        rule_instance_mock = mock.Mock()
        rule_instance_class.return_value = rule_instance_mock
        with mock.patch('rgc.main.collect') as mockcollect,\
             mock.patch('sys.stderr'),\
             mock.patch.dict('rgc.main.AVAILABLE_RULES', {'isold': rule_instance_class}),\
             mock.patch('rgc.main._impossible_to_authenticate', return_value=False),\
             mock.patch('sys.exit'):

            sys.argv = ['rgc', '--rule', 'isold', '--container', 'trash', '--dryrun']
            main()

            self.assertEquals([mock.call(rule=rule_instance_mock, container='trash', dryrun=True)], mockcollect.call_args_list)

    def test_rule_validation(self):
        """
        Devemos mostrar a mensagem de "help" caso falte alguma informação
        para o rgc poder rodar
        """
        with mock.patch('sys.stderr'),\
             mock.patch('sys.exit'),\
             mock.patch('rgc.main._impossible_to_authenticate', return_value=False):

            sys.argv = ['rgc', '--rule', 'isold', '--container', 'trash', '--dryrun']
            _validate_params({'rule': 'isold', 'container': 'trash', 'dryrun': True})
            self.assertTrue(sys.stderr.write.call_count > 1)
            self.assertEquals(mock.call("Invalid rule: isold"), sys.stderr.write.call_args_list[0])
