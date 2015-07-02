# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 16:05:46 2015

@author: jean
"""

import random
from pof import Neighborhood

    
# -----------------------------------------------------------------------------        
class BitflipNeighborhood(Neighborhood): 
    '''
    Provides movements for a complete enumeration of the neighborhood.
    '''
    def __init__(self, search_space):
        # Used as state for complete enumeration
        self.index = 0
        # Used as state for random path enumeration
        self.diffUsed = None 
        self.diffUnused = None        
        # Call superclass initializer
        super(BitflipNeighborhood, self).__init__(search_space)
    
    '''
    Complete enumeration of the neighborhood.
    '''
    def nextNeighbor(self, x):
        if self.index == self.search_space.dimension:
            return None
            
        y = x.clone()        
        
        if y.isActive(self.index):
            # If it is currently being used, delete it.
            y.delComponent(self.index)
        else:
            # If it is not currently being used, add it.
            y.addComponent(self.index)
        # Updates the next component
        self.index += 1
        
        # Returns the next neighbor
        return y
        
    '''
    Randomized enumeration (sampling) of the neighborhood.
    '''
    def randomNeighbor(self, x):
        y = x.clone()
        if y.unused : # if unused is not empty
            if y.used : # if used is not empty
                if random.choice([True, False]):
                    # Chooses one random component from the unused to be added
                    comp = y.unused[random.randrange(len(y.unused))]
                    y.addComponent(comp)
                else:
                    # Choses one random component from the used to be removed
                    comp = y.used[random.randrange(len(y.used))]
                    y.delComponent(comp)
            else:
                # Choses one random component from the used to be removed
                comp = y.unused[random.randrange(len(y.unused))]
                y.addComponent(comp)
        else:
            # Choses one random component from the used to be removed
            comp = y.used[random.randrange(len(y.used))]
            y.delComponent(comp)
            
        # Returns a randomly created bitflip move.
        return y
        
    '''
    Returns a random neighbor of x which is one step closer to y.
    '''
    def randomNeighborTowards(self, x, z):
        y = x.clone()        
        # Set diff as np.array containing the indexes in which x != y
        self.diffUsed, self.diffUnused = x.differenceTo(z)
                
        if self.diffUsed:
            comp = self.diffUsed.pop()
            y.addComponent(comp)
        elif self.diffUnused:
            comp = self.diffUnused.pop()
            y.delComponent(comp)
        else:
            self.diffUsed = None 
            self.diffUnused = None
        
        # Returns the next solution (y) in a path between x and z.
        return y