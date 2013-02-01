#coding: utf-8
import os

import cloudfiles
from clint.textui import progress


def delete(cont, obj):
    """
    Deletes the object.
    """
    cont.delete_object(obj.name)


def collect(user, key, rule, container='', dryrun=False, showprogress=False, cb=delete):
    """
    Connects to rackspace with the user and the key and crawls every container
    applying the rule to each cloudfile object. If the rule applies, i.e.
    returns True, the callback ('cb') is called with the container as first
    argument and the object as second argument. The default callback is delete.

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

    collected = []
    for cont in containers:
        objs = progress.bar(cont.get_objects(), label="Collecting Objects",
                            hide=not showprogress)
        for obj in objs:
            if rule.apply(obj):
                if not dryrun:
                    cb(cont, obj)
                collected.append(obj.name)

    return collected

