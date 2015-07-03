# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 12:53:38 2015

@author: jean
"""

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