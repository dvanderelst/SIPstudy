import matplotlib

from matplotlib import pyplot as plt
from Library import FormatUtils
from Library import AnalysisBehavior
from Library import Settings


split_ratio = 2/3
last_n_sessions = 10000

matplotlib.rcParams['font.family'] = 'serif'
output_folder = 'behavior_output/'

data = AnalysisBehavior.read_data()


# Calculate increasing session number (days since first date)
data['session_from_first'] = data.groupby(['Subject', 'Feeder_Interval'])['date'].rank(method='dense').astype(int) - 1
# Calculate decreasing session number (days since last date)
data['session_from_last'] = data.groupby(['Subject', 'Feeder_Interval'])['date'].rank(method='dense', ascending=False).astype(int) - 1
# Select only the last n sessions
data = data.query('session_from_last < @last_n_sessions')

intervention_data = data.query('Intervention == True')
baseline_data = data.query('Intervention == False')

grouped = intervention_data.groupby(['Feeder_Interval', 'TimeToFeeding'], observed=False)
proportions = grouped.Active.mean()
proportions = proportions.reset_index()
proportions = proportions.dropna()

baseline_activity = baseline_data.Active.mean()
intervals = intervention_data.Feeder_Interval.unique()
intervals.sort()

intervention60 = intervention_data.query('Feeder_Interval == 60')
intervention120 = intervention_data.query('Feeder_Interval == 120')
intervention180 = intervention_data.query('Feeder_Interval == 180')
intervention240 = intervention_data.query('Feeder_Interval == 240')
intervention300 = intervention_data.query('Feeder_Interval == 300')

average_cut_off = ((60 * split_ratio) + (120 * split_ratio) + (180 * split_ratio) + (240 * split_ratio) + (300 * split_ratio)) / 5

result_full = AnalysisBehavior.piecewise_linear(intervention_data, split_time=average_cut_off, full=False, use_actual=True)

result60 = AnalysisBehavior.piecewise_linear(intervention60, split_time=60*split_ratio)
result120 = AnalysisBehavior.piecewise_linear(intervention120, split_time=120*split_ratio)
result180 = AnalysisBehavior.piecewise_linear(intervention180, split_time=180*split_ratio)
result240 = AnalysisBehavior.piecewise_linear(intervention240, split_time=240*split_ratio)
result300 = AnalysisBehavior.piecewise_linear(intervention300, split_time=300*split_ratio)

print(result60['pvalue1'], result60['pvalue2'])
print(result120['pvalue1'], result120['pvalue2'])
print(result180['pvalue1'], result180['pvalue2'])
print(result240['pvalue1'], result240['pvalue2'])
print(result300['pvalue1'], result300['pvalue2'])

r60p1 = FormatUtils.format_pvalue(result60['pvalue1'], subscript='1')
r60p2 = FormatUtils.format_pvalue(result60['pvalue2'], subscript='2')
r120p1 = FormatUtils.format_pvalue(result120['pvalue1'], subscript='1')
r120p2 = FormatUtils.format_pvalue(result120['pvalue2'], subscript='2')
r180p1 = FormatUtils.format_pvalue(result180['pvalue1'], subscript='1')
r180p2 = FormatUtils.format_pvalue(result180['pvalue2'], subscript='2')
r240p1 = FormatUtils.format_pvalue(result240['pvalue1'], subscript='1')
r240p2 = FormatUtils.format_pvalue(result240['pvalue2'], subscript='2')
r300p1 =FormatUtils.format_pvalue(result300['pvalue1'], subscript='1')
r300p2 = FormatUtils.format_pvalue(result300['pvalue2'], subscript='2')

prediction1 = result_full['prediction1']
prediction2 = result_full['prediction2']
pvalue1 = result_full['pvalue1']
pvalue2 = result_full['pvalue2']

pvalue1 = FormatUtils.format_pvalue(pvalue1, subscript='1')
pvalue2 = FormatUtils.format_pvalue(pvalue2, subscript='2')


#%%

plt.figure()

colors = Settings.colors

plt.plot(prediction1['TimeToFeeding'], prediction1['Predicted'], label='Predicted Activity (First Half)', linewidth=2, color='black', markersize=10, marker='$↓$', zorder=10)
plt.plot(prediction2['TimeToFeeding'], prediction2['Predicted'], label='Predicted Activity (Second Half)', linewidth=2, color='black', marker='$↑$', markersize=10, zorder=10)
plt.gca().invert_xaxis()
plt.axhline(y=baseline_activity, color='gray', linestyle='--', label='Baseline Activity', zorder=0)

intervals.sort()
for index, interval in enumerate(intervals):
    selected_data = proportions.query('Feeder_Interval == @interval')
    current_color = colors[str(interval)]
    plt.plot(selected_data['TimeToFeeding'], selected_data['Active'], alpha=1, label=str(interval) + ' s', linewidth=2, color=current_color, marker = '.')



# Add all the formatted p-values
plt.text(200, 0.75, '60s:   ' + r60p1, fontsize=12, color=colors['60'])
plt.text(200, 0.70, '120s: ' + r120p1, fontsize=12, color=colors['120'])
plt.text(200, 0.65, '180s: ' + r180p1, fontsize=12, color=colors['180'])
plt.text(200, 0.60, '240s: ' + r240p1, fontsize=12, color=colors['240'])
plt.text(200, 0.55, '300s: ' + r300p1, fontsize=12, color=colors['300'])
# Add all the formatted p-values
plt.text(120, 0.75, r60p2, fontsize=12, color=colors['60'])
plt.text(120, 0.70, r120p2, fontsize=12, color=colors['120'])
plt.text(120, 0.65, r180p2, fontsize=12, color=colors['180'])
plt.text(120, 0.60, r240p2, fontsize=12, color=colors['240'])
plt.text(120, 0.55, r300p2, fontsize=12, color=colors['300'])

ax = plt.gca()
ax.set_facecolor('#F1F0EA')

plt.ylim(0, 1)
plt.xlabel('Time to Feeding (s)')
plt.ylabel('Activity (Proportion)')

plt.text(225, 0.50, pvalue1, fontsize=12, color='black')
plt.text(45, 0.20, pvalue2, fontsize=12, color='black')

plt.xticks(range(0, 300, 45))
plt.grid()
plt.legend(ncol=3)
plt.tight_layout()
plt.savefig(output_folder + 'activity.png', dpi=300)
plt.savefig(output_folder + 'activity.pdf')
plt.show()
