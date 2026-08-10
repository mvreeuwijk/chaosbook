"""Iterated maps: x_{n+1} = f(x_n, parameters).

Every map takes the current state as its first argument and its
parameters after it, so it can be passed directly to orbit() and the
plotting helpers.
"""


def logistic(x, r):
    """The logistic map x_{n+1} = r x (1 - x)."""
    return r * x * (1 - x)
