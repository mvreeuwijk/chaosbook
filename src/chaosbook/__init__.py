"""chaosbook - computational toolkit for 'From Stability to Chaos'.

Every function here is introduced in the book's cookbook, where the full
implementation is shown as plain code before being packaged.
"""

from .maps import logistic, sine, tent, shift
from .iterate import orbit
from .cobweb import cobweb
from .bifurcation import bifurcation_diagram
from .lyapunov import lyapunov, lyapunov_sweep
from .flows import lorenz, threebody, corotating
from .fractal import chaos_game, box_dimension

__version__ = "0.1.0"

__all__ = [
    "logistic",
    "sine",
    "tent",
    "shift",
    "orbit",
    "cobweb",
    "bifurcation_diagram",
    "lyapunov",
    "lyapunov_sweep",
    "lorenz",
    "threebody",
    "corotating",
    "chaos_game",
    "box_dimension",
]
