import numpy as np

from chaosbook import lorenz, corotating, threebody
from scipy.integrate import solve_ivp


def test_origin_is_a_fixed_point():
    assert lorenz(0, [0, 0, 0]) == [0, 0, 0]


def test_nontrivial_fixed_point():
    r, b = 28.0, 8.0 / 3.0
    q = np.sqrt(b * (r - 1))
    assert np.allclose(lorenz(0, [q, q, r - 1]), [0, 0, 0], atol=1e-12)


def test_threebody_reduces_to_kepler_when_moon_is_massless():
    # With m2 = 0 the satellite follows a circular Kepler orbit around m1.
    G, m1 = 6.67e-11, 5.97e24
    r0 = 1.0e8
    vc = np.sqrt(G * m1 / r0)
    period = 2 * np.pi * r0 / vc
    sol = solve_ivp(threebody, [0, period], [r0, 0, 0, vc],
                    args=(G, m1, 0.0), rtol=1e-10, atol=1e-3,
                    t_eval=np.linspace(0, period, 200))
    radius = np.sqrt(sol.y[0] ** 2 + sol.y[1] ** 2)
    assert np.allclose(radius, r0, rtol=1e-3)


def test_corotating_makes_the_primaries_stationary():
    G, m1, R = 6.67e-11, 5.97e24, 3.84e8
    m2 = m1 / 4
    omega = np.sqrt(G * (m1 + m2) / R**3)
    t = np.linspace(0, 5e6, 100)
    x1 = -m2 * R / (m1 + m2) * np.cos(omega * t)
    y1 = -m2 * R / (m1 + m2) * np.sin(omega * t)
    xr, yr = corotating(x1, y1, t, omega)
    assert np.allclose(xr, -m2 * R / (m1 + m2))
    assert np.allclose(yr, 0, atol=1e-6 * R)
