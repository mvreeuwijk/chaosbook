import matplotlib.pyplot as plt

from chaosbook import cobweb, logistic


def test_cobweb_draws_three_lines_on_given_axes():
    fig, ax = plt.subplots()
    out = cobweb(logistic, 0.1, 50, ax=ax, r=0.5)
    assert out is ax
    assert len(ax.lines) == 3
    plt.close(fig)


def test_cobweb_path_starts_at_x0_on_the_x_axis():
    fig, ax = plt.subplots()
    cobweb(logistic, 0.3, 10, ax=ax, r=2.5)
    path = ax.lines[2]
    assert path.get_xdata()[0] == 0.3
    assert path.get_ydata()[0] == 0
    plt.close(fig)
