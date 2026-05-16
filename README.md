# SIP Study — Code and Data

This repository contains the data and analysis code for the study *"Effects of a fixed-time food delivery on the behavior of domestic cats (Felis catus)"*. Four adult cats were each exposed to fixed-time (FT) food-delivery schedules of 60, 120, 180, 240, and 300 seconds, with intervening baseline periods, and their step counts, activity allocation, spatial use, and water consumption were measured.

## What is in this repo

- `data/` — raw measurements (see [Data](#data) below).
- `Library/` — shared Python modules for reading the data, fitting the models, and rendering tables.
- `SCRIPT_process_*.py` — one script per analysis (activity, location, drinking, steps). Each reads the raw data, fits the models for its section, and writes its figures and serialized results to its own output folder.
- `SCRIPT_compile_stat_results.py` — assembles the supplementary materials from the templates in `supplement/templates/` and the per-section pickled results, writing `supplement/supplement.md` (and `supplement.pdf` if a TeX engine is available).
- `behavior_output/`, `drinking_output/`, `steps_output/` — generated figures (`.png`, `.pdf`) and statistics tables. The pickled intermediates (`*.pck`) are git-ignored; the figures and tables themselves are committed so they are visible on GitHub without running any code.
- `supplement/` — the supplementary materials: editable section templates in `templates/`, and the generated `supplement.md` that the paper refers readers to.

## Data

Three CSV files in `data/`:

- `SIP_data.csv` — daily water consumption per cat. Columns include subject, date, body weight, in-session water consumption (`session`), overnight consumption (`overnight`), and 24-hour total (`total`). Used by `SCRIPT_process_drinking.py`.
- `SIP_fitbit_data.csv` — hourly step counts from each cat's collar-mounted Fitbit Zip. Used by `SCRIPT_process_steps.py`.
- `SIP_observations_2-7-25_take2.csv` — 15-second instantaneous time-sampling observations of behavior category and zone location. Used by `SCRIPT_process_activity.py` and `SCRIPT_process_location.py`.

The exact zone-to-category mapping and the date-window definitions for the drinking analysis are documented in `Library/AnalysisBehavior.read_data` and `Library/AnalysisDrink.read_data` respectively.

## Reproducing the analyses

Requires Python 3.12+ with `numpy`, `pandas`, `scipy`, `statsmodels`, `matplotlib`, `seaborn`, `natsort`, and `tabulate`. The PDF supplement additionally needs `pandoc` and a TeX engine (`xelatex` by default; see `Library/Markdown.py` to switch); the Markdown supplement renders without either.

From the repo root, run each analysis script and then the compiler:

```bash
python SCRIPT_process_steps.py
python SCRIPT_process_activity.py
python SCRIPT_process_location.py
python SCRIPT_process_drinking.py
python SCRIPT_compile_stat_results.py
```

The first four scripts regenerate the figures and the pickled per-section results. The fifth reads those results plus the section templates in `supplement/templates/` and rewrites `supplement/supplement.md` (and `supplement.pdf` if a TeX engine is available).

## Supplementary materials

The full statistical output accompanying the paper (baseline regressions, GLM tables, KS-test tables, with brief explanatory prose for each section) is available in two formats: [`supplement/supplement.md`](supplement/supplement.md) (renders inline on GitHub) and [`supplement/supplement.pdf`](supplement/supplement.pdf) (single downloadable file for citation). Both are generated from the templates in `supplement/templates/` plus the per-section pickled results — edit the templates to change the prose, then re-run `SCRIPT_compile_stat_results.py` to refresh both outputs. Do not edit `supplement.md` or `supplement.pdf` directly; they are regenerated on every run.
