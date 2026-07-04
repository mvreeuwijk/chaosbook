# `creators/` - Maple figure sources & Python-porting guide

This folder contains **every Maple worksheet that generates a figure in the book**, one
subfolder per chapter, together with the machine-readable figure->script mapping and the
reference material needed to re-implement each figure in Python.

The worksheets are the *ground truth* for what each figure shows: the model equations,
parameter values, initial conditions, integration ranges and plot styling all live inside
them. This guide plus `MODELS.md` summarise that content so a port can be written without
first reverse-engineering Maple.

## Contents

```
creators/
  README.md               <- this file
  MODELS.md               <- canonical equations & parameters for every system used
  figure_maple_map.csv    <- figure_file -> maple_script (+ confidence)
  porting_manifest.csv    <- figure_file -> script, model, plot_type, caption  (richest file)
  phenomenon/  disc1d/  disc2d/  cont1d/  cont2d/  cont3d/   <- the .mws / .mw worksheets
```

Two Maple formats are present:
- **`.mws`** - legacy Maple worksheet (a text container; command text is stored inside
  `MPLTEXT` tokens and long strings/filenames are wrapped across lines).
- **`.mw`**  - newer XML Maple worksheet (`<Worksheet>...`); cleaner to parse.

## How the mapping was built

Each worksheet exports its figures with a call of the form

```
plotsetup(ps, plotoutput=`cont2d_LV_time.eps`, plotoptions=`portrait,noborder`);
print(<plot>);
plotsetup(default);
```

The book's `\includegraphics{Figs_<chapter>/<name>}` calls were matched to the worksheet
whose `plotoutput` writes `<name>`. Where a worksheet doesn't state the name explicitly the
match falls back to the naming convention (numbered variants such as `cont2d_LV.mws ..
cont2d_LV7.mws` all regenerate the same `cont2d_LV_*` figures). See the `confidence` column:

| confidence | meaning |
|------------|---------|
| `high`   | script explicitly writes the figure file (verified from `plotoutput`) |
| `medium` | inferred from figure/script naming convention |
| `n/a`    | no Maple script - figure is a hand-drawn schematic (xfig/TikZ) |
| `review` | best guess, please confirm |

## Recommended Python port layout

A clean, test-friendly structure that mirrors this folder:

```
chaos/                     # library: the maths, no plotting
  maps.py                  # logistic, sine, tent, Henon, standard, circle ... (x_{n+1}=f(x_n))
  flows.py                 # RHS functions f(t,x) for Lotka-Volterra, van der Pol, Lorenz, Rossler ...
  bifurcation.py           # bifurcation-diagram & Lyapunov helpers
  analysis.py              # cobweb, return map, Poincare section, invariant density helpers
figures/                   # one function per book figure, imports chaos/, saves to _static/
  cont2d.py  disc1d.py ...
tests/
```

Keep the *model* (in `chaos/`) separate from the *figure* (in `figures/`); most book
figures are just a different view (time series / phase / cobweb / bifurcation) of a handful
of shared systems catalogued in `MODELS.md`.

## Maple -> Python translation cheat-sheet

| Maple | Python equivalent |
|-------|-------------------|
| `dsolve({odes, ics}, numeric)` | `scipy.integrate.solve_ivp(f, tspan, x0, dense_output=True, rtol=1e-9)` |
| `DEtools[DEplot]` (phase portrait) | integrate several `x0`, then `matplotlib` `plot`/`quiver` |
| `plots[odeplot]` | `plt.plot(sol.t, sol.y[i])` |
| `plots[implicitplot]` (nullclines, contours) | `plt.contour(X, Y, F, levels=[0])` |
| `plots[fieldplot]` (direction field) | `plt.quiver(X, Y, U, V)` |
| `plots[pointplot]` / iterated map | `np.fromiter` iteration, `plt.plot(marker='.')` |
| `fsolve` / `solve` (fixed points) | `scipy.optimize.brentq` / `fsolve`, or `sympy.solve` for exact |
| `eigenvals(Jacobian)` | `numpy.linalg.eigvals(J)` |
| `plotsetup(ps, plotoutput=`name.eps`)` ... `plotsetup(default)` | `fig.savefig("name.pdf")` (use PDF/SVG for the Python build) |
| Maple 1-based, `seq(...)` | Python 0-based, list/`numpy` comprehension |

Practical notes for the port:
- **Determinism.** Reproduce the exact parameters/initial conditions from the worksheet (and
  `MODELS.md`) so ported figures overlay the originals; chaotic runs diverge otherwise.
- **Bifurcation diagrams.** Standard recipe: for each parameter value iterate the map ~1000
  steps, discard the first ~500 (transient), scatter-plot the rest.
- **Lyapunov exponents.** 1-D map: average `log|f'(x_n)|`. Flows: integrate the variational
  equation alongside the state and periodically re-orthonormalise (Benettin).
- **Poincare sections.** Use `solve_ivp` event functions (`event.terminal=False`) to detect
  plane crossings instead of Maple's manual sampling.
- **Output format.** The originals are EPS; emit PDF or SVG from Python and point Sphinx/MyST
  at the new asset names (they can keep the same basename).

---

## Per-chapter script index

Auto-generated from the mapping. "Figures" lists the book figure basenames each worksheet
produces. See `porting_manifest.csv` for the full per-figure table with captions.


### Phenomenon (intro: Lorenz & three-body)

| Maple script | # | Model | Figures produced |
|--------------|---|-------|------------------|
| `phenomenon_3body_examples.mw` | 8 | three-body / restricted problem | `phenomenon_3body_example1a`, `phenomenon_3body_example1b`, `phenomenon_3body_example2a`, `phenomenon_3body_example2b`, `phenomenon_3body_example3a`, `phenomenon_3body_example3b`, `phenomenon_3body_example_sensitivity`, `phenomenon_3body_example_sensitivity_corot` |
| `phenomenon_lorenz.mw` | 5 | Lorenz system | `phenomenon_lorenz_phasespace_close`, `phenomenon_lorenz_phasespace_far`, `phenomenon_lorenz_xt_series`, `phenomenon_lorenz_xt_two_series_em3`, `phenomenon_lorenz_xt_two_series_em5` |

> Hand-drawn schematics (no Maple source): `3body`


### disc1d - one-dimensional maps

| Maple script | # | Model | Figures produced |
|--------------|---|-------|------------------|
| `disc1d_unknownmapping.mws` | 6 | Henon map, sine map | `disc1d_unknownmapping_return_henon`, `disc1d_unknownmapping_return_noise`, `disc1d_unknownmapping_return_sin3map`, `disc1d_unknownmapping_series_henon`, `disc1d_unknownmapping_series_noise`, `disc1d_unknownmapping_series_sin3map` |
| `disc1d_logist_return.mws` | 4 | logistic map | `disc1d_logist_return_r1_5`, `disc1d_logist_return_r3_2`, `disc1d_logist_return_r3_5`, `disc1d_logist_return_r3_9` |
| `disc1d_logist_series.mws` | 4 | logistic map | `disc1d_logist_series_r1_5`, `disc1d_logist_series_r3_2`, `disc1d_logist_series_r3_5`, `disc1d_logist_series_r3_9` |
| `disc1d_logist_cobweb.mws` | 3 | logistic map | `disc1d_logist_cobweb_r2_7`, `disc1d_logist_cobweb_r3_2`, `disc1d_logist_cobweb_r3_9` |
| `disc1d_logist_series_bifurcation.mws` | 3 | logistic map | `disc1d_logist_series_bifurcation`, `disc1d_logist_series_bifurcation_zoom_doubling`, `disc1d_logist_series_bifurcation_zoom_p3` |
| `disc1d_logist_attractor_local.mws` | 2 | logistic map | `disc1d_logist_attractor_local_r1_5`, `disc1d_logist_attractor_local_r2_0` |
| `disc1d_logist_lyap.mws` | 2 | logistic map | `disc1d_logist_lyap_r39_lin`, `disc1d_logist_lyap_r39_log` |
| `disc1d_logist_p3graph.mws` | 2 | logistic map | `disc1d_logist_p3graph_r380`, `disc1d_logist_p3graph_r384` |
| `disc1d_shiftmap_series.mws` | 2 | - | `disc1d_shiftmap_returnplot`, `disc1d_shiftmap_series` |
| `disc1d_tentmap.mws` | 2 | tent map | `disc1d_tentmap_returnplot`, `disc1d_tentmap_series` |
| `disc1d_bifurcation_implicit_sin.mws` | 1 | - | `disc1d_bifurcation_implicit_sin` |
| `disc1d_doubling_logist.mw` | 1 | logistic map | `disc1d_doubling_logist` |
| `disc1d_doubling_sinmap.mw` | 1 | sine map | `disc1d_doubling_sinmap` |
| `disc1d_logist_analytical.mw` | 1 | logistic map | `disc1d_logist_analytical` |
| `disc1d_logist_attractor.mws` | 1 | logistic map | `disc1d_logist_attractor_r1_5` |
| `disc1d_logist_bifur_theo.mws` | 1 | logistic map | `disc1d_logist_bifur_theo` |
| `disc1d_logist_lyap_bifurcation.mws` | 1 | logistic map | `disc1d_logist_lyap_bifurcation` |
| `disc1d_logist_p2graph.mws` | 1 | logistic map | `disc1d_logist_p2graph` |
| `disc1d_logist_pdf.mw` | 1 | logistic map | `disc1d_logist_pdf` |
| `disc1d_logist_stability_p3both.mws` | 1 | logistic map | `disc1d_logist_stability_p3both` |
| `disc1d_not_so_universal.mws` | 1 | - | `disc1d_not_so_universal` |
| `disc1d_sin3map_pdf.mw` | 1 | sine map | `disc1d_sin3map_pdf` |
| `disc1d_tanh_analytical.mw` | 1 | - | `disc1d_tanh_analytical` |
| `disc1d_universality_logist.mw` | 1 | logistic map | `disc1d_universality_logist` |
| `disc1d_universality_sinmap.mw` | 1 | sine map | `disc1d_universality_sinmap` |

### disc2d - two-dimensional maps

| Maple script | # | Model | Figures produced |
|--------------|---|-------|------------------|
| `disc2d_standardmap_saddlenode.mw` | 11 | standard (Chirikov) map | `disc2d_manifolds`, `disc2d_standardmap_manifolds`, `disc2d_standardmap_saddlenode_n=-3`, `disc2d_standardmap_saddlenode_n=-4`, `disc2d_standardmap_saddlenode_n=-5`, `disc2d_standardmap_saddlenode_n=-6`, `disc2d_standardmap_saddlenode_n=0`, `disc2d_standardmap_saddlenode_n=3`, `disc2d_standardmap_saddlenode_n=4`, `disc2d_standardmap_saddlenode_n=5`, `disc2d_standardmap_saddlenode_n=6` |
| `disc2d_standardmap.mw` | 8 | standard (Chirikov) map | `disc2d_standardmap_chaos`, `disc2d_standardmap_chaos_deviations`, `disc2d_standardmap_chaos_return`, `disc2d_standardmap_phase`, `disc2d_standardmap_phasetorus`, `disc2d_standardmap_quasi`, `disc2d_standardmap_quasi_deviations`, `disc2d_standardmap_quasi_return` |
| `disc2d_DuffingMap_series.mw` | 6 | Duffing oscillator | `disc2d_Duffing_bifurx`, `disc2d_Duffing_bifury`, `disc2d_Duffing_phase1`, `disc2d_Duffing_phase2`, `disc2d_Duffing_series1`, `disc2d_Duffing_series2` |
| `disc2d_HenonStretchContract.mw` | 6 | Henon map | `disc2d_HenonStretch0`, `disc2d_HenonStretch12`, `disc2d_HenonStretch16`, `disc2d_HenonStretch20`, `disc2d_HenonStretch4`, `disc2d_HenonStretch8` |
| `disc2d_circlemap.mw` | 6 | circle map | `disc2d_circle`, `disc2d_circlemap_bifurcation`, `disc2d_circlemap_lyapunov`, `disc2d_circlemap_return_p2`, `disc2d_circlemap_series`, `disc2d_circlemap_winding` |
| `disc2d_HenonFold.mw` | 5 | Henon map | `disc2d_HenonFold0`, `disc2d_HenonFold1`, `disc2d_HenonFold2`, `disc2d_HenonFold3`, `disc2d_HenonFold4` |
| `disc2d_kickedrotor.mw` | 4 | kicked rotor | `disc2d_kickedrotor`, `disc2d_kickedrotor_delta`, `disc2d_kickedrotor_theta`, `disc2d_kickedrotor_v` |
| `disc2d_Paraball.mw` | 3 | particle-in-a-bowl map | `disc2d_bowl_chaos`, `disc2d_bowl_energies`, `disc2d_bowl_periodic` |
| `disc2d_lincirclemap.mw` | 3 | circle map | `disc2d_lincircle_cobweb`, `disc2d_lincircle_quasi`, `disc2d_lincircle_quasi_cobweb` |
| `HenonStretchfoldHJrnd.mw` | 1 | Henon map | `disc2d_HenonFold5` |
| `disc2d_HenonAttractor.mw` | 1 | Henon map | `disc2d_HenonAttractor` |
| `disc2d_HenonLyap.mw` | 1 | Henon map | `disc2d_HenonLyap` |

> Needs review: `disc2d_manifolds` -> disc2d_standardmap_saddlenode.mw


### cont1d - one-dimensional flows

| Maple script | # | Model | Figures produced |
|--------------|---|-------|------------------|
| `cont1d_FerroSpins.mw` | 26 | mean-field ferromagnet | `cont1d_ferro_spin_T_0_50`, `cont1d_ferro_spin_T_0_50_a0`, `cont1d_ferro_spin_T_0_50_a1`, `cont1d_ferro_spin_T_0_50_a2`, `cont1d_ferro_spin_T_0_50_a3`, `cont1d_ferro_spin_T_0_50_a4`, `cont1d_ferro_spin_T_0_50_a5`, `cont1d_ferro_spin_T_0_50_b0`, `cont1d_ferro_spin_T_0_50_b1`, `cont1d_ferro_spin_T_0_50_b2`, `cont1d_ferro_spin_T_0_50_b3`, `cont1d_ferro_spin_T_0_50_b4`, `cont1d_ferro_spin_T_0_50_b5`, `cont1d_ferro_spin_T_1_50`, `cont1d_ferro_spin_T_1_50_a0`, `cont1d_ferro_spin_T_1_50_a1`, `cont1d_ferro_spin_T_1_50_a2`, `cont1d_ferro_spin_T_1_50_a3`, `cont1d_ferro_spin_T_1_50_a4`, `cont1d_ferro_spin_T_1_50_a5`, `cont1d_ferro_spin_T_1_50_b0`, `cont1d_ferro_spin_T_1_50_b1`, `cont1d_ferro_spin_T_1_50_b2`, `cont1d_ferro_spin_T_1_50_b3`, `cont1d_ferro_spin_T_1_50_b4`, `cont1d_ferro_spin_T_1_50_b5` |
| `cont1d_ferro_field_hysteresis.mw` | 11 | mean-field ferromagnet | `cont1d_ferro_field_hysdata_T_0_5`, `cont1d_ferro_field_hysdata_T_0_75`, `cont1d_ferro_field_hysdata_T_1_0`, `cont1d_ferro_field_hysdata_T_1_25`, `cont1d_ferro_field_hysdata_T_1_5`, `cont1d_ferro_field_hysteresis_T_0_5`, `cont1d_ferro_field_hysteresis_T_0_75`, `cont1d_ferro_field_hysteresis_T_1_0`, `cont1d_ferro_field_hysteresis_T_1_25`, `cont1d_ferro_field_hysteresis_T_1_5`, `cont1d_ferro_field_hysteresis_zoom` |
| `cont1d_bifur_pitchfork.mw` | 8 | pitchfork normal form | `cont1d_bifur_pitchfork`, `cont1d_bifur_pitchfork1`, `cont1d_bifur_pitchfork2`, `cont1d_bifur_pitchfork3`, `cont1d_bifur_pitchfork_sub`, `cont1d_bifur_pitchfork_sub1`, `cont1d_bifur_pitchfork_sub2`, `cont1d_bifur_pitchfork_sub3` |
| `cont1d_ferro_field_bifurcation.mw` | 5 | mean-field ferromagnet | `cont1d_ferro_field_bifurcation1`, `cont1d_ferro_field_bifurcation2`, `cont1d_ferro_field_bifurcation3`, `cont1d_ferro_field_bifurcation_large_m`, `cont1d_ferro_field_bifurcation_small_m` |
| `cont1d_ferro_pitchfork.mw` | 5 | mean-field ferromagnet | `cont1d_ferro_pitchfork`, `cont1d_ferro_pitchfork1`, `cont1d_ferro_pitchfork2`, `cont1d_ferro_pitchfork3`, `cont1d_ferro_pitchfork_stability` |
| `cont1d_saddle.mw` | 4 | saddle-node normal form | `cont1d_bifur_saddle`, `cont1d_bifur_saddle1`, `cont1d_bifur_saddle2`, `cont1d_bifur_saddle3` |
| `cont1d_transcrit.mw` | 4 | transcritical normal form | `cont1d_bifur_transcrit`, `cont1d_bifur_transcrit1`, `cont1d_bifur_transcrit2`, `cont1d_bifur_transcrit3` |
| `cont1d_climate_single_fp.mw` | 2 | energy-balance climate model | `cont1d_climate_multiple_fp`, `cont1d_climate_single_fp` |
| `cont1d_ferro_pitch_numerical.mw` | 2 | mean-field ferromagnet | `cont1d_ferro_pitch_evolution1`, `cont1d_ferro_pitch_evolution2` |
| `cont1d_generic_graphical.mw` | 2 | generic 1-D flow | `cont1d_generic_graphical_stable`, `cont1d_generic_graphical_unstable` |
| `normalforms.mws` | 2 | cubic normal form | `cont1d_simplecubic_evolution`, `cont1d_simplecubic_graph` |
| `cont1d_ferro_field_hysteresis_3d.mw` | 1 | mean-field ferromagnet | `cont1d_ferro_field_hysteresis_3d` |

### cont2d - two-dimensional flows

| Maple script | # | Model | Figures produced |
|--------------|---|-------|------------------|
| `cont2d_Hopf.mws` | 4 | Hopf-bifurcation system | `cont2d_Hopf_phase1`, `cont2d_Hopf_phase2`, `cont2d_Hopf_time1`, `cont2d_Hopf_time2` |
| `cont2d_gradient2.mws` | 4 | gradient system | `cont2d_gradient_ell1`, `cont2d_gradient_ell2`, `cont2d_gradient_hyp1`, `cont2d_gradient_hyp2` |
| `cont2d_global.mws` | 3 | - | `cont2d_global_phase1`, `cont2d_global_phase2`, `cont2d_global_r` |
| `cont2d_Hopf2.mws` | 2 | Hopf-bifurcation system | `cont2d_Hopf_ev1`, `cont2d_Hopf_ev2` |
| `cont2d_LV.mws` | 2 | Lotka-Volterra predator-prey | `cont2d_LV_phase`, `cont2d_LV_time` |
| `cont2d_LV_Allee2.mws` | 2 | Lotka-Volterra predator-prey | `cont2d_LV_Allee_stab_Im`, `cont2d_LV_Allee_stab_Re` |
| `cont2d_LV_Allee5.mws` | 2 | Lotka-Volterra predator-prey | `cont2d_LV_Allee_extinct1`, `cont2d_LV_Allee_extinct2` |
| `cont2d_pitchfork.mw` | 2 | pitchfork normal form | `cont2d_pitchfork_fixed`, `cont2d_pitchfork_stab` |
| `cont2d_pitchfork5.mws` | 2 | pitchfork normal form | `cont2d_pitchfork_phase1`, `cont2d_pitchfork_phase2` |
| `cont2d_LV6.mws` | 1 | Lotka-Volterra predator-prey | `cont2d_LV_E` |
| `cont2d_Limit.mws` | 1 | - | `cont2d_Limit_phase` |
| `cont2d_Limit2.mws` | 1 | - | `cont2d_Limit_time` |
| `cont2d_conservative.mws` | 1 | conservative system (double well) | `cont2d_conservative_E` |
| `cont2d_global2.mws` | 1 | - | `cont2d_global_fixed` |
| `cont2d_vdPol.mws` | 1 | van der Pol oscillator | `cont2d_vdPol_phase` |

> Hand-drawn schematics (no Maple source): `cont2d_phasespace`, `cont2d_phase_r1`, `cont2d_phase_r2`, `cont2d_phase_r3`, `cont2d_phase_i1`, `cont2d_phase_i2`, `cont2d_phase_i3`, `cont2d_classification`, `cont2d_zoo`


> Needs review: `cont2d_zoo` -> (review - no maple script found)


### cont3d - three-dimensional flows

| Maple script | # | Model | Figures produced |
|--------------|---|-------|------------------|
| `cont3d_lorenz.mw` | 13 | Lorenz system | `cont3d_LorenzLyapComprehensive`, `cont3d_LorenzLyapCumulative`, `cont3d_LorenzLyapEffective`, `cont3d_lorenz_attraction`, `cont3d_lorenz_attractor`, `cont3d_lorenz_attractoryz`, `cont3d_lorenz_lyapunov`, `cont3d_lorenz_map`, `cont3d_lorenz_poincare`, `cont3d_lorenz_time`, `cont3d_lorenz_zmax`, `cont3d_lorenzlyapattractor`, `cont3d_lyap_formal` |
| `cont3d_rossler.mw` | 12 | Rossler system | `cont3d_rosslerattractor`, `cont3d_rosslerbifurcation`, `cont3d_rosslerperiod1a`, `cont3d_rosslerperiod1b`, `cont3d_rosslerperiod2a`, `cont3d_rosslerperiod2b`, `cont3d_rosslerperiod3a`, `cont3d_rosslerperiod3b`, `cont3d_rosslerperiod4a`, `cont3d_rosslerperiod4b`, `cont3d_rosslerreturn`, `cont3d_rosslertopology` |
| `cont4d_3body.mw` | 7 | three-body / restricted problem | `cont4d_3body_Poincare`, `cont4d_3body_V`, `cont4d_3body_Vcut`, `cont4d_3body_traj1`, `cont4d_3body_traj2`, `cont4d_3body_traj3`, `cont4d_3body_traj4` |
| `cont3d_poincare_example.mw` | 4 | - | `cont3d_poincare_exmap`, `cont3d_poincare_exphase`, `cont3d_poincare_exseq`, `cont3d_poincaresection` |
| `cont3d_forced.mws` | 3 | double-well potential | `cont3d_doublewell`, `cont3d_doublewell_phasespace`, `cont3d_doublewell_poincare` |
| `new.mw` | 1 | Lorenz system | `cont3d_lorenz_bifurcation` |