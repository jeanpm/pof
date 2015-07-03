# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 16:05:46 2015

@author: jean
"""

import random
from pof import Neighborhood

    
# -----------------------------------------------------------------------------        
class AddOrRemoveNeighborhood(Neighborhood):       
    '''
    Complete enumeration of the neighborhood.
    '''
    def nextNeighbor(self, x):
        for index in xrange(self.search_space.dimension):
            y = x.clone()
            if y.isActive(self.index): # If it is active, remove it.
                y.delComponent(self.index)        
            else: # If it is not currently active, add it.
                y.addComponent(self.index)        
            self.index += 1  # The next component
            # Returns the current neighbor
            yield y
        
    '''
    Randomized enumeration (sampling) of the neighborhood.
    '''
    def randomNeighbor(self, x):
        y = x.clone()
        if y.unused : # if is not empty
            if y.used : # if is not empty
                # Add or remove a component with equal probability.
                if random.choice([True, False]):
                    # Chooses one random component from the unused to be added
                    comp = random.choice(y.unused) 
                    y.addComponent(comp)
                else:
                    # Choses one random component from the used to be removed
                    comp = random.choice(y.used)
                    y.delComponent(comp)
            else:
                # If y.used is empty, then:
                # Choses one random component to be removed
                comp = random.choice(y.unused) 
                y.addComponent(comp)
        else:
            # Choses one random component from the used to be removed
            comp = random.choice(y.used) 
            y.delComponent(comp)
            
        # Returns a randomly created bitflip move.
        return y
        
    '''
    Returns a random neighbor of x which is one step closer to y.
    '''
    def randomNeighborTowards(self, x, z):
        y = x.clone()        
        # Set diff as np.array containing the indexes in which x != y
        diffUsed, diffUnused = y.differenceTo(z)
        step = 0
        while diffUsed or diffUnused:
            if step % 2 == 0:
                if diffUsed: # if it is not empty
                    comp = diffUsed.pop()
                    y.addComponent(comp)
                elif diffUnused: # if it is not empty
                    comp = diffUnused.pop()
                    y.delComponent(comp)
            else:
                if diffUnused: # if it is not empty
                    comp = diffUnused.pop()
                    y.delComponent(comp)
                elif diffUsed: # if it is not empty
                    comp = diffUsed.pop()
                    y.addComponent(comp)
            # Yields the next solution (y) in a path between x and z.
            step += 1
            yield y