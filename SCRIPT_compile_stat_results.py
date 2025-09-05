import pandas as pd
import pickle
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

header = '# Step Counts Statistics\n\n'
md_file_handle.write(header)

header = '## Linear Model Results\n\n'
md_file_handle.write(header)

cats = list(regression_results.keys())
cats.sort()

for cat in cats:
    results = regression_results[cat]
    results = results['results']
    header = f'### Linear Model Results for {cat}\n\n'
    md = Markdown.model2code(results)
    md_file_handle.write(header)
    md_file_handle.write(md + '\n\n')


header = '## Kolmogorov–Smirnov Tests\n\n'
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

header = '# Activity Pattern Statistics\n\n'
md_file_handle.write(header)

for interval in [60, 120, 180, 240, 300]:
    result = activity_results[f'result{interval}']
    result_1 = result['result1']
    result_2 = result['result2']

    result_1 = Markdown.model2code(result_1)
    result_2 = Markdown.model2code(result_2)

    header = f'## Activity Pattern Results for {interval} Interval\n\n'
    md_file_handle.write(header)

    md_file_handle.write(f'### Logistic Generalized Linear Model, {interval}s, First 2/3s of interval\n\n')
    md_file_handle.write(result_1 + '\n\n')
    md_file_handle.write(f'### Logistic Generalized Linear Model, {interval}s, Last 1/3 of interval\n\n')
    md_file_handle.write(result_2 + '\n\n')


########################
# LOCATION STATISTICS
########################

results_file = 'behavior_output/piecewise_linear_location_results.pck'
results_file_handle = open(results_file, 'rb')
location_results = pickle.load(results_file_handle)
results_file_handle.close()

header = '# Space Allocation Statistics\n\n'
md_file_handle.write(header)

# For the location, we also tested whether
# 1) The proportion of time spent at the feeder changed with feeder interval
# 2) whether each of these differed from the baseline
# 'result_interval,': result_interval, #-->tests effect of interval
# 'result': result  # --> includes interval as factor, tests whether each of interval levels differs from baseline

header = f'## Effect of Interval on Space Allocation\n\n'
result_interval = location_results['result_interval']
result_interval_md = Markdown.model2code(result_interval)
md_file_handle.write(header)
md_file_handle.write(result_interval_md + '\n\n')

header = f'## Testing for Differences Between Baseline and Experimental Conditions\n\n'
result = location_results['result']
result_md = Markdown.model2code(result)
md_file_handle.write(header)
md_file_handle.write(result_md + '\n\n')

for interval in [60, 120, 180, 240, 300]:
    result = location_results[f'result{interval}']
    result_1 = result['result1']
    result_2 = result['result2']

    result_1 = Markdown.model2code(result_1)
    result_2 = Markdown.model2code(result_2)

    header = f'## Location results for {interval} interval\n\n'
    md_file_handle.write(header)

    md_file_handle.write(f'### Logistic Generalized Linear Model, {interval}s, First 2/3s of interval\n\n')
    md_file_handle.write(result_1 + '\n\n')
    md_file_handle.write(f'### Logistic Generalized Linear Model, {interval}s, Last 1/3 of interval\n\n')
    md_file_handle.write(result_2 + '\n\n')

########################
# DRINKING STATISTICS
########################
header = '# Water Consumption Statistics\n\n'
md_file_handle.write(header)
# The data in the paper is for phase 1, dependent var = session
results_file = 'drinking_output/all_linear_regression_results.pck'
results_file_handle = open(results_file, 'rb')
results = pickle.load(results_file_handle)
results_file_handle.close()
phase = 1
dependent_variable = 'session'
for cat in cats:
    label = f"{cat}_phase_{phase}_{dependent_variable}"
    regression_results = results[label]
    regression_results = regression_results['results']
    header = f'## Linear Model for {cat}\n\n'
    md_file_handle.write(header)

    md = Markdown.model2code(regression_results)
    md_file_handle.write(md + '\n\n')


ks_file = 'drinking_output/statistics.txt'
lines = open(ks_file, 'r').readlines()
relevant_lines = lines[1:21]
relevant_lines = [line.strip() for line in relevant_lines]
# Split each line by commas to get 4 columns
parsed_data = []
for line in relevant_lines:
    # Split by comma and strip whitespace
    parts = [part.strip() for part in line.split(',')]
    parsed_data.append(parts)

# Create DataFrame with 4 columns
columns = ['Subject', 'Comparison', 'KS statistics', 'p-value']
df = pd.DataFrame(parsed_data, columns=columns)
# Update the Comparison column to show "Interval Xs vs Baseline"
df['Comparison'] = df['Comparison'].apply(lambda x: f"Interval {x}s vs Baseline")

header = '## Kolmogorov–Smirnov Tests\n\n'
md = df.to_markdown(index=False)
md_file_handle.write(header)
md_file_handle.write(md)



########################
# FINISHING UP
########################

md_file_handle.close()
Markdown.md_to_pdf(md_file, out_path='compiled_stats/compiled_stats.pdf')