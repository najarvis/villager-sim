#! python3

__author__ = 'Nick Jarvis'

import numpy as np
import random

v = np.random.rand(5, 5)
u = np.full((5, 5), 3, dtype=np.dtype('d'))

print(v * u)
