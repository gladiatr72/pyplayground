#!/usr/bin/env python

import re

from yaml import load, dump
try:
        from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
        from yaml import Loader, Dumper

def parse_dud():
	""" """

def parse_open_close():
	""" """

def parse_jaws():
	""" """

def parse_view():
	""" """

def parse_simple_opt():
	""" """

repile=load(file('thing.yml'),Loader=Loader)


print repile
