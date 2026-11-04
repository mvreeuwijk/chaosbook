import numpy as np

import chaosbook as cb


def test_correlation_dimension_of_a_line_is_one():
    rng = np.random.default_rng(0)
    X = rng.random(3000)
    Y = 0.5 * X
    D, r, C = cb.correlation_dimension(X, Y)
    assert abs(D - 1) < 0.15
    assert np.all(np.diff(C) >= 0)


def test_correlation_dimension_of_a_filled_square_is_two():
    rng = np.random.default_rng(0)
    D, _, _ = cb.correlation_dimension(rng.random(3000), rng.random(3000))
    assert abs(D - 2) < 0.2


def test_correlation_dimension_of_gasket_below_box_dimension():
    X, Y = cb.chaos_game(n=10000, seed=1)
    D2, _, _ = cb.correlation_dimension(X, Y)
    assert abs(D2 - np.log(3) / np.log(2)) < 0.2


def test_generalized_dimensions_uniform_square_all_two():
    rng = np.random.default_rng(0)
    Dq = cb.generalized_dimensions(rng.random(50000), rng.random(50000),
                                   qs=[0, 1, 2], pmin=2, pmax=5)
    assert np.all(np.abs(Dq - 2) < 0.1)


def test_generalized_dimensions_nonincreasing_and_d0_matches_box():
    X, Y = cb.chaos_game(n=20000, seed=1)
    qs = [0, 1, 2, 4]  # q < 0 is dominated by under-sampled boxes
    Dq = cb.generalized_dimensions(X, Y, qs=qs, pmin=2, pmax=7)
    assert np.all(np.diff(Dq) <= 1e-9)
    assert abs(Dq[qs.index(0)] - np.log(3) / np.log(2)) < 0.1


def test_binomial_measure_matches_closed_form():
    k, p1 = 9, 0.7
    m = np.array([1.0])
    for _ in range(k):
        m = np.ravel(np.column_stack([p1 * m, (1 - p1) * m]))
    x = (np.arange(2 ** k) + 0.5) / 2 ** k
    qs = np.array([-5, -2, 0, 2, 5])
    Dq = cb.generalized_dimensions(x, qs=qs, pmin=2, pmax=k, weights=m,
                                   origin=0.0, size=1.0)
    exact = -np.log(p1 ** qs + (1 - p1) ** qs) / ((qs - 1) * np.log(2))
    assert np.allclose(Dq, exact, atol=1e-6)
