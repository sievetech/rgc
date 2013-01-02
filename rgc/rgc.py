#coding: utf-8
import os

import cloudfiles
from clint.textui import progress


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

    deleted = []
    for cont in containers:
        for obj in progress.bar(cont.get_objects(), label="Removing Objects"):
            if rule.apply(obj):
                if not dryrun:
                    cont.delete_object(obj.name)
                deleted.append(obj.name)

    return deleted

