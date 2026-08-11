"""chaosbook - computational toolkit for 'From Stability to Chaos'.

Every function here is introduced in the book's cookbook, where the full
implementation is shown as plain code before being packaged.
"""

from .maps import logistic
from .iterate import orbit
from .cobweb import cobweb
from .bifurcation import bifurcation_diagram
from .flows import lorenz, threebody, corotating
from .fractal import chaos_game, box_dimension

__version__ = "0.1.0"

__all__ = [
    "logistic",
    "orbit",
    "cobweb",
    "bifurcation_diagram",
    "lorenz",
    "threebody",
    "corotating",
    "chaos_game",
    "box_dimension",
]
