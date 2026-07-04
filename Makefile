# Minimal Makefile for Sphinx documentation
#
# The book ships as one Sphinx source tree per language edition (maple/, and
# later python/). Each edition has its own conf.py and index.md but pulls the
# shared resources (refs.bib, custom.sty, custom.css) from ../shared via config.
#
#   make maple    -> build/maple/html
#   make python   -> build/python/html   (once the python/ tree exists)
#   make html     -> alias for the default edition (maple)

SPHINXBUILD   = sphinx-build
BUILDDIR      = build

.PHONY: help clean html maple python

help:
	@echo "targets: maple, python, html (=maple), clean"

clean:
	rm -rf "$(BUILDDIR)"/*

maple:
	@$(SPHINXBUILD) -M html maple "$(BUILDDIR)/maple"

python:
	@$(SPHINXBUILD) -M html python "$(BUILDDIR)/python"

# Default edition for a bare `make html`.
html: maple
