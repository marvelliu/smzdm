#!/usr/bin/env python

import os
import glob
import imp 
def get_all_subclasses(cls):

    all_subclasses = []
    
    g = globals().copy()   # use a copy to make sure it will not change during iteration
    g.update(locals())     # add local symbols
    for k, v in g.items(): # iterate over all globals object
        print k
        try:
            if (v is not cls) and issubclass(v, cls): # found a strict sub class?
               all_subclasses.append(v) 
        except TypeError:  # issubclass raises a TypeError if arg is not a class...
            pass
    return all_subclasses

def my_import(name):
    components = name.split('.')
    mod = __import__(components[0])
    print components[0]
    print components[1:]
    for comp in components[1:]:
        print mod
        print comp
        mod = getattr(mod, comp)
    return mod
