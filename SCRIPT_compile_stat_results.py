import pandas as pd
import pickle

from rich.markdown import Markdown

from Library import Markdown

md_file = 'compiled_stats/compiled.md'

md_file_handle = open(md_file, 'w')

########################
# STEP STATISTICS
########################

step_stats_file = 'steps_output/statistics_steps.txt'
step_stats_df = pd.read_csv(step_stats_file, sep=',', header=None)
step_stats_df.columns = ['Subject', 'Comparison', 'KS statistics', 'p-value']

regression_results_file = 'steps_output/regression.pck'
regression_results_file_handle = open(regression_results_file, 'rb')
regression_results = pickle.load(regression_results_file_handle)
regression_results_file_handle.close()

header = '# Step Statistics\n\n'
md_file_handle.write(header)

header = '## Linear model results\n\n'
md_file_handle.write(header)

cats = list(regression_results.keys())
cats.sort()

for cat in cats:
    results = regression_results[cat]
    results = results['results']
    header = f'### Linear model results for {cat}\n\n'
    md = Markdown.model2code(results)
    md_file_handle.write(header)
    md_file_handle.write(md + '\n\n')


header = '## Kolmogorov–Smirnov tests\n\n'
md = step_stats_df.to_markdown(index=False)
md_file_handle.write(header)
md_file_handle.write(md+ '\n\n')


########################
# ACTIVITY STATISTICS
########################

results_file = 'behavior_output/piecewise_linear_activity_results.pck'
results_file_handle = open(results_file, 'rb')
activity_results = pickle.load(results_file_handle)
results_file_handle.close()

header = '# Activity Statistics\n\n'
md_file_handle.write(header)

for interval in [60, 120, 180, 240, 300]:
    result = activity_results[f'result{interval}']
    result_1 = result['result1']
    result_2 = result['result2']

    result_1 = Markdown.model2code(result_1)
    result_2 = Markdown.model2code(result_2)

    header = f'## Activity results for {interval} interval\n\n'
    md_file_handle.write(header)

    md_file_handle.write(f'### Logistic generalized linear model, {interval}s, first 2/3s of interval\n\n')
    md_file_handle.write(result_1 + '\n\n')
    md_file_handle.write(f'### Logistic generalized linear model, {interval}s, last 1/3 of interval\n\n')
    md_file_handle.write(result_2 + '\n\n')


########################
# LOCATION STATISTICS
########################

results_file = 'behavior_output/piecewise_linear_location_results.pck'
results_file_handle = open(results_file, 'rb')
activity_results = pickle.load(results_file_handle)
results_file_handle.close()

header = '# Location Statistics\n\n'
md_file_handle.write(header)

# For the location, we also tested whether
# 1) The proportion of time spent at the feeder changed with feeder interval
# 2) whether each of these differed from the baseline
# 'result_interval,': result_interval, #-->tests effect of interval
# 'result': result  # --> includes interval as factor, tests whether each of interval levels differs from baseline



header = f'## Effect of interval on location\n\n'
result_interval = activity_results['result_interval']
result_interval_md = Markdown.model2code(result_interval)
md_file_handle.write(header)
md_file_handle.write(result_interval_md + '\n\n')

header = f'## Testing for differences between baseline and experimental conditions\n\n'
result = activity_results['result']
result_md = Markdown.model2code(result)
md_file_handle.write(header)
md_file_handle.write(result_md + '\n\n')

for interval in [60, 120, 180, 240, 300]:
    result = activity_results[f'result{interval}']
    result_1 = result['result1']
    result_2 = result['result2']

    result_1 = Markdown.model2code(result_1)
    result_2 = Markdown.model2code(result_2)

    header = f'## Location results for {interval} interval\n\n'
    md_file_handle.write(header)

    md_file_handle.write(f'### Logistic generalized linear model, {interval}s, first 2/3s of interval\n\n')
    md_file_handle.write(result_1 + '\n\n')
    md_file_handle.write(f'### Logistic generalized linear model, {interval}s, last 1/3 of interval\n\n')
    md_file_handle.write(result_2 + '\n\n')



########################
# FINISHING UP
########################

md_file_handle.close()
Markdown.md_to_pdf(md_file, out_path='compiled_stats/compiled_stats.pdf')