"""chaosbook - computational toolkit for 'From Stability to Chaos'.

Every function here is introduced in the book's cookbook, where the full
implementation is shown as plain code before being packaged.
"""

from .maps import logistic
from .iterate import orbit

__version__ = "0.1.0"

__all__ = [
    "logistic",
    "orbit",
]
