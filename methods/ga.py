# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 20:59:49 2015

@author: jean
"""

import numpy as np
import random

def xover(x, z, neighborhood):
    y = x
    dist = y.distanceTo(z)
    if dist > 1:
        dist = dist/2 
        for y in neighborhood.randomNeighborTowards(y, z):
            dist -= 1
            if dist == 0: break      
    return y


def mutate(x, neighborhood):
    return neighborhood.randomNeighbor(x)


def evaluate(pop):
    return np.argsort([pop[i].evaluate() for i in xrange(len(pop))])
    
def truncation(pop, t):
    idx = evaluate(pop)
    idx = idx[:len(idx)*t]
    tmp = idx[0]
    idx = np.random.choice(idx, len(pop))
    idx[0] = tmp
    return pop[idx]


def genetic_algorithm(neighborhood, pop, t=0.15):
    pop = truncation(pop, t)
    for j in xrange(1, len(pop)):
        pop[j] = xover(pop[j], random.choice(pop), neighborhood)
        pop[j] = mutate(pop[j], neighborhood)
    return pop