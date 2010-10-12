# -*- coding: utf-8 -*-
"""Recipe parse2plone"""

import fnmatch

from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SpecialUsers import system
from Testing.makerequest import makerequest 

from lxml.html import parse
from optparse import OptionParser
from os import path as os_path
from os import walk
from pkg_resources import working_set
from sys import argv, exc_info, executable
from transaction import commit
from zExceptions import BadRequest
from zc.buildout.easy_install import scripts as create_scripts


class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options

    def install(self):
        """Installer"""

        bindir = self.buildout['buildout']['bin-directory']

        create_scripts(

            # http://pypi.python.org/pypi/zc.buildout#the-scripts-function
            # A sequence of distribution requirements.
            [('import', 'parse2plone', 'main')],

            # A working set,
            working_set,

            # The Python executable to use,
            executable,

            # The destination directory.
            bindir,

            # http://pypi.python.org/pypi/zc.buildout#the-scripts-function-providing-script-arguments
            # The value passed is a source string to be placed between the parentheses in the call
            arguments='app')

        # Return files that were created by the recipe. The buildout
        # will remove all returned files upon reinstall.
        return tuple()

    def update(self):
        """Updater"""
        pass


line = """
================================================================================
"""

def parse_options():
    parser = OptionParser()
    parser.add_option("-i", "--ignore", dest="ignore",
                      help="Number of dirs to ignore")
    return parser

def setup_app(app):
    app=makerequest(app) 
    newSecurityManager(None, system)
    site=app.Plone
    return site

def get_files(dir):
    results = []
    for path, subdirs, files in walk(dir):
        for file in fnmatch.filter(files, '*.html'):
            results.append(os_path.join(path, file))
    return results

def path_to_list(file):
    return file.split('/')

def list_to_path(file):
    return '/'.join(file)

def ignore_parts(files, ignore):
    results = []
    for file in files:
        parts = path_to_list(file)
        parts = parts[int(ignore):]
        results.append(parts)
    return results

def prep_files(files, ignore):
    results = []
    files = ignore_parts(files, ignore)
    for file in files:
        results.append(list_to_path(file))
    return results

def check_exists(parent, obj):
    if obj in parent:
        return True
    else:
        return False

def get_parent(parent, prefix):
    if prefix is not '':
        print 'get parent with %s and %s' % (parent, prefix)
        return parent.restrictedTraverse(prefix)
    else:
        return parent

def set_title(obj, title):
    obj.setTitle(title.title())
    obj.reindexObject()
    commit()

def create_folder(parent, obj):
    print 'creating %s inside %s' % (obj, parent)
    parent.invokeFactory('Folder', obj)
    commit()
    return parent[obj]

def add_files(site, files):
    results = []
    for file in files:
        parts = path_to_list(file)
        parent = site
        for i in range(len(parts)):
            path    = list_to_path(parts[:i+1])
            prefix  = path_to_list(path)[:-1]
            obj     = path_to_list(path)[-1:][0]
            parent  = get_parent(parent, list_to_path(prefix))
            if check_exists(parent, obj):
                print '%s exists inside %s' % (obj, parent)
            else:
                print '%s does not exist inside %s' % (obj, parent)
                folder = create_folder(parent, obj)
                set_title(folder, obj)

def main(app):
    parser = parse_options()
    options, args = parser.parse_args()
    site = setup_app(app)
    dir = argv[1]
    files = get_files(dir)
    files = prep_files(files, options.ignore)
    add_files(site, files)

