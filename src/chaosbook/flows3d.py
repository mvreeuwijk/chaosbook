"""Right-hand sides of the flows of 'Chaos in continuous systems'."""

import numpy as np
from scipy.optimize import brentq


def rossler(t, xyz, a=0.432, b=2.0, c=4.0):
    """The Rossler system  x' = -y - z,  y' = x + a y,  z' = b + z (x - c).

    Defaults are the book's chaotic case a = 0.432, b = 2, c = 4.
    """
    x, y, z = xyz
    return [-y - z, x + a * y, b + z * (x - c)]


def forced_double_well(t, xyz, f=0.15, A=0.3, omega=1.0):
    """Damped, forced double well as an autonomous 3-D flow.

    x' = y,  y' = x - x^3 - f y + A cos z,  z' = omega  (z = omega t).
    """
    x, y, z = xyz
    return [y, x - x**3 - f * y + A * np.cos(z), omega]


def circle_limit_cycle(t, xy, a=0.2):
    """x' = -y + a x (1 - x^2 - y^2),  y' = x + a y (1 - x^2 - y^2).

    Stable limit cycle r = 1; in polar form r' = a r (1 - r^2), theta' = 1.
    """
    x, y = xy
    s = 1 - x**2 - y**2
    return [-y + a * x * s, x + a * y * s]


def rotating_threebody(t, state, mu=0.2):
    """Restricted three-body problem, dimensionless, in the co-rotating frame.

    state = (x, y, u, v); the primaries of masses 1 - mu and mu sit at
    (-mu, 0) and (1 - mu, 0). u' = 2v - dV/dx, v' = -2u - dV/dy with the
    effective potential of :func:`threebody_potential`.
    """
    x, y, u, v = state
    mu1, mu2 = 1 - mu, mu
    s1 = np.hypot(x + mu2, y)
    s2 = np.hypot(x - mu1, y)
    return [u, v,
            2 * v + x - mu1 * (x + mu2) / s1**3 - mu2 * (x - mu1) / s2**3,
            -2 * u + y - mu1 * y / s1**3 - mu2 * y / s2**3]


def threebody_potential(x, y, mu=0.2):
    """V = -mu1/d1 - mu2/d2 - (x^2 + y^2)/2 - mu1 mu2/2."""
    mu1, mu2 = 1 - mu, mu
    return (-mu1 / np.hypot(x + mu2, y) - mu2 / np.hypot(x - mu1, y)
            - (x**2 + y**2) / 2 - mu1 * mu2 / 2)


def lagrange_points(mu=0.2):
    """Collinear Lagrange points on the x axis, in the book's numbering.

    Returns three x positions (x_L1, x_L2, x_L3): beyond the light body
    (x > 1 - mu), between the bodies, and beyond the heavy body (x < -mu).
    """
    dV = lambda x: _dVdx(x, mu)
    xl1 = brentq(dV, 1 - mu + 1e-3, 5.0)
    xl2 = brentq(dV, -mu + 1e-3, 1 - mu - 1e-3)
    xl3 = brentq(dV, -5.0, -mu - 1e-3)
    return xl1, xl2, xl3


def _dVdx(x, mu):
    mu1, mu2 = 1 - mu, mu
    return (mu1 * (x + mu2) / np.abs(x + mu2) ** 3
            + mu2 * (x - mu1) / np.abs(x - mu1) ** 3 - x)
