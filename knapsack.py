# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 16:01:39 2015

@author: jean
"""

import numpy as np
import random
from pof import Solution

class Knapsack(object):
    def __init__(self, instance_file, search_space):        
        with open(instance_file) as f:
            self.N = int(next(f))
            self.profit = np.empty(self.N, int)
            self.weight = np.empty(self.N, int)
            for i, line in enumerate(f):
                if i == self.N:
                    break
                j, self.profit[i], self.weight[i] = [int(x) for x in line.split()]
            self.capacity = int(line)

        # Calls the initializer (constructor) of the class 'search_space'
        self.search_space = search_space(self.N)
        
        # Auxiliary info
        self.density = self.profit.astype(float)/self.weight
        ix = np.argsort(-self.density)
        cumweight = self.weight[ix].cumsum()
        # Lazy upper bound (feasible, minimization)
        k = (cumweight <= self.capacity).sum()
        ub = -self.profit[ix[:k]].sum()
        # Fractional knapsack lower bound (infeasible, minimization)
        self.ref = ub - self.density[ix[k]] * (self.capacity - cumweight[k-1])        
        data = np.zeros(self.N, bool)
        data[ix[:k]] = True
        self.heuristicSolution = data


# -----------------------------------------------------------------------------      
class KpBinarySolution(Solution):
    '''
    Class representing complete or incomplete solutions. An initial solution do
    not possesses any component, therefore, it is an incomplete solution.
    '''
    def __init__(self, problem):
        # The number of available components to compose a solution
        self.problem = problem        
        # It is better to be a list since components must be removed, inserted.
        self.unused = problem.search_space.components.tolist()
        self.used = []
        self.components = np.copy(problem.search_space.components)
        self.data = np.zeros(problem.search_space.dimension, dtype='int32')
        
        # Shuffle the indices of the components
        subset = np.copy(problem.search_space.components)
        np.random.shuffle(subset)
        # Adds a random number of components to the solution
        for i in subset[:random.randrange(problem.search_space.dimension)]:
            self.addComponent(i)
                    
    def __str__(self):
        return np.array_str(self.data) + ":: " + str(self.evaluate())
        
        
    def addComponent(self, c):
        self.unused.remove(c)
        self.used.append(c)
        self.data[c] = 1
    
    def delComponent(self, c):
        self.used.remove(c)
        self.unused.append(c)
        self.data[c] = 0
        
    def differenceTo(self, y):
        diffUsed = set(y.used) - set(self.used)
        diffUnused = set(y.unused) - set(self.unused)
        return (diffUsed, diffUnused)
    
    def isActive(self, c):
        return True if self.data[c] == 1 else False
        
    def clone(self):
        newsol = KpBinarySolution(self.problem)
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
        p = np.sum(self.data * self.problem.profit)
        w = np.sum(self.data * self.problem.weight) - self.problem.capacity
        obj = np.where(w <= 0, -p, w)
        return obj
