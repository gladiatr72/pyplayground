import re
import pprint

pp = pprint.PrettyPrinter(indent=4,width=80)

def _dud():
    print "*** dud"

def _multilist():
    print "*** multilist"


def _parse_include():
    print "*** include"

def _parse_view():
    print "*** view"

def _parse_zone():
    print "*** zone"

def _open_close():
    print "*** close"

def _parse_jaws():
    print "*** jaws"

def _simple_opt():
    print "*** simple_opt"

def _fallthrough():
    print "*** fallthrough"

dud=re.compile(r'(^\/\/|^\s*$|^#)')

repile = [
    {
        "name":"include",
        "regex":re.compile(r'^\s*include\s"(?P<filename>.*)"\s*;'),
        "func":_parse_include,
    },
    {
        "name":"view",
        "regex":re.compile(r'\s*view\s"(?P<view>.*)"\s+{\s*'),
        "func":_parse_view,
    },
    {
        "name":"zone",
        "regex":re.compile(r'^\s*zone\s+"(?P<zone>[\w.-]+)"\s+{.*'),
        "func":_parse_zone,
    },
    {
        "name":"open_close",
        "regex":re.compile(r'^\s*(.*)\s*{.*}\s*'),
        "func":_open_close,
    },
    {
        "name":"stanz_jaws",
        "regex":re.compile(r'^\s*(.*)\s*([{}])\s*'),
        "func":_parse_jaws,
    },
    {
        "name":"multilist",
        "regex":re.compile(r';.*;'),
        "func":_multilist
    },
    {
        "name":"simple_opt",
        "regex":re.compile(r'^\s*([^{}]+)\s+([^{}\s]+)[;\s]*$'),
        "func":_simple_opt,
    },
]

fh=file('etc/named.conf','rb')

collection=[]

for line in iter(fh.readline,''):
    collect=[
        (test['func'], fh.tell())
            for test in repile
            if (re.match(test['regex'],line) and not re.match(dud,line) ) ]

    if collect:
        collection.append(collect)



print len(collection)

for el in collection:
    pp.pprint(el)
    print "\n\n"

#print { el[0][0]:el[0][1] for el in collect }

#pprint(callist)

#for el in collect:
#    pp.pprint(el)
#    print "*********"
#    print
#



