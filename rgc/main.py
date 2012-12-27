#coding: utf-8
from modargs import args
import sys
from rgc import collect

def main():
    # O modargs sempre espera que a chamada da linha de comando tenha sido
    # $ prog command args
    # Por isso ignoramos o primeiro item da tupla retornada por ele.
    _, params = args.parse(sys.argv[1:])
    if 'help' in params:
        show_help()
    collect(params)
    sys.exit(0)


def show_help():
    print >> sys.stderr, """
    rgc - Rackspace garbage Collector

    How to use:

    $ rgc --rule <rulename> --container <containername>

    Details:

    You must have two environ variables to be able to use rgc.
      * user: Your Rackspace Cloudfiles username
      * key : Your Rackspace Cloudfiles API key
    """
    sys.exit(0)

#user=sieve key=908ae8y37yr7a43yt7yt rgc --days 30 --type brand