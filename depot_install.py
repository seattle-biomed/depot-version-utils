#!/usr/bin/env python

import os
import string
import re
#import yaml
import list_versions

def graft_install(app, version):
    """Install an application using graft.

    Returns null."""

    package_name = '-'.join((app, version))
    command = "/depot/graft-2.4/bin/graft -i %s" % package_name
    os.popen(command)

def graft_remove(app, version):
    """Remove an application using graft.

    Returns null."""

    package_name = '-'.join((app, version))
    command = "/depot/graft-2.4/bin/graft -d -D %s" % package_name
    os.popen(command)

# graft_dir is the top level directory applications are grafted into:
graft_dir = '/apps'

# Define default application versions in the apps dictionary:
apps = {}

# host_customizations is a dictionary of dictionaries containing non-default
# application versions installed on hosts:
host_customizations = {}

# Get hostname of machine we're running on:
hostname = string.join(os.popen('/bin/hostname -s').readlines())
hostname = re.sub('\n', '', hostname)

# Assign versions for host:
host_versions = apps
if hostname in host_customizations:
    for app, version in host_customizations[hostname].items():
        host_versions[app] = version

# retrieve installed versions:
installed_versions = list_versions.depot_installed_versions(graft_dir)

for app, version in installed_versions.items():
    if app in host_versions:
        if installed_versions[app] != host_versions[app]:
            print "Remove %s version %s" % (app, version)
            graft_remove(app, version)
            os.popen('/sbin/ldconfig')
    else:
        print "Remove %s version %s" % (app, version)
        graft_remove(app, version)

for app, version in host_versions.items():
    if host_versions[app] != '':
        if app in installed_versions:
            if installed_versions[app] != host_versions[app]:
                print "Install %s version %s" % (app, version)
                graft_install(app, version)
        else:
            print "Install %s version %s" % (app, version)
            graft_install(app, version)
