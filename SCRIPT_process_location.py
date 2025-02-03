import matplotlib
from matplotlib import pyplot as plt

import Library.FormatUtils
from Library import AnalysisBehavior
from Library import Settings


matplotlib.rcParams['font.family'] = 'serif'
output_folder = 'behavior_output/'

data = AnalysisBehavior.read_data()

intervention_data = data.query('Intervention == True')
baseline_data = data.query('Intervention == False')

grouped = intervention_data.groupby(['Feeder_Interval', 'TimeToFeeding'], observed=False)
proportions = grouped.AtFeeder.mean()
proportions = proportions.reset_index()
proportions = proportions.dropna()

baseline_activity = baseline_data.AtFeeder.mean()

intervals = intervention_data.Feeder_Interval.unique()
intervals.sort()

model_description = 'AtFeeder ~ C(Subject) + C(Feeder_Interval) + TimeToFeeding'
result, summary = AnalysisBehavior.logit_model(data, model_description)
#%%
p60 = result.pvalues['C(Feeder_Interval)[T.60]']
p120 = result.pvalues['C(Feeder_Interval)[T.120]']
p180 = result.pvalues['C(Feeder_Interval)[T.180]']
p240 = result.pvalues['C(Feeder_Interval)[T.240]']
p300 = result.pvalues['C(Feeder_Interval)[T.300]']

pvalue60 = Library.FormatUtils.format_pvalue(p60)
pvalue120 = Library.FormatUtils.format_pvalue(p120)
pvalue180 = Library.FormatUtils.format_pvalue(p180)
pvalue240 = Library.FormatUtils.format_pvalue(p240)
pvalue300 = Library.FormatUtils.format_pvalue(p300)

# Does time at feeder change with feeder interval
model_description = 'AtFeeder ~ C(Subject) + Feeder_Interval + TimeToFeeding'
result_interval, summary_interval = AnalysisBehavior.logit_model(intervention_data, model_description)
p_feeder_interval = result_interval.pvalues['Feeder_Interval']
p_feeder_interval = Library.FormatUtils.format_pvalue(p_feeder_interval)
p_feeder_interval_text = f'Interval, {p_feeder_interval}'

#%% Plot Figure

plt.figure()

colors = Settings.colors

#plt.plot(prediction1['TimeToFeeding'], prediction1['Predicted'], label='Predicted Activity (First Half)', linewidth=2, color='black', markersize=10, marker='$↓$', zorder=10)
#plt.plot(prediction2['TimeToFeeding'], prediction2['Predicted'], label='Predicted Activity (Second Half)', linewidth=2, color='black', marker='$↑$', markersize=10, zorder=10)
plt.gca().invert_xaxis()
plt.axhline(y=baseline_activity, color='gray', linestyle='--', label='Baseline', zorder=0)

intervals.sort()
for index, interval in enumerate(intervals):
    selected_data = proportions.query('Feeder_Interval == @interval')
    current_color = colors[str(interval)]
    plt.plot(selected_data['TimeToFeeding'], selected_data['AtFeeder'], alpha=1, label=str(interval) + ' s', linewidth=2, color=current_color, marker = '.')

ax = plt.gca()
ax.set_facecolor('#F1F0EA')

plt.text(120, 0.83, pvalue60, fontsize=12, color=colors['60'])
plt.text(175, 0.75, pvalue120, fontsize=12, color=colors['120'])
plt.text(205, 0.55, pvalue180, fontsize=12, color=colors['180'])
plt.text(275, 0.55, pvalue240, fontsize=12, color=colors['240'])
plt.text(250, 0.80, pvalue300, fontsize=12, color=colors['300'])

plt.text(90, 0.35, p_feeder_interval_text, fontsize=12, color='black')

plt.ylim(0, 1)
plt.xlabel('Time to Feeding (s)')
plt.ylabel('Time at Feeder (Proportion)')
plt.xticks(range(0, 300, 45))
plt.grid()
plt.legend(ncol=3)
plt.tight_layout()
plt.savefig(output_folder + 'location.png', dpi=300)
plt.savefig(output_folder + 'location.pdf')
plt.show()