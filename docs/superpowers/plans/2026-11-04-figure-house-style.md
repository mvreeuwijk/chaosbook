# Figure house style for the Python edition

Status: analysis done (4 November 2026), implementation not started.

## Goal

Every Python-edition figure is generated at its final size and shown without
any scaling, in both the PDF and the HTML. Its text then has the right size
next to the body text automatically. Multi-panel figures become one combined
figure with automatic panel labels (a), (b), (c), ... The Python edition may
diverge from the Maple edition for this.

A figure counts as done only when it has been checked in **both** the PDF and
the HTML (desktop and phone width). Looking right in one does not guarantee
looking right in the other.

## Findings

### PDF

- `\sphinxincludegraphics` places an image at its natural size, taken from the
  PNG's dpi metadata (`savefig(dpi=N)`), so natural size = figsize in inches.
  It only ever shrinks (to `\linewidth` or `\textheight`), never enlarges.
  `bbox_inches="tight"` crops the figure and breaks this (12 calls, 7 scripts).
- Text block: 6.38 in wide (16.2 cm), 23.7 cm tall; about 6.1 in inside an
  admonition box. Body text 11 pt.
- `book.mplstyle` has 13 pt labels and 11 pt ticks, so printed text size is
  11 pt x scale, where scale = printed width / figsize width.
- The `:width:` values were copied from the Maple edition, but the Python
  images have different sizes and shapes. Scales therefore range from 0.30 to
  1.28: tick labels print at 3 to 14 pt.
- `{subfigure}` ignores `:width:` in LaTeX and makes every panel 0.495 of the
  text width (8 cm), bottom-aligned. Three-panel figures wrap to 2 + 1, panels
  of different aspect ratio are staggered, and tall grids run off the page:
  3.21 loses its last three panels and the caption (+22 cm), 4.12 overflows by
  11 cm, and 1.5, 2.4, 3.19, 4.7, 4.9 and 6.19 also overflow.
- Cookbook notebook outputs: 100 dpi, no width, printed 11 to 16 cm wide.

### HTML (sphinx-book-theme, measured with Playwright)

- Content column: 774 px for figures at a 1440 px desktop viewport; 390 px on
  a phone. Body text 16 px.
- Images with no `:width:` show at their pixel size, capped at the column.
  Python PNGs are 150 dpi, so a 4.2 in figure is 630 px wide.
- `:width: 60mm` becomes CSS `60mm` = 227 px. That 630 px image with 11 pt
  ticks (23 px at 150 dpi) is shown at 0.36 scale, so its ticks are about 8 px
  next to 16 px body text. 3.5, 3.7, 3.8, 3.11 (151 px) and 5.4 (119 px) are
  the worst.
- `:width: 100%` figures fill 774 px with ticks around 24 px, larger than the
  body text: 1.1, 2.18, 2.19, 3.4, 6.4, 8.1, 8.4.
- Subfigures are laid out two per row at 387 px, whatever the panel count, so
  2.2 (three panels) wraps to 2 + 1 here too, and mixed aspect ratios give
  ragged rows (2.4, 3.1, 3.19, 4.3 to 4.9, 5.12, 5.14, 6.10, 6.19).

### Why one rule works for both

The PDF shows images at figsize inches. A browser shows an SVG at its declared
size, which matplotlib writes in points, so a 6.3 in SVG is 605 CSS px.
Matplotlib text at 8 pt is then 10.7 px. Relative to the body this is 8/11 in
print and 10.7/16 on the web, close enough that one figure source serves both.
If the web figures look a little small, a single CSS rule can enlarge all
figure images by the same factor (16 px / 11 pt = 1.09 puts a 6.3 in figure at
660 px, which still fits the 774 px column). On a phone every figure is scaled
down to 390 px; that is unavoidable and acceptable.

## House style

**Saving.**
- Each script saves `name.pdf` (vector, for LaTeX) and `name.svg` (for HTML)
  at exactly the figsize. PNG at `dpi=300` only as a fallback (for example
  raster-heavy images such as 4.10's spin fields, where SVG would be huge).
- The `.md` references `_static/<chapter>/name.*`; Sphinx picks PDF for LaTeX
  and SVG for HTML.
- No `bbox_inches="tight"`; use constrained layout with a fixed figsize.
- No `:width:` or `:height:` on any figure.

**Sizes** (all at most 6.3 in wide, so LaTeX never rescales):

| class | figsize (in) | use |
|---|---|---|
| F (full) | 6.3 x 2.0 to 4.4 | wide time series, every combined multi-panel figure |
| M (medium) | 3.8 x 2.7 | ordinary single x-y plot |
| S (square) | 3.0 x 3.0 | phase portraits, cobwebs, return maps, 3-D views |
| S-tall | 3.0 x up to 4.5 | portrait-shaped schematics |
| inside a box | at most 6.0 wide | admonitions are about 0.3 in narrower |

No figure taller than 5.5 in. Panels in a row get equal heights through
`width_ratios`, not equal widths.

**Style** (`creators/python/book.mplstyle`):
- 9 pt base font, axis labels and titles; 8 pt ticks and legends.
- `mathtext.fontset: cm`, serif family, `axes.formatter.use_mathtext: True`.
- `lines.linewidth: 1.0`, `lines.markersize: 3`, `axes.linewidth: 0.6`.
- `figure.constrained_layout.use: True`, `savefig.bbox: standard`.
- Helper `panel_labels(axes, order="row" | "col")` writing (a), (b), ... in
  9 pt bold. Column order lets a grid be transposed while captions keep their
  letters.

## Inventory

`python/*.md` has 121 figure environments: 72 single-image and 49 multi-image
(182 images). The exercise includes add 9 single figures, the cookbook
notebook 19 outputs. The two `about.md` photos are left as they are.

### Multi-panel figures, each to become one combined figure

Layouts are at full width (6.3 in). "Reword" means the caption describes
panels by position or not at all and needs (a), (b) wording.

| Fig | source | panels | script | layout, figsize (in) | caption |
|---|---|---|---|---|---|
| 1.2 | phenomenon.md:72 | 2 | phenomenon/fig_lorenz.py | 2x1, shared t, 6.3x3.2 | |
| 1.3 | phenomenon.md:108 | 2 | phenomenon/fig_lorenz.py | 1x2 3-D, 6.3x3.0 | |
| 1.5 | phenomenon.md:235 | 6 | phenomenon/fig_3body.py | 2x3, 6.3x4.3, column order | reword "left/right column" |
| 2.1 | disc1d.md:56 | 4 | disc1d/fig_series_cobweb_return.py | 2x2, 6.3x4.0 | |
| 2.2 | disc1d.md:77 | 3 | disc1d/fig_series_cobweb_return.py | 1x3, 6.3x2.2 | |
| 2.3 | disc1d.md:126 | 4 | disc1d/fig_series_cobweb_return.py | 1x4 squares, 6.3x1.8 | |
| 2.4 | disc1d.md:150 | 6 | to locate (likely disc1d/fig_series_cobweb_return.py) | 2x3, series over return plots, 6.3x4.0 | reword |
| 2.6 | disc1d.md:241 | 2 | disc1d/fig_fixedpoints.py | 1x2, 6.3x2.3 | |
| 2.8 | disc1d.md:435 | 2 | disc1d/fig_fixedpoints.py | 1x2, 6.3x3.0 | |
| 2.9 | disc1d.md:547 | 2 | disc1d/fig_bifurcation.py | 1x2, 6.3x2.4 | |
| 2.12 | disc1d.md:626 | 2 | disc1d/fig_bifurcation.py | 1x2, 6.3x2.4 | |
| 2.16 | disc1d.md:872 | 2 | disc1d/fig_shift_tent.py | 1x2, ratio 3:2, 6.3x2.4 | |
| 2.17 | disc1d.md:934 | 2 | disc1d/fig_shift_tent.py | 1x2, ratio 3:2, 6.3x2.4 | |
| 2.20 | disc1d.md:1178 | 2 | disc1d/fig_analytical_statistical.py | 1x2, 6.3x2.4 | |
| 2.21 | disc1d.md:1212 | 2 | disc1d/fig_universality.py | 1x2, 6.3x2.4 | |
| 2.22 | disc1d.md:1276 | 2 | disc1d/fig_universality.py | 1x2, 6.3x2.4 | |
| 3.1 | disc2d.md:182 | 4 | disc2d/fig_duffing.py | 2x2, ratio 3:2, 6.3x4.4 | |
| 3.3 | disc2d.md:357 | 2 | disc2d/fig_bowl.py | 1x2, 6.3x2.4 | |
| 3.13 | disc2d.md:977 | 2 | disc2d/fig_circlemap.py | 1x2, ratio 3:2, 6.3x2.5 | |
| 3.19 | disc2d.md:1218 | 6 | disc2d/fig_standardmap.py | 2x3, 6.3x4.2, column order | |
| 3.20 | disc2d.md:1273 | 2 | disc2d/fig_standardmap.py | 1x2, 6.3x3.0 | |
| 3.21 | disc2d.md:1327 | 9 | disc2d/fig_standardmap.py | 3x3 shared axes, 6.3x5.5 | |
| 4.1 | cont1d.md:143 | 2 | cont1d/fig_flow_basics.py | 1x2, 6.3x3.0 | |
| 4.2 | cont1d.md:192 | 2 | cont1d/fig_flow_basics.py | 1x2, 6.3x2.4 | |
| 4.3 | cont1d.md:259 | 4 | cont1d/fig_normalforms.py | 1x4, ratios 1:1:1:1.6, 6.3x2.0 | |
| 4.4 | cont1d.md:300 | 4 | cont1d/fig_normalforms.py | as 4.3 | |
| 4.5 | cont1d.md:336 | 4 | cont1d/fig_normalforms.py | as 4.3 | |
| 4.6 | cont1d.md:399 | 4 | cont1d/fig_normalforms.py | as 4.3 | |
| 4.7 | cont1d.md:424 | 5 | cont1d/fig_ferro_pitchfork.py | 3 squares over 2 diagrams, 6.3x4.4 | |
| 4.8 | cont1d.md:508 | 2 | cont1d/fig_ferro_pitchfork.py | 1x2, 6.3x2.6 | reword "in each panel" |
| 4.9 | cont1d.md:613 | 5 | cont1d/fig_ferro_field.py | as 4.7 | |
| 4.10 | cont1d.md:744 | 24 | cont1d/fig_ferro_spins.py | 4x6 image grid, no ticks, 6.3x4.4 | |
| 4.11 | cont1d.md:796 | 2 | cont1d/fig_ferro_spins.py | 1x2, 6.3x2.6 | |
| 4.12 | cont1d.md:816 | 10 | cont1d/fig_hysteresis.py | 2x5 shared y, 6.3x3.2 | reword "left/right column" |
| 4.13 | cont1d.md:905 | 2 | cont1d/fig_hysteresis.py | 1x2, 6.3x3.0 | |
| 4.14 | cont1d.md:983 | 2 | cont1d/fig_climate.py | 1x2, 6.3x2.4 | |
| 5.8 | cont2d.md:543 | 4 | cont2d/fig_conservative_gradient.py | 2x2, 6.3x5.4 | |
| 5.10 | cont2d.md:731 | 2 | cont2d/fig_limit_cycles.py | 1x2, ratio 3:2, 6.3x2.5 | reword (caption is only "Limit cycle") |
| 5.12 | cont2d.md:1142 | 4 | cont2d/fig_pitchfork.py | 2x2, 6.3x4.8 | |
| 5.13 | cont2d.md:1182 | 4 | cont2d/fig_hopf.py | 2x2, 6.3x4.0 | |
| 5.14 | cont2d.md:1246 | 4 | cont2d/fig_global.py | 2x2, 6.3x4.8 | |
| 6.2 | cont3d.md:44 | 2 | cont3d/fig_lorenz.py | 1x2 3-D, 6.3x3.0 | |
| 6.8 | cont3d.md:376 | 2 | cont3d/fig_lorenz.py | 1x2, ratio 3:2, 6.3x2.5 | |
| 6.10 | cont3d.md:466 | 3 | cont3d/fig_poincare_example.py | 1x3, ratios 1:1:1.4, 6.3x2.1 | |
| 6.13 | cont3d.md:556 | 4 | cont3d/fig_rossler.py | 1x4 3-D, 6.3x1.9 | |
| 6.15 | cont3d.md:600 | 2 | cont3d/fig_rossler.py + fig_lorenz.py | 1x2, 6.3x2.4 (one script draws both) | |
| 6.17 | cont3d.md:697 (in box) | 2 | cont3d/fig_forced.py | 1x2, 6.0x2.8 | "a)" to "(a)" |
| 6.18 | cont3d.md:811 | 2 | cont3d/fig_threebody.py | 1x2, 6.3x3.0 | |
| 6.19 | cont3d.md:872 | 5 | cont3d/fig_threebody.py | 4 squares over the Poincare section, 6.3x4.0 | |

### Single-image figures

Target class per figure; "now" is how it looks today in both outputs.

| Fig | source | now | target |
|---|---|---|---|
| 1.1 | phenomenon.md:43 | too large | F 6.3x2.4 |
| 1.4 | phenomenon.md:135 | too large | M 3.8x2.5 |
| 1.6 | phenomenon.md:265 | too tall | S-tall 3.0x4.5 |
| 2.5 | disc1d.md:222 | too small | M |
| 2.7 | disc1d.md:283 | too small | S |
| 2.10, 2.14, 2.23 | disc1d.md:590, 684, 1437 | small | M |
| 2.11, 2.13 | disc1d.md:615, 651 | OK | M |
| 2.15 | disc1d.md:731 | small | M 3.8x3.4 |
| 2.18, 2.19 | disc1d.md:1024, 1054 | too large | F 6.3x2.2 |
| 3.2 | disc2d.md:295 | too small | M 3.8x2.4 |
| 3.4 | disc2d.md:514 | too large | F 6.3x2.3 |
| 3.5, 3.7, 3.8, 3.12, 3.15, 3.16 | disc2d.md:624, 703, 719, 951, 1039, 1159 | too small | S |
| 3.6 | disc2d.md:690 | OK | M |
| 3.9 | disc2d.md:735 | too large | M 3.8x2.5 |
| 3.10 | disc2d.md:747 | too small | M 3.8x2.0 |
| 3.11 | disc2d.md:891 | too small | S 2.5x2.5 |
| 3.14 | disc2d.md:1020 | small | M 3.8x3.4 |
| 3.17 | disc2d.md:1175 | too small | S |
| 3.18, 3.23 | disc2d.md:1192, 1390 | OK | S |
| 3.22 | disc2d.md:1351 | too small | F 6.3x2.8 |
| 5.1 | cont2d.md:92 | OK | F 6.3x2.2 |
| 5.2 | cont2d.md:122 | too small | M |
| 5.3, 5.7, 5.9 | cont2d.md:143, 442, 613 | too small | S |
| 5.4 | cont2d.md:256 | worst: too small | S 2.5x2.4 |
| 5.5 | cont2d.md:267 | OK | F 6.3x4.0 |
| 5.6 | cont2d.md:293 | small | M 3.8x3.4 |
| 5.11 | cont2d.md:807 (in box) | too small | S |
| 6.1 | cont3d.md:29 | OK | F 6.3x2.2 |
| 6.3 | cont3d.md:144 | OK | M |
| 6.4 | cont3d.md:204 | far too large | F 6.3x2.6 |
| 6.5 | cont3d.md:223 | too large | M 3.8x3.8 |
| 6.6, 6.14 | cont3d.md:240, 582 | too large | S |
| 6.7 | cont3d.md:329 | small | M |
| 6.9 | cont3d.md:408 | too small | sketch 2.6x1.9 |
| 6.11 | cont3d.md:508 (in box) | too small | S |
| 6.12 | cont3d.md:544 | too large | S 3.4x3.1 |
| 6.16 | cont3d.md:659 (in box) | too small | M 3.8x1.9 |
| 7.1 | fractals.md:13 | too large | S-tall 3.0x4.2 |
| 7.2 | fractals.md:89 | too large | M 3.8x2.0 |
| 7.3 | fractals.md:109 | too small | F 6.3x1.6 |
| 7.4 | fractals.md:150 | too small | F 6.3x2.1 |
| 7.5, 7.6, 7.7, 7.9 | fractals.md:225, 368, 394, 529 | OK | M |
| 7.8 | fractals.md:510 | too large | F 6.3x3.0 |
| 8.1 | practice.md:20 | too large | F 6.3x3.0 |
| 8.2, 8.6, 8.8, 8.10, 8.11 | practice.md:45, 245, 290, 387, 431 | OK | F 6.3x2.2 to 2.9 |
| 8.3 | practice.md:56 | small | M |
| 8.4 | practice.md:136 | too large and too tall | F 6.3x4.0 |
| 8.5 | practice.md:232 | too large | S |
| 8.7 | practice.md:258 | OK | M |
| 8.9 | practice.md:343 | small | M 3.8x2.9 |
| app_lorenz | app_lorenz.md:57 | too large | M 3.8x2.1 |
| app_lorenz RB_DNS | app_lorenz.md:13 | OK (photo-like, no script) | keep |

Exercise figures (`python/_includes/`): phenomenon ex0036r03 to M; disc1d
ex0093r00 to M; disc2d ex0082r00_1 to a 1.3x1.8 sketch and ex0082r00_2 to M;
cont2d NuclearReactorCooling is a drawing and stays; cont3d ex0089r01_1 to M
3.8x1.9; fractals 7.10 and 7.11 to M; FractalCurve to F 6.3x2.8.

## Order of work

1. Style and saving, once: `book.mplstyle`, the save helpers (PDF + SVG, no
   tight bbox), size classes and `panel_labels` in a shared helper.
2. Figures that break the page: 3.21, 4.12, 1.5, 2.4, 4.7, 4.9, 6.19, 3.19.
3. The author's examples: 2.2, 2.4, 2.5, 2.7, and the chapter 3 singles.
4. Oversized figures: 6.4, 1.1, 2.18, 2.19, 8.4, then the rest of the list.
5. The remaining two-panel figures, chapter by chapter (one PR per chapter).
6. Cookbook notebook: set the figure size in its first cell so outputs are
   about 3.8 in wide.

For each chapter: regenerate, delete every `:width:`/`:height:`, replace
`{subfigure}` with `{figure}`, reword captions where marked, then check the
PDF pages and the HTML page at 1440 px and 390 px before opening the PR.

## Notes on the Maple edition

Not in scope, but found on the way: page overflows at 1.5, 3.21, 4.7, 4.9 and
6.19; ragged subfigure rows in several chapters; the caption of Maple figure
6.19 starts with ". The behaviour".

## Measured printed font size (before the rework)

`creators/python/fontsize_report.py` computes, for every image in a LaTeX
build, the printed width and the scale against its natural size, and from
that the printed tick-label size (11 pt x scale in the old style). On the
book as published on 4 November 2026 (130 figures, About photos excluded):

| tick labels on paper | figures |
|---|---|
| under 7.5 pt (too small) | 37 |
| 7.5 to 9.5 pt (good) | 74 |
| over 9.5 pt (too large) | 19 |

Range: 3.2 pt (Figure 5.4) to 14.0 pt (Figure 6.4), against 11 pt body
text.

Checked against the author's comments on chapters 1 to 3: every figure
called too small prints its tick labels at 4.1 to 7.4 pt (2.5, 2.7, 2.14,
2.23, 2.24, 3.2, 3.5, 3.7, 3.8, 3.10, 3.11, 3.12, 3.14, 3.15, 3.16, 3.17),
every figure called too big at 10.8 to 11.3 pt (1.1, 1.4, 2.18, 2.19, 3.4,
3.9, the exercise 1.3.1 image), and the figures passed without comment at
7.7 to 9.0 pt. Only three figures outside the band went uncommented (2.10
at 6.9, 2.15 at 7.0, 3.22 at 6.5 pt). The cause is the one described above:
`:width:` values copied from the Maple edition onto images of different
size, and subfigures forcing every panel to half the text width.

After the rework every image has scale 1.0, so every figure prints its
tick labels at 9 pt and its axis labels at 10 pt.
