"""Right-hand sides of the book's flows, in solve_ivp form f(t, state)."""


def lorenz(t, xyz, sigma=10.0, r=28.0, b=8.0 / 3.0):
    """The Lorenz equations."""
    x, y, z = xyz
    return [sigma * (y - x), -x * z + r * x - y, x * y - b * z]
