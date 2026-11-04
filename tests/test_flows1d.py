import numpy as np

import chaosbook as cb


def cubic(x, r=1.0):
    return r * x - x**3


def ferro(x, T=0.5, m=0.0):
    return -x + np.tanh((x + m) / T)


def test_fixed_points_of_cubic_normal_form():
    xs = cb.fixed_points(cubic, -2, 2, r=1.0)
    assert np.allclose(xs, [-1, 0, 1], atol=1e-9)


def test_fixed_points_empty_when_none_exist():
    assert len(cb.fixed_points(lambda x: 1 + x**2, -3, 3)) == 0


def test_fixed_points_forwards_parameters():
    assert len(cb.fixed_points(cubic, -2, 2, r=-1.0)) == 1
    assert len(cb.fixed_points(cubic, -2, 2, r=2.0)) == 3


def test_stability_sign_numerical_and_analytic_agree():
    xs = cb.fixed_points(cubic, -2, 2, r=1.0)
    num = cb.stability(cubic, xs, r=1.0)
    ana = cb.stability(cubic, xs, dfdx=lambda x, r: r - 3 * x**2, r=1.0)
    assert np.allclose(num, ana, atol=1e-5)
    assert cb.classify(ana) == ["stable", "unstable", "stable"]


def test_ferromagnet_nonzero_fixed_point():
    x = cb.fixed_points(ferro, 0.2, 1.0, T=0.5)
    assert len(x) == 1 and abs(x[0] - 0.957) < 1e-3
    assert abs(cb.stability(ferro, x, T=0.5)[0] + 0.833) < 1e-3


def test_saddle_node_branches_split_into_stable_and_unstable():
    f = lambda x, r: r - x**2
    segs = cb.fixed_point_branches(f, "r", 0.0, 1.0, -1.2, 1.2,
                                   shape=(300, 300))
    stable = [s for s in segs if s[2]]
    unstable = [s for s in segs if not s[2]]
    assert stable and unstable
    assert all(np.all(s[1] > -0.05) for s in stable)
    assert all(np.all(s[1] < 0.05) for s in unstable)


def test_sweep_shows_hysteresis_below_critical_temperature():
    ms = np.linspace(-1, 1, 41)
    up = cb.continuation_sweep(ferro, "m", ms, -1.0, tinf=60, T=0.5)
    down = cb.continuation_sweep(ferro, "m", ms[::-1], up[-1], tinf=60, T=0.5)[::-1]
    i = np.argmin(abs(ms))                       # m = 0
    assert up[i] < -0.5 and down[i] > 0.5        # two different states
    hot_up = cb.continuation_sweep(ferro, "m", ms, -1.0, tinf=60, T=1.5)
    hot_down = cb.continuation_sweep(ferro, "m", ms[::-1], hot_up[-1], tinf=60, T=1.5)[::-1]
    assert np.allclose(hot_up, hot_down, atol=1e-3)
