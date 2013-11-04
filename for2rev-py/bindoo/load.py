#!/usr/bin/env python

# -*- coding: utf-8 -*-

import pprint
import re
from count_paren import count_paren

pp = pprint.PrettyPrinter(indent=4,width=20)

class load(object):
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
            "name":"view",
            "regex":
            'func':_view
        },
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

    def open_nconf(self,filename='/etc/named.conf'):
        """
        read_nconf(filename)

        generator to process BIND9 include directives and return a cohesive
        series of lines

        returns a the tuple (line, file position)
        """

        fh = open('../' + filename)

        for line in iter(fh.readline,''):
            res = self.INCLUDE.match(line)
            if not res:
                yield line
            else:
                incfile = res.group('filename')
                for line in open_nconf(filename=incflie):
                    yield line


    def __init__(self,filename='../etc/named.conf',current_depth=0):
        nconf=filename
        nct=self.nconf_tree
        col=self.collection

        try:
            fh=open_nconf(filename=nconf)
            for line in iter(fh.readline,''):
                if not re.match(self.DUD,line):
                    for test in self.repile:
                        res=re.match(test['regex'],line)
                        if res:
                            try:
                                col[test['func']].append( (res.groups(),fh.tell()) )
                            except KeyError:
                                col[test['func']] = [ ( res.groups(), fh.tell() ) ]
                            break

        except IOError as e:
           print "I/O error({0}): {1}".format(e.errno,e.strerror)

        pp.pprint(self.collection)
        self.deploy()
