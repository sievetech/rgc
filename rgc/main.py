#coding: utf-8
import sys
import os

from modargs import args
from rgc import collect

hash_rule = {'olderthan': None, 'newerthan': None}

def main():
    # O modargs sempre espera que a chamada da linha de comando tenha sido
    # $ prog command args
    # Por isso ignoramos o primeiro item da tupla retornada por ele.

    _, params = args.parse(sys.argv[1:])

    if _impossible_to_authenticate():
        print >> sys.stderr, "Authentication tokens not present, please verify that you have os.environ['user'] and os.environ['key']"
        show_help()

    if 'help' in params:
        show_help()

    rule = params.get('rule', None)
    if not rule:
        print >> sys.stderr, "No rule selected."
        show_help()

    collect(params)
    sys.exit(0)


def _impossible_to_authenticate():
    has_user = os.environ.get('user', None)
    has_key = os.environ.get('key', None)
    return not has_user or not has_key

def show_help():
    print >> sys.stderr, """
    rgc - Rackspace garbage Collector

    How to use:

    $ rgc --rule <rulename> --container <containername>

    Details:

    You must have two environ variables to be able to use rgc.
      * user: Your Rackspace Cloudfiles username
      * key : Your Rackspace Cloudfiles API key

    Available rules: {0}
    """.format(hash_rule.keys())
    sys.exit(0)

#user=sieve key=908ae8y37yr7a43yt7yt rgc --days 30 --type brand