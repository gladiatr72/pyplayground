#!/usr/bin/env python

from __future__ import print_function
import re
import types

include=re.compile(r'^\s*include\s"(?P<filename>.*)"\s*;')

def readNconf(filename='/etc/named.conf'):
    """ 
    readNconf(filename)

    generator that processes BIND9 include directives while reading out the
    configuration
    """

    fh=file('../' + filename)

    for line in fh:
        res=include.match(line)
        if type(res) == type(None): 
            yield line
        else:
            incfile=res.groups('filename')[0]
            print('incfile is ', incfile)
            for el in readNconf(filename=incfile):
                yield el

def tramp(gen, *args, **kwargs):
    g = gen(*args, **kwargs)
    while isinstance(g,types.GeneratorType):
        g=g.next()
    return g

if __name__ == '__main__':
    for el in readNconf(filename='./etc/named.conf'):
        while isinstance(el, types.GeneratorType):
            pass
        else:
            pass

    
    


    
