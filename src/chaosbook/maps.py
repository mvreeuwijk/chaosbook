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


def henon(x, a=1.4, b=0.3):
    """The Henon map x_{n+1} = y_n + 1 - a x_n^2,  y_{n+1} = b x_n."""
    return np.array([x[1] + 1 - a * x[0] ** 2, b * x[0]])


def duffing_map(x, a=2.52, b=0.1):
    """The Duffing map x_{n+1} = y_n,  y_{n+1} = -b x_n + a y_n - y_n^3."""
    return np.array([x[1], -b * x[0] + a * x[1] - x[1] ** 3])


def circle_map(x, Omega, K=1.0):
    """The lift of the sine circle map x_{n+1} = x_n + Omega + K/(2 pi) sin(2 pi x_n).

    No mod 1 is applied, so winding numbers can be measured; take
    ``x % 1`` to place the orbit on the circle.
    """
    return x + Omega + K / (2 * np.pi) * np.sin(2 * np.pi * x)


def standard_map(x, K):
    """The standard map, both coordinates mod 1:

    y_{n+1} = y_n + K/(2 pi) sin(2 pi x_n),  x_{n+1} = x_n + y_{n+1}.
    """
    y = (x[1] + K / (2 * np.pi) * np.sin(2 * np.pi * x[0])) % 1.0
    return np.array([(x[0] + y) % 1.0, y])
