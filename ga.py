# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 20:59:49 2015

@author: jean
"""

import numpy as np
import random

import knapsack as kp
import mst
from binspace import BinarySpace
from swap import SwapNeighborhood
from bitflip import BitflipNeighborhood
import pylab

import random

random.seed(0)
np.random.seed(0)

t = 0.1
N = 15
POPSIZE = 30
MAXEVALS = 3000
instance_file = "src/testset/test.100.1.1"

#P  = kp.Knapsack(instance_file, BinarySpace)
P  = mst.MST(N)
N1 = BitflipNeighborhood(P.search_space)
N2 = SwapNeighborhood(P.search_space)

#x = kp.KpBinarySolution(P)
x = mst.MSTSolution(P)

def xover(x, z):
    dist = x.distanceTo(z)
    y = x.clone()    
    for i in range(dist/2):
        y = N1.randomNeighborTowards(y, z)
    return y


def mutate(x):
    return N1.randomNeighbor(x)


def evaluate(pop):
    return np.argsort([pop[i].evaluate() for i in xrange(POPSIZE)])

gaExp = np.zeros(MAXEVALS/POPSIZE * 2)
gaExp = np.reshape(gaExp, (MAXEVALS/POPSIZE, 2))
nevals = 0
gen = 0

def truncation(pop, t=0.2):
    idx = evaluate(pop)
    idx = idx[:len(idx)*t]
    gaExp[gen, 1] = pop[idx[0]].evaluate()
    tmp = idx[0]
    idx = np.random.choice(idx, POPSIZE)
    idx[0] = tmp
    return pop[idx]

#pop = np.array([kp.KpBinarySolution(P) for i in xrange(POPSIZE)])
pop = np.array([mst.MSTSolution(P) for i in xrange(POPSIZE)])

while nevals < MAXEVALS:
    gaExp[gen, 0] = nevals
    pop = truncation(pop, t)    
    for j in xrange(1,POPSIZE):
        pop[j] = xover(pop[j], pop[random.randrange(POPSIZE)])
        pop[j] = mutate(pop[j])
    nevals += POPSIZE
    gen += 1
print nevals

idx =  np.argsort([pop[i].evaluate() for i in xrange(POPSIZE)])
#print pop[idx[0]].used, ", LB=", int(P.ub)
print "f(x) = ", pop[idx[0]].evaluate() , " f(x*) = ", P.ref
#print [(i,j) for i,j in x.used]

y = pop[idx[0]]
   
i = 50
j = len(gaExp[:,0])
pylab.plot(gaExp[i:j,0], gaExp[i:j,1], label="GA")
pylab.plot(hcExp[i:j,0], hcExp[i:j,1], label="HC")
pylab.plot(hcExp[i:j,0], [P.ref] * len(hcExp[i:j,1]), label="*")
pylab.legend(loc='upper right')

import networkx as nx
G = nx.Graph()
G.add_nodes_from(range(N))
data = [(a,b,P.distance[a,b]) for a,b in y.used]
G.add_weighted_edges_from(data)
nx.draw(G, pos=nx.spring_layout(G))
