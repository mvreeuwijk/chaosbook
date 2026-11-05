# -*- coding: utf-8 -*-
#
# Sphinx configuration for the Python edition of "From Stability to Chaos".
# Parallel in structure to the other language edition's conf.py; shared
# resources (refs.bib, custom.sty, custom.css) come from ../shared via the
# settings below.

import os
import sys

# Shared Sphinx extensions (../shared/_ext).
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'shared', '_ext')))

extensions = [
    'myst_nb',  # notebooks + MyST markdown (loads the MyST parser itself)
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.mathjax',
    'sphinx_design',
    'sphinxcontrib.bibtex',
    'sphinx_subfigure',
    'sphinx_math_dollar',
    # Figures are saved at their printed size and included without :width:;
    # this shows them at that same physical size in HTML
    # (creators/python/bookfig.py has the house style).
    'natural_size',
]
natural_size_html_scale = 1.1

autosectionlabel_prefix_document = True

master_doc = 'index'

project = u'From Stability to Chaos'
author = u'Harmen J. Jonker and Maarten van Reeuwijk'
copyright = u'2025, Harmen J. Jonker and Maarten van Reeuwijk'

mathjax_path = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
mathjax3_config = {
    "tex": {
        "macros": {
            "d": r"\mathrm{d}",
        }
    }
}

import datetime as _datetime
_today = _datetime.date.today()
release = f'{_today:%B} {_today.day}, {_today.year}'
version = release
today = ''

# _includes are pulled in via {include}; lite/ is the JupyterLite lab layer,
# built separately by python/lite/build_lite.py (its notebooks are contents
# for the browser, not pages of this site).
exclude_patterns = ["_includes/**", "lite/**"]

# Edition templates: the curated top menu and the sidebar Exercises section
# (same structure as the other edition).
templates_path = ['_templates']

pygments_style = 'sphinx'


# -- Notebook execution (myst-nb) ------------------------------------------
# "cache": execute during the Sphinx build, re-running only when the
# notebook changes (spec decision 5). If a clean-slate rebuild ever hits a
# jupyter-cache FileExistsError on this machine (OneDrive interference),
# delete build/ and rebuild; CI runners start clean and are unaffected.
nb_execution_mode = "cache"
nb_execution_timeout = 300

# -- HTML ------------------------------------------------------------------

html_theme = 'sphinx_book_theme'
html_theme_options = {
    "repository_url": "https://github.com/mvreeuwijk/chaosbook",
    "use_repository_button": True,
    "use_edit_page_button": False,
    "use_issues_button": False,
    "use_download_button": False,
    "home_page_in_toc": False,
    "collapse_navigation": True,
    "navigation_depth": 2,
    "show_nav_level": 1,
    # Top header: book title (left), curated part menu (centre), PDF and
    # GitHub (right), as in the other edition.
    "navbar_start": ["navbar-logo"],
    "navbar_center": ["navbar-center.html"],
    "navbar_end": ["navbar-icon-links"],
    "icon_links": [
        {
            "name": "Download PDF",
            "url": "https://mvreeuwijk.github.io/chaosbook/chaosbook.pdf",
            "icon": "fa-solid fa-file-pdf",
            "type": "fontawesome",
        },
        {
            "name": "GitHub",
            "url": "https://github.com/mvreeuwijk/chaosbook",
            "icon": "fa-brands fa-github",
            "type": "fontawesome",
        },
    ],
}
html_title = u'From Stability to Chaos'
html_static_path = ['../shared/_static', '_static']
html_css_files = ['custom.css']

# Left sidebar: no sidebar on the frontpage; elsewhere the book navigation
# plus a dedicated "Exercises" section linking to each chapter's exercises.
html_sidebars = {
    "index": [],
    "**": [
        "navbar-logo.html",
        "icon-links.html",
        "search-button-field.html",
        "sbt-sidebar-nav.html",
        "exercises-nav.html",
    ],
}
html_use_smartypants = False
smartquotes = False

# -- LaTeX (the book and cookbook PDFs) ------------------------------------
# Identical to the other edition's LaTeX setup: the same title page
# (custom.sty's serif \maketitle via the 'maketitle' element, not Sphinx's own
# \sphinxmaketitle), the same book class, appendix handling and PDF-bookmark
# fixes, so the two PDFs look the same.

latex_additional_files = ['../shared/custom.sty']

latex_elements = {
    'papersize': 'a4paper',
    'fontpkg': '',
    'fncychap': '',
    # Show the subtitle on the title page only (temporarily append it to \title
    # for \maketitle, then restore the plain title so it does not leak into the
    # running page header).
    'maketitle': (
        r'\makeatletter'
        r'\let\sfc@title\@title'
        r'\gdef\@title{\sfc@title\\[4mm]{\Large A Hands-On Introduction to Nonlinear Dynamics}}'
        r'\maketitle'
        r'\gdef\@title{\sfc@title}'
        r'\makeatother'
    ),
    'pointsize': '11pt',
    'releasename': "",
    'babel': '',
    'printindex': '',
    'fontenc': '',
    'inputenc': '',
    'classoptions': '',
    'utf8extra': '',
    'preamble': r'\usepackage{custom}\renewcommand{\contentsname}{Table of contents}\hypersetup{hypertexnames=false}'
               r'\usepackage{etoolbox}'
               r'\preto\appendix{\cleardoublepage\phantomsection\addcontentsline{toc}{part}{Appendices}'
               r'\renewcommand{\thefigure}{\thechapter.\arabic{figure}}'
               r'\renewcommand{\theequation}{\thechapter.\arabic{equation}}'
               r'\renewcommand{\thetable}{\thechapter.\arabic{table}}}'
               r'\pdfstringdefDisableCommands{'
               r'\def\gg{}'
               r'\def\rightarrow{}'
               r'\def\infty{}'
               r'\def\tau{}'
               r'\def\mu{}'
               r'\def\alpha{}'
               r'\def\beta{}'
               r'\def\gamma{}'
               r'\def\delta{}'
               r'\def\varepsilon{}'
               r'\def\epsilon{}'
               r'\def\omega{}'
               r'\def\Omega{}'
               r'\def\theta{}'
               r'\def\pi{}'
               r'\def\lambda{}'
               r'\def\phi{}'
               r'\def\varphi{}'
               r'\def\psi{}'
               r'\def\chi{}'
               r'\def\rho{}'
               r'\def\eta{}'
               r'\def\sigma{}'
               r'\def\zeta{}'
               r'\def\kappa{}'
               r'\def\cdot{}'
               r'\def\cdots{}'
               r'\def\ldots{}'
               r'\def\pm{}'
               r'\def\times{}'
               r'\def\le{}'
               r'\def\ge{}'
               r'\def\neq{}'
               r'\def\approx{}'
               r'\def\sim{}'
               r'\def\propto{}'
               r'\def\equiv{}'
               r'\def\quad{}'
               r'\def\qquad{}'
               r'}',
    'figure_align': 'tbp',
}

# The cookbook is a separate deliverable: its own standalone PDF. It is built
# as a 'howto' (article-based) document, not a 'manual' (book): its top-level
# headings then become sections rather than chapters (so they flow instead of
# each starting a new page), and Sphinx does not append latex_appendices to
# 'howto' documents (the appendices belong to the book only).
latex_documents = [
  ('index', 'main.tex', u'From Stability to Chaos',
   u'Harmen J. Jonker and Maarten van Reeuwijk', 'manual'),
  ('app_cookbook', 'cookbook.tex', u'The Python Cookbook',
   u'Harmen J. Jonker and Maarten van Reeuwijk', 'howto'),
]

latex_docclass = {"manual": "book"}

# Appendices belong inside the book, rendered as Appendix A, B, ... (the
# cookbook is a separate document, and the appendices landing page is
# HTML-only, so neither is listed here).
latex_appendices = ['app_twobody', 'app_lorenz', 'app_polar']

numfig = True
numfig_format = {'figure': 'Figure %s', 'table': 'Table %s', 'section': '%s'}

bibtex_bibfiles = ['../shared/refs.bib']
suppress_warnings = ['bibtex.duplicate_citation']
bibtex_encoding = "iso-8859-1"
bibtex_default_style = "apa"
bibtex_reference_style = "author_year"

myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_admonition",
    "html_image",
    "linkify",
    "substitution",
    "tasklist",
]
myst_dmath_double_inline = True
