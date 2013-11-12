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

    DUD=re.compile(r'(^\/\/|^\s*$|^#)')
    INCLUDE = re.compile(r'^\s*include\s"(?P<filename>.*)"\s*;')
    VIEW=[ 'root' ]



    def _view(self,payload, depth):

        view=payload[0]    
        self.view.append(view)
        self.sentinel_view=view
        self.sentinel_depth=depth

        print("View starts:",view," at depth ", self.depth)

        return view

    def _zone(self,res,depth):

        # self.cfgen = self.open_nconf(filename=nconf)
        zone=res[0]

        sentinel = depth


        for line,depth in stanza:

            self.depth+=len(re.findall(r'{',line))
            self.depth-=len(re.findall(r'}',line))

            print(line,depth,sentinel)
            if depth >= sentinel:
                break
            
            res=re.match(r'^.*file\s+"(.*)"\s*;\s*$',line)
            print(type(res))

            if res:
                file=res.group(1)
                pp.pprint(zone,file)

	def expand_chroot(include):
		"""
		 derive the (actual) path of the named.conf directory
		 structure.  This is necessary to accomodate include
		 paths that do not follow the actual filesystem layout
		"""

		croot=self.confroot.split('/')
		iroot=include.split('/')

		rootlist=croot[:croot.index(croot[croot.index(iroot[1:-1][0])])]

		return '/'.join([ "%s" % el for el in rootlist])

    def open_nconf(self,*args,**kwargs):
        """
        open_nconf(filename)

        generator to process BIND9 include directives and return a cohesive
        series of lines

        returns a the tuple (line, file position)
        """

        confroot=""

        try:
            if 'filename' in kwargs:
                filename=kwargs['filename']
                fh = open(filename)
                self.fh.append(fh)
            else:
                fh=self.fh[-1]

            #print('open',filename)

            for line in fh:
                if self.DUD.match(line):
                    continue

                res = self.INCLUDE.match(line)

                if not res:
                    yield (line, self.depth)
                else:
                    incfile = res.group('filename')

                    if not confroot:
						confroot=chroot_expand(incfile)

                    include=confroot + incfile

                    for line, depth in self.open_nconf(filename=include):
                        yield (line, depth)

        except IOError as e:
           print("I/O error({0}): {1}".format(e.errno,e.strerror),filename)

        if type(filename) != types.FileType:
            self.fh.pop()


    def deploy(self,line,depth):
       
        for check in self.REPILE:
            res=check['regex'].match(line)
            if res and check['func']:
                #print(res.groups())
                check['func'](res,depth)
                break

	def open_bystanza(handle):
		if type(file) == types.StringTypes:
			nconf=open_nconf(handle)
		if type(file) == types.GeneratorType:
			nconf=handle




    def __init__(self,filename='../etc/named.conf',current_depth=0):

        self.depth=0
        self.sentinel_depth=0
        self.sentinel_view="root"
        self.view=[]
        self.fh=[]

        self.REPILE=[
            {  
                "name": "view",
                "regex": re.compile(r'\s*view\s"(?P<view>.*)"\s+{\s*'),
                "func": self._view
            },
            {
                "name":"zone",
                "regex":re.compile(r'^\s*zone\s+"(?P<zone>[\w.-]+)"\s+{.*'),
                'func': self._zone
            },
        ]


        nconf=filename
        self.confroot=os.path.dirname(nconf)

        self.cfgen = self.open_bystanza(filename=nconf)
		#self.cfgen = self.open_nconf(filename=nconf)

if __name__ == '__main__':
    pass
