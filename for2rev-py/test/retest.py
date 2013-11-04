#!/usr/bin/env python

import re
import pprint


pp = pprint.PrettyPrinter(indent=4,width=20)

tests={ 'close': [ re.compile(r'}'), -1 ], 'open':[re.compile(r'{'), 1] }

lines=[ l for l in file('named.neuter')]


count=0
total={}
depth=0

for l in lines:
    for t in ( 'open', 'close'):
        adj=tests[t][1]
        regex=tests[t][0]

        ps=re.findall(regex,l)
        try:
            total[t]+=len(ps)
        except KeyError:   
            total[t]=len(ps) 

        depth+=(len(ps) * adj)
    print depth, l

pp.pprint(total)
pp.pprint((count, count - total['close']))
