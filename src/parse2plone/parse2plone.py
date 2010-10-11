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
from sys import argv, executable
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

def fix_files(files, ignore):
    results = []
    for file in files:
        elements = file.split('/')
        elements = elements[int(ignore):]
        results.append(elements)
    return results

def main(app):
    parser = parse_options()
    options, args = parser.parse_args()
    site = setup_app(app)
    dir = argv[1]
    files = get_files(dir)
    files = fix_files(files, options.ignore)
    print files
