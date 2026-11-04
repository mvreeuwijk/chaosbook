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
