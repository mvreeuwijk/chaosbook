import numpy as np
from scipy.integrate import solve_ivp

import chaosbook as cb


def oscillator(t, s, w=2.0):
    return [s[1], -w**2 * s[0]]


def test_section_of_harmonic_oscillator():
    t, X = cb.poincare_section(oscillator, [1.0, 0.0], 10.0, (0, 0.0),
                               direction=1)
    # x = cos(2 t) crosses zero upward at t = 3 pi / 4 + k pi
    assert np.allclose(np.diff(t), np.pi, atol=1e-6)
    assert np.allclose(X[:, 0], 0.0, atol=1e-8)
    t2, _ = cb.poincare_section(oscillator, [1.0, 0.0], 10.0, (0, 0.0))
    assert len(t2) >= 2 * len(t) - 1     # both directions


def test_section_passes_parameters_and_discards():
    t, X = cb.poincare_section(oscillator, [1.0, 0.0], 10.0, (0, 0.0),
                               discard=5.0, w=1.0)
    assert t.min() >= 5.0
    assert np.allclose(np.diff(t), np.pi, atol=1e-6)


def test_maxima_of_sine_refined():
    t = np.linspace(0, 20, 400)
    tm, xm = cb.maxima(t, np.sin(t))
    assert np.allclose(xm, 1.0, atol=1e-4)
    assert np.allclose(tm, np.pi / 2 + 2 * np.pi * np.arange(len(tm)), atol=1e-2)


def test_stroboscopic_section_sampling():
    X = cb.stroboscopic_section(oscillator, [1.0, 0.0], np.pi, 5, w=2.0)
    assert X.shape == (5, 2)
    assert np.allclose(X[:, 0], 1.0, atol=1e-6)   # period pi: back to start


def test_lorenz_map_is_one_dimensional_and_steep():
    sol = solve_ivp(cb.lorenz, [0, 120], [2, 5, 5],
                    t_eval=np.arange(0, 120, 0.01), rtol=1e-9, atol=1e-12)
    _, z = cb.maxima(sol.t, sol.y[2])
    z = z[3:]
    a, b = z[:-1], z[1:]
    assert 30 < a.min() and a.max() < 50
    # tent-like: next maximum is a decreasing function of the distance to
    # the cusp, so a left and a right branch of opposite slope
    cusp = a[np.argmax(b)]
    left, right = a < cusp, a > cusp
    assert np.polyfit(a[left], b[left], 1)[0] > 1
    assert np.polyfit(a[right], b[right], 1)[0] < -1


def test_lorenz_section_y0_both_signs_of_x():
    t, X = cb.poincare_section(cb.lorenz, [2, 5, 5], 60.0, (1, 0.0),
                               discard=10.0)
    assert len(X) > 20
    assert (X[:, 0] > 0).any() and (X[:, 0] < 0).any()
    assert np.allclose(X[:, 1], 0, atol=1e-8)


def _rossler_maxima(c):
    sol = solve_ivp(lambda t, s: cb.rossler(t, s, c=c), [0, 500], [1, 0, 0],
                    t_eval=np.arange(0, 500, 0.02), rtol=1e-9, atol=1e-12)
    _, xm = cb.maxima(sol.t, sol.y[0])
    return xm[len(xm) // 2:]


def test_rossler_period_doubling_route():
    for c, period in [(3.0, 1), (3.4, 2), (3.55, 4)]:
        xm = _rossler_maxima(c)
        assert len(np.unique(np.round(xm, 2))) == period
    chaos = _rossler_maxima(4.0)
    assert len(np.unique(np.round(chaos, 1))) > 20


def test_forced_double_well_visits_both_wells():
    X = cb.stroboscopic_section(cb.forced_double_well, [0, 0, 0],
                                2 * np.pi, 400, discard=50)
    assert (X[:, 0] > 0.5).any() and (X[:, 0] < -0.5).any()
    # weak forcing: stuck in one well
    Xw = cb.stroboscopic_section(cb.forced_double_well, [0.9, 0, 0],
                                 2 * np.pi, 200, discard=50, A=0.05)
    assert (Xw[:, 0] > 0).all()


def test_circle_limit_cycle_poincare_map():
    a = 0.2
    t, X = cb.poincare_section(cb.circle_limit_cycle, [0.01, 0.0], 40 * np.pi,
                               (1, 0.0), direction=1, a=a)
    r = X[:, 0]
    assert np.all(np.diff(r[:8]) > 0) and abs(r[-1] - 1) < 1e-6
    P = lambda r: (1 - (r**2 - 1) / r**2 * np.exp(-4 * a * np.pi)) ** -0.5
    assert np.allclose(r[1:], P(r[:-1]), rtol=1e-5)


def test_rotating_threebody_conserves_energy_and_lagrange_points():
    mu = 0.2
    x0 = [0.1, 0, 0, 1]
    sol = solve_ivp(lambda t, s: cb.rotating_threebody(t, s, mu=mu), [0, 50],
                    x0, rtol=1e-11, atol=1e-13)
    H = lambda s: 0.5 * (s[2] ** 2 + s[3] ** 2) + cb.threebody_potential(s[0], s[1], mu)
    assert abs(H(sol.y[:, -1]) - H(sol.y[:, 0])) < 1e-6
    xl = cb.lagrange_points(mu)
    assert np.allclose(xl, [1.27, 0.44, -1.08], atol=0.01)
    V = [cb.threebody_potential(x, 0, mu) for x in xl]
    assert V[1] < V[0] < V[2]


def test_lyapunov_exponents():
    lam = cb.lyapunov_exponent(cb.lorenz, [2, 5, 5], 100, dt=0.05,
                               transient=20)
    assert 0.6 < lam < 1.2                      # literature: 0.906
    stable = cb.lyapunov_exponent(oscillator, [1, 0], 5, dt=0.1)
    assert abs(stable) < 0.05                   # neutral oscillator
    damped = lambda t, s: [-s[0], -2 * s[1]]
    assert cb.lyapunov_exponent(damped, [1, 1], 5, dt=0.1) < -0.5


def test_effective_lyapunov_between_symmetric_jacobian_eigenvalues():
    sol = solve_ivp(cb.lorenz, [0, 20], [2, 5, 5], t_eval=np.arange(0, 20, 0.01),
                    rtol=1e-10, atol=1e-12)
    sol2 = solve_ivp(cb.lorenz, [0, 20], [2 + 1e-7, 5, 5],
                     t_eval=np.arange(0, 20, 0.01), rtol=1e-10, atol=1e-12)
    le, ev = cb.effective_lyapunov(cb.lorenz, sol.t, sol.y.T, sol2.y.T)
    assert np.all(le >= ev[:, 0] - 1e-6) and np.all(le <= ev[:, -1] + 1e-6)
    assert abs(np.mean(le) - 0.9) < 0.4
    # the eigenvalues add up to the divergence -(sigma + 1 + b)
    assert np.allclose(ev.sum(axis=1), -(10 + 1 + 8 / 3), atol=1e-4)


def test_flow_parameter_may_be_called_f():
    # the double-well damping coefficient is called f, like the flow itself
    sol = solve_ivp(lambda t, s: cb.forced_double_well(t, s, f=0.15, A=0.3),
                    [0, 10], [0, 0, 0], t_eval=np.linspace(0, 10, 200))
    le, ev = cb.effective_lyapunov(cb.forced_double_well, sol.t, sol.y.T,
                                   sol.y.T + 1e-8, f=0.15, A=0.3)
    assert np.all(np.isfinite(le))
    t, X = cb.poincare_section(cb.forced_double_well, [0, 0, 0], 10, (0, 0.5),
                               f=0.15, A=0.3)
    assert np.allclose(X[:, 0], 0.5, atol=1e-8)
