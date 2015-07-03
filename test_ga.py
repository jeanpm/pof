# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 13:58:05 2015

@author: jean
"""

import numpy as np
import random

from problems.knapsack import Knapsack, KpBinarySolution
#from pof.problems import mst
from spaces.binspace import BinarySpace
from neighbor.swap import SwapNeighborhood
from neighbor.addremove import AddOrRemoveNeighborhood
from methods.ga import genetic_algorithm


import matplotlib.pyplot as plt

random.seed(0)
np.random.seed(0)

t = 0.2
N = 100
POPSIZE = 30
MAXEVALS = 3000
instance_file = "../src/testset/test.100.1.1"

P  = Knapsack(instance_file, BinarySpace)
#P  = mst.MST(N)
N1 = AddOrRemoveNeighborhood(P.search_space)
N2 = SwapNeighborhood(P.search_space)

#x = kp.KpBinarySolution(P)
#x = mst.MSTSolution(P)


gaExp = np.zeros(MAXEVALS/POPSIZE * 2)
gaExp = np.reshape(gaExp, (MAXEVALS/POPSIZE, 2))
nevals = 0
gen = 0



pop = np.array([KpBinarySolution(P) for i in xrange(POPSIZE)])
#pop = np.array([mst.MSTSolution(P) for i in xrange(POPSIZE)])

while nevals < MAXEVALS:
    gaExp[gen, 0] = nevals
    pop = genetic_algorithm(N1, pop, 0.15)
    idx =  np.argmin([pop[i].evaluate() for i in xrange(POPSIZE)])
    gaExp[gen, 1] = pop[idx].evaluate()
    nevals += POPSIZE
    gen += 1
print nevals



fy = pop[0].evaluate() 
print "f(x)  = ", fy
print "f(x*) = ", P.ref
#print [(i,j) for i,j in x.used]

#gax = pop[idx[0]]
#
#plt.figure(figsize=(10,4))
#plt.subplot(1, 2, 1)
#layout = mst.print_spanning_tree(hcx.data, P.adjmat)
#plt.title("ST from HC, f(x) = " + str(fx))
#
#plt.subplot(1, 2, 2)
#mst.print_spanning_tree(gax.data, P.adjmat, layout)
#plt.title("ST from GA, f(x) = " + str(fy))
#
#plt.show()
#
i = 30
j = len(gaExp[:,0])
plt.figure()
plt.axis('on')
plt.plot(gaExp[i:j,0], gaExp[i:j,1], label="GA")
plt.plot(hcExp[i:j,0], hcExp[i:j,1], label="HC")
plt.plot(hcExp[i:j,0], [P.ref] * len(hcExp[i:j,1]), label="*")
plt.legend(loc='upper right')
plt.draw()
