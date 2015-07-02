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

import numpy as np
import random

random.seed(0)
np.random.seed(0)

MAXEVALS = 3000
instance_file = "src/testset/test.100.1.1"

N = 15
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
#print x, "LB=", int(P.lb)
print "f(x) = ", fx
print "f(x*) = ", P.ref
#print [(i,j) for i,j in x.used]
   
hcExp = hcExp[range(0,len(hcExp), POPSIZE)]

import networkx as nx

def print_spanning_tree(adj_matrix):
    H = nx.Graph()
    H.add_nodes_from(xrange(len(adj_matrix)))
    nz = np.nonzero(adj_matrix)
    e  = zip(nz[0], nz[1])
    w  = adj_matrix[nz]
    data = [ (e[i][0], e[i][1], w[i]) for i in xrange(len(e))]
    H.add_weighted_edges_from(data)
    nx.draw(H, pos=nx.spring_layout(H))

print "Spanning tree found"
print_spanning_tree(P.distance * x.data)
print "Optimal spanning tree"
print_spanning_tree(P.adjmat)

