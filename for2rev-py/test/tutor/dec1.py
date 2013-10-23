#!/usr/bin/env python

def decorator(fn):
    def inner(n):
        return fn(n)+1

    return inner

def wrap_with_prints(fn):
    print('wrap_with_prints runs only once')
    
    def wrapped():
        print('About to run %s') % fn.__name__
        fn()
        print('Done running %s') % fn.__name__

    return wrapped

@decorator
def f(n):
    return n+1


@wrap_with_prints
def fn_to_decorate():
    print('Running the function that was decorated')



