#!/usr/bin/env python

import sys
import os
import re
import pprint
import pyaml

named_conf="etc/named.conf"

pp = pprint.PrettyPrinter(indent=4,width=80)

re_zoneline=re.compile(r'^\s{0,}zone\s+"(.*)" { type.*file "(.*)"; notify.*', flags = 0)
re_included=re.compile(r'^\s{0,}include\s+"(.*)";.*')
re_zonestanz=re.compile(r'^\s+zone\s+{(\s+$|$)')
re_zonestanz_zone=re.compile(r'^\s+zone\s+"(.*)".*')
re_zonestanz_file=re.compile(r'^\s+file\s+"(.*)".*')
re_viewline=re.compile(r'^view\s+"(.*)"\s*{\s*$')

def find_nconf(conflist):
    for nconf in conflist:

        included=[ os.curdir + re.match(re_included,line).group(1) 
                for line in file(nconf,'r') 
                if re.match(re_included,line)]
        

        if len(included) == 0:
            return []
        else:
            for conf in included:
                included.extend(find_nconf([conf]))

            return included

re_viewloc=re.compile(r'\s{0}view\s+(.*)\s*{\s*')

def gather_view(config_files):
    views={}
    for nconf in config_files:
        viewlines=[ re.match(re_viewloc,line)
            for line in file(nconf, 'r')
            if re.match(re_viewloc,line)]
        

def gather_zone(config_files):
    zones={}
    for nconf in config_files:

        zonelines=[ re.match(re_zoneline,line).group(1) + '|' + re.match(re_zoneline,line).group(2) 
                for line in file(nconf,'r') 
                if re.match(re_zoneline,line)]

        fh_nconf=file(nconf,'r') 

        zonestanz_loc=[ fh_nconf.tell()
                for line in iter(fh_nconf.readline, '')
                if re.match(re_zonestanz,line) ]
        
        print zonestanz_loc

        for loc in zonestanz_loc:
            fh_nconf=seek(loc)
            zone=re.match(re_zonestanz_zone, fh_nconf.readline()).group(1)

            for line in fh_nconf:
                if re.match(re_zonestanz_file, line):
                    zones[re_zonestanz_file.group(1)] = zone
                    break

        fh_nconf.close()

        for zl in zonelines:
            [z, f ] = zl.split('|')
            zones[z] = f

    return zones

def gather_views(config_files):
    views={}
    for nconf in config_files:
        fh_nconf=file(nconf, 'r')
        view_loc={ re.match(re_viewline,line).group(1) : [ nconf, fh_nconf.tell() ]
                for line in iter(fh_nconf.readline, '')
                if re.match(re_viewline,line) }

        if view_loc.keys():
            for k in view_loc.keys():
                views[k] = view_loc[k]
        
        fh_nconf.close()

    return views

    
if __name__ == "__main__":
    config_files=find_nconf([ named_conf ])
    config_files.insert(0,named_conf)
    views=gather_views(config_files)
    #views=gather_zone(config_files)

    pp.pprint(views)


