#!/usr/bin/env python


from __future__ import print_function
import winpdb

import os, stat, re
import pprint

pp=pprint.PrettyPrinter(indent=4, width=40)
debug=False

def walktree(target,search):

    if search:
        res=re.compile(search)
        dname=os.path.dirname(search)
        bname=os.path.basename(search)
    else:
        search=dname=bname=None


    try:
        targetlist=os.listdir(target)
    except OSError:
        if debug:
            print(target, ": (no access)",end="\n")
        return None

    if debug:
        print("In: ", target)

    directories = [ 
            os.path.join(target,dir)
            for dir in targetlist
            if os.lstat(os.path.join(target, dir))[0] >> 13 & 2 ]

    for node in targetlist:
        if node not in directories:
            fullpath = os.path.join(target,node)
            if search:
                r=res.search(node)
                if r:
                    print("\t", fullpath, end='')
                    if os.lstat(fullpath)[0] >> 13 & 1:
                        print(" (symlink) ")
                    else:
                        print()
            else:
                print(fullpath, ' ',end='')
                if os.lstat(fullpath)[0] >> 13 & 1:
                    print(" (symlink) ",end="")
                print("\t", fullpath)

    try:
        for dir in directories:
            walktree(dir,search)
    except:
        pass


if __name__ == '__main__':

    import sys

    if len(sys.argv) > 2:
        target=sys.argv[1]
        search=sys.argv[2]
        walktree(target=target,search=search)
    else:
        walktree(target=sys.argv[1],search='.*')
