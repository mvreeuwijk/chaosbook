"""Planar example flows of the chapter 'Two-dimensional continuous systems'.

All have the ``solve_ivp`` signature ``f(t, state, **params)``, with
parameter names following the book.
"""

import numpy as np


def lotka_volterra(t, state, alpha=0.75):
    """Scaled Lotka-Volterra predator-prey: x' = x - x y, y' = x y - alpha y."""
    x, y = state
    return [x - x * y, x * y - alpha * y]


def lotka_volterra_invariant(x, y, alpha=0.75):
    """Constant of motion H = exp(x + y) / (x**alpha * y) of the system above."""
    return np.exp(x + y) / (x**alpha * y)


def lotka_volterra_allee(t, state, alpha=0.5, beta=3.0 / 16.0):
    """Predator-prey with an Allee effect: x' = x^2/(x+beta) - x y, y' = x y - alpha y^2."""
    x, y = state
    return [x * x / (x + beta) - x * y, x * y - alpha * y * y]


def vanderpol(t, state, mu=1.0):
    """Van der Pol oscillator as a first-order system: x' = y, y' = -x + mu (1 - x^2) y."""
    x, y = state
    return [y, -x + mu * (1 - x * x) * y]


def double_well(t, state):
    """Conservative double-well oscillator x' = y, y' = x - x^3."""
    x, y = state
    return [y, x - x**3]


def hopf(t, state, mu=0.1):
    """Hopf normal form: x' = -y - x(-mu + r^2), y' = x - y(-mu + r^2)."""
    x, y = state
    s = -mu + x * x + y * y
    return [-y - x * s, x - y * s]
