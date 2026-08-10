import numpy as np

from chaosbook import box_dimension, chaos_game


def test_chaos_game_is_reproducible_and_bounded():
    X1, Y1 = chaos_game(n=2000, seed=1)
    X2, Y2 = chaos_game(n=2000, seed=1)
    assert np.array_equal(X1, X2) and np.array_equal(Y1, Y2)
    assert len(X1) == 2001
    assert X1.min() >= 0 and X1.max() <= 1
    assert Y1.min() >= 0 and Y1.max() <= 1


def test_gasket_dimension_is_log3_over_log2():
    X, Y = chaos_game(n=10000, seed=1)
    dim, boxsize, boxcount = box_dimension(X, Y)
    assert abs(dim - np.log(3) / np.log(2)) < 0.1
    assert len(boxsize) == 21 and len(boxcount) == 21


def test_straight_line_has_dimension_one():
    X = np.linspace(0, 1, 5000)
    Y = np.zeros(5000)
    dim, _, _ = box_dimension(X, Y)
    assert abs(dim - 1) < 0.1
