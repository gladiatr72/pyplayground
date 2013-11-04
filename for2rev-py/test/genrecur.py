#!/home/sdspence/u/run/python/bin/python

"""
  Generator implementation of BIND9 configuration reader
"""

from __future__ import print_function
import re
import types

INCLUDE = re.compile(r'^\s*include\s"(?P<filename>.*)"\s*;')

def _view():
    pass

def _zone():
    pass

def _open_close():
    pass

def _stanz_jaws():
    pass

def _simple_opt():
    pass


REPILE = [
    {
        "name":"view",
        "regex":re.compile(r'\s*view\s"(?P<view>.*)"\s+{\s*'),
        'func':_view
    },
    {
        "name":"zone",
        "regex":re.compile(r'^\s*zone\s+"(?P<zone>[\w.-]+)"\s+{.*'),
        'func':_zone
    },
    {
        "name":"fallthrough",
        "regex":re.compile(r'^.*$'),
        'func':None,
    },

]

BITS = [
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


def read_nconf(filename='/etc/named.conf'):
    """
    read_nconf(filename)

    generator that processes BIND9 include directives while reading out the
    configuration
    """

    fh = open('../' + filename)

    view='root'

    for line in iter(fh.readline,''):
        res = INCLUDE.match(line)
        if not res:
            yield line
        else:
            incfile = res.group('filename')
            for line in read_nconf(filename=incfile):
                yield line


if __name__ == '__main__':
    for el in read_nconf(filename='./etc/named.conf'):
        while isinstance(el, types.GeneratorType):
            pass
        else:
            print(el)
