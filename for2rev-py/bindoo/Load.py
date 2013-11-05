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
import types
from CountParen import CountParen

pp = pprint.PrettyPrinter(indent=4,width=20)

class Load(object):
    """
    bindoo.Load('/path/to/named.conf')
    """


    def _view(self,payload, depth):

        view=payload[0]    
        self.view.append(view)
        self.sentinel_view=view
        self.sentinel_depth=depth
        #self.depth+=1

        #print("View starts:",view," at depth ", self.depth)
        

        return view

    def _zone(self,res,depth):
        return 'zone'

    def _zone_oneline(self,res,depth):
        return 'zone'


    DUD=re.compile(r'(^\/\/|^\s*$|^#)')
    INCLUDE = re.compile(r'^\s*include\s"(?P<filename>.*)"\s*;')
    VIEW=[ 'root' ]

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
            #print('open',filename)

            for line in fh:
                if self.DUD.match(line):
                    continue

                res = self.INCLUDE.match(line)

                self.depth+=len(re.findall(r'{',line))
                self.depth-=len(re.findall(r'}',line))

                if self.depth < self.sentinel_depth:  #and len(self.view) > 0:
                    self.view.pop()



                if not res:
                    yield (line, self.depth)
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


    def deploy(self,line,depth):
       
        for check in self.REPILE:
            res=check['regex'].match(line)
            if res and check['func']:
                #print(res.groups())
                check['func'](res.groups(),depth)
                break

    def __init__(self,filename='../etc/named.conf',current_depth=0):

        self.depth=0
        self.sentinel_depth=0
        self.sentinel_view="root"
        self.view=[]

        self.REPILE=[
            {  
                "name": "view",
                "regex": re.compile(r'\s*view\s"(?P<view>.*)"\s+{\s*'),
                "func": self._view
            },
            {
                "name": "zone_oneline",
                "regex": re.compile(r'^\s*zone\s+"(?P<zone>[\w.-]+)"\s+.*\sfile\s+"(?P<zoneflie>.*?)".*'),
                "func": self._zone_oneline
            },
            {
                "name":"zone",
                "regex":re.compile(r'^\s*zone\s+"(?P<zone>[\w.-]+)"\s+{.*'),
                'func': self._zone
            },
        ]


        nconf=filename
        self.confroot=os.path.dirname(nconf)

        self.cfgen = self.open_nconf(filename=nconf)

        for ( line, depth ) in self.cfgen:
            self.deploy(line,depth)

if __name__ == '__main__':
    pass
