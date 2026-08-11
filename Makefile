# Minimal Makefile for Sphinx documentation
#
# The book ships as one Sphinx source tree per language edition (maple/, and
# later python/). Each edition has its own conf.py and index.md but pulls the
# shared resources (refs.bib, custom.sty, custom.css) from ../shared via config.
#
#   make maple            -> build/maple/html
#   make python           -> build/python/html   (once the python/ tree exists)
#   make html              -> alias for the default edition (maple)
#   make python-figures    -> regenerate every creators/python/*/ figure script

SPHINXBUILD   = sphinx-build
BUILDDIR      = build
PYTHON       ?= python

.PHONY: help clean html maple python python-figures

help:
	@echo "targets: maple, python, html (=maple), python-figures, clean"

clean:
	rm -rf "$(BUILDDIR)"/*

maple:
	@$(SPHINXBUILD) -M html maple "$(BUILDDIR)/maple"

python:
	@$(SPHINXBUILD) -M html python "$(BUILDDIR)/python"

# Default edition for a bare `make html`.
html: maple

python-figures:
	@set -e; for f in creators/python/*/*.py; do echo "== $$f"; "$(PYTHON)" "$$f"; done
