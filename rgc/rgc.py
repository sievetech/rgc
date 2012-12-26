#coding: utf-8
import cloudfiles
import os


def collect(arglist):
    cloud = cloudfiles.get_connection(os.environ['user'], os.environ['key'])
    cloud.create_container('test_create_container')
    print  "ok"