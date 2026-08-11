"""Lyapunov exponents of one-dimensional maps."""

import numpy as np

from .iterate import orbit


def lyapunov(f, dfdx, x0, n=1000, nskip=100, **params):
    """Estimate the Lyapunov exponent of x_{k+1} = f(x_k, **params).

    Iterates the map from x0, discards the first nskip points as
    transient, and returns the mean of log|f'(x_k)| over the next n
    points. dfdx is the derivative of the map, with the same signature
    as f.
    """
    X = orbit(f, x0, nskip + n, **params)
    with np.errstate(divide="ignore"):
        return np.mean(np.log(np.abs(dfdx(X[nskip:-1], **params))))


def lyapunov_sweep(f, dfdx, rmin, rmax, nr=500, n=1000, x0=0.57, nskip=100):
    """The Lyapunov exponent as a function of the parameter r.

    Assumes the map's varying parameter is named r, i.e. f(x, r).
    Returns the arrays (rs, lams).
    """
    rs = np.linspace(rmin, rmax, nr + 1)
    lams = np.array([lyapunov(f, dfdx, x0, n=n, nskip=nskip, r=r)
                     for r in rs])
    return rs, lams
