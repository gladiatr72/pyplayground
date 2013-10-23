# -*- coding: utf-8 -*-  

import re

class count_paren(object):
    def __init__(self,func):
        self.open=0
        self.fopen=0
        self.func = func

    def __call__(self, *args):
        opener=len(re.findall(r'{',args[0]))
        self.open+=opener
        self.open-=len(re.findall(r'}',args[0]))
        self.fopen+=opener

        self.func(args,depth=self.open,total=self.fopen) 



if __name__ == '__main__':

    @count_paren
    def test(arg1,**args):
        """ """ 
        print args['depth'],
        print args['total'],
        print line



    output=[ test(line) for line in file('../etc/named.conf') ]



