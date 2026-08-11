# Pilot chapters: phenomenon + disc1d — design

**Date:** 2026-08-11
**Status:** approved
**Builds on:** `2026-08-10-python-edition-vision-design.md` (sub-project ②);
the `chaosbook` package and the cookbook are shipped and live at
`https://mvreeuwijk.github.io/chaosbook/python/`.

## Goal

Convert the first two chapters to the Python edition as the pilot proving
the full cutting-edge pipeline: *phenomenon* ("start at the end" — 3D
continuous problems: Lorenz, three-body) and *disc1d* (one-dimensional
maps). Together they exercise all four serverless interactive figure
families (3D rotate, animation, slider, deep zoom).

## Decisions made during brainstorming

1. **MyST `.md` chapters + offline creators scripts** — chapters stay
   markdown like the Maple edition; figures are built offline by
   `creators/python/` scripts emitting interactive assets and static twins.
   (Rejected: executable myst-nb chapters — conflates pedagogical snippets
   with figure production, slow builds; notebook chapters — poor home for
   proofs/numbered equations.)
2. **Creators are published, reader-facing code** — clean package-based
   scripts surfaced from each figure ("code behind this figure" link), not
   a private audit trail. (Rejected: audit-trail-only; merging creators
   into the companion notebooks.)
3. **Panels kept; interactive added after** — numbered multi-panel figures
   stay identical in HTML and PDF (prose panel references intact, shared
   numbering); the interactive companion is an HTML-only addition directly
   beneath. (Rejected: replacing panels in HTML — breaks panel references
   and forks numbering.)
4. **Exercises ported with Python wording** — Maple-specific instructions
   recast to Python/chaosbook. (Rejected: deferring; porting verbatim.)
5. **All pilot figures are regenerated in Python** (user requirement) and
   the creators' role is elevated accordingly (decision 2).

## 1. Chapter conversion model

- Create `python/phenomenon.md` and `python/disc1d.md` from the Maple
  chapters: **prose and mathematics copied verbatim** (shared exposition —
  ROADMAP edition boundaries), with:
  - Maple code admonitions (`:::{admonition} Maple :class: maple`) replaced
    by Python admonitions (`:class: python`) whose code uses
    `import chaosbook as cb` and `solve_ivp`, in the cookbook's style;
  - every figure reference pointing at the regenerated Python figures in
    `python/_static/<chapter>/` (same basenames as the Maple originals);
  - zero Maple mentions anywhere.
- Exercises: create `python/_includes/phenomenon_exercises.md` and
  `python/_includes/disc1d_exercises.md`, ported with Python/chaosbook
  wording.
- `python/index.md`: add the two chapters to the Text toctree (numbered),
  before the cookbook.
- Cross-references to not-yet-converted targets (`chap:cont3d`,
  `app:twobody`): reword gracefully ("in a later chapter" / "in an
  appendix of the full edition") until those targets exist; no broken
  references in the build.
- Hand-drawn schematics with no Maple source (e.g. the three-body
  schematic `3body.png`) are copied from `maple/_static/`, per
  `shared/README.md`.

## 2. Creators as published code

- Layout: `creators/python/<chapter>/fig_<name>.py` — one short script per
  figure family, importing `chaosbook`, using the book's exact parameters.
  Each script emits:
  - the **static twin(s)**: PNG (HTML) and PDF (LaTeX) into
    `python/_static/<chapter>/`, same basenames as the Maple figures;
  - the **interactive asset** (where the figure has a companion): a plotly
    HTML file into `python/_static/<chapter>/interactive/`.
- Generated figures are **committed**; Sphinx never regenerates them. A
  `make python-figures` target runs all creators scripts.
- **Reader-facing link**: each figure caption in the HTML edition carries a
  small "· code" link to the generating script on GitHub (upgraded to a
  JupyterLite launch in sub-project ③). Mechanism: a one-line link appended
  to the `{figure}` caption inside `{only} html`.
- Scripts are written to be read: package imports, minimal plumbing, brief
  header comment naming the figures produced.
- `creators/porting_manifest.csv` gains `python_source` and
  `python_status` columns; every pilot figure row is filled in. Validation:
  static twins visually match the Maple originals (same systems, same
  parameters, same ranges).

## 3. Interactive figures

- Numbered `{figure}` directives stay **static in both outputs** so
  `{numref}` and panel references work identically in HTML and PDF.
- Selected figures get an HTML-only interactive companion embedded directly
  beneath (inside `{only} html`): an `<iframe>` onto the plotly asset.
- **Self-hosted plotly**: one shared `plotly.min.js` in `python/_static/`;
  interactive HTML files reference it relatively — no CDN dependency.
- Pilot companions (six, covering all four families):

| Chapter | Companion | Family |
|---|---|---|
| phenomenon | Rotatable 3D Lorenz attractor | 3D rotate |
| phenomenon | Twin-trajectory sensitivity animation (play button) | animation |
| phenomenon | Three-body trajectories, inertial ↔ co-rotating | animation |
| disc1d | Logistic explorer: series + cobweb + return plot under one r-slider | slider |
| disc1d | Bifurcation diagram deep zoom (precomputed fine grid) | zoom |
| disc1d | Bifurcation + Lyapunov Λ(r) linked view with slider | slider |

- Slider figures use **precomputed frames** (fixed r-grid) — serverless;
  full parameter freedom belongs to the JupyterLite layer (sub-project ③).

## 4. Package additions

Only what the chapters need, generic-tools-first (the tools must never
assume the bundled systems):

- `maps.py`: `sine(x, r)`, `tent(x, r)`, `shift(x)` — book definitions.
- `flows.py`: `threebody(t, state)` with the mass/distance parameters as
  keyword arguments — restricted three-body problem in the rotating frame,
  equations and parameters from `creators/MODELS.md` (exact signature fixed
  in the implementation plan against MODELS.md).
- `bifurcation.py` (or a new `lyapunov.py` if cleaner): a
  `lyapunov(f, dfdx, x0, n, **params)`-style function — mean of
  log|f'(x_n)| along the orbit after a transient — plus a swept version
  for Λ(r) diagrams (exact signatures fixed in the implementation plan,
  following the orbit() conventions).
- Qualitative tests for each (fixed points, known Λ values — e.g.
  Λ = ln 2 for the tent/shift maps and logistic r=4; three-body Jacobi
  constant conservation over a short integration).
- Chapter-specific one-off machinery (Feigenbaum Newton–Raphson, analytic
  PDFs, binary shift table) lives in the creators scripts, not the package.

## 5. Build & sequencing

- CI needs no changes: figures are committed assets; pushing publishes the
  chapters. plotly joins `requirements.txt` (used by creators scripts, not
  by the Sphinx build).
- Sequencing inside the pilot: **phenomenon first** (small — proves
  package additions → creators → static twins → interactive embed → chapter
  page end-to-end), then **disc1d** (volume: 23 figures, sliders, zoom).
  Each gets its own implementation plan.
- The PDF (book-level `latex_documents`) is NOT extended in the pilot: the
  Python edition's PDF deliverable remains the cookbook until enough
  chapters exist to justify a book PDF.

## Implementation notes (recorded after the phenomenon chapter shipped)

- **Three-body frame:** `MODELS.md` describes the restricted three-body
  problem "in the rotating frame", but the chapter's own equations are
  inertial-frame with moving primaries. The shipped `flows.threebody`
  correctly follows the chapter (inertial), with `flows.corotating` as the
  view transform. When porting later chapters, cross-check `MODELS.md`
  frame descriptions against the actual chapter equations rather than
  trusting them verbatim.
- **Code-link placement:** links are a standalone `{only} html` paragraph
  directly after the figure/subfigure block (MyST captions don't support
  embedded links well), and **every** creators-script figure gets one —
  disc1d must apply the link exhaustively across its 23 figures.
- **Evidence-based numeric checks (pilot retrospective, binding for the
  rollout chapters):** every implementer task that produces or quotes
  numbers (worked-example outputs, tables, figure anchors like slopes or
  constants) must RUN the code and paste the actual output into its
  report, diffed against the book's quoted values — asserting "matches"
  without evidence is not acceptance. The pilot needed several correction
  rounds (sympy digits vs the old engine's, δ(η) NaNs, the N=50 round-off
  table that never diverged) precisely where first-pass reports asserted
  correctness unchecked.
- **Figure style (user direction, 2026-08-11):** axis/tick labels use
  LaTeX mathtext symbols (`$x_n$`, `$\Lambda(r)$`, `$\delta$`, `$\eta$` —
  never "xn", "Lambda(r)"), and the apparent font size must be uniform
  across the book's figures: one shared matplotlib style, and figure
  sizes standardised per display class so page scaling doesn't shrink or
  blow up labels.

## Out of scope (deliberate)

- JupyterLite wiring and companion notebooks (sub-project ③) — the "· code"
  links point at GitHub until then.
- Chapters beyond phenomenon and disc1d.
- Click-to-launch phase portraits and draggable Poincaré planes (need a
  live kernel; sub-project ③).
- A Python-edition book PDF. *(Amended 2026-08-11, user direction: CI now
  compiles the chapters into a draft book PDF, published at
  `python/chaosbook-python.pdf`, so print figure quality can be judged as
  chapters roll out. Linked from the edition frontpage as "Download PDF
  (draft)" per user direction later the same day.)*
