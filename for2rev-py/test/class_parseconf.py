#!/usr/bin/env python

import re
import pprint


class parse_nconf(object):
    """ 
    read BIND 9 configuration files.  Not really a parser; more an importer
    """

   
    repile = [
        {
            "name":"dud",
            "regex":re.compile(r'(^\/\/|^\s*$|^#)'),
            "func":self.None,
        },
        {
            "name":"include",
            "regex":re.compile(r'^\s*include\s"(?P<filename>.*)"\s*;'),
            "func":self.self.parse_include,
        },
        {
            "name":"view",
            "regex":re.compile(r'\s*view\s"(?P<view>.*)"\s+{\s*'),
            "func":self.parse_view,
        },
        {
            "name":"zone",
            "regex":re.compile(r'^\s*zone\s+"(?P<zone>[\w.-]+)"\s+{.*'),
            "func":self.parse_zone,
        },
        {
            "name":"open_close",
            "regex":re.compile(r'^\s*(.*)\s*{.*}\s*'),
            "func":self.parse_open_close,
        },
        {
            "name":"stanz_jaws",
            "regex":re.compile(r'^\s*(.*)\s*([{}])\s*'),
            "func":self.parse_jaws,
        },
        {
            "name":"simple_opt",
            "regex":re.compile(r'^\s*([^{}]+)\s+([^{}\s]+)[;\s]*$'),
            "func":self.parse_simple_opt,
        },
        {
            "name":"fallthrough",
            "regex":re.compile(r'^(.*)$'),
            "func":self.None,
        },
    ]

    nconf_tree={
        'view':None,
        'cfg': {
            'file':{},
            'working':[]
        },
        'views':{},
        'zones': {},
    }

    nconf_tree['cfg']['working'].insert(0,default_root)

    def __init__(self,baseconf='named.conf',root='etc/'):
        """ """
        nconf_tree['working']=root + baseconf

        parse_nconf()

        return self

        
def parse_dud(line,regex,nconf):
        """ """
        return


def parse_view(line,regex,nconf):
    """ """
    res=re.match(regex,line)
    view=res.group('view')

    nconf['view'] = view
    nconf['views'][view] = {}

    return nconf


def parse_zone(line,regex,nconf):
    """ """

    res=re.match(regex,line)
    zone=res.group('zone')


    nconf_frag={}

    zonefrag={
        zone:{ 
            'zonefile': None,
            'cfg':[],
        }
    }

    if re.match(r'^.*{\s*$',line):
        zonefrag[zone]['cfg'].insert(0,line)
        working=nconf['cfg']['working'][0]
        fh=nconf['cfg']['file'][working]
        
        if fh.closed:
            fh=file(nconf['cfg']['working'][0])

        for line in iter(fh):
            zonefrag[zone]['cfg'].append(line)
            zline=re.match(r'^\s+file\s+"(?P<filename>.*)";',line)
            if zline:
                zonefrag[zone]['zonefile'] = zline.group('filename')
            elif re.match(r'^.*}\s*;\s*$',line):
                break
    else:
        zline=re.match(r'\s*zone\s+"(?P<zone>[\w\-.]+)"?.*\s+file\s+"?(?P<zonefile>[\w/\-.]+)"?.*',line)
        zonefrag[zone]['cfg'].append(line)
        zonefrag[zone]['zonefile']=zline.group('zonefile')

    return zonefrag

def parse_simple_opt(line,regex,nconf):
        """ """


def parse_include(line,regex,nconf):
    """ """
    res=re.match(regex,line)
    view=nconf['view']
    include=res.group('filename')

    nconf['cfg']['working'].insert(0,include)
    nconf['view']=view

    return parse_nconf(nconf)


def parse_nconf(self):

    nconf_tree = self.nconf_tree

    working = self.nconf_tree['cfg']['working'][0]

    if not nconf_tree['cfg']['file'].has_key(working[0]):
        fh=file('./' + working)
        nconf_tree['cfg']['file'][working] = fh
    else:
        fh=file(nconf_tree['cfg']['file'][working])

    for line in iter(fh):
        for el in repile:
            if re.match(el['regex'],line):
               
                if el['func']:
                    chunk=el['func'](line,el['regex'],nconf_tree)
                    if chunk:
                        chunks.append(chunk)                   
                        if chunk.has_key('view') and ( chunk['view'] == nconf_tree['view']):
                            nconf_tree.update(chunk)
                        else:
                            view=nconf_tree['view']
                            if not nconf_tree['views'].has_key(view):
                                nconf_tree['views'] = { 'view':chunk }
                            else:
                                nconf_tree['views'][view].update(chunk)
                break
    else:
        if len(nconf_tree['cfg']['working']) > 1:
            nconf_tree['cfg']['working'].pop(0)

    
    return nconf_tree



if __name__ == "__main__":
    dbug=False
    pp = pprint.PrettyPrinter(indent=4,width=20)

    default_root = 'etc/named.conf'

    nconf_tree = skel_nconf()

    nconf_tree['cfg']['working'].insert(0,default_root)

    #nconf_tree['cfg']['offset']=0


    thing=parse_nconf(nconf_tree)

    if dbug:
        print "end"
        #pp.pprint(thing)

