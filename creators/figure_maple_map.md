# Figure → Maple script mapping

Links each figure used in the book chapters to the Maple worksheet that generates it. Maple scripts live in `latexsource/Figs_<chapter>/creators/`.

**Confidence:** *high* = the script explicitly writes this figure file (verified from the `plotsetup(..., plotoutput=...)` call inside the worksheet); *medium* = inferred from the figure/script naming convention (a numbered-variant or shared-stem script family); *n/a* = no Maple script found, figure is a hand-drawn schematic; *REVIEW* = best guess, please confirm.


## Chapter: Phenomenon

| # | Figure file | Maple script (in `Figs_phenomenon/creators/`) | Confidence |
|---|-------------|----------------------------------------|------------|
| 1 | `phenomenon_lorenz_xt_series` | phenomenon_lorenz.mw | high |
| 2 | `phenomenon_lorenz_xt_two_series_em3` | phenomenon_lorenz.mw | high |
| 3 | `phenomenon_lorenz_xt_two_series_em5` | phenomenon_lorenz.mw | high |
| 4 | `phenomenon_lorenz_phasespace_close` | phenomenon_lorenz.mw | high |
| 5 | `phenomenon_lorenz_phasespace_far` | phenomenon_lorenz.mw | high |
| 6 | `3body` | (no maple script - xfig/manual schematic) | n/a |
| 7 | `phenomenon_3body_example1a` | phenomenon_3body_examples.mw | high |
| 8 | `phenomenon_3body_example1b` | phenomenon_3body_examples.mw | high |
| 9 | `phenomenon_3body_example2a` | phenomenon_3body_examples.mw | high |
| 10 | `phenomenon_3body_example2b` | phenomenon_3body_examples.mw | high |
| 11 | `phenomenon_3body_example3a` | phenomenon_3body_examples.mw | high |
| 12 | `phenomenon_3body_example3b` | phenomenon_3body_examples.mw | high |
| 13 | `phenomenon_3body_example_sensitivity` | phenomenon_3body_examples.mw | high |
| 14 | `phenomenon_3body_example_sensitivity_corot` | phenomenon_3body_examples.mw | high |

## Chapter: 1-D discrete maps (disc1d)

| # | Figure file | Maple script (in `Figs_disc1d/creators/`) | Confidence |
|---|-------------|----------------------------------------|------------|
| 1 | `disc1d_logist_series_r1_5` | disc1d_logist_series.mws | high |
| 2 | `disc1d_logist_series_r3_2` | disc1d_logist_series.mws | high |
| 3 | `disc1d_logist_series_r3_5` | disc1d_logist_series.mws | high |
| 4 | `disc1d_logist_series_r3_9` | disc1d_logist_series.mws | high |
| 5 | `disc1d_logist_cobweb_r2_7` | disc1d_logist_cobweb.mws | high |
| 6 | `disc1d_logist_cobweb_r3_2` | disc1d_logist_cobweb.mws | high |
| 7 | `disc1d_logist_cobweb_r3_9` | disc1d_logist_cobweb.mws | high |
| 8 | `disc1d_logist_return_r1_5` | disc1d_logist_return.mws | high |
| 9 | `disc1d_logist_return_r3_2` | disc1d_logist_return.mws | high |
| 10 | `disc1d_logist_return_r3_5` | disc1d_logist_return.mws | high |
| 11 | `disc1d_logist_return_r3_9` | disc1d_logist_return.mws | high |
| 12 | `disc1d_unknownmapping_series_henon` | disc1d_unknownmapping.mws | high |
| 13 | `disc1d_unknownmapping_return_henon` | disc1d_unknownmapping.mws | high |
| 14 | `disc1d_unknownmapping_series_noise` | disc1d_unknownmapping.mws | high |
| 15 | `disc1d_unknownmapping_return_noise` | disc1d_unknownmapping.mws | high |
| 16 | `disc1d_unknownmapping_series_sin3map` | disc1d_unknownmapping.mws | high |
| 17 | `disc1d_unknownmapping_return_sin3map` | disc1d_unknownmapping.mws | high |
| 18 | `disc1d_logist_attractor_r1_5` | disc1d_logist_attractor.mws | high |
| 19 | `disc1d_logist_attractor_local_r2_0` | disc1d_logist_attractor_local.mws | high |
| 20 | `disc1d_logist_attractor_local_r1_5` | disc1d_logist_attractor_local.mws | high |
| 21 | `disc1d_logist_p2graph` | disc1d_logist_p2graph.mws | high |
| 22 | `disc1d_logist_p3graph_r380` | disc1d_logist_p3graph.mws | high |
| 23 | `disc1d_logist_p3graph_r384` | disc1d_logist_p3graph.mws | high |
| 24 | `disc1d_logist_bifur_theo` | disc1d_logist_bifur_theo.mws | high |
| 25 | `disc1d_logist_stability_p3both` | disc1d_logist_stability_p3both.mws | high |
| 26 | `disc1d_bifurcation_implicit_sin` | disc1d_bifurcation_implicit_sin.mws | high |
| 27 | `disc1d_logist_series_bifurcation` | disc1d_logist_series_bifurcation.mws | high |
| 28 | `disc1d_logist_series_bifurcation_zoom_doubling` | disc1d_logist_series_bifurcation.mws | high |
| 29 | `disc1d_logist_series_bifurcation_zoom_p3` | disc1d_logist_series_bifurcation.mws | high |
| 30 | `disc1d_logist_lyap_r39_lin` | disc1d_logist_lyap.mws | high |
| 31 | `disc1d_logist_lyap_r39_log` | disc1d_logist_lyap.mws | high |
| 32 | `disc1d_logist_lyap_bifurcation` | disc1d_logist_lyap_bifurcation.mws | high |
| 33 | `disc1d_shiftmap_series` | disc1d_shiftmap_series.mws | high |
| 34 | `disc1d_shiftmap_returnplot` | disc1d_shiftmap_series.mws | high |
| 35 | `disc1d_tentmap_series` | disc1d_tentmap.mws | high |
| 36 | `disc1d_tentmap_returnplot` | disc1d_tentmap.mws | high |
| 37 | `disc1d_logist_analytical` | disc1d_logist_analytical.mw | high |
| 38 | `disc1d_tanh_analytical` | disc1d_tanh_analytical.mw | high |
| 39 | `disc1d_logist_pdf` | disc1d_logist_pdf.mw | high |
| 40 | `disc1d_sin3map_pdf` | disc1d_sin3map_pdf.mw | high |
| 41 | `disc1d_doubling_logist` | disc1d_doubling_logist.mw | high |
| 42 | `disc1d_doubling_sinmap` | disc1d_doubling_sinmap.mw | high |
| 43 | `disc1d_universality_logist` | disc1d_universality_logist.mw | high |
| 44 | `disc1d_universality_sinmap` | disc1d_universality_sinmap.mw | high |
| 45 | `disc1d_not_so_universal` | disc1d_not_so_universal.mws | high |

## Chapter: 2-D discrete maps (disc2d)

| # | Figure file | Maple script (in `Figs_disc2d/creators/`) | Confidence |
|---|-------------|----------------------------------------|------------|
| 1 | `disc2d_Duffing_series1` | disc2d_DuffingMap_series.mw | high |
| 2 | `disc2d_Duffing_phase1` | disc2d_DuffingMap_series.mw | high |
| 3 | `disc2d_Duffing_series2` | disc2d_DuffingMap_series.mw | high |
| 4 | `disc2d_Duffing_phase2` | disc2d_DuffingMap_series.mw | high |
| 5 | `disc2d_Duffing_bifurx` | disc2d_DuffingMap_series.mw | high |
| 6 | `disc2d_Duffing_bifury` | disc2d_DuffingMap_series.mw | high |
| 7 | `disc2d_bowl_chaos` | disc2d_Paraball.mw | high |
| 8 | `disc2d_bowl_periodic` | disc2d_Paraball.mw | high |
| 9 | `disc2d_bowl_energies` | disc2d_Paraball.mw | high |
| 10 | `disc2d_HenonAttractor` | disc2d_HenonAttractor.mw | high |
| 11 | `disc2d_HenonLyap` | disc2d_HenonLyap.mw | high |
| 12 | `disc2d_HenonFold0` | disc2d_HenonFold.mw | high |
| 13 | `disc2d_HenonFold1` | disc2d_HenonFold.mw | high |
| 14 | `disc2d_HenonFold2` | disc2d_HenonFold.mw | high |
| 15 | `disc2d_HenonFold3` | disc2d_HenonFold.mw | high |
| 16 | `disc2d_HenonFold4` | disc2d_HenonFold.mw | high |
| 17 | `disc2d_HenonFold5` | HenonStretchfoldHJrnd.mw | high |
| 18 | `disc2d_HenonStretch0` | disc2d_HenonStretchContract.mw | medium |
| 19 | `disc2d_HenonStretch4` | disc2d_HenonStretchContract.mw | medium |
| 20 | `disc2d_HenonStretch8` | disc2d_HenonStretchContract.mw | medium |
| 21 | `disc2d_HenonStretch12` | disc2d_HenonStretchContract.mw | medium |
| 22 | `disc2d_HenonStretch16` | disc2d_HenonStretchContract.mw | medium |
| 23 | `disc2d_HenonStretch20` | disc2d_HenonStretchContract.mw | medium |
| 24 | `disc2d_kickedrotor` | disc2d_kickedrotor.mw | high |
| 25 | `disc2d_kickedrotor_delta` | disc2d_kickedrotor.mw | high |
| 26 | `disc2d_kickedrotor_v` | disc2d_kickedrotor.mw | high |
| 27 | `disc2d_kickedrotor_theta` | disc2d_kickedrotor.mw | high |
| 28 | `disc2d_circle` | disc2d_circlemap.mw | medium |
| 29 | `disc2d_lincircle_cobweb` | disc2d_lincirclemap.mw | high |
| 30 | `disc2d_lincircle_quasi` | disc2d_lincirclemap.mw | high |
| 31 | `disc2d_lincircle_quasi_cobweb` | disc2d_lincirclemap.mw | high |
| 32 | `disc2d_circlemap_series` | disc2d_circlemap.mw | high |
| 33 | `disc2d_circlemap_return_p2` | disc2d_circlemap.mw | high |
| 34 | `disc2d_circlemap_winding` | disc2d_circlemap.mw | high |
| 35 | `disc2d_circlemap_bifurcation` | disc2d_circlemap.mw | high |
| 36 | `disc2d_circlemap_lyapunov` | disc2d_circlemap.mw | medium |
| 37 | `disc2d_standardmap_quasi` | disc2d_standardmap.mw | high |
| 38 | `disc2d_standardmap_chaos` | disc2d_standardmap.mw | high |
| 39 | `disc2d_standardmap_quasi_return` | disc2d_standardmap.mw | high |
| 40 | `disc2d_standardmap_chaos_return` | disc2d_standardmap.mw | high |
| 41 | `disc2d_standardmap_quasi_deviations` | disc2d_standardmap.mw | high |
| 42 | `disc2d_standardmap_chaos_deviations` | disc2d_standardmap.mw | high |
| 43 | `disc2d_standardmap_phase` | disc2d_standardmap.mw | high |
| 44 | `disc2d_standardmap_phasetorus` | disc2d_standardmap.mw | high |
| 45 | `disc2d_standardmap_saddlenode_n=-6` | disc2d_standardmap_saddlenode.mw | medium |
| 46 | `disc2d_standardmap_saddlenode_n=-5` | disc2d_standardmap_saddlenode.mw | medium |
| 47 | `disc2d_standardmap_saddlenode_n=-4` | disc2d_standardmap_saddlenode.mw | medium |
| 48 | `disc2d_standardmap_saddlenode_n=-3` | disc2d_standardmap_saddlenode.mw | medium |
| 49 | `disc2d_standardmap_saddlenode_n=0` | disc2d_standardmap_saddlenode.mw | medium |
| 50 | `disc2d_standardmap_saddlenode_n=3` | disc2d_standardmap_saddlenode.mw | medium |
| 51 | `disc2d_standardmap_saddlenode_n=4` | disc2d_standardmap_saddlenode.mw | medium |
| 52 | `disc2d_standardmap_saddlenode_n=5` | disc2d_standardmap_saddlenode.mw | medium |
| 53 | `disc2d_standardmap_saddlenode_n=6` | disc2d_standardmap_saddlenode.mw | medium |
| 54 | `disc2d_manifolds` | disc2d_standardmap_saddlenode.mw | REVIEW |
| 55 | `disc2d_standardmap_manifolds` | disc2d_standardmap_saddlenode.mw | high |

## Chapter: 1-D continuous (cont1d)

| # | Figure file | Maple script (in `Figs_cont1d/creators/`) | Confidence |
|---|-------------|----------------------------------------|------------|
| 1 | `cont1d_simplecubic_graph` | normalforms.mws | medium |
| 2 | `cont1d_simplecubic_evolution` | normalforms.mws | medium |
| 3 | `cont1d_generic_graphical_stable` | cont1d_generic_graphical.mw | medium |
| 4 | `cont1d_generic_graphical_unstable` | cont1d_generic_graphical.mw | medium |
| 5 | `cont1d_bifur_pitchfork1` | cont1d_bifur_pitchfork.mw | medium |
| 6 | `cont1d_bifur_pitchfork2` | cont1d_bifur_pitchfork.mw | medium |
| 7 | `cont1d_bifur_pitchfork3` | cont1d_bifur_pitchfork.mw | medium |
| 8 | `cont1d_bifur_pitchfork` | cont1d_bifur_pitchfork.mw | high |
| 9 | `cont1d_bifur_saddle1` | cont1d_saddle.mw | medium |
| 10 | `cont1d_bifur_saddle2` | cont1d_saddle.mw | medium |
| 11 | `cont1d_bifur_saddle3` | cont1d_saddle.mw | medium |
| 12 | `cont1d_bifur_saddle` | cont1d_saddle.mw | medium |
| 13 | `cont1d_bifur_transcrit1` | cont1d_transcrit.mw | medium |
| 14 | `cont1d_bifur_transcrit2` | cont1d_transcrit.mw | medium |
| 15 | `cont1d_bifur_transcrit3` | cont1d_transcrit.mw | medium |
| 16 | `cont1d_bifur_transcrit` | cont1d_transcrit.mw | medium |
| 17 | `cont1d_bifur_pitchfork_sub1` | cont1d_bifur_pitchfork.mw | medium |
| 18 | `cont1d_bifur_pitchfork_sub2` | cont1d_bifur_pitchfork.mw | medium |
| 19 | `cont1d_bifur_pitchfork_sub3` | cont1d_bifur_pitchfork.mw | medium |
| 20 | `cont1d_bifur_pitchfork_sub` | cont1d_bifur_pitchfork.mw | medium |
| 21 | `cont1d_ferro_pitchfork1` | cont1d_ferro_pitchfork.mw | medium |
| 22 | `cont1d_ferro_pitchfork2` | cont1d_ferro_pitchfork.mw | medium |
| 23 | `cont1d_ferro_pitchfork3` | cont1d_ferro_pitchfork.mw | medium |
| 24 | `cont1d_ferro_pitchfork` | cont1d_ferro_pitchfork.mw | high |
| 25 | `cont1d_ferro_pitchfork_stability` | cont1d_ferro_pitchfork.mw | medium |
| 26 | `cont1d_ferro_pitch_evolution1` | cont1d_ferro_pitch_numerical.mw | medium |
| 27 | `cont1d_ferro_pitch_evolution2` | cont1d_ferro_pitch_numerical.mw | medium |
| 28 | `cont1d_ferro_field_bifurcation1` | cont1d_ferro_field_bifurcation.mw | medium |
| 29 | `cont1d_ferro_field_bifurcation2` | cont1d_ferro_field_bifurcation.mw | medium |
| 30 | `cont1d_ferro_field_bifurcation3` | cont1d_ferro_field_bifurcation.mw | medium |
| 31 | `cont1d_ferro_field_bifurcation_large_m` | cont1d_ferro_field_bifurcation.mw | medium |
| 32 | `cont1d_ferro_field_bifurcation_small_m` | cont1d_ferro_field_bifurcation.mw | medium |
| 33 | `cont1d_ferro_field_hysteresis_T_1_5` | cont1d_ferro_field_hysteresis.mw | medium |
| 34 | `cont1d_ferro_field_hysdata_T_1_5` | cont1d_ferro_field_hysteresis.mw | medium |
| 35 | `cont1d_ferro_field_hysteresis_T_1_25` | cont1d_ferro_field_hysteresis.mw | medium |
| 36 | `cont1d_ferro_field_hysdata_T_1_25` | cont1d_ferro_field_hysteresis.mw | medium |
| 37 | `cont1d_ferro_field_hysteresis_T_1_0` | cont1d_ferro_field_hysteresis.mw | medium |
| 38 | `cont1d_ferro_field_hysdata_T_1_0` | cont1d_ferro_field_hysteresis.mw | medium |
| 39 | `cont1d_ferro_field_hysteresis_T_0_75` | cont1d_ferro_field_hysteresis.mw | medium |
| 40 | `cont1d_ferro_field_hysdata_T_0_75` | cont1d_ferro_field_hysteresis.mw | medium |
| 41 | `cont1d_ferro_field_hysteresis_T_0_5` | cont1d_ferro_field_hysteresis.mw | medium |
| 42 | `cont1d_ferro_field_hysdata_T_0_5` | cont1d_ferro_field_hysteresis.mw | medium |
| 43 | `cont1d_ferro_field_hysteresis_3d` | cont1d_ferro_field_hysteresis_3d.mw | high |
| 44 | `cont1d_ferro_field_hysteresis_zoom` | cont1d_ferro_field_hysteresis.mw | medium |
| 45 | `cont1d_ferro_spin_T_0_50_a0` | cont1d_FerroSpins.mw | medium |
| 46 | `cont1d_ferro_spin_T_0_50_b0` | cont1d_FerroSpins.mw | medium |
| 47 | `cont1d_ferro_spin_T_1_50_a0` | cont1d_FerroSpins.mw | medium |
| 48 | `cont1d_ferro_spin_T_1_50_b0` | cont1d_FerroSpins.mw | medium |
| 49 | `cont1d_ferro_spin_T_0_50_a1` | cont1d_FerroSpins.mw | medium |
| 50 | `cont1d_ferro_spin_T_0_50_b1` | cont1d_FerroSpins.mw | medium |
| 51 | `cont1d_ferro_spin_T_1_50_a1` | cont1d_FerroSpins.mw | medium |
| 52 | `cont1d_ferro_spin_T_1_50_b1` | cont1d_FerroSpins.mw | medium |
| 53 | `cont1d_ferro_spin_T_0_50_a2` | cont1d_FerroSpins.mw | medium |
| 54 | `cont1d_ferro_spin_T_0_50_b2` | cont1d_FerroSpins.mw | medium |
| 55 | `cont1d_ferro_spin_T_1_50_a2` | cont1d_FerroSpins.mw | medium |
| 56 | `cont1d_ferro_spin_T_1_50_b2` | cont1d_FerroSpins.mw | medium |
| 57 | `cont1d_ferro_spin_T_0_50_a3` | cont1d_FerroSpins.mw | medium |
| 58 | `cont1d_ferro_spin_T_0_50_b3` | cont1d_FerroSpins.mw | medium |
| 59 | `cont1d_ferro_spin_T_1_50_a3` | cont1d_FerroSpins.mw | medium |
| 60 | `cont1d_ferro_spin_T_1_50_b3` | cont1d_FerroSpins.mw | medium |
| 61 | `cont1d_ferro_spin_T_0_50_a4` | cont1d_FerroSpins.mw | medium |
| 62 | `cont1d_ferro_spin_T_0_50_b4` | cont1d_FerroSpins.mw | medium |
| 63 | `cont1d_ferro_spin_T_1_50_a4` | cont1d_FerroSpins.mw | medium |
| 64 | `cont1d_ferro_spin_T_1_50_b4` | cont1d_FerroSpins.mw | medium |
| 65 | `cont1d_ferro_spin_T_0_50_a5` | cont1d_FerroSpins.mw | medium |
| 66 | `cont1d_ferro_spin_T_0_50_b5` | cont1d_FerroSpins.mw | medium |
| 67 | `cont1d_ferro_spin_T_1_50_a5` | cont1d_FerroSpins.mw | medium |
| 68 | `cont1d_ferro_spin_T_1_50_b5` | cont1d_FerroSpins.mw | medium |
| 69 | `cont1d_ferro_spin_T_0_50` | cont1d_FerroSpins.mw | medium |
| 70 | `cont1d_ferro_spin_T_1_50` | cont1d_FerroSpins.mw | medium |
| 71 | `cont1d_climate_single_fp` | cont1d_climate_single_fp.mw | high |
| 72 | `cont1d_climate_multiple_fp` | cont1d_climate_single_fp.mw | medium |

## Chapter: 2-D continuous (cont2d)

| # | Figure file | Maple script (in `Figs_cont2d/creators/`) | Confidence |
|---|-------------|----------------------------------------|------------|
| 1 | `cont2d_LV_time` | cont2d_LV.mws | high |
| 2 | `cont2d_phasespace` | (no maple script found - likely hand-drawn schematic) | n/a |
| 3 | `cont2d_LV_phase` | cont2d_LV.mws | high |
| 4 | `cont2d_phase_r1` | (no maple script found - likely hand-drawn schematic) | n/a |
| 5 | `cont2d_phase_r2` | (no maple script found - likely hand-drawn schematic) | n/a |
| 6 | `cont2d_phase_r3` | (no maple script found - likely hand-drawn schematic) | n/a |
| 7 | `cont2d_phase_i1` | (no maple script found - likely hand-drawn schematic) | n/a |
| 8 | `cont2d_phase_i2` | (no maple script found - likely hand-drawn schematic) | n/a |
| 9 | `cont2d_phase_i3` | (no maple script found - likely hand-drawn schematic) | n/a |
| 10 | `cont2d_classification` | (no maple script found - likely hand-drawn schematic) | n/a |
| 11 | `cont2d_zoo` | (review - no maple script found) | REVIEW |
| 12 | `cont2d_LV_E` | cont2d_LV6.mws | high |
| 13 | `cont2d_gradient_ell1` | cont2d_gradient2.mws | high |
| 14 | `cont2d_gradient_ell2` | cont2d_gradient2.mws | high |
| 15 | `cont2d_gradient_hyp1` | cont2d_gradient2.mws | high |
| 16 | `cont2d_gradient_hyp2` | cont2d_gradient2.mws | high |
| 17 | `cont2d_conservative_E` | cont2d_conservative.mws | high |
| 18 | `cont2d_Limit_time` | cont2d_Limit2.mws | high |
| 19 | `cont2d_Limit_phase` | cont2d_Limit.mws | high |
| 20 | `cont2d_vdPol_phase` | cont2d_vdPol.mws | high |
| 21 | `cont2d_pitchfork_phase1` | cont2d_pitchfork5.mws | high |
| 22 | `cont2d_pitchfork_phase2` | cont2d_pitchfork5.mws | high |
| 23 | `cont2d_pitchfork_fixed` | cont2d_pitchfork.mw | high |
| 24 | `cont2d_pitchfork_stab` | cont2d_pitchfork.mw | high |
| 25 | `cont2d_Hopf_time1` | cont2d_Hopf.mws | high |
| 26 | `cont2d_Hopf_phase1` | cont2d_Hopf.mws | high |
| 27 | `cont2d_Hopf_time2` | cont2d_Hopf.mws | high |
| 28 | `cont2d_Hopf_phase2` | cont2d_Hopf.mws | high |
| 29 | `cont2d_Hopf_ev1` | cont2d_Hopf2.mws | high |
| 30 | `cont2d_Hopf_ev2` | cont2d_Hopf2.mws | high |
| 31 | `cont2d_global_phase1` | cont2d_global.mws | high |
| 32 | `cont2d_global_phase2` | cont2d_global.mws | high |
| 33 | `cont2d_global_r` | cont2d_global.mws | high |
| 34 | `cont2d_global_fixed` | cont2d_global2.mws | high |
| 35 | `cont2d_LV_Allee_stab_Re` | cont2d_LV_Allee2.mws | high |
| 36 | `cont2d_LV_Allee_stab_Im` | cont2d_LV_Allee2.mws | high |
| 37 | `cont2d_LV_Allee_extinct1` | cont2d_LV_Allee5.mws | high |
| 38 | `cont2d_LV_Allee_extinct2` | cont2d_LV_Allee5.mws | high |

## Chapter: 3-D continuous (cont3d)

| # | Figure file | Maple script (in `Figs_cont3d/creators/`) | Confidence |
|---|-------------|----------------------------------------|------------|
| 1 | `cont3d_lorenz_time` | cont3d_lorenz.mw | high |
| 2 | `cont3d_lorenz_attractor` | cont3d_lorenz.mw | high |
| 3 | `cont3d_lorenz_attraction` | cont3d_lorenz.mw | medium |
| 4 | `cont3d_lorenz_lyapunov` | cont3d_lorenz.mw | high |
| 5 | `cont3d_LorenzLyapEffective` | cont3d_lorenz.mw | medium |
| 6 | `cont3d_lyap_formal` | cont3d_lorenz.mw | medium |
| 7 | `cont3d_LorenzLyapComprehensive` | cont3d_lorenz.mw | medium |
| 8 | `cont3d_LorenzLyapCumulative` | cont3d_lorenz.mw | medium |
| 9 | `cont3d_lorenzlyapattractor` | cont3d_lorenz.mw | medium |
| 10 | `cont3d_lorenz_attractoryz` | cont3d_lorenz.mw | high |
| 11 | `cont3d_lorenz_zmax` | cont3d_lorenz.mw | high |
| 12 | `cont3d_lorenz_map` | cont3d_lorenz.mw | high |
| 13 | `cont3d_poincaresection` | cont3d_poincare_example.mw | high |
| 14 | `cont3d_poincare_exphase` | cont3d_poincare_example.mw | high |
| 15 | `cont3d_poincare_exmap` | cont3d_poincare_example.mw | high |
| 16 | `cont3d_poincare_exseq` | cont3d_poincare_example.mw | high |
| 17 | `cont3d_lorenz_poincare` | cont3d_lorenz.mw | high |
| 18 | `cont3d_rosslerattractor` | cont3d_rossler.mw | high |
| 19 | `cont3d_rosslertopology` | cont3d_rossler.mw | high |
| 20 | `cont3d_rosslerperiod1a` | cont3d_rossler.mw | high |
| 21 | `cont3d_rosslerperiod1b` | cont3d_rossler.mw | high |
| 22 | `cont3d_rosslerperiod2a` | cont3d_rossler.mw | high |
| 23 | `cont3d_rosslerperiod2b` | cont3d_rossler.mw | high |
| 24 | `cont3d_rosslerperiod3a` | cont3d_rossler.mw | high |
| 25 | `cont3d_rosslerperiod3b` | cont3d_rossler.mw | high |
| 26 | `cont3d_rosslerperiod4a` | cont3d_rossler.mw | high |
| 27 | `cont3d_rosslerperiod4b` | cont3d_rossler.mw | high |
| 28 | `cont3d_rosslerreturn` | cont3d_rossler.mw | high |
| 29 | `cont3d_rosslerbifurcation` | cont3d_rossler.mw | high |
| 30 | `cont3d_lorenz_bifurcation` | new.mw | high |
| 31 | `cont3d_doublewell` | cont3d_forced.mws | medium |
| 32 | `cont3d_doublewell_phasespace` | cont3d_forced.mws | high |
| 33 | `cont3d_doublewell_poincare` | cont3d_forced.mws | high |
| 34 | `cont4d_3body_V` | cont4d_3body.mw | medium |
| 35 | `cont4d_3body_Vcut` | cont4d_3body.mw | medium |
| 36 | `cont4d_3body_traj1` | cont4d_3body.mw | medium |
| 37 | `cont4d_3body_traj2` | cont4d_3body.mw | medium |
| 38 | `cont4d_3body_traj3` | cont4d_3body.mw | medium |
| 39 | `cont4d_3body_traj4` | cont4d_3body.mw | medium |
| 40 | `cont4d_3body_Poincare` | cont4d_3body.mw | medium |

---

**Summary:** 264 figures mapped across 6 chapters — 154 verified from script contents (high), 99 inferred by naming convention (medium), 9 hand-drawn schematics with no Maple script, 2 needing review.
