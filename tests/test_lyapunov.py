import numpy as np

from chaosbook import logistic, lyapunov, lyapunov_sweep


def dlogistic(x, r):
    return r * (1 - 2 * x)


def test_logistic_r4_has_lyapunov_log2():
    lam = lyapunov(logistic, dlogistic, 0.3, n=5000, r=4.0)
    assert abs(lam - np.log(2)) < 0.05


def test_stable_fixed_point_has_negative_lyapunov():
    # at r=2.5 the orbit sits on x*=1-1/r where sigma = 2-r = -0.5
    lam = lyapunov(logistic, dlogistic, 0.3, n=2000, r=2.5)
    assert np.isclose(lam, np.log(0.5), atol=1e-6)


def test_sweep_is_negative_before_first_bifurcation():
    rs, lams = lyapunov_sweep(logistic, dlogistic, 2.5, 3.5, nr=100)
    assert lams[rs < 2.95].max() < 0


def test_tent_and_shift_have_lyapunov_log2():
    from chaosbook import shift, tent

    lam_tent = lyapunov(tent, lambda x: np.where(x < 0.5, 2.0, -2.0),
                        1 / np.pi, n=200, nskip=0)
    lam_shift = lyapunov(shift, lambda x: 2.0 + 0 * x,
                         1 / np.pi, n=200, nskip=0)
    assert np.isclose(lam_tent, np.log(2))
    assert np.isclose(lam_shift, np.log(2))


def test_derivative_free_and_pname():
    lam = lyapunov(logistic, None, 0.3, n=2000, r=2.5)
    assert np.isclose(lam, np.log(0.5), atol=1e-4)
    from chaosbook import lyapunov_spectrum, henon
    f = lambda x, a: a * x * (1 - x)
    rs, lams = lyapunov_sweep(f, None, 2.5, 2.9, nr=4, pname="a")
    assert lams.max() < 0
    hen = lambda X: np.array([1 - 1.4 * X[0]**2 + X[1], 0.3 * X[0]])
    jac = lambda X: np.array([[-2.8 * X[0], 1.0], [0.3, 0.0]])
    a = lyapunov_spectrum(hen, jac, [0.1, 0.1], n=3000)
    b = lyapunov_spectrum(hen, None, [0.1, 0.1], n=3000)
    assert np.allclose(a, b, atol=1e-3)
