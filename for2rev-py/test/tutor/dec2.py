#!/usr/bin/env python

class dec2(object):

    contents=[]

    def __init__(self,filename='../etc/named.conf'):
        nconf=filename

        self.contents=[ line for line in file(nconf,'r') ]


    def play(self):
        print self.contents

