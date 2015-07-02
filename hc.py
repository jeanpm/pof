# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 12:05:24 2015

@author: jean
"""

import knapsack as kp
import mst
from binspace import BinarySpace
from swap import SwapNeighborhood
from bitflip import BitflipNeighborhood
import matplotlib.pyplot as plt

import numpy as np
import random

random.seed(0)
np.random.seed(0)

MAXEVALS = 6000
instance_file = "src/testset/test.100.1.1"

N = 50
#P  = kp.Knapsack(instance_file, BinarySpace)
P  = mst.MST(N)
N1 = BitflipNeighborhood(P.search_space)
N2 = SwapNeighborhood(P.search_space)

#x = kp.KpBinarySolution(P)
x = mst.MSTSolution(P)


nevals = 0
fx = x.evaluate()

hcExp = np.zeros(MAXEVALS * 2)
hcExp = np.reshape(hcExp, (MAXEVALS, 2))

state1 = True
while nevals < MAXEVALS:
    if nevals % 2 == 0:
        y = N1.randomNeighbor(x)
        fy = y.evaluate()
        nevals += 1
        if fy <= fx:
            fx = fy
            x.copy(y)        
    else:
        y = N2.randomNeighbor(x)
        if y is not None:
            fy = y.evaluate()
            nevals += 1
            if fy <= fx:
                fx = fy
                x.copy(y)
    hcExp[nevals-1] = [nevals, fx]

print nevals 
print "UB=", P.ub
print "f(x)  = ", fx
print "f(x*) = ", P.ref
#print [(i,j) for i,j in x.used]
   
hcExp = hcExp[range(0,len(hcExp), 10)]

print "ST from HC"
layout = mst.print_spanning_tree(x.data, P.adjmat)
plt.draw()   

#print "Optimal spanning tree"
#mst.print_spanning_tree(P.adjmat)

