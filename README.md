# From Stability to Chaos

MyST/Sphinx sources for the book *From Stability to Chaos: A Hands-On
Introduction to Nonlinear Dynamics* (Harmen Jonker and Maarten van Reeuwijk).

This repository contains only the generated documentation (Markdown + assets)
that builds the HTML and PDF. The LaTeX sources, Maple worksheets and the
LaTeX -> MyST converter live in the separate `convertchaosbook` repository.

## Layout

The book ships as one Sphinx source tree per language edition:

    maple/     the Maple edition (complete)
    python/    the Python edition (planned; not yet created)
    shared/    resources common to every edition (refs.bib, custom.sty, custom.css)
    creators/  Maple worksheets + porting guide (source of truth for the ports)

Each edition has its own `conf.py` and `index.md` but pulls the shared
resources from `../shared` via config. See `shared/README.md` for how a new
edition plugs in.

## Build

    pip install -r requirements.txt
    make maple                             # HTML -> build/maple/html
    make python                            # HTML -> build/python/html (once python/ exists)

PDF (per edition):

    sphinx-build -b latex maple build/maple/latex
    cd build/maple/latex && latexmk -pdf main.tex
