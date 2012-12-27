#coding: utf-8
import cloudfiles
import os


def collect(rule=None, container=None, dryrun=None):
    cloud = cloudfiles.get_connection(os.environ['user'], os.environ['key'])


    print  "ok"