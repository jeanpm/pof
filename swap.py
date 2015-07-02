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
        # Used as state for random path enumeration
        self.diffUsed = None 
        self.diffUnused = None        
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
        if x.unused and x.used : # if unused is not empty
            y = x.clone()        
            # Choses one random component from the used and removes
            comp = y.used[random.randrange(len(y.used))]
            y.delComponent(comp)        
    
            # Chooses one random component from the unused and inserts
            comp = y.unused[random.randrange(len(y.unused))]
            y.addComponent(comp)
        # Returns None if not possible
        return y
        
    '''
    Returns a random neighbor of x which is one step closer to y.
    '''
    def randomNeighborTowards(self, x, z):
        # There is no path between solutions with different number of components
        # in this type of neighborhood.
        if len(x.used) != len(z.used):
            return None
            
        y = x.clone()
        # Set diff as np.array containing the indexes in which x != y
        self.diffUsed = set(z.used) - set(x.used)
        self.diffUnused = set(z.unused) - set(x.unused)

        if not self.diffUsed and not self.diffUnused:
            return y
        
        comp = self.diffUsed.pop()
        y.addComponent(comp)        
        comp = self.diffUnused.pop()
        y.delComponent(comp)       
        
        # Returns the next solution (y) in a path between x and z.
        return y