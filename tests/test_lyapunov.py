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
