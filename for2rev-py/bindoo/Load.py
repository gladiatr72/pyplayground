#!/usr/bin/env python

# -*- coding: utf-8 -*-

from __future__ import print_function
import pprint
import re
import os
from CountParen import CountParen

pp = pprint.PrettyPrinter(indent=4,width=20)

class Load(object):
    """
    The goal is to read a bind9 configuration into some sort of
    useful pythonic form
    """

    root=None

    """ number of open parenthese pairs """
    open=None

    """ track paren depth through the configuration stream """
    previous_depth=None
    current_depth=None


    nconf_tree={}
    collection={}





    def deploy(self):
        """
        Process the lines marked for
        """

        if self.current_depth != self.previous_depth:
            self.previous_depth=self.current_depth
            self.current_depth=depth

        nct=self.nconf_tree

        pp.pprint(self.collection)


    def puke(self):
        pp = pprint.PrettyPrinter(indent=4,width=20)
        pp.pprint(self.nconf_tree)

        return self.nconf_tree

    def _include(self):
        pass

    def _view(self):
        pass

    def _zone(self):
        pass


    def _open_close(self):
        pass


    def _stanz_jaws(self):
        pass


    def _simple_opt(self):
        pass


    DUD=re.compile(r'(^\/\/|^\s*$|^#)')
    INCLUDE = re.compile(r'^\s*include\s"(?P<filename>.*)"\s*;')
    VIEW = re.compile(r'\s*view\s"(?P<view>.*)"\s+{\s*')

    repile=[
        {
            "name":"zone",
            "regex":re.compile(r'^\s*zone\s+"(?P<zone>[\w.-]+)"\s+{.*'),
            'func':_zone
        },
        {
            "name":"open_close",
            "regex":re.compile(r'^\s*(.*)\s*{.*}\s*'),
            'func':_open_close
        },
        {
            "name":"stanz_jaws",
            "regex":re.compile(r'^\s*(.*)\s*([{}])\s*'),
            'func':_stanz_jaws
        },
        {
            "name":"simple_opt",
            "regex":re.compile(r'^\s*([^{}]+)\s+([^{}\s]+)[;\s]*$'),
            'func':_simple_opt
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

        try:
            fh = open(filename)

            for line in iter(fh.readline,''):
                res = self.INCLUDE.match(line)
                if not res:
                    yield line
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
                    print('***', include, '***')

                    for line in self.open_nconf(filename=include):
                        yield line

        except IOError as e:
           print("I/O error({0}): {1}".format(e.errno,e.strerror),filename)


    def __init__(self,filename='../etc/named.conf',current_depth=0):
        nconf=filename
        nct=self.nconf_tree
        col=self.collection
        self.confroot=os.path.dirname(nconf)

        for line in self.open_nconf(filename=nconf):
            if not re.match(self.DUD,line):
                for test in self.repile:
                    res=re.match(test['regex'],line)
                    if res:
                        try:
                            print(line)
                        except KeyError:
                            pass
                        break

        pp.pprint(self.collection)
        self.deploy()


if __name__ == '__main__':
    pass

