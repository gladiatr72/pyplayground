#!/usr/bin/env python
"""
The goal is to read a bind9 configuration into some sort of
useful pythonic form
"""

# -*- coding: utf-8 -*-

from __future__ import print_function
import pprint
import re
import os
from CountParen import CountParen

pp = pprint.PrettyPrinter(indent=4,width=20)

class Load(object):
    """
    bindoo.Load('/path/to/named.conf')
    """

    root=None

    """ number of open parenthese pairs """
    open=None

    """ track paren depth through the configuration stream """
    previous_depth=None
    current_depth=None


    nconf_tree={}
    collection={}

    def deploy(self,line,depth):
        """
        Process the lines marked for ...
        """

        if self.current_depth != self.previous_depth:
            self.previous_depth=self.current_depth
            self.current_depth=depth

        nct=self.nconf_tree


    def _view(self):
        return 'view'

    def _zone(self):
        return 'zone' 


    DUD=re.compile(r'(^\/\/|^\s*$|^#)')
    INCLUDE = re.compile(r'^\s*include\s"(?P<filename>.*)"\s*;')

    repile=[
        {   
            "name": "view",
            "regex": re.compile(r'\s*view\s"(?P<view>.*)"\s+{\s*'),
            "func": _view
        },
        {
            "name":"zone",
            "regex":re.compile(r'^\s*zone\s+"(?P<zone>[\w.-]+)"\s+{.*'),
            'func': _zone
        },
        {
            "name":"open_close",
            "regex":re.compile(r'^\s*(.*)\s*{.*}\s*'),
            'func': None
        },
        {
            "name":"stanz_jaws",
            "regex":re.compile(r'^\s*(.*)\s*([{}])\s*'),
            'func': None
        },
        {
            "name":"simple_opt",
            "regex":re.compile(r'^\s*([^{}]+)\s+([^{}\s]+)[;\s]*$'),
            'func': None
        },
    ]

    def open_nconf(self,filename):
        """
        read_nconf(filename)

        generator to process BIND9 include directives and return a cohesive
        series of lines

        returns a the tuple (line, file position)
        """

        confroot=""
        depth=0

        try:
            fh = open(filename)
            print('open',filename)

            for line in iter(fh.readline,''):
                res = self.INCLUDE.match(line)

                depth+=len(re.findall(r'{',line))
                depth-=len(re.findall(r'}',line))

                if not res:
                    yield (line, depth)
                else:
                    incfile = res.group('filename')

                    # derive the (actual) path of the named.conf directory
                    # structure.  This is necessary to accomodate include
                    # paths that do not follow the actual filesystem layout

                    if not confroot:
                        croot=self.confroot.split('/')
                        iroot=incfile.split('/')

                        rootlist=croot[:croot.index(croot[croot.index(iroot[1:-1][0])])]
                        confroot='/'.join([ "%s" % el for el in rootlist])

                    include=confroot + incfile

                    for line, depth in self.open_nconf(filename=include):
                        yield (line, depth)

        except IOError as e:
           print("I/O error({0}): {1}".format(e.errno,e.strerror),filename)


    def __init__(self,filename='../etc/named.conf',current_depth=0):
        nconf=filename
        nct=self.nconf_tree
        col=self.collection
        self.confroot=os.path.dirname(nconf)

        for ( line, depth ) in self.open_nconf(filename=nconf):
            if not re.match(self.DUD,line):
                self.deploy(line,depth)

if __name__ == '__main__':
    pass

