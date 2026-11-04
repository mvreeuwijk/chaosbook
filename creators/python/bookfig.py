"""House style for the Python edition's figures.

Every figure is generated at the size it is printed and included without any
scaling (no :width: in the .md), so its text has the size set in
book.mplstyle on the page. The web pages show each image at the same physical
size (shared/_ext/natural_size.py reads the size from the PNG's dpi).

Usage in a figure script::

    import sys; from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import bookfig as bf

    fig, ax = plt.subplots(figsize=bf.MEDIUM)
    ...
    bf.save(fig, bf.out("disc1d") / "disc1d_name.png")

Size classes (inches; the text block is 6.38 in wide, 0.3 in less inside a
box):

    FULL_W   full text width, for wide time series and every combined
             multi-panel figure: figsize=(bf.FULL_W, height)
    MEDIUM   an ordinary single x-y plot
    SQUARE   phase portraits, cobwebs, return maps, 3-D views
    BOX_W    maximum width inside an admonition (example or code box)

Multi-panel figures are one figure with panel labels (a), (b), ... from
panel_labels(); never a {subfigure} of separate images.
"""

from pathlib import Path
from string import ascii_lowercase

import matplotlib
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
STYLE = HERE / "book.mplstyle"
plt.style.use(STYLE)

FULL_W = 6.3
BOX_W = 6.0
MEDIUM = (3.8, 2.7)
SQUARE = (3.0, 3.0)
MAX_H = 5.5          # no figure taller than this (0.6 of the text height)

DPI = 300


def out(chapter):
    """The chapter's image folder, python/_static/<chapter>/."""
    p = HERE.parents[1] / "python" / "_static" / chapter
    p.mkdir(parents=True, exist_ok=True)
    return p


def panel_labels(axes, order="row", start=0, loc=(0.0, 1.0), pad=(-0.02, 0.02),
                 **kw):
    """Write (a), (b), ... at the top left, just outside each axes.

    axes  : a 2-D array from plt.subplots, or a flat list in label order.
    order : "row" labels across rows first, "col" down columns first (so a
            grid can be transposed while the caption keeps its letters).
    """
    import numpy as np
    arr = np.asarray(axes, dtype=object)
    if arr.ndim == 2 and order == "col":
        flat = arr.T.ravel()
    else:
        flat = arr.ravel()
    style = dict(fontsize=matplotlib.rcParams["axes.labelsize"],
                 va="bottom", ha="right")
    style.update(kw)
    for i, ax in enumerate(flat):
        if ax is None or not ax.get_visible():
            continue
        ax.text(loc[0] + pad[0], loc[1] + pad[1],
                f"({ascii_lowercase[start + i]})",
                transform=ax.transAxes, **style)


def save(fig, path, check=True):
    """Save at exactly the figure size (no tight bbox), 300 dpi, and close.

    With check=True the size classes are enforced: wider than FULL_W or
    taller than MAX_H raises, because LaTeX would then rescale the image.
    """
    w, h = fig.get_size_inches()
    if check and (w > FULL_W + 1e-6 or h > MAX_H + 1e-6):
        raise ValueError(f"{Path(path).name}: figure {w:.2f} x {h:.2f} in "
                         f"exceeds {FULL_W} x {MAX_H} in")
    fig.savefig(path, dpi=DPI)
    plt.close(fig)
