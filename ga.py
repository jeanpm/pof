# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 20:59:49 2015

@author: jean
"""

import numpy as np
import random

#import knapsack as kp
import mst
#from binspace import BinarySpace
from swap import SwapNeighborhood
from bitflip import BitflipNeighborhood
import matplotlib.pyplot as plt

random.seed(0)
np.random.seed(0)

t = 0.3
N = 50
POPSIZE = 10
MAXEVALS = 6000
instance_file = "src/testset/test.100.1.1"

#P  = kp.Knapsack(instance_file, BinarySpace)
P  = mst.MST(N)
N1 = BitflipNeighborhood(P.search_space)
N2 = SwapNeighborhood(P.search_space)

#x = kp.KpBinarySolution(P)
#x = mst.MSTSolution(P)

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
print "f(x)  = ", pop[idx[0]].evaluate() 
print "f(x*) = ", P.ref
#print [(i,j) for i,j in x.used]

y = pop[idx[0]]


print "ST from GA"
mst.print_spanning_tree(y.data, P.adjmat, layout)
plt.draw()

i = 100
j = len(gaExp[:,0])
plt.figure()
plt.axis('on')
plt.plot(gaExp[i:j,0], gaExp[i:j,1], label="GA")
plt.plot(hcExp[i:j,0], hcExp[i:j,1], label="HC")
plt.plot(hcExp[i:j,0], [P.ref] * len(hcExp[i:j,1]), label="*")
plt.legend(loc='upper right')
plt.draw()