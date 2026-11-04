import numpy as np

import chaosbook as cb


def henon_jac(x, a=1.4, b=0.3):
    return np.array([[-2 * a * x[0], 1.0], [b, 0.0]])


def test_orbit_of_a_2d_map_has_shape_n_plus_1_by_2():
    X = cb.orbit(cb.henon, (0.1, 0.3), 100)
    assert X.shape == (101, 2)
    assert np.allclose(X[0], [0.1, 0.3])


def test_orbit_still_returns_1d_array_for_scalar_maps():
    assert cb.orbit(cb.logistic, 0.1, 10, r=2.5).shape == (11,)


def test_henon_fixed_point():
    a, b = 1.4, 0.3
    xs = (-(1 - b) + np.sqrt((1 - b) ** 2 + 4 * a)) / (2 * a)
    assert np.allclose(cb.henon(np.array([xs, b * xs])), [xs, b * xs])


def test_henon_lyapunov_spectrum():
    lam = cb.lyapunov_spectrum(cb.henon, henon_jac, (0.1, 0.3), n=20000)
    assert abs(lam[0] - 0.42) < 0.02            # positive: chaos
    assert np.isclose(lam.sum(), np.log(0.3), atol=1e-6)  # area contraction b


def test_standard_map_preserves_area():
    def jac(x, K):
        c = K * np.cos(2 * np.pi * x[0])
        return np.array([[1 + c, 1.0], [c, 1.0]])
    lam = cb.lyapunov_spectrum(cb.standard_map, jac, (0.1, 0.1), n=5000, K=2.0)
    assert abs(lam.sum()) < 1e-8
    assert lam[0] > 0


def test_circle_map_winding_number():
    assert np.isclose(cb.winding_number(cb.circle_map, 0.0, 500, Omega=0.3, K=0.0), 0.3)
    # inside the 1:2 Arnold tongue at K=1 the winding number locks to 1/2
    assert np.isclose(cb.winding_number(cb.circle_map, 0.0, 2000, Omega=0.5, K=1.0), 0.5,
                      atol=1e-3)


def test_duffing_map_definition():
    assert np.allclose(cb.duffing_map(np.array([1.0, 1.0]), a=2.52, b=0.1),
                       [1.0, -0.1 + 2.52 - 1.0])
