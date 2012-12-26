#coding: utf-8
from modargs import args
import sys
from rgc import collect

def main():
    params = args.parse(sys.argv[1:])
    collect(params)
    sys.exit(0)

#user=sieve key=908ae8y37yr7a43yt7yt rgc --days 30 --type brand