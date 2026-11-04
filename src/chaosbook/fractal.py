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


def _as_points(X, Y):
    """Stack coordinate arrays into an (N, d) array of points."""
    X = np.asarray(X, dtype=float).ravel()
    if Y is None:
        return X[:, None]
    Y = np.asarray(Y, dtype=float).ravel()
    return np.column_stack([X, Y])


def correlation_dimension(X, Y=None, rmin=None, rmax=None, nr=20,
                          max_points=3000, seed=1):
    """Estimate the correlation dimension D2 of the point set (X, Y).

    Computes the correlation integral C(r), the fraction of pairs of
    points closer than r, at nr logarithmically spaced radii between
    rmin and rmax (default: 1/100 and 1/10 of the extent of the data),
    and fits a straight line to log C against log r. Y may be omitted
    for a one-dimensional set. For more than max_points points a random
    subset (seeded) is used to keep the O(N^2) pair count affordable.
    Returns (dimension, r, C), where dimension is the fitted slope.
    """
    P = _as_points(X, Y)
    if len(P) > max_points:
        rng = np.random.default_rng(seed=seed)
        P = P[rng.choice(len(P), size=max_points, replace=False)]
    extent = np.max(P.max(axis=0) - P.min(axis=0))
    rmin = extent / 100 if rmin is None else rmin
    rmax = extent / 10 if rmax is None else rmax
    r = np.logspace(np.log10(rmin), np.log10(rmax), nr)

    counts = np.zeros(nr)
    for i in range(1, len(P)):  # every pair i > j exactly once
        d = np.sqrt(((P[:i] - P[i]) ** 2).sum(axis=1))
        counts += np.searchsorted(np.sort(d), r, side="right")
    C = counts / (len(P) * (len(P) - 1) / 2)
    slope, _ = np.polyfit(np.log(r), np.log(C), 1)
    return slope, r, C


def generalized_dimensions(X, Y=None, qs=range(-10, 11), pmin=2, pmax=9,
                           weights=None, origin=None, size=None):
    """Generalized (Renyi) dimensions D_q from box-counting probabilities.

    Covers the point set (X, Y) (Y may be omitted for a 1-D set) with square
    boxes of size eps = size / 2**p for p = pmin..pmax, and accumulates the
    probability p_i of every occupied box (each point has weight 1/N, or
    pass weights for a measure given as a list of masses). For each q the
    slope of log sum_i p_i**q against log eps, divided by q - 1, gives D_q;
    q = 1 uses the information dimension, slope of sum_i p_i log p_i.
    The root box has lower corner origin and edge length size (default: the
    bounding box of the data). Returns the array of D_q, one per q.
    """
    P = _as_points(X, Y)
    w = np.full(len(P), 1.0 / len(P)) if weights is None else np.asarray(weights, float)
    w = w / w.sum()
    origin = P.min(axis=0) if origin is None else np.atleast_1d(np.asarray(origin, float))
    size = np.max(P.max(axis=0) - P.min(axis=0)) if size is None else size

    ps = np.arange(pmin, pmax + 1)
    boxes = []  # one probability vector per box size
    for p in ps:
        n = 2 ** p
        idx = np.minimum(np.floor((P - origin) / (size / n)).astype(int), n - 1)
        _, inv = np.unique(idx, axis=0, return_inverse=True)
        boxes.append(np.bincount(inv.ravel(), weights=w))
    logeps = np.log(size / 2.0 ** ps)

    Dq = []
    for q in qs:
        if q == 1:
            y = [np.sum(pi[pi > 0] * np.log(pi[pi > 0])) for pi in boxes]
            denom = 1.0
        else:
            y = [np.log(np.sum(pi[pi > 0] ** q)) for pi in boxes]
            denom = q - 1.0
        slope, _ = np.polyfit(logeps, y, 1)
        Dq.append(slope / denom)
    return np.array(Dq)
