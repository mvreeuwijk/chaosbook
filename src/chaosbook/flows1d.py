"""Tools for one-dimensional flows  dx/dt = f(x; parameters).

All functions accept any user-supplied right-hand side ``f(x, **params)``
that is written with numpy operations (so that it can be evaluated on an
array of x values).  Nothing here assumes a particular system.
"""

import numpy as np
from scipy.integrate import solve_ivp


def fixed_points(f, xmin, xmax, n=2001, **params):
    """All fixed points of dx/dt = f(x, **params) in [xmin, xmax].

    Scans f on a grid of n points for sign changes and refines every
    bracket by bisection (grid points where f is exactly 0 are kept as
    well).  Returns a sorted array; it is empty when there is no fixed
    point.  A double root (tangency without sign change, as at a
    saddle-node) can be missed unless the grid happens to resolve it.
    """
    x = np.linspace(xmin, xmax, n)
    y = np.asarray(f(x, **params), dtype=float)
    roots = list(x[y == 0])
    idx = np.nonzero(y[:-1] * y[1:] < 0)[0]
    if idx.size:
        a, b = x[idx], x[idx + 1]
        fa = y[idx]
        for _ in range(60):
            c = 0.5 * (a + b)
            fc = np.asarray(f(c, **params), dtype=float)
            left = fa * fc <= 0
            b = np.where(left, c, b)
            a = np.where(left, a, c)
            fa = np.where(left, fa, fc)
        roots.extend(0.5 * (a + b))
    return np.unique(np.round(np.array(roots, dtype=float), 12))


def stability(f, xstar, dfdx=None, h=1e-6, **params):
    """sigma = f'(x*) at the fixed point(s) xstar.

    Uses the analytic derivative ``dfdx(x, **params)`` when given and a
    central difference of f otherwise.  sigma < 0 means stable, sigma > 0
    unstable (see :func:`classify`).
    """
    xstar = np.asarray(xstar, dtype=float)
    if dfdx is not None:
        return np.asarray(dfdx(xstar, **params), dtype=float)
    return (np.asarray(f(xstar + h, **params), dtype=float)
            - np.asarray(f(xstar - h, **params), dtype=float)) / (2 * h)


def classify(sigma, tol=1e-6):
    """Label each sigma = f'(x*) as 'stable', 'unstable' or 'marginal'."""
    return ["stable" if s < -tol else "unstable" if s > tol else "marginal"
            for s in np.atleast_1d(sigma)]


def fixed_point_branches(f, pname, pmin, pmax, xmin, xmax, shape=(600, 600),
                         dfdx=None, **params):
    """Fixed-point branches x*(p) of f(x, p=..., **params), coloured by stability.

    Draws the zero level set of f over the (p, x) rectangle (so folds are
    followed correctly, as with a Maple ``implicitplot``) and cuts every
    curve wherever f'(x*) changes sign.  Returns a list of
    ``(p, x, stable)`` tuples: two arrays and a bool (True = stable).
    Choose a grid with no node exactly on a symmetry line such as x = 0.
    """
    from contourpy import contour_generator

    P = np.linspace(pmin, pmax, shape[0])
    X = np.linspace(xmin, xmax, shape[1])
    PP, XX = np.meshgrid(P, X, indexing="xy")
    Z = np.asarray(f(XX, **{pname: PP}, **params), dtype=float)
    segs = []
    for line in contour_generator(P, X, Z).lines(0.0):
        p, x = line[:, 0], line[:, 1]
        sig = stability(f, x, dfdx=dfdx, **{pname: p}, **params)
        st = sig < 0
        cut = np.nonzero(st[1:] != st[:-1])[0] + 1
        for lo, hi in zip(np.r_[0, cut], np.r_[cut, len(p)]):
            hi_ = min(hi + 1, len(p))     # overlap one point: no visible gap
            if hi_ - lo >= 2:
                segs.append((p[lo:hi_], x[lo:hi_], bool(st[lo])))
    return segs


def continuation_sweep(f, pname, values, x0, tinf=100.0, **params):
    """Quasi-static sweep of a parameter, integrating to the long-time state.

    For every p in ``values`` integrate dx/dt = f(x, p) from the previous
    long-time state over a time ``tinf`` (the first step starts at x0) and
    record the final x.  Run it forwards and backwards over ``values`` to
    see hysteresis and the jumps (hard bifurcations).
    """
    out = np.empty(len(values))
    x = float(x0)
    for i, p in enumerate(values):
        kw = {**params, pname: p}
        sol = solve_ivp(lambda t, y: f(y, **kw), [0, tinf], [x],
                        rtol=1e-8, atol=1e-10)
        x = float(sol.y[0, -1])
        out[i] = x
    return out
