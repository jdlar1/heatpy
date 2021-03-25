import numpy as np

from heatpy.io import create_array

def test_create_array():
    a = create_array()
    assert isinstance(a, np.ndarray)