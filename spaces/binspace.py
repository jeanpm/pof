# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 12:48:47 2015

@author: jean
"""

import numpy as np

# -----------------------------------------------------------------------------
class BinarySpace(object):
    '''
    A search space containing complete and incomplete {0,1,-1}^n solutions.
    '''
    def __init__(self, n):    
        self.dimension = n
        # The components in this case are the indices of variables
        self.components = np.array([idx for idx in xrange(n)])      



