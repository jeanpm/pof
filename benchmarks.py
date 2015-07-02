# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 18:06:08 2015

@author: jean
"""

def oneMax(x):
    return len(x.used)
    
def trapk(x, k=5):
    idxs = range(0, x.search_space.dimension, k)
    fx = 0
    for i in idxs:
        unitation = 0
        unused = 0
        for val in x.data[i:(i+k)]:
            if val >= 0:
                unitation += val
            else: 
                unused += 1
        #unitation += unused 
        if unitation == k:
            fx += k
        else :
            fx += k - 1 - unitation
    return fx
        