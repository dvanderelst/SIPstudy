import numpy
import numpy as np
import natsort
from scipy.stats import probplot
from Library import Stats
from Library import Settings
from Library import Utils
from Library import Legend
from scipy.stats import ttest_ind
from matplotlib import pyplot as plt
from scipy.stats import kstest, norm
import matplotlib

##########################
phase = 1
alpha_level = 0.0005
output_folder = 'drinking_output/'
##########################

max_days_log = {}
all_residuals = []
for dependent_variable in ['session', 'overnight', 'total']:

    if phase == 1:
        figure_size = (12, 8)
        nr_rows = 2
        max_day_range = 92

    if phase == 2:
        figure_size = (12, 4)
        nr_rows = 1
        max_day_range = 80


    matplotlib.rcParams['font.family'] = 'serif'
    colors = Settings.colors
    data = Utils.read_phase(phase=phase)

    max_plot_range = numpy.max(data[dependent_variable]) + 10

    cats = list(data.subject.unique())
    cats = natsort.natsorted(cats)

    intervals = list(data.interval.unique())
    if np.nan in intervals: intervals.remove(np.nan)

    plt.figure(figsize=figure_size)

    tests_output = open(f'{output_folder}statistics_phase{phase}_{dependent_variable}.txt', 'w')

    for plot_index, cat_name in enumerate(cats):
        plot_nr = Utils.plot_nr(phase=phase, index=plot_index)
        plt.subplot(nr_rows, 3, plot_nr)
        selected_cat = data.query('subject ==@cat_name')
        selected_cat.loc[:, 'days'] = selected_cat['days'] - numpy.min(selected_cat['days'])
        max_day = numpy.max(selected_cat.days)
        max_days_log[cat_name] = max_day
        base_line_data = selected_cat.query('interval == "baseline"')
        regression_result = Stats.regression(base_line_data, dependent_variable, alpha_level)
        residuals = regression_result['residuals']
        all_residuals.extend(residuals)
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
                prediction_mean = Stats.predict(regression_result, mn_day)
                prediction_std =  regression_result['prstd']
                shifted_residuals = residuals + prediction_mean
                shifted_residuals_std = np.std(shifted_residuals)
                session_data = selected_data[dependent_variable].values
                print(np.std(shifted_residuals), prediction_std)

                try:
                    session_data = session_data[~np.isnan(session_data)]
                    stat, ks_result_p = kstest(session_data, 'norm', args=(prediction_mean, shifted_residuals_std))
                except ValueError as ve:
                    stat = 'NaN'
                    ks_result_p = 1

                formatted1 = Utils.format_ktest_result_apa(stat, ks_result_p, alpha_level)

                tt_result = ttest_ind(session_data, shifted_residuals)
                tt_result_p = tt_result[1]
                formatted2 = Utils.format_ttest_result_apa(tt_result, alpha_level)

                marker = '+'
                size = 150
                if ks_result_p < alpha_level: marker = '*'
                mn_session = numpy.nanmean(selected_data[dependent_variable])
                plt.scatter(mn_day, mn_session, marker=marker, s=150, color=current_color)
                if interval == '60': interval = '  ' + interval
                custom_legend.add_entry(label=interval + 's', color=current_color, marker='o', linestyle='')
                #print(interval, predicted, mn_session, max_day)
                print(cat_name, interval, formatted1, formatted2)
                statistics_line = f'{cat_name}, interval: {interval}, {formatted1}, {formatted2}\n'
                tests_output.write(statistics_line)

        custom_legend.add_entry(label=f'Average, p > {alpha_level}', color='black', marker='+', linestyle='')
        custom_legend.add_entry(label=f'Average, p < {alpha_level}', color='black', marker='*', linestyle='')
        custom_legend.add_entry(label='Baseline Regression', color='gray', marker='None', linestyle='--')
        custom_legend.add_entry(label='Observation conf.', color='gray', marker='s', linestyle='None', alpha=0.1)

        Stats.plot_line(regression_result, colors['baseline'])
        plt.ylim(-10, max_plot_range)
        plt.xlim(-1, max_day_range)

        plt.title(cat_name, fontsize=18)

        ax = plt.gca()

        if plot_index in [0, 2]: plt.ylabel('Water consumption (ml)', fontsize=16)
        if plot_index not in [0,2]: ax.set_yticks([])
        if phase == 1 and plot_index in [0, 1]: ax.set_xticks([])
        plt.xlabel('Days', fontsize=18)
        if phase == 1 and plot_index in [0, 1]: plt.xlabel('')

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        plt.xticks(fontsize=16)  # X-axis tick labels font size
        plt.yticks(fontsize=16)  # Y-axis tick labels font size

        ax = plt.gca()
        ax.set_facecolor('#F1F0EA')

    plot_nr = Utils.plot_nr(phase=phase, index=100)
    plt.subplot(nr_rows, 3, plot_nr)
    plt.axis('off')
    custom_legend.draw_legend('upper left')
    plt.tight_layout()

    output_file = f"{output_folder}phase_{phase}_{dependent_variable}.png"

    plt.savefig(output_file, dpi=300)
    plt.show()
    tests_output.close()

    # plt.figure()
    # plt.hist(residuals, color=colors['baseline'])
    # plt.show()


output_file = f"{output_folder}phase_{phase}_averages.xlsx"
grps = data.groupby(['subject', 'interval'])
mn = grps.session.agg(['mean', 'std'])
mn.to_excel(output_file, index=True)

all_residuals = np.array(all_residuals)
# Create Q-Q plot
fig, ax = plt.subplots()
probplot(all_residuals, dist="norm", plot=ax)  # Compare to normal distribution
ax.get_lines()[1].set_color("red")   # Optional: Set the trend line color
plt.title("Q-Q Plot")
plt.show()