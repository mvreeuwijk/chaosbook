import numpy as np

from chaosbook import logistic, orbit


def test_orbit_length_and_start():
    X = orbit(logistic, 0.1, 50, r=2.5)
    assert len(X) == 51
    assert X[0] == 0.1


def test_orbit_converges_to_fixed_point():
    X = orbit(logistic, 0.1, 200, r=2.5)
    assert np.isclose(X[-1], 1 - 1 / 2.5)
