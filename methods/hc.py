# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 12:05:24 2015

@author: jean
"""

def hill_climbing(neighborhood, x):
    y = neighborhood.randomNeighbor(x)
    if y is not None and y.isBetterThan(x):
        return y
    return x

