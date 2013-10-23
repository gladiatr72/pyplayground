#!/usr/bin/env python

for x in xrange(1,100):
    primes=[ 2,3,5,7,9,11,13,17 ]
    for mod in primes:
        if not x % mod:
            print("%s div by %s") % (x,mod)
            break
    else:
        print("%s is prime") % x
