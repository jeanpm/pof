# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 15:59:45 2015

@author: jean
"""


# -----------------------------------------------------------------------------
class Solution(object):

    '''
    '''
    def __init__(self, problem):
        self.problem = problem
    
    '''
    Add the component c to the current solution. Subclasses should provide
    efficient ways to perform this task.
    '''
    def addComponent(self, c):
        raise NotImplementedError()
    
    '''
    Remove the component c from the current solution. Subclasses should provide
    efficient ways to perform this task.
    '''    
    def delComponent(self, c):
        raise NotImplementedError()
        
    '''
    Determines if a component is currently being used or not.
    '''
    def isActive(self, c):
        raise NotImplementedError()
        
    '''
    Evaluate this solution according to some specific problem.
    '''
    def evaluate(self):
        raise NotImplementedError()


# -----------------------------------------------------------------------------
class Neighborhood(object):
    '''
    Indireclty defines the neighborhood structure through the use of abstract
    neighborhood enumeration strategies.
    '''
    def __init__(self, search_space):
        self.search_space  = search_space
    
    '''
    Complete enumeration of the neighborhood.
    '''
    def nextNeighbor(self, x):
        raise NotImplementedError()
        
    '''
    Randomized enumeration (sampling) of the neighborhood.
    '''
    def randomNeighbor(self, x):
        raise NotImplementedError()
        
    '''
    Returns a random neighbor of x which is one step closer to y.
    '''
    def randomNeighborTowards(self, x, y):
        raise NotImplementedError()
    
