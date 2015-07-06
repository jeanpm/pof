# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 13:58:05 2015

@author: jean
"""

import numpy as np

#from problems.knapsack import Knapsack, KpBinarySolution
from problems.mst  import MST, MSTSolution, print_spanning_tree
#from spaces.binspace import BinarySpace
from neighbor.addremove import AddOrRemoveNeighborhood
from methods.ga import genetic_algorithm
import matplotlib.pyplot as plt

from testconf import *
import time

#P  = Knapsack(instance_file, BinarySpace)
P  = MST(N)
N1 = AddOrRemoveNeighborhood(P.search_space)


gaExp = np.zeros(MAXEVALS/POPSIZE * 2)
gaExp = np.reshape(gaExp, (MAXEVALS/POPSIZE, 2))

start = time.time()
for exp in xrange(NEXP):
    random.seed(exp)
    np.random.seed(exp)
    
    gen = 0
    nevals = 0
    
    #pop = np.array([KpBinarySolution(P) for i in xrange(POPSIZE)])
    pop = np.array([MSTSolution(P) for i in xrange(POPSIZE)])
    
    while nevals < MAXEVALS:
        gaExp[gen, 0] = nevals
        pop = genetic_algorithm(N1, pop, t)
        idx =  np.argmin([pop[i].evaluate() for i in xrange(POPSIZE)])
        gaExp[gen, 1] += pop[idx].evaluate()
        nevals += POPSIZE
        gen += 1
    
print nevals, " evaluations in ", time.time() - start, " seconds."

gaExp[:, 1] /= 30.0

fy = pop[0].evaluate() 
print "f(x)  = ", fy
print "f(x*) = ", P.ref
#print [(i,j) for i,j in x.used]

gax = pop[0]
#
plt.figure(figsize=(10,4))
plt.subplot(1, 2, 1)
layout = print_spanning_tree(hcx.data, P.adjmat)
plt.title("ST from HC, f(x) = " + str(fx))

plt.subplot(1, 2, 2)
print_spanning_tree(gax.data, P.adjmat, layout)
plt.title("ST from GA, f(x) = " + str(gax.evaluate()))

plt.show()
#
i = 0
j = len(gaExp[:,0])
plt.figure()
plt.axis('on')
plt.plot(gaExp[i:j,0], gaExp[i:j,1], label="GA")
plt.plot(hcExp[i:j,0], hcExp[i:j,1], label="HC")
plt.plot(hcExp[i:j,0], [P.ref] * len(hcExp[i:j,1]), label="*")
plt.legend(loc='upper right')
plt.draw()
