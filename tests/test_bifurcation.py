import matplotlib.pyplot as plt
import numpy as np

from chaosbook import bifurcation_diagram, logistic


def test_stable_branch_follows_fixed_point():
    fig, ax = plt.subplots()
    rs, xs = bifurcation_diagram(logistic, 2.0, 2.8, nr=8, n=400, ax=ax)
    for r in np.unique(rs):
        branch = xs[rs == r]
        assert np.allclose(branch, 1 - 1 / r, atol=1e-3)
    plt.close(fig)


def test_period_two_beyond_first_doubling():
    fig, ax = plt.subplots()
    rs, xs = bifurcation_diagram(logistic, 3.2, 3.2, nr=0, n=1000, ax=ax)
    values = np.unique(np.round(xs, 6))
    assert len(values) == 2
    plt.close(fig)
