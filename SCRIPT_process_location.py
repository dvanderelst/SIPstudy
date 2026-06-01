import numpy as np
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
from Library import FormatUtils
from Library import AnalysisBehavior
from Library import Settings
import pickle
split_ratio = 2/3


matplotlib.rcParams['font.family'] = 'serif'
output_folder = 'behavior_output/'

data = AnalysisBehavior.read_data()

intervention_data = data.query('Intervention == True')
baseline_data = data.query('Intervention == False')

grouped = intervention_data.groupby(['Feeder_Interval', 'TimeSinceFeeding'], observed=False)
means = grouped.AtFeeder.mean().reset_index()
counts = grouped.AtFeeder.count().reset_index()
counts = counts.rename(columns={'AtFeeder': 'n'})
proportions = pd.merge(means, counts, on=['Feeder_Interval', 'TimeSinceFeeding'])
proportions = proportions.dropna()
proportions['se'] = np.sqrt(proportions['AtFeeder'] * (1 - proportions['AtFeeder']) / proportions['n'])

baseline_activity = baseline_data.AtFeeder.mean()

intervals = intervention_data.Feeder_Interval.unique()
intervals.sort()

model_description = 'AtFeeder ~ C(Subject) + C(Feeder_Interval) + TimeSinceFeeding'
result, summary = AnalysisBehavior.logit_model(data, model_description)
#%%
p60 = result.pvalues['C(Feeder_Interval)[T.60]']
p120 = result.pvalues['C(Feeder_Interval)[T.120]']
p180 = result.pvalues['C(Feeder_Interval)[T.180]']
p240 = result.pvalues['C(Feeder_Interval)[T.240]']
p300 = result.pvalues['C(Feeder_Interval)[T.300]']

pvalue60 = FormatUtils.format_pvalue(p60)
pvalue120 = FormatUtils.format_pvalue(p120)
pvalue180 = FormatUtils.format_pvalue(p180)
pvalue240 = FormatUtils.format_pvalue(p240)
pvalue300 = FormatUtils.format_pvalue(p300)

# Does time at feeder change with feeder interval
model_description = 'AtFeeder ~ C(Subject) + Feeder_Interval + TimeSinceFeeding'
result_interval, summary_interval = AnalysisBehavior.logit_model(intervention_data, model_description)
p_feeder_interval = result_interval.pvalues['Feeder_Interval']

slope_feeder_interval = result_interval.params['Feeder_Interval']

p_feeder_interval = FormatUtils.format_pvalue(p_feeder_interval, slope_feeder_interval)
p_feeder_interval_text = f'Interval, {p_feeder_interval}'

#%%
# Do the same analysis as for the data on the activity: 2/3 vs 1/3
intervention60 = intervention_data.query('Feeder_Interval == 60')
intervention120 = intervention_data.query('Feeder_Interval == 120')
intervention180 = intervention_data.query('Feeder_Interval == 180')
intervention240 = intervention_data.query('Feeder_Interval == 240')
intervention300 = intervention_data.query('Feeder_Interval == 300')

result60 = AnalysisBehavior.piecewise_linear_location(intervention60, split_time=60 * split_ratio)
result120 = AnalysisBehavior.piecewise_linear_location(intervention120, split_time=120 * split_ratio)
result180 = AnalysisBehavior.piecewise_linear_location(intervention180, split_time=180 * split_ratio)
# Drop Minerva from the final-third fit only: she was at the feeder for all
# of her observations in this segment, producing quasi-separation that prevents
# the logit from converging. Excluding her leaves the TimeSinceFeeding slope and
# p-value essentially unchanged but yields a properly converged model.
result240 = AnalysisBehavior.piecewise_linear_location(
    intervention240, split_time=240 * split_ratio,
    exclude_subjects_part2=['Minerva'])
result300 = AnalysisBehavior.piecewise_linear_location(intervention300, split_time=300 * split_ratio)

r60p1 = FormatUtils.format_pvalue(result60['pvalue1'], result60['slope1'], subscript='1')
r60p2 = FormatUtils.format_pvalue(result60['pvalue2'], result60['slope2'], subscript='2')
r120p1 = FormatUtils.format_pvalue(result120['pvalue1'], result120['slope1'], subscript='1')
r120p2 = FormatUtils.format_pvalue(result120['pvalue2'], result120['slope2'], subscript='2')
r180p1 = FormatUtils.format_pvalue(result180['pvalue1'], result180['slope1'], subscript='1')
r180p2 = FormatUtils.format_pvalue(result180['pvalue2'], result180['slope2'], subscript='2')
r240p1 = FormatUtils.format_pvalue(result240['pvalue1'], result240['slope1'], subscript='1')
r240p2 = FormatUtils.format_pvalue(result240['pvalue2'], result240['slope2'], subscript='2')
r300p1 = FormatUtils.format_pvalue(result300['pvalue1'], result300['slope1'], subscript='1')
r300p2 = FormatUtils.format_pvalue(result300['pvalue2'], result300['slope2'], subscript='2')

#%% Plot Figure

plt.figure()

colors = Settings.colors

#plt.gca().invert_xaxis()
plt.axhline(y=baseline_activity, color='gray', linestyle='--', label='Baseline', zorder=0)

intervals.sort()
for index, interval in enumerate(intervals):
    selected_data = proportions.query('Feeder_Interval == @interval')
    current_color = colors[str(interval)]
    split = interval * split_ratio
    # Plot transparent band for ±1 SE
    lower = selected_data['AtFeeder'] - selected_data['se']
    upper = selected_data['AtFeeder'] + selected_data['se']
    plt.fill_between(selected_data['TimeSinceFeeding'], lower, upper,
                     color=current_color, alpha=0.2, linewidth=0)
    # Plot line on top of band
    plt.plot(selected_data['TimeSinceFeeding'], selected_data['AtFeeder'],
             alpha=1, label=str(interval) + 's', linewidth=2, color=current_color)
    # Add scatter markers for first 2/3 and final 1/3
    first = selected_data.query('TimeSinceFeeding <= @split')
    last = selected_data.query('TimeSinceFeeding > @split')
    plt.scatter(first['TimeSinceFeeding'], first['AtFeeder'], facecolors='white', edgecolors=current_color, marker='o', s=30, linewidths=1.5, zorder=3)
    plt.scatter(last['TimeSinceFeeding'], last['AtFeeder'], color=current_color, marker='o', s=30, zorder=3)

from matplotlib.lines import Line2D
# Legend entries explaining the marker convention (neutral color, no data)
plt.scatter([], [], facecolors='white', edgecolors='black', marker='o', s=30, linewidths=1.5, label='First 2/3 of interval')
plt.scatter([], [], color='black', marker='o', s=30, label='Final 1/3 of interval')
plt.gca().add_line(Line2D([0], [0], marker='s', markerfacecolor='gray', alpha=0.2, markersize=10, color='black', linewidth=1, label='Standard Error'))

ax = plt.gca()
ax.set_facecolor('#F1F0EA')

# plt.text(65, 0.85, pvalue60, fontsize=12, color=colors['60'])
# plt.text(150, 0.80, pvalue120, fontsize=12, color=colors['120'])
# plt.text(35, 0.55, pvalue180, fontsize=12, color=colors['180'])
# plt.text(240, 0.75, pvalue240, fontsize=12, color=colors['240'])
# plt.text(215, 0.60, pvalue300, fontsize=12, color=colors['300'])
#
# plt.text(180, 0.40, p_feeder_interval_text, fontsize=12, color='black')
#
# # Add the p values for the piecewise linear models
# plt.text(15, 0.25, '60s:   ' + r60p1, fontsize=12, color=colors['60'])
# plt.text(15, 0.20, '120s: ' + r120p1, fontsize=12, color=colors['120'])
# plt.text(15, 0.15, '180s: ' + r180p1, fontsize=12, color=colors['180'])
# plt.text(15, 0.10, '240s: ' + r240p1, fontsize=12, color=colors['240'])
# plt.text(15, 0.05, '300s: ' + r300p1, fontsize=12, color=colors['300'])
# # Add all the formatted p-values
# plt.text(120, 0.25, r60p2, fontsize=12, color=colors['60'])
# plt.text(120, 0.20, r120p2, fontsize=12, color=colors['120'])
# plt.text(120, 0.15, r180p2, fontsize=12, color=colors['180'])
# plt.text(120, 0.10, r240p2, fontsize=12, color=colors['240'])
# plt.text(120, 0.05, r300p2, fontsize=12, color=colors['300'])

plt.ylim(0, 1)
plt.xlabel('Time Since Feeding (s)')
plt.ylabel('Time at Feeder (Average Proportion)')
plt.xticks(range(0, 300, 45))
plt.grid()
plt.legend(ncol=3)
plt.tight_layout()
plt.savefig(output_folder + 'location.png', dpi=300)
plt.savefig(output_folder + 'location.pdf')
plt.show()


# Save the piecewise_linear_activity results to a pickle file for later use
pickle_file = f"{output_folder}piecewise_linear_location_results.pck"
pickle_file_handle = open(pickle_file, 'wb')

pickle.dump({
    'result60': result60,
    'result120': result120,
    'result180': result180,
    'result240': result240,
    'result300': result300,
    'result_interval': result_interval, #-->tests effect of interval
    'result': result  # --> includes interval as factor, tests whether each of interval levels differs from baseline
}, pickle_file_handle)
pickle_file_handle.close()
