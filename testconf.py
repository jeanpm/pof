# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 15:27:36 2015

@author: jean
"""

import random
import numpy as np


random.seed(0)
np.random.seed(0)


instance_file = "../src/testset/test.100.1.1"

t = 0.15
N = 20
NEXP = 1
POPSIZE = 30
nevals = 0
MAXEVALS = 9000

assert MAXEVALS % POPSIZE == 0

#execfile("test_hc.py")
#execfile("test_ga.py")




