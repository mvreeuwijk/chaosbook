# Homepage + top-menu redesign (Maple edition)

**Date:** 2026-07-04
**Scope:** `maple/` edition only. Structure is designed so the future `python/`
edition mirrors it and a Maple/Python switcher + Solutions section can be added
without rework.

## Goal

Give the book a proper landing page and a top menu that exposes the site's
top-level parts, separating the exercises and the cookbook from the main text.

## Decisions (from brainstorming)

- **Navigation:** keep `sphinx_book_theme` (preserve the reading experience);
  add a curated top header rather than switching to `pydata_sphinx_theme`.
- **Exercises:** moved *out* of the chapters into their own section (one
  standalone page per chapter). Chapters get a short "Exercises for this
  chapter →" link instead of the inline block.
- **Homepage:** hero + cover figure + section cards.

## Information architecture

`index.md` toctree becomes four captioned parts:

| Part | Pages |
|------|-------|
| **Text** | phenomenon, disc1d, disc2d, cont1d, cont2d, cont3d, fractals |
| **Exercises** | exercises landing + 7 per-chapter exercise pages |
| **Cookbook** | app_cookbook (promoted out of appendices) |
| **Appendices** | appendices landing + app_twobody, app_lorenz, app_polar |

## Top header / menu

Configure the theme header via the pydata `navbar_*` slots:

- `navbar_start`: book title (text logo).
- `navbar_center`: curated links **Text · Exercises · Cookbook · Appendices**,
  each pointing at that part's landing page. Implemented as a custom template
  partial (`_templates/navbar-center.html`) for exact control, wired in via
  `html_theme_options["navbar_center"]`.
- `navbar_end`: GitHub repository button.
- Future: a Maple/Python switcher (navbar_end dropdown) and a Solutions link.

## Homepage

- Left column: title, subtitle, authors, one-line blurb, **Start reading →**
  button linking to the first chapter (`phenomenon`).
- Right column: cover figure — default `cont3d_lorenz_attractor` (swappable).
- Below: a `{grid}` of four cards (Text / Exercises / Cookbook / Appendices).
- The `{bibliography}` moves off the homepage to a dedicated **References** page.

## Content moves

- `_includes/*_exercises.md` stay as the single source of the exercise content;
  new `exercises/<chapter>.md` pages give each an H1 title and `{include}` the
  matching file. The `{include}` lines are removed from the chapter files.
- New landing pages: `exercises/index.md` (grid of the 7), `appendices.md`
  (grid of the 3), `references.md` (the bibliography).

## Housekeeping

- Fix stale `repository_url`: `jcrsk/CIVE70079` → `mvreeuwijk/chaosbook`.

## Out of scope (future)

- Solutions section, Maple/Python edition switcher, the Python edition itself.
- The part structure and header are built to accommodate these.

## Verification

- `sphinx-build -b html maple …` builds clean (no new warnings vs. baseline).
- Top menu shows the four parts; each chapter links to its exercises; homepage
  renders hero + cover + cards; References page carries the bibliography.
