"""chaosbook - computational toolkit for 'From Stability to Chaos'.

The book's listings first show how to do each computation with numpy,
scipy and sympy; the package wraps the recurring ones. Some of the
functions are introduced as recipes in the cookbook; the rest are
introduced where a chapter first needs them.

Calling convention: maps and one-dimensional flows take ``f(x, **params)``;
flows in two or more dimensions take ``f(t, x, **params)``, the
``scipy.integrate.solve_ivp`` form. See the cookbook for details.
"""

from .maps import (logistic, sine, tent, shift, henon, duffing_map,
                   circle_map, standard_map)
from .iterate import orbit, winding_number
from .cobweb import cobweb
from .bifurcation import bifurcation_diagram
from .lyapunov import lyapunov, lyapunov_sweep, lyapunov_spectrum
from .flows import lorenz, threebody, corotating
from .fractal import chaos_game, box_dimension
from .fractal import correlation_dimension, generalized_dimensions

__version__ = "0.1.0"

__all__ = [
    "logistic",
    "sine",
    "tent",
    "shift",
    "henon",
    "duffing_map",
    "circle_map",
    "standard_map",
    "orbit",
    "winding_number",
    "cobweb",
    "bifurcation_diagram",
    "lyapunov",
    "lyapunov_sweep",
    "lyapunov_spectrum",
    "lorenz",
    "threebody",
    "corotating",
    "chaos_game",
    "box_dimension",
    "correlation_dimension",
    "generalized_dimensions",
]
from .phaseplane import jacobian, classify_fixed_point, fixed_points_nd, phase_portrait
from .flows2d import (lotka_volterra, lotka_volterra_invariant,
                      lotka_volterra_allee, vanderpol, double_well, hopf)

__all__ += [
    "jacobian",
    "classify_fixed_point",
    "fixed_points_nd",
    "phase_portrait",
    "lotka_volterra",
    "lotka_volterra_invariant",
    "lotka_volterra_allee",
    "vanderpol",
    "double_well",
    "hopf",
]

from .flows1d import (fixed_points, stability, classify,
                      fixed_point_branches, continuation_sweep)

__all__ += [
    "fixed_points",
    "stability",
    "classify",
    "fixed_point_branches",
    "continuation_sweep",
]

from .poincare import (poincare_section, stroboscopic_section, maxima,
                       effective_lyapunov, lyapunov_exponent,
                       lyapunov_spectrum_flow)
from .flows3d import (rossler, forced_double_well, circle_limit_cycle,
                      rotating_threebody, threebody_potential,
                      lagrange_points)

__all__ += [
    "poincare_section",
    "stroboscopic_section",
    "maxima",
    "effective_lyapunov",
    "lyapunov_exponent",
    "lyapunov_spectrum_flow",
    "rossler",
    "forced_double_well",
    "circle_limit_cycle",
    "rotating_threebody",
    "threebody_potential",
    "lagrange_points",
]
