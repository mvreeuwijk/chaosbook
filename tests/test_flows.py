import numpy as np

from chaosbook import lorenz


def test_origin_is_a_fixed_point():
    assert lorenz(0, [0, 0, 0]) == [0, 0, 0]


def test_nontrivial_fixed_point():
    r, b = 28.0, 8.0 / 3.0
    q = np.sqrt(b * (r - 1))
    assert np.allclose(lorenz(0, [q, q, r - 1]), [0, 0, 0], atol=1e-12)
