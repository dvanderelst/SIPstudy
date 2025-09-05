import pandas as pd
import pickle

from rich.markdown import Markdown

from Library import Markdown

md_file = 'compiled_stats/compiled.md'

md_file_handle = open(md_file, 'w')

step_stats_file = 'steps_output/statistics_steps.txt'
step_stats_df = pd.read_csv(step_stats_file, sep=',', header=None)
step_stats_df.columns = ['Subject', 'Comparison', 'KS statistics', 'p-value']

regression_results_file = 'steps_output/regression.pck'
regression_results_file_handle = open(regression_results_file, 'rb')
regression_results = pickle.load(regression_results_file_handle)
regression_results_file_handle.close()

header = '# Step Statistics\n\n'
md_file_handle.write(header)

header = '# Linear model results\n\n'
md_file_handle.write(header)

cats = list(regression_results.keys())
cats.sort()

for cat in cats:
    results = regression_results[cat]
    results = results['results']
    header = f'## Linear model results for {cat}\n\n'
    md = Markdown.as_code(results.summary().as_text())
    md_file_handle.write(header + '\n\n')
    md_file_handle.write(md + '\n\n')


header = '## Step Statistics\n\n'
md = step_stats_df.to_markdown(index=False)
md_file_handle.write(header)
md_file_handle.write(md)
md_file_handle.close()

Markdown.md_to_pdf(md_file, out_path='compiled_stats/compiled_stats.pdf')