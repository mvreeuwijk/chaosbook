"""Iterating maps into orbits."""

import numpy as np


def orbit(f, x0, n, **params):
    """Iterate the map x_{k+1} = f(x_k, **params) starting from x0.

    Returns the numpy array [x_0, x_1, ..., x_n] of length n + 1.
    """
    X = np.zeros(n + 1)
    X[0] = x0
    for k in range(n):
        X[k + 1] = f(X[k], **params)
    return X
