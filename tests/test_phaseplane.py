import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pytest

from chaosbook import (jacobian, classify_fixed_point, fixed_points,
                       phase_portrait, lotka_volterra, vanderpol, hopf,
                       lotka_volterra_invariant, lotka_volterra_allee)
from scipy.integrate import solve_ivp


def test_jacobian_of_a_linear_system_is_its_matrix():
    A = np.array([[1.0, 2.0], [-3.0, 0.5]])
    J = jacobian(lambda t, x: A @ x, [0.3, -0.2])
    assert np.allclose(J, A, atol=1e-7)


def test_jacobian_of_nonlinear_flow_and_params():
    J = jacobian(lotka_volterra, [0.75, 1.0], alpha=0.75)
    assert np.allclose(J, [[0, -0.75], [1, 0]], atol=1e-6)


@pytest.mark.parametrize("A,kind", [
    ([[-1, 0], [0, -2]], "stable node"),
    ([[1, 0], [0, 2]], "unstable node"),
    ([[1, 0], [0, -2]], "saddle"),
    ([[-0.1, -1], [1, -0.1]], "stable spiral"),
    ([[0.1, -1], [1, 0.1]], "unstable spiral"),
    ([[0, -1], [1, 0]], "centre"),
    ([[0, 0], [0, -1]], "degenerate"),
])
def test_classification(A, kind):
    assert classify_fixed_point(A)[1] == kind


def test_classification_eigenvalues_and_shape_check():
    ev, _ = classify_fixed_point([[0, -1], [1, 0]])
    assert np.allclose(sorted(ev.imag), [-1, 1])
    with pytest.raises(ValueError):
        classify_fixed_point(np.eye(3))


def test_lotka_volterra_fixed_points_and_types():
    pts = fixed_points(lotka_volterra, [[0.1, 0.1], [0.8, 0.9], [2, 2]], alpha=0.75)
    assert any(np.allclose(p, [0, 0], atol=1e-6) for p in pts)
    assert any(np.allclose(p, [0.75, 1], atol=1e-6) for p in pts)
    kinds = {tuple(np.round(p, 3)): classify_fixed_point(jacobian(lotka_volterra, p, alpha=0.75))[1]
             for p in pts}
    assert kinds[(0.0, 0.0)] == "saddle"
    assert kinds[(0.75, 1.0)] == "centre"


def test_vanderpol_origin_is_unstable_spiral_for_small_mu():
    _, kind = classify_fixed_point(jacobian(vanderpol, [0, 0], mu=1.0))
    assert kind == "unstable spiral"
    _, kind = classify_fixed_point(jacobian(vanderpol, [0, 0], mu=3.0))
    assert kind == "unstable node"


def test_hopf_changes_stability_at_mu_zero():
    for mu, kind in [(-0.1, "stable spiral"), (0.1, "unstable spiral")]:
        assert classify_fixed_point(jacobian(hopf, [0, 0], mu=mu))[1] == kind


def test_lotka_volterra_invariant_is_conserved():
    sol = solve_ivp(lotka_volterra, [0, 20], [0.25, 0.25], rtol=1e-11, atol=1e-13)
    H = lotka_volterra_invariant(sol.y[0], sol.y[1])
    assert np.ptp(H) / H[0] < 1e-7


def test_allee_fixed_point_location():
    a, b = 0.5, 3 / 16
    p = fixed_points(lotka_volterra_allee, [[0.3, 0.6]], alpha=a, beta=b)[0]
    assert np.allclose(p, [a - b, (a - b) / a], atol=1e-6)


@pytest.mark.parametrize("style", ["stream", "quiver", None])
def test_phase_portrait_draws_and_trajectory_reaches_limit_cycle(style):
    fig, ax = plt.subplots()
    out = phase_portrait(vanderpol, (-3, 3), (-3, 3), ax=ax, n=12, style=style,
                         nullclines=True, trajectories=[[0.01, 0], [3, 0]],
                         tmax=30, mu=1.0)
    assert out is ax
    for line in ax.lines:
        x, y = line.get_data()
        assert np.hypot(x[-1], y[-1]) > 1.5  # outer cycle, not the origin
    plt.close(fig)
