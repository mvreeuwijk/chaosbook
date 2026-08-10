import numpy as np

from chaosbook import logistic


def test_logistic_fixed_points():
    r = 2.5
    assert logistic(0, r) == 0
    xstar = 1 - 1 / r
    assert np.isclose(logistic(xstar, r), xstar)


def test_logistic_works_on_arrays():
    x = np.array([0.0, 0.5, 1.0])
    assert np.allclose(logistic(x, 4.0), [0.0, 1.0, 0.0])
