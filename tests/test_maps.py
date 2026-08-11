import numpy as np

from chaosbook import logistic, shift, sine, tent


def test_logistic_fixed_points():
    r = 2.5
    assert logistic(0, r) == 0
    xstar = 1 - 1 / r
    assert np.isclose(logistic(xstar, r), xstar)


def test_logistic_works_on_arrays():
    x = np.array([0.0, 0.5, 1.0])
    assert np.allclose(logistic(x, 4.0), [0.0, 1.0, 0.0])


def test_sine_tent_shift_definitions():
    assert np.isclose(sine(0.5, 0.5), 0.5)
    assert tent(0.25) == 0.5
    assert tent(0.5) == 1.0
    assert np.isclose(shift(0.75), 0.5)
    assert np.isclose(shift(0.3), 0.6)
