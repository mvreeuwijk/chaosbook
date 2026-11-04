# -*- coding: utf-8 -*-
#
# Sphinx configuration for the Python edition of "From Stability to Chaos".
# Parallel in structure to the other language edition's conf.py; shared
# resources (refs.bib, custom.sty, custom.css) come from ../shared via the
# settings below.

extensions = [
    'myst_nb',  # notebooks + MyST markdown (loads the MyST parser itself)
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.mathjax',
    'sphinx_design',
    'sphinxcontrib.bibtex',
    'sphinx_subfigure',
    'sphinx_math_dollar',
]

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
            "url": "https://mvreeuwijk.github.io/chaosbook/python/chaosbook-python.pdf",
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

# -- LaTeX (the cookbook PDF) ----------------------------------------------

latex_additional_files = ['../shared/custom.sty']

latex_elements = {
    'papersize': 'a4paper',
    'fontpkg': '',
    'fncychap': '',
    'pointsize': '11pt',
    'releasename': "",
    'babel': '',
    'printindex': '',
    'fontenc': '',
    'inputenc': '',
    'classoptions': '',
    'utf8extra': '',
    'preamble': r'\usepackage{custom}\hypersetup{hypertexnames=false}',
    'figure_align': 'tbp',
}

# The cookbook is a standalone PDF built as a 'howto' (article-based)
# document: its top-level headings become sections rather than chapters, so
# they flow instead of each starting a new page.
#
# main.tex is the draft book PDF of the converted chapters (user direction
# 2026-08-11: published by CI so figure quality in print can be judged as
# chapters roll out; it becomes the edition's real book PDF once enough
# chapters exist).
latex_documents = [
  ('index', 'main.tex', u'From Stability to Chaos',
   u'Harmen J. Jonker and Maarten van Reeuwijk', 'manual'),
  ('app_cookbook', 'cookbook.tex', u'The Python Cookbook',
   u'Harmen J. Jonker and Maarten van Reeuwijk', 'howto'),
]

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
