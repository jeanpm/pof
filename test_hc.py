# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 13:29:21 2015

@author: jean
"""


#from problems.knapsack import Knapsack, KpBinarySolution
from problems.mst  import MST, MSTSolution
#from spaces.binspace import BinarySpace
from neighbor.swap import SwapNeighborhood
from neighbor.addremove import AddOrRemoveNeighborhood
from methods.hc import hill_climbing

import numpy as np
import time
from testconf import *

#P  = Knapsack(instance_file, BinarySpace)
P  = MST(N)
N1 = AddOrRemoveNeighborhood(P.search_space)
N2 = SwapNeighborhood(P.search_space)

#hcx = KpBinarySolution(P)
hcx = MSTSolution(P)

hcExp = np.zeros(MAXEVALS * 2)
hcExp = np.reshape(hcExp, (MAXEVALS, 2))

state1 = True

start = time.time()
while nevals < MAXEVALS:
    if nevals % 2 == 0:
        hcx = hill_climbing(N1, hcx)
        nevals += 1
    else:
        hcx = hill_climbing(N2, hcx)        
        nevals += 1    
    # Store current fitness value
    hcExp[nevals-1] = [nevals, hcx.evaluate()]
print nevals, " evaluations in ", time.time() - start, " seconds."


fx = hcx.evaluate()
print "UB=", P.ub
print "f(x)  = ", hcx.evaluate()
print "f(x*) = ", P.ref
#print [(i,j) for i,j in x.used]
   
hcExp = hcExp[range(0,len(hcExp), POPSIZE)]
