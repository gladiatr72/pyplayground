#!/usr/bin/env python

import bindoo
import pprint

pp = pprint.PrettyPrinter(indent=4,width=80)

A=bindoo.Load('/home/sdspence/u/named/etc/named.conf')

pp.pprint(A.fh)
