"""Iterating maps into orbits."""

import numpy as np


def orbit(f, x0, n, **params):
    """Iterate the map x_{k+1} = f(x_k, **params) starting from x0.

    x0 may be a number (one-dimensional map) or a sequence such as
    (x0, y0) for a map of higher order; f then takes and returns an
    array of the same length.

    Returns the numpy array [x_0, x_1, ..., x_n]: of length n + 1 for a
    one-dimensional map, of shape (n + 1, d) for a d-dimensional map.
    """
    x0 = np.asarray(x0, dtype=float)
    X = np.zeros((n + 1,) + x0.shape)
    X[0] = x0
    for k in range(n):
        X[k + 1] = f(X[k], **params)
    return X


def winding_number(f, x0, n=1000, **params):
    """The winding number W = (f^n(x0) - x0) / n of a circle map.

    f must be the *lift* of the map (no mod 1 applied), so that the
    accumulated rotation is not lost.
    """
    x = float(x0)
    for _ in range(n):
        x = f(x, **params)
    return (x - x0) / n
