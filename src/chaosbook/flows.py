"""Right-hand sides of the book's flows, in solve_ivp form f(t, state)."""

import numpy as np


def lorenz(t, xyz, sigma=10.0, r=28.0, b=8.0 / 3.0):
    """The Lorenz equations."""
    x, y, z = xyz
    return [sigma * (y - x), -x * z + r * x - y, x * y - b * z]


def threebody(t, state, G=6.67e-11, m1=5.97e24, m2=1.4925e24, R=3.84e8):
    """The restricted three-body problem in the inertial frame.

    A massless satellite at (x, y) with velocity (u, v) moves in the
    gravitational field of two primaries (masses m1 and m2, separation R)
    that circle their common centre of mass at the Kepler frequency
    omega = sqrt(G (m1 + m2) / R^3). state = (x, y, u, v).
    """
    omega = np.sqrt(G * (m1 + m2) / R**3)
    x, y, u, v = state
    x1 = -m2 * R / (m1 + m2) * np.cos(omega * t)
    y1 = -m2 * R / (m1 + m2) * np.sin(omega * t)
    x2 = m1 * R / (m1 + m2) * np.cos(omega * t)
    y2 = m1 * R / (m1 + m2) * np.sin(omega * t)
    d1 = np.sqrt((x1 - x) ** 2 + (y1 - y) ** 2)
    d2 = np.sqrt((x2 - x) ** 2 + (y2 - y) ** 2)
    return [u,
            v,
            G * m1 * (x1 - x) / d1**3 + G * m2 * (x2 - x) / d2**3,
            G * m1 * (y1 - y) / d1**3 + G * m2 * (y2 - y) / d2**3]


def corotating(x, y, t, omega):
    """Rotate inertial-frame coordinates into the frame co-rotating at omega."""
    c, s = np.cos(omega * t), np.sin(omega * t)
    return c * x + s * y, -s * x + c * y
