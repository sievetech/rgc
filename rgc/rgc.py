#coding: utf-8
import os

import cloudfiles
from clint.textui import progress


def _process(cont, deleted, dryrun, objects, rule):
    for obj in progress.bar(objects, label="Removing Objects"):
        if rule.apply(obj):
            if not dryrun:
                try:
                    cont.delete_object(obj.name)
                except Exception as e:
                    print e
            deleted.append(obj.name)


def collect(user, key, rule, container='', dryrun=False):
    """
    Connects to rackspace with the user and the key and crawls every container
    applying the rule to each cloudfile object. If the rule applies, i.e.
    returns True, the object is deleted.

    If a container name is passed to the parameter 'container', only that
    container will be crawled.

    If dryrun is True, the objects will not be deleted.

    The function returns a list with the names of the objects to which the
    rule was successfully applied.
    """
    conn = cloudfiles.get_connection(user, key)
    if container:
        containers = [conn.get_container(container)]
    else:
        containers = conn.get_all_containers()

    for cont in containers:
        objects = cont.get_objects(marker="")
        while objects:
            deleted = []
            _process(cont, deleted, dryrun, objects, rule)
            objects = cont.get_objects(marker=objects[-1])
            print "Removed {0} objects".format(len(deleted))

    return deleted

