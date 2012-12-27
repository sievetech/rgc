# coding=utf-8

import sys
import unittest
import mock
import os

from rgc.main import main, _impossible_to_authenticate

class MainTest(unittest.TestCase):


    def test_help_command(self):
        with mock.patch('sys.stderr'),\
             mock.patch('rgc.main.collect'),\
             mock.patch('sys.exit'):
            os.environ['user'] = 'sieve'
            os.environ['key'] = 'sieve-key'
            sys.argv = ['rgc', '--help']
            main()
            self.assertTrue(sys.stderr.write.call_count > 1)

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
             mock.patch('rgc.main.collect'),\
             mock.patch('sys.exit'):

            if 'user' in os.environ:
                del os.environ['user']
            if 'key' in os.environ:
                del os.environ['key']

            sys.argv = ['rgc']
            main()
            self.assertTrue(sys.stderr.write.call_count > 1)
            self.assertEquals(mock.call("Authentication tokens not present, please verify that you have os.environ['user'] and os.environ['key']"), sys.stderr.write.call_args_list[0])
