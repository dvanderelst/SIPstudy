import numpy
from Library import Stats
from Library import Settings
from Library import Utils
from Library import Legend
from scipy.stats import ttest_ind
from matplotlib import pyplot as plt
import matplotlib

##########################
phase = 1
dependent_variable = "session" #total, overnight, session
alpha_level = 0.0005
##########################

if phase == 1:
    figure_size = (20, 4)
    nr_subplots = 5
    max_day_range = 92

if phase == 2:
    figure_size = (12, 4)
    nr_subplots = 3
    max_day_range = 80


matplotlib.rcParams['font.family'] = 'serif'
colors = Settings.colors
data = Utils.read_phase(phase=phase)

max_plot_range = numpy.max(data[dependent_variable]) + 10

cats = list(data.subject.unique())
intervals = list(data.interval.unique())

plt.figure(figsize=figure_size)

tests_output = open(f'statistics_phase{phase}_{dependent_variable}.txt', 'w')

for plot_index, cat_name in enumerate(cats):
    plt.subplot(2, 3, plot_index + 1)
    selected_cat = data.query('subject ==@cat_name')
    #selected_cat['days'] = selected_cat['days'] - numpy.min(selected_cat['days'])
    selected_cat.loc[:, 'days'] = selected_cat['days'] - numpy.min(selected_cat['days'])
    max_day = numpy.max(selected_cat.days)
    base_line_data = selected_cat.query('interval == "baseline"')
    regression_result = Stats.regression(base_line_data, dependent_variable, alpha_level)
    residuals = regression_result['residuals']

    custom_legend = Legend.CustomLegend()
    for interval in intervals:
        selected_data = selected_cat.query('interval == @interval')

        transparency = 1
        size = 50
        if interval != "baseline": transparency = 0.25
        if interval == 'baseline': size = 25
        plt.scatter(selected_data.days, selected_data[dependent_variable], color=colors[interval], alpha=transparency, s=size)
        custom_legend.add_entry(label='Baseline', color='gray', marker='o', linestyle='')

        if interval != "baseline":
            current_color = colors[interval]
            mn_day = numpy.mean(selected_data.days)
            predicted = Stats.predict(regression_result, mn_day)
            shifted_residuals = predicted + residuals
            session_data = selected_data[dependent_variable].values
            tt_result = ttest_ind(session_data, shifted_residuals)
            tt_result_p = tt_result[1]
            formatted = Utils.format_ttest_result_apa(tt_result, alpha_level)
            marker = '+'
            size = 150
            if tt_result_p < alpha_level: marker = '*'
            mn_session = numpy.mean(selected_data[dependent_variable])
            plt.scatter(mn_day, mn_session, marker=marker, s=150, color=current_color)
            if interval == '60': interval = '  ' + interval
            custom_legend.add_entry(label=interval + ' ms', color=current_color, marker='o', linestyle='')
            #print(interval, predicted, mn_session, max_day)
            print(cat_name, interval, formatted)
            statistics_line = f'{cat_name}, interval: {interval}, {formatted}\n'
            tests_output.write(statistics_line)

    custom_legend.add_entry(label=f'Average, p > {alpha_level}', color='black', marker='+', linestyle='')
    custom_legend.add_entry(label=f'Average, p < {alpha_level}', color='black', marker='*', linestyle='')
    custom_legend.add_entry(label='Baseline Regression', color='gray', marker='None', linestyle='--')
    custom_legend.add_entry(label='Prediction conf.', color='gray', marker='s', linestyle='None', alpha=0.1)

    Stats.plot_line(regression_result, colors['baseline'])
    plt.ylim(-10, max_plot_range)
    plt.xlim(-1, max_day_range)
    plt.xlabel('Days', fontsize=18)
    plt.title(cat_name, fontsize=18)

    ax = plt.gca()

    if plot_index == 0: plt.ylabel('Water consumption (ml)', fontsize=16)
    if plot_index > 0: ax.set_yticks([])

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    plt.xticks(fontsize=16)  # X-axis tick labels font size
    plt.yticks(fontsize=16)  # Y-axis tick labels font size

    ax = plt.gca()
    ax.set_facecolor('#F1F0EA')

plt.subplot(2, nr_subplots, plot_index + 2)
plt.axis('off')
custom_legend.draw_legend('upper left')
plt.tight_layout()

output_file = f"phase_{phase}_{dependent_variable}.png"

plt.savefig(output_file, dpi=300)
plt.show()
tests_output.close()

# plt.figure()
# plt.hist(residuals, color=colors['baseline'])
# plt.show()
