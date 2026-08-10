"""Bifurcation diagrams for one-dimensional maps."""

import matplotlib.pyplot as plt
import numpy as np

from .iterate import orbit


def bifurcation_diagram(f, rmin, rmax, nr=200, n=500, x0=0.57, ax=None):
    """Compute and plot the bifurcation diagram of x_{k+1} = f(x_k, r).

    For nr + 1 parameter values r between rmin and rmax the map is
    iterated n times from x0, and the second half of every orbit (the
    part that has converged onto the attractor) is plotted against r.
    Returns the arrays (rs, xs) that make up the diagram.

    Assumes the map's varying parameter is named r, i.e. f(x, r).
    """
    nmin = n // 2
    rs = []
    xs = []
    for i in range(nr + 1):
        if nr == 0:
            r = rmin
        else:
            r = rmin + (rmax - rmin) * i / nr
        X = orbit(f, x0, n, r=r)
        for x in X[nmin:]:
            rs.append(r)
            xs.append(x)
    rs = np.array(rs)
    xs = np.array(xs)
    if ax is None:
        ax = plt.gca()
    ax.plot(rs, xs, ",")
    ax.set_xlabel("r")
    ax.set_ylabel("x(r)")
    return rs, xs
