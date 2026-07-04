# Creators — app_cookbook

Sources for the *Maple cookbook* appendix
(`latexsource/app_cookbook.tex`; figures live in
`latexsource/Figs_app_cookbook/`).

The appendix was transcribed from the LaTeX cookbook in the Feb-2013 book
(`Book_Feb2013/cookbook.tex`); the two Maple worksheets below are the ground
truth from which both the recipes and their 21 figures were produced.

- **`cookbook2012_book.mw`** — the Maple worksheet behind the 2012/2013 version
  of the cookbook. Executing it reproduces every figure used in the appendix
  (`cookbook_plot_f`, `cookbook_plot_cobweb`, `cookbook_bifurcation_cont`,
  `cookbook_Lorentz`, `cookbook_Sierpinsky`, `cookbook_boxcounting`, …). It also
  contains the exact Maple input for every recipe, so the code shown in the
  `\begin{maple}` boxes and the printed output can be regenerated verbatim.
  Copied from `Book_Feb2013/Figs_cookbook/creators/cookbook2012_book.mw`.

- **`cookbook2006.mws`** — the original *Chaotic Processes Cookbook* worksheet
  (van Reeuwijk, Jonker & Mudde, 2006), the earliest version of this document.
  Kept for provenance; the appendix follows the later 2012/2013 revision.

Both are legacy Maple worksheet containers (`.mw`/`.mws`): open them in Maple to
run the recipes, or read the command text directly (stored inside the worksheet
tokens). The generated figures are stored as PDF in
`latexsource/Figs_app_cookbook/` and are converted to PNG for the web build by
the normal figure pipeline.
