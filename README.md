# From Stability to Chaos

**A Hands-On Introduction to Nonlinear Dynamics** — by Harmen J. Jonker and
Maarten van Reeuwijk.

[![Deploy book to GitHub Pages](https://github.com/mvreeuwijk/chaosbook/actions/workflows/pages.yml/badge.svg)](https://github.com/mvreeuwijk/chaosbook/actions/workflows/pages.yml)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/Text-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Code: MIT](https://img.shields.io/badge/Code-MIT-blue.svg)](LICENSE-CODE)

A hands-on tour from simple one-dimensional maps to strange attractors and
fractal geometry. The book is built around the idea of *learning by doing*: it
develops the theory alongside concrete computations — with a weekly exercise
for every topic — so each idea can be explored, visualised and experimented
with directly. It grew out of the *Chaotic Processes* course at TU Delft; see
the [About page](maple/about.md) for the full story.

## Read it

- **Online:** Python edition <https://mvreeuwijk.github.io/chaosbook/>,
  Maple edition <https://mvreeuwijk.github.io/chaosbook/maple/>.
- **PDF:** each edition's book and cookbook are published alongside its pages
  and rebuilt on every push to `main` (Python: `chaosbook.pdf`, `cookbook.pdf`
  at the site root; Maple: `maple/chaosbook.pdf`, `maple/cookbook.pdf`).
- **Exercise labs:** every chapter of the Python edition has a JupyterLite lab
  that runs in the browser, with nothing to install
  (<https://mvreeuwijk.github.io/chaosbook/lite/lab/index.html>).

## Status

- **Python edition — complete.** The main edition: all chapters, the cookbook,
  the appendices, an exercise lab per chapter, interactive figures, and the
  small `chaosbook` package (`src/chaosbook/`, tested in `tests/`).
- **Maple edition — complete.** The original edition, published alongside
  under `/maple/`.

The two editions share the mathematical exposition, figures' content and
exercises, and differ in the code, the figure-generation workflow and the
labs. See [ROADMAP.md](ROADMAP.md).

## Layout

The book is a mono-repo: one Sphinx source tree per edition, plus shared
resources and the figure-generation audit trail.

    python/    the Python edition (chapters, cookbook notebook, labs in python/lite/)
    maple/     the Maple edition
    shared/    resources common to every edition (refs.bib, custom.sty, custom.css)
    src/       the chaosbook Python package (tests in tests/)
    creators/  figure sources: creators/python/<chapter>/ scripts for the Python
               edition, Maple worksheets for the Maple edition, and the
               porting manifest
    build/     generated HTML/PDF (git-ignored)

Each edition has its own `conf.py` and `index.md` but pulls shared resources
from `../shared` via config. See [`shared/README.md`](shared/README.md) for how a
new edition plugs in, and [`creators/README.md`](creators/README.md) for the
figure → worksheet mapping.

## Build

    pip install -r requirements.txt
    make python                            # HTML -> build/python/html
    make maple                             # HTML -> build/maple/html
    make python-figures                    # regenerate every Python-edition figure
    make python-lite LITEDIR=<short path>  # the JupyterLite lab layer

PDF (per edition; `main.tex` is the book, `cookbook.tex` the cookbook):

    sphinx-build -b latex python build/python/latex
    cd build/python/latex && latexmk -pdf main.tex

The published site is assembled by `.github/workflows/pages.yml`: the Python
edition at the root, the Maple edition under `maple/`, the labs under `lite/`.

## Contributing & errata

Corrections, typo reports and suggestions are very welcome — especially errata,
since the exercises and figures are central to the book. Please
[open an issue](https://github.com/mvreeuwijk/chaosbook/issues) (an *erratum*
template is provided) or send a pull request. See [CONTRIBUTING.md](CONTRIBUTING.md)
for build details and conventions.

## Citation

If you use or reference the book, please cite it. Machine-readable metadata is
in [CITATION.cff](CITATION.cff); once a stable release is archived on Zenodo, a
DOI will be added there and cited here.

## License

- **Text, figures and other creative content:** [CC BY-NC-SA 4.0](LICENSE)
- **Code** (Maple worksheets, Python code, printed code fragments):
  [MIT](LICENSE-CODE)
