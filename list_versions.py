#!/usr/bin/env python

import re
import os

# For each item in /apps/bin, parse its link

# Take first item in bin subdirectory; look for it in /apps/bin; if it exists,
# parse version from directory in lin

def depot_parse_version(dirname):
    """Parse the application name and version from a depot application
    directory.

    Returns tuple."""

    # This is a non-greedy match for the application name, so that mcl
    # version 06-058 isn't returned as mcl-06 version 058:
    return re.match("^([^.]*?)-(\d[\d\.\-_]*[A-Za-z]{0,3}[\-]?\d?[\d\.]*\d?)$", dirname).groups()

def depot_installed_versions(top_depot_dir):
    """Detail all installed versions of applications

    Returns dictionary."""

    # define dictionary that will hold applications and their versions:
    versions = {}
    
    # Walk /apps/bin, /apps/lib, etc:
    for short_depot_dir in os.listdir(top_depot_dir):

        depot_dir = '/'.join((top_depot_dir, short_depot_dir))

        # Test to see if it's really a directory:
        if not os.path.isdir(depot_dir):
            continue
        
        contents = os.listdir(depot_dir)

        for entry in contents:
            full_path = '/'.join((depot_dir, entry))

            # If the file isn't a symbolic link, move on.  This could
            # burn us if a depot install is only under a subdirectory
            # of a short_depot_dir directory:
            if not os.path.islink(full_path):
                continue
            
            link_dest = os.readlink(full_path)
            
            # Assume file layout of "/depot/<application name>/...":
            try:
                (dest_parent_dir,) = re.match("^/depot/([^/]+)/",
                                              link_dest).groups(1)
            # Handle links that do not point into the depot:
            except AttributeError:
                print "Faulty link:"
                print "%s -> %s\n" % (full_path, link_dest)

                # re-throw exception
                raise
            
            (app, version) = depot_parse_version(dest_parent_dir)

            # Check to see if we have the key already - check for duplicate
            # installations:
            if app in versions:
                if versions[app] != version:
                    raise 'depot_multiple_app_versions_installed'
            else:
                versions[app] = version

    return versions

# If this file is called as an executable by itself, print out all installed
# versions of depot software:
if __name__ == '__main__':
    versions = depot_installed_versions('/apps')
    keys = versions.keys()
    keys.sort()
    for k in keys:
        print "%s: %s" % (k, versions[k]) 

