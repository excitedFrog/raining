#Python 3.6.1

import numpy as np

class Universe(Object):
    def __init__(self):
        super().__init__()
        self._size = tuple()  # Universe can be 2-dimensional or 3-dimensional
        self.space = None
        self.space1 = None

    @property
    def size(self):
        return self._size

    @shape.setter
    def size(self, a_tuple):
        self._size = a_tuple
        self.space = np.zeros(a_tuple)
        self.space1 = np.ones(a_tuple)
