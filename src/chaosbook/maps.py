"""Iterated maps: x_{n+1} = f(x_n, parameters).

Every map takes the current state as its first argument and its
parameters after it, so it can be passed directly to orbit() and the
plotting helpers.
"""

import numpy as np


def logistic(x, r):
    """The logistic map x_{n+1} = r x (1 - x)."""
    return r * x * (1 - x)


def sine(x, r):
    """The sine map x_{n+1} = r sin(pi x)."""
    return r * np.sin(np.pi * x)


def tent(x):
    """The tent map x_{n+1} = 1 - 2 |x - 1/2|."""
    return 1 - 2 * np.abs(x - 0.5)


def shift(x):
    """The shift map x_{n+1} = 2 x mod 1."""
    return (2 * x) % 1.0
