#coding: utf-8
import os

import cloudfiles


def collect(user, key, rule, container='', dryrun=False):
    conn = cloudfiles.get_connection(user, key)
    if container:
        containers = [conn.get_container(container)]
    else:
        containers = conn.get_all_containers()

    deleted = []
    for cont in containers:
        for obj in cont.get_objects():
            if rule.apply(obj):
                if not dryrun:
                    cont.delete_object(obj.name)
                deleted.append(obj.name)

    return deleted

