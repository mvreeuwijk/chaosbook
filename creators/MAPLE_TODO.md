# Maple TODO: figures to regenerate once Maple is available

Some figures in the Maple edition showed wrong or out-of-date content. They
currently use the corrected Python figures, copied under the same filenames.
To restore Maple-generated figures, run each script below in Maple. First set
the current directory to the target folder, so that the PNG (and EPS) are
written there:

```maple
currentdir("<repo>/maple/_static/cont2d"):
read "<repo>/creators/cont2d/cont2d_global_phase_corrected.mpl";
read "<repo>/creators/cont2d/cont2d_global_fixed_corrected.mpl";

currentdir("<repo>/maple/_static/cont3d"):
read "<repo>/creators/cont3d/cont3d_LorenzLyapComprehensive_corrected.mpl";
```

| Script | Writes | What was wrong |
|---|---|---|
| `cont2d/cont2d_global_phase_corrected.mpl` | `cont2d_global_phase1.png`, `cont2d_global_phase2.png`, `cont2d_global_r.png` | The old worksheet integrated the clockwise system. The chapter prints the counter-clockwise one (θ̇ = +1). `cont2d_global_r.png` was already consistent, so regenerating it is optional. |
| `cont2d/cont2d_global_fixed_corrected.mpl` | `cont2d_global_fixed.png` | The stability colours were swapped. Black should be stable and grey unstable. |
| `cont3d/cont3d_LorenzLyapComprehensive_corrected.mpl` | `cont3d_LorenzLyapComprehensive.png` (+ `_top`/`_bottom` panels) | Only the top panel existed. The bottom panel (cumulative averages) is now added. |

After running the scripts:

- Compare each new PNG with the Python version in `python/_static/` and check that they agree.
- Each of these PNGs has a `.pdf` twin in `maple/_static/`. The chapters reference the `.png` explicitly, so the build does not use the twins. They currently hold a raster copy of the Python PNG. Regenerate or delete them so they match.
- Delete the intermediate `_top`/`_bottom` PNGs, and update `python_status` in `porting_manifest.csv`.

`cont3d_lorenzphysics` (app_lorenz) is not on this list. It was never
Maple-generated, and both editions use the matplotlib figure from
`creators/python/app_lorenz/fig_lorenzphysics.py`.

## Figures replaced by the Python image, no corrected Maple script yet (figure audit, 2026-11-04)

These Maple images were wrong in content: they did not show what the caption
or the text describes. The Maple edition now uses the Python PNG of the same
basename. Where a `.pdf` twin exists it was rewritten as a raster copy of that
PNG. No corrected `.mpl` script was written, because each fix needs more than
a one-line change to the worksheet. When Maple is available, change the
worksheet as described, regenerate the PNG (and PDF), compare it with
`python/_static/`, and remove the note from `python_status` in
`porting_manifest.csv`.

| Figure (`maple/_static/...`) | Maple source | What was wrong | What the worksheet must change |
|---|---|---|---|
| `phenomenon/3body.png` | none (xfig schematic) | No labels: m1–m3, x1–x3, O and the difference vectors, which the text uses, were missing. | Redraw with the labels of `creators/python/phenomenon/fig_schematics.py`, or keep the Python schematic. |
| `practice/practice_horizon.png` | `creators/practice/make_figures.py` (Python) | The horizon marker sat at t ≈ 8.7 (the first time the spread exceeded 0.4 × saturation), but the text defines t_h by the extrapolated exponential reaching the attractor size (≈ 10). | Fixed in `make_figures.py` (t_h = ln(sat/δ0)/Λe). Rerunning it gives a different random ensemble from the Python figure; either is correct. |
| `disc1d/disc1d_shiftmap_series.png` | `disc1d/disc1d_shiftmap_series.mws` | Garbled axis labels ("l[l]", "l"); the x label collided with the tick 200. | Use `labels=["n", "y[n]"]` and re-export with a margin. |
| `disc1d/disc1d_logist_lyap_bifurcation.png` | `disc1d/disc1d_logist_lyap_bifurcation.mws` | Λ(r) was drawn on the x(r) axis with no Λ scale and clipped at −1, so the "very negative" values in the text were not visible. | Two stacked panels: x(r) on top, Λ(r) below with its own axis (view down to about −2). |
| `disc2d/disc2d_circle.png` | `disc2d/disc2d_circlemap.mw` | The π tick labels rendered as "≠" (≠/2, ≠, 3≠/2). | Fix the symbol font on export (or typeset the labels as `typeset(Pi/2)` etc.). |
| `disc2d/disc2d_circlemap_return_p2.png` | `disc2d/disc2d_circlemap.mw` | A spurious thick vertical line at x = 0, a wrap-around artefact of `f2mod1`, although `discont=true` is set. | Plot f(f(x)) piecewise between the jumps of the mod-1 operation, or remove points where the value jumps by more than 1/2. |
| `disc2d/disc2d_circlemap_bifurcation.png` | `disc2d/disc2d_circlemap.mw` | Bifurcation diagram and Λ overlaid in one frame with no Λ axis; the axis label was clipped to "Omeg". | Two stacked panels: x(Ω) on top, Λ(Ω) below, with the Ω label in full. |
| `disc2d/disc2d_kickedrotor.png` | `disc2d/disc2d_kickedrotor.mw` | The sketch lacked the θ and r labels the text uses, and labelled the vertical axis "J". | Add the θ arc and r label, label the vertical axis z, as in `creators/python/disc2d/fig_schematics.py`. |
| `fractals/fractals_boxcount_fit.png` | none (matplotlib) | The fit gave slope −1.90, but the text says the procedure recovers log 3/log 2 = 1.585 for the gasket. | Nothing in Maple; the Python figure (slope −1.57) is the reference. |
| `fractals/fractals_tnti.png` | none (matplotlib) | A stray detached dash at the left end of the r = 0.3 curve in (b). | Nothing in Maple; the Python figure is the reference. |

Pending:

- `exercises/ex0036r03_fig1.png` (three-body exercise): the pstex text layer
  was lost, so the schematic has no labels (earth, moon, satellite, R, x, y).
  The Python figure has been redrawn with the labels
  (`creators/python/exercises/fig_exercises.py`); the Maple image is left
  as it is until the Maple figures are regenerated.

Fixed in the Maple text rather than the image (no Maple change needed):
the hysteresis figure now includes the ten existing Maple panels; the
three-body sensitivity figure includes the existing co-rotating panel
`phenomenon_3body_example_sensitivity_corot.png`; the standard-map chaotic
start is (0.05, 0.4), as in `disc2d/disc2d_standardmap.mw`; the reactor
exercise uses `exercises/NuclearReactorCooling.png`; and the cookbook code
and printed output now match its images (`x=-2..3`, the list `p`, `r := 3.5`,
the phase-portrait initial conditions).

## Cosmetic problems in Maple images (figure audit, 2026-11-04)

These images show the right content but are hard to read. Fix them when the
worksheets are rerun; none needs a text change.

| Figure (`maple/_static/...`) | Problem |
|---|---|
| `phenomenon/phenomenon_3body_example{1a..3b}.png` | The "y/R" label is clipped at the left edge of the left-column panels. |
| `practice/practice_assimilation.png` | The legend of the RMS-error panel overlaps the curves at t ≈ 10.5-12. |
| `disc1d/disc1d_not_so_universal.png` | No axis labels (δ, η). |
| `disc1d/disc1d_logist_return_*`, `tentmap_returnplot`, `shiftmap_returnplot`, `unknownmapping_{return,series}_*`, `logist_lyap_r39_lin` | Rotated y-labels clipped or printed over the ticks; `logist_lyap_r39_lin` has no legend for the o/+ markers. |
| `disc2d/disc2d_standardmap_{quasi,chaos}_deviations.png` | The n-axis is drawn at the top, with clipped labels. |
| `cont1d/cont1d_generic_graphical_unstable.png` | The unstable fixed point is a grey disc; elsewhere it is an open circle. |
| `cont1d/` normal-form and ferromagnet panels | Axis labels and ticks sit inside the plot, crossed by the curves (re-export with boxed axes). |
| `cont2d/` pitchfork, global and Hopf panels | Labels and ticks collide with the curves. |
| `cont3d/` Lorenz, Rössler, Poincaré and double-well figures | Labels Z_n, x[n] instead of z_n, x_n; labels inside the plots; some clipped. |
| `cont3d/cont4d_3body_traj1-4.png` | No y-axis label (y/R). |
| `app_cookbook`: `cookbook_plot_lines2.png` | A title "y=sin(ax)" that the printed code does not request. |

Open question: in `cont3d_lorenzlyapattractor.png` the Maple and Python
editions mark different regions (Python: circles for Λe > 6 on the outer rims
of the lobes; Maple: circles near the z-axis at z ≈ 30-45). The Python script
computes Λe from the formula in the text and its picture matches the caption,
so the Maple worksheet is the one to check.
