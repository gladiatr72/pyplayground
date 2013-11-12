#!/usr/bin/env python

import os
import pprint
import time

pp=pprint.PrettyPrinter(indent=4,width=20)


seconds=600
now=time.time()

for p, d, f in os.walk('..'):
    for name in f:
        fullpath = os.path.join(p,name)
        try:
            mtime = os.path.getmtime(fullpath)
        except:
            pass

        if mtime > ( now - seconds ):
            print fullpath + ' ' + str(mtime)



