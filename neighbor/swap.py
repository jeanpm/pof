# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 16:10:24 2015

@author: jean
"""

import random
from pof import Neighborhood

    
# -----------------------------------------------------------------------------        
class SwapNeighborhood(Neighborhood): 
    '''
    Provides movements for a complete enumeration of the neighborhood.
    '''
    def __init__(self, search_space):
        # Used as state for complete enumeration
        self.indexA = 0
        self.indexB = 0
        self.prevx  = None
    
        # Call superclass initializer
        super(SwapNeighborhood, self).__init__(search_space)
    
    '''
    Complete enumeration of the neighborhood.
    '''
    def nextNeighbor(self, x):
        if not x.used : # x must have at least one component
            return None
            
        if self.prevx is None or self.prevx != x:
            self.indexA = 0
            self.indexB = 0            
            
        if self.indexB == len(x.unused):
            self.indexA += 1
            self.indexB = 0
        if self.indexA == len(x.used):
            return None        
        
        y = x.clone()        
        # Delete one component and add another (SWAP)
        y.delComponent(y.used[self.indexA])
        y.addComponent(y.unused[self.indexB])
        
        self.indexB += 1
        self.prevx = x
        
        # Returns the next neighbor
        return y
        
    '''
    Randomized enumeration (sampling) of the neighborhood.
    '''
    def randomNeighbor(self, x):
        y = None
        if x.unused and x.used : # if both are not empty
            y = x.clone()        
            # Choses one random component from the used and removes it
            comp = random.choice(y.used)
            y.delComponent(comp)    
            # Chooses one random component from the unused and inserts it
            comp = random.choice(y.unused)
            y.addComponent(comp)
        # Returns None if not possible
        return y
        
    '''
    Returns a random neighbor of x which is one step closer to y.     
    TODO: This might be more efficient if the difference is stored and modified 
    along the path, instead of computing it at every call.
    '''
    def randomNeighborTowards(self, x, z):
        # In swap neighborhoods, there is no path between solutions with a 
        # different number of components.
        assert len(x.used) == len(z.used)
            #raise Exception("x and z must have the same number of components")
            
        y = x.clone()
        # Components (used by z and unused by x), (unused by z and used by x).
        diffUsed, diffUnused = x.differenceTo(z)

        while diffUsed and diffUnused: # If both sets are non-empty
            comp = diffUsed.pop()
            y.addComponent(comp)        
            comp = diffUnused.pop()
            y.delComponent(comp)
            # Yields the next solution (y) in a path between x and z.
            yield y