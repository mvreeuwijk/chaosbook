"""Chaos-game fractals and box-counting dimension."""

import numpy as np


def chaos_game(n=10000, seed=1):
    """Play the chaos game whose attractor is the Sierpinski gasket.

    Returns the point arrays (X, Y), each of length n + 1.
    """
    rng = np.random.default_rng(seed=seed)
    X = np.zeros(n + 1)
    Y = np.zeros(n + 1)
    X[0], Y[0] = 1, 0
    for k in range(n):
        dice = rng.integers(3)
        if dice == 0:
            X[k + 1] = 0.5 * X[k]
            Y[k + 1] = 0.5 * Y[k]
        elif dice == 1:
            X[k + 1] = 0.5 * X[k] + 0.25
            Y[k + 1] = 0.5 * Y[k] + 0.5
        else:
            X[k + 1] = 0.5 * X[k] + 0.5
            Y[k + 1] = 0.5 * Y[k]
    return X, Y


def box_dimension(X, Y, pmax=20):
    """Estimate the box-counting dimension of the point set (X, Y).

    Covers the points with square boxes whose size shrinks from the
    extent of the data down to 1/100th of it in pmax logarithmic steps,
    counts the occupied boxes at every size, and fits a straight line to
    log(count) against log(size). Returns (dimension, boxsize, boxcount),
    where dimension is minus the fitted slope.
    """
    xmin, ymin = X.min(), Y.min()
    lmax = max(X.max() - xmin, Y.max() - ymin)
    lmin = lmax / 100
    b = np.exp(np.log(lmax / lmin) / pmax)

    boxsize = np.zeros(pmax + 1)
    boxcount = np.zeros(pmax + 1)
    for p in range(pmax + 1):
        boxsize[p] = lmin * b**p
        gridsize = int(lmax / boxsize[p]) + 1
        grid = np.zeros((gridsize, gridsize))
        for x, y in zip(X, Y):
            i = int((x - xmin) / boxsize[p])
            j = int((y - ymin) / boxsize[p])
            grid[i, j] = 1
        boxcount[p] = grid.sum()
    slope, _ = np.polyfit(np.log(boxsize), np.log(boxcount), 1)
    return -slope, boxsize, boxcount
