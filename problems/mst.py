# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 11:09:28 2015

@author: jean
"""

import numpy as np
from pof import Solution
from spaces.edgespace import EdgeSpace
from scipy.sparse.csgraph import minimum_spanning_tree, connected_components
import networkx as nx
import matplotlib.pyplot as plt

                
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
        
        self.sol = minimum_spanning_tree(self.distance)
        self.adjmat = self.sol.toarray().astype(int)
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
        self.fx = None
        
        self.components = problem.search_space.components
        self.present = []
        self.absent  = []
        # It all starts with undefined components
        self.unknown = list(problem.search_space.components)
        
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
        
    def __getComponentIndex(self, lista, c):
        for i, val in enumerate(lista):
            if (val[0], val[1]) == (c[0], c[1]):
                return i
        raise IndexError("Component not in the list")
        
    def __updatedata(self, c, value):
        self.data[c[0],c[1]] = value
        self.data[c[1],c[0]] = value
        
        
    def addComponent(self, c):
        unusedIndex = self.__getComponentIndex(self.unused, c)
        self.addComponentByIndex(unusedIndex)
    
    def delComponent(self, c):
        usedIndex = self.__getComponentIndex(self.used, c)
        self.delComponentByIndex(usedIndex)  
    
    def delComponentByIndex(self, index):
        c = self.used.pop(index)
        self.unused.append(c)
        self.__updatedata(c, 0)
        
    def addComponentByIndex(self, index):
        c = self.unused.pop(index)
        self.used.append(c)
        self.__updatedata(c, self.problem.distance[c[0],c[1]])     
        
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
        du,dun = self.differenceTo(y)
        dist = len(du) + len(dun)
        return dist

    def evaluate(self):
        if self.fx is None:
            self.ncomponents = connected_components(self.data)[0]
            wsum = sum( [self.problem.distance[c] for c in self.used] )
            self.fx = (self.ncomponents-1) * self.problem.ub + wsum
        return self.fx

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
    nx.draw_networkx_edges(H, pos=layout, width=3, edge_color="red")    

    G = nx.Graph()    
    G.add_nodes_from(xrange(len(adj_matrix)))
    G.add_weighted_edges_from(data)
    nx.draw_networkx_nodes(G, pos=layout, node_size=100, node_color="white")
    nx.draw_networkx_edges(G, pos=layout, style='dashed', width=2)        
    
    return layout
