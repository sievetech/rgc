# coding=utf-8

import sys
import unittest
import mock
import os

from rgc.main import main

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

    def test_no_environ_vars(self):
        """
        Deveos mostrar a mensagem de "help" caso falte alguma informação
        para o rgc poder rodar
        """
        self.fail()
