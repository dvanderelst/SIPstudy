import matplotlib
import pandas as pd
import numpy as np
from Library import Logistic
from Library import PredictionData
from Library import Settings
import statsmodels.formula.api as smf
from matplotlib import pyplot as plt
import seaborn as sns

matplotlib.rcParams['font.family'] = 'serif'

output_folder = 'behavior_output/'
prediction_data = PredictionData.make_data(full=False)

data = pd.read_csv('data/SIP_observations.csv', index_col=0)
data = data.query('action_cat != "OutofView"')
data = data.query('action_cat != "Pace"')
data['TimeToFeeding'] = data['Feeder_Interval'] - data['rel_time']
data['Active'] = (data['action_cat'] == 'Active') * 1
data['Feeder'] = data['Location'] == 'Feeder'
data['Intervention'] = data['Phase'].str.contains('Inter')

# todo: How do we deal with TimeToFeeding == 0?
# data = data.query('TimeToFeeding > 0')

intervention = data.query('Intervention == True')
base_line = data.query('Intervention == False')


grouped = intervention.groupby(['Feeder_Interval', 'TimeToFeeding'], observed=False)
proportions = grouped.Active.mean()
proportions = proportions.reset_index()
proportions = proportions.dropna()


baseline_activity = base_line.Active.mean()

intervals = intervention['Feeder_Interval'].unique()
observation_points = intervention['TimeToFeeding'].unique()

# %% Is there a difference in activity between different feeder intervals, right before feeding?
almost_feeding_time = 15

selected = intervention.copy()
selected = selected.query('TimeToFeeding == @almost_feeding_time')
selected['Active'] = selected['Active'].astype('int')
model = smf.logit("Active ~ C(Subject) + Feeder_Interval", data=selected)
result = model.fit()
print(result.summary())

# %% Does activity decrease until split_time and then increase as we get closer to feeding time?
split_time = 150
selected = intervention.copy()
selected['TimeToFeedingNormalized'] = selected['TimeToFeeding'] / 15
selected['Active'] = selected['Active'].astype('int')

# -- Logistic Regression -- max time to split_time
first_part = selected.query('TimeToFeeding >= @split_time')
model = smf.logit("Active ~ C(Subject) + Feeder_Interval + TimeToFeeding", data=first_part)
result_part1 = model.fit()
print('# PART 1')
print(result_part1.summary())

prediction_data1 = prediction_data.query('TimeToFeeding >= @split_time')
prediction_data1['Predicted'] = result_part1.predict(prediction_data1)
prediction1 = prediction_data1.groupby('TimeToFeeding')['Predicted'].mean()
prediction1 = prediction1.reset_index()

pvalue1 = result_part1.pvalues['TimeToFeeding']
# format pvalue with 2 decimals
if pvalue1 < 0.01:
    pvalue1 = "p < 0.01"
else:
    pvalue1 = "p = {:.2f}".format(pvalue1)

# -- Logistic Regression -- from split_time to 0
second_part = selected.query('TimeToFeeding < @split_time')
model = smf.logit("Active ~ C(Subject) + Feeder_Interval + TimeToFeeding", data=second_part)
result_part2 = model.fit()
print('# PART 2')
print(result_part2.summary())

prediction_data2 = prediction_data.query('TimeToFeeding < @split_time')
prediction_data2['Predicted'] = result_part2.predict(prediction_data2)
prediction2 = prediction_data2.groupby('TimeToFeeding')['Predicted'].mean()
prediction2 = prediction2.reset_index()

pvalue2 = result_part2.pvalues['TimeToFeeding']
# format pvalue with 2 decimals
if pvalue2 < 0.01:
    pvalue2 = "p < 0.01"
else:
    pvalue2 = "p = {:.2f}".format(pvalue1)

# %%
plt.figure()

plt.plot(prediction1['TimeToFeeding'], prediction1['Predicted'], label='Predicted Activity (First Half)', linewidth=2, color='black', markersize=10, marker='$↓$', zorder=10)
plt.plot(prediction2['TimeToFeeding'], prediction2['Predicted'], label='Predicted Activity (Second Half)', linewidth=2, color='black', marker='$↑$', markersize=10, zorder=10)
plt.gca().invert_xaxis()


plt.axhline(y=baseline_activity, color='gray', linestyle='--', label='Baseline Activity', zorder=0)

colors = Settings.colors
intervals.sort()
for index, interval in enumerate(intervals):
    selected_data = proportions.query('Feeder_Interval == @interval')
    current_color = colors[str(interval)]
    plt.plot(selected_data['TimeToFeeding'], selected_data['Active'], alpha=1, label=str(interval) + ' s', linewidth=2, color=current_color, marker = '.')

plt.ylim(0, 1)
plt.xlabel('Time to Feeding (s)')
plt.ylabel('Activity (Proportion)')

ax = plt.gca()
# Set visibility of spines
ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)
ax.set_facecolor('#F1F0EA')

# add p-values to graph
plt.text(225, 0.45, pvalue1, fontsize=12, color='black')
plt.text(45, 0.20, pvalue2, fontsize=12, color='black')

plt.xticks(range(0, 300, 45))
plt.grid()
plt.legend(ncol=3)
plt.tight_layout()
plt.savefig(output_folder + 'activity.png', dpi=300)
plt.savefig(output_folder + 'activity.pdf')
plt.show()


#%%
# plt.figure()
# sns.lineplot(x='TimeToFeeding', y='Predicted', hue='Feeder_Interval', data=prediction_data1)
# plt.show()
