"""Cobweb diagrams for one-dimensional maps."""

import matplotlib.pyplot as plt
import numpy as np

from .iterate import orbit


def cobweb(f, x0, n, xmin=0.0, xmax=1.0, ax=None, **params):
    """Draw a cobweb diagram of x_{k+1} = f(x_k, **params) from x0.

    Plots the map, the diagonal and the cobweb path on ax (the current
    axes if not given) and returns the axes.
    """
    if ax is None:
        ax = plt.gca()
    X = orbit(f, x0, n, **params)
    px = [X[0]]
    py = [0]
    for k in range(n):
        px += [X[k], X[k]]
        py += [X[k], X[k + 1]]
    xs = np.linspace(xmin, xmax, 200)
    ax.plot(xs, f(xs, **params), "k")
    ax.plot(xs, xs, "b")
    ax.plot(px, py, "r")
    ax.set_xlabel("$x_n$")
    ax.set_ylabel("$x_{n+1}$")
    return ax
