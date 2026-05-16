"""Assemble the supplement from templates in supplement/templates/.

Each template is a markdown file with `<!-- INSERT: name -->` markers.
For each known marker, the corresponding generator function is called
to produce the substitution. Unrecognized markers are left in place so
it's obvious in the output what is not yet wired up.

Templates are concatenated in alphabetical order of filename, which is
why they are prefixed 00_..., 01_..., etc.

Outputs:
  supplement/supplement.md
  supplement/supplement.pdf
"""

import pickle
import re
from pathlib import Path

import pandas as pd

from Library import Markdown

TEMPLATE_DIR = Path('supplement/templates')
OUTPUT_MD = Path('supplement/supplement.md')
OUTPUT_PDF = Path('supplement/supplement.pdf')

INSERT_RE = re.compile(r'<!--\s*INSERT:\s*(\w+)\s*-->')


# ---------- Generators (one per <!-- INSERT: name --> marker) ----------

def _load_steps_regressions():
    with open('steps_output/regression.pck', 'rb') as f:
        return pickle.load(f)


def steps_formula() -> str:
    """R-style formula for the per-cat baseline step-count regression."""
    results = _load_steps_regressions()
    any_cat = next(iter(results))
    return Markdown.model_formula(results[any_cat]['results'])


def steps_regressions() -> str:
    """Per-cat baseline OLS regressions for daily step count."""
    results = _load_steps_regressions()
    chunks = []
    for cat in sorted(results.keys()):
        chunks.append(f'### {cat}')
        chunks.append(Markdown.model2code(results[cat]['results']))
    return '\n\n'.join(chunks)


def steps_ks_table() -> str:
    """Per-cat × per-interval KS tests of FT vs. baseline residuals."""
    df = pd.read_csv('steps_output/statistics_steps.txt', sep=',', header=None)
    df.columns = ['Subject', 'Comparison', 'KS statistic', 'p-value']
    return df.to_markdown(index=False)


def activity_models() -> str:
    """Per-FT-interval piecewise logit models (first 2/3 + final 1/3) for activity."""
    with open('behavior_output/piecewise_linear_activity_results.pck', 'rb') as f:
        results = pickle.load(f)
    chunks = []
    for interval in [60, 120, 180, 240, 300]:
        result = results[f'result{interval}']
        chunks.append(f'### {interval}s interval')
        chunks.append('**First segment (first 2/3 of interval):**')
        chunks.append(Markdown.model2code(result['result1']))
        chunks.append('**Second segment (final 1/3 of interval):**')
        chunks.append(Markdown.model2code(result['result2']))
    return '\n\n'.join(chunks)


def _load_location_results():
    with open('behavior_output/piecewise_linear_location_results.pck', 'rb') as f:
        return pickle.load(f)


def location_baseline_vs_experimental() -> str:
    """Categorical logit: AtFeeder ~ Subject + C(Feeder_Interval, baseline ref) + TimeSinceFeeding."""
    return Markdown.model2code(_load_location_results()['result'])


def location_baseline_vs_experimental_formula() -> str:
    return Markdown.model_formula(_load_location_results()['result'])


def location_interval_model() -> str:
    """Continuous interval-length logit (intervention only)."""
    return Markdown.model2code(_load_location_results()['result_interval'])


def location_interval_model_formula() -> str:
    return Markdown.model_formula(_load_location_results()['result_interval'])


def location_models() -> str:
    """Per-FT-interval piecewise logit models (first 2/3 + final 1/3) for location."""
    results = _load_location_results()
    chunks = []
    for interval in [60, 120, 180, 240, 300]:
        result = results[f'result{interval}']
        chunks.append(f'### {interval}s interval')
        chunks.append('**First segment (first 2/3 of interval):**')
        chunks.append(Markdown.model2code(result['result1']))
        chunks.append('**Second segment (final 1/3 of interval):**')
        chunks.append(Markdown.model2code(result['result2']))
    return '\n\n'.join(chunks)


def _load_drinking_regressions():
    with open('drinking_output/all_linear_regression_results.pck', 'rb') as f:
        return pickle.load(f)


def drinking_formula() -> str:
    """R-style formula for the per-cat baseline drinking regression (phase 1, session)."""
    results = _load_drinking_regressions()
    any_label = next(label for label in results if label.endswith('phase_1_session'))
    return Markdown.model_formula(results[any_label]['results'])


def drinking_regressions() -> str:
    """Per-cat baseline OLS regressions for in-session water consumption (phase 1)."""
    results = _load_drinking_regressions()
    cats = sorted({label.split('_')[0] for label in results if label.endswith('phase_1_session')})
    chunks = []
    for cat in cats:
        chunks.append(f'### {cat}')
        chunks.append(Markdown.model2code(results[f'{cat}_phase_1_session']['results']))
    return '\n\n'.join(chunks)


def drinking_ks_table() -> str:
    """Per-cat × per-interval KS tests of FT vs. baseline residuals (phase 1, session)."""
    lines = open('drinking_output/statistics.txt').readlines()
    # File interleaves "Phase: X, Dependent Variable: Y" headers with 20 stat rows
    # per section (4 cats x 5 intervals). The phase-1-session section is the first
    # block: a header on line 0, then 20 rows on lines 1-20.
    rows = [[x.strip() for x in line.strip().split(',')] for line in lines[1:21]]
    df = pd.DataFrame(rows, columns=['Subject', 'Comparison', 'KS statistic', 'p-value'])
    df['Comparison'] = df['Comparison'].apply(lambda x: f'Interval {x}s vs Baseline')
    return df.to_markdown(index=False)


GENERATORS = {
    'steps_formula': steps_formula,
    'steps_regressions': steps_regressions,
    'steps_ks_table': steps_ks_table,
    'activity_models': activity_models,
    'location_baseline_vs_experimental': location_baseline_vs_experimental,
    'location_baseline_vs_experimental_formula': location_baseline_vs_experimental_formula,
    'location_interval_model': location_interval_model,
    'location_interval_model_formula': location_interval_model_formula,
    'location_models': location_models,
    'drinking_formula': drinking_formula,
    'drinking_regressions': drinking_regressions,
    'drinking_ks_table': drinking_ks_table,
}


# ---------- Assembler ----------

def render(text: str) -> str:
    def replace(match):
        name = match.group(1)
        if name in GENERATORS:
            return GENERATORS[name]()
        return match.group(0)
    return INSERT_RE.sub(replace, text)


def main():
    templates = sorted(TEMPLATE_DIR.glob('*.md'))
    rendered = [render(t.read_text()) for t in templates]
    OUTPUT_MD.write_text('\n\n'.join(rendered))
    print(f'wrote {OUTPUT_MD}')
    try:
        Markdown.md_to_pdf(str(OUTPUT_MD), out_path=str(OUTPUT_PDF))
        print(f'wrote {OUTPUT_PDF}')
    except Exception as e:
        print(f'skipped PDF generation: {e}')


if __name__ == '__main__':
    main()
