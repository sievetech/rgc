#coding: utf-8

import sys
import os

from cloudfiles.errors import AuthenticationFailed, NoSuchContainer
from modargs import args
from rgc import collect
from rules import AVAILABLE_RULES


def main():
    # O modargs sempre espera que a chamada da linha de comando tenha sido
    # $ prog command args
    # Por isso ignoramos o primeiro item da tupla retornada por ele.

    _, params = args.parse(sys.argv[1:])

    _validate_params(params)

    user = os.environ['user']
    key =  os.environ['key']
    container = params.get('container', None)
    dryrun = params.get('dryrun', False)
    rule = params.get('rule', None)
    rule_param = params.get('ruleparam', None)

    rule_instance = AVAILABLE_RULES[rule](rule_param)

    try:
        print collect(container=container, dryrun=dryrun, rule=rule_instance, user=user, key=key)

    except AuthenticationFailed as auth:
        print "User or API KEY wrong ", auth.message
    except NoSuchContainer as nocontainer:
        print "No such container: ", nocontainer.message
    except Exception as e:
        print "Ops, an error ocorred : ", e.message
    sys.exit(0)


def _validate_params(params):
    if _impossible_to_authenticate():
        print >> sys.stderr, "Authentication tokens not present, please verify that you have os.environ['user'] and os.environ['key']"
        _show_help()

    if 'help' in params:
        _show_help()

    rule = params.get('rule', None)
    if not rule:
        print >> sys.stderr, "No rule selected."
        _show_help()

    if rule not in AVAILABLE_RULES:
        print >> sys.stderr, "Invalid rule: {0}".format(rule)
        _show_help()


def _impossible_to_authenticate():
    has_user = os.environ.get('user', None)
    has_key = os.environ.get('key', None)
    return not has_user or not has_key


def _show_help():
    print >> sys.stderr, """
    rgc - Rackspace garbage Collector

    How to use:

    $ rgc --rule <rulename> --container <containername>

    Details:

    You must have two environ variables to be able to use rgc.
      * user: Your Rackspace Cloudfiles username
      * key : Your Rackspace Cloudfiles API key

    Available rules: {0}
    """.format(AVAILABLE_RULES.keys())
    sys.exit(0)

#user=sieve key=908ae8y37yr7a43yt7yt rgc --days 30 --type brand