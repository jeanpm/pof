# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 11:09:28 2015

@author: jean
"""

import numpy as np
from pof import Solution
from scipy.sparse.csgraph import minimum_spanning_tree
from scipy.sparse.csgraph import connected_components
import networkx as nx
import matplotlib.pyplot as plt
import random

# -----------------------------------------------------------------------------
class EdgeSpace(object):
    '''
    A search space containing complete and incomplete {0,1,-1}^n solutions.
    '''
    def __init__(self, n):    
        self.dimension = n
        # The components in this case are the indices of variables
        self.components = []
        for i in range(n):
            for j in range(i+1, n):
                self.components.append((i,j))
                
# -----------------------------------------------------------------------------      
# Minimum Spanning Tree
class MST(object):
    def __init__(self, N):
        self.N = N
        MAX_DIST = 50
        distance = np.random.random_integers(0, MAX_DIST,size=(N,N))
        
        self.distance = (distance + distance.T)/2
#        self.distance = distance - np.diag(distance.diagonal())
        
        self.ub = N*N * np.max(distance)

        # Calls the initializer (constructor) of the class 'search_space'
        self.search_space = EdgeSpace(self.N)
        
        self.st = minimum_spanning_tree(self.distance)
        self.adjmat = self.st.toarray().astype(int)
        self.ref = np.sum(self.adjmat)
        

# -----------------------------------------------------------------------------      
class MSTSolution(Solution):
    '''
    Class representing complete or incomplete solutions. An initial solution do
    not possesses any component, therefore, it is an incomplete solution.
    '''
    def __init__(self, problem):
        # The number of available components to compose a solution
        self.problem = problem        
        # It is better to be a list since components must be removed, inserted.
        self.unused = list(problem.search_space.components)
        self.used = []        
        self.data = np.zeros([problem.N, problem.N], dtype='int32')
        
        # Shuffle the indices of the components
#        subset = np.copy(problem.search_space.components)
#        np.random.shuffle(subset)
#        # Adds a random number of components to the solution
#        for i in subset[:random.randrange(problem.search_space.dimension)]:
#            self.addComponent(i)     
#        self.ncomponents = 1
        #print "Random solution created"

                    
    def __str__(self):
        return np.array_str(self.data) + ":: " + str(self.evaluate())
        
    def removeTuple(self, lista, c):
        for i, val in enumerate(lista):
            if (val[0], val[1]) == (c[0], c[1]):
                del lista[i]
                return    
        
    def addComponent(self, c):
        #self.unused.remove(c)
        self.removeTuple(self.unused, c)
        self.used.append(tuple(c))
        self.data[c[0],c[1]] = self.problem.distance[c[0],c[1]]
        self.data[c[1],c[0]] = self.problem.distance[c[0],c[1]]
    
    def delComponent(self, c):
        #self.used.remove(c)
        self.removeTuple(self.used, c)
        self.unused.append(tuple(c))
        self.data[c[0],c[1]] = 0
        self.data[c[1],c[0]] = 0
        
    def differenceTo(self, y):
        diffUsed = set(y.used) - set(self.used)
        diffUnused = set(y.unused) - set(self.unused)
        return (diffUsed, diffUnused)
                
    
    def isActive(self, c):
        return True if self.data[c[0],c[1]] > 0  else False
        
    def clone(self):
        newsol = MSTSolution(self.problem)
        newsol.data = np.copy(self.data)
        newsol.used = list(self.used)
        newsol.unused = list(self.unused)
        return newsol
        
    def copy(self, x):
        self.data = np.copy(x.data)
        self.search_space = x.problem.search_space
        self.used = list(x.used)
        self.unused = list(x.unused)
        
    def distanceTo(self, y):
        dist = np.sum(self.data != y.data)
        return dist

    def evaluate(self):
        self.ncomponents = connected_components(self.data)[0]
        wsum = sum( [self.problem.distance[c] for c in self.used] )
        fx = (self.ncomponents-1) * self.problem.ub + wsum
        return fx

#-----------------------------------------------------------------------------
# Auxiliar function for drawing a spanning tree
#-----------------------------------------------------------------------------

def print_spanning_tree(adj_matrix, opt_matrix, layout=None):
    plt.axis('off')
    H = nx.Graph()
    H.add_nodes_from(xrange(len(adj_matrix)))
    nz = np.nonzero(adj_matrix)
    nz1 = np.nonzero(opt_matrix)
    e  = zip(nz[0], nz[1])
    e1  = zip(nz1[0], nz1[1])
    w  = adj_matrix[nz]
    w1 = opt_matrix[nz1]
    data = [ (e[i][0], e[i][1], w[i]) for i in xrange(len(e))]
    data1 = [ (e1[i][0], e1[i][1], w1[i]) for i in xrange(len(e1))]            
    
    H.add_weighted_edges_from(data1, attr="weight")
    if layout is None:
        layout = nx.spring_layout(H, weight="weight")
    nx.draw_networkx_edges(H, pos=layout, style='dashed')
    raw_input()    
    
    for e in data1:
        H.remove_edge(e[0], e[1])
        
    H.add_weighted_edges_from(data)
    nx.draw_networkx_nodes(H, pos=layout, node_size=100, node_color="white")
    nx.draw_networkx_edges(H, pos=layout, width=1.5)
    
    return layout
