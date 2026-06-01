import numpy
import numpy as np
import natsort
from scipy.stats import probplot

from Library import FormatUtils
from Library import Stats
from Library import Settings
from Library import AnalysisDrink
from Library import Legend
from matplotlib import pyplot as plt
from scipy.stats import ks_2samp
import matplotlib
import pickle

##########################
phase = 1
alpha_level = 0.001
output_folder = 'drinking_output/'
##########################

max_days_log = {}

tests_output = open(f'{output_folder}statistics.txt', 'w')

all_linear_regression_results = {}

for phase in [1, 2]:
    for dependent_variable in ['session', 'overnight', 'total']:
        print(f"+ Phase: {phase}, dependent_variable: {dependent_variable}")
        title_line = f"Phase: {phase}, Dependent Variable: {dependent_variable}\n"
        tests_output.write(title_line)

        figure_size = (12, 8)
        nr_rows = 2
        max_day_range = 92

        if phase == 2:
            figure_size = (12, 4)
            nr_rows = 1
            max_day_range = 80

        matplotlib.rcParams['font.family'] = 'serif'
        colors = Settings.colors
        data = AnalysisDrink.read_data(phase=phase)

        max_plot_range = numpy.max(data[dependent_variable]) + 10

        # Get a list of cats
        cats = list(data.subject.unique())
        cats = natsort.natsorted(cats)

        # Get a list of intervals (including "baseline")
        # This will be a list of strings
        intervals = list(data.interval.unique())
        if np.nan in intervals: intervals.remove(np.nan)

        plt.figure(figsize=figure_size)


        for plot_index, cat_name in enumerate(cats):
            print(f"++ Processing Cat {cat_name}")

            # Run the regression on the baseline data
            selected_cat = data.query('subject ==@cat_name')
            selected_cat.loc[:, 'days'] = selected_cat['days'] - numpy.min(selected_cat['days'])
            max_day = numpy.max(selected_cat.days)
            max_days_log[cat_name] = max_day
            base_line_data = selected_cat.query('interval == "baseline"')
            regression_result = Stats.regression(base_line_data, dependent_variable, alpha_level)

            label = f"{cat_name}_phase_{phase}_{dependent_variable}"
            all_linear_regression_results[label] = regression_result

            residuals = regression_result['residuals']

            plot_nr = AnalysisDrink.plot_nr(phase=phase, index=plot_index)
            plt.subplot(nr_rows, 3, plot_nr)
            custom_legend = Legend.CustomLegend()

            for interval in intervals:
                print(f"+++ Processing Interval {interval}")
                selected_data = selected_cat.query('interval == @interval')
                transparency = 1
                size = 50
                if interval != "baseline": transparency = 0.25
                if interval == 'baseline': size = 25

                plt.scatter(selected_data.days, selected_data[dependent_variable], color=colors[interval], alpha=transparency, s=size)
                custom_legend.add_entry(label='Baseline', color='gray', marker='o', linestyle='')

                if interval != "baseline":
                    marker = '+'
                    size = 150
                    current_color = colors[interval]

                    # Get the prediction errors
                    prediction = Stats.predict(regression_result, selected_data.days)
                    prediction_errors = selected_data[dependent_variable] - prediction
                    prediction_errors = prediction_errors[~np.isnan(prediction_errors)]


                    # Compare two empirical distributions
                    stat, ks_result_p = ks_2samp(residuals, prediction_errors)
                    formatted = FormatUtils.format_ktest_result_apa(stat, ks_result_p, alpha_level)
                    if ks_result_p < alpha_level: marker = '*'
                    mn_session = numpy.nanmean(selected_data[dependent_variable])
                    mn_day = numpy.mean(selected_data.days)
                    plt.scatter(mn_day, mn_session, marker=marker, s=150, color=current_color)
                    if interval == '60': interval = '  ' + interval
                    custom_legend.add_entry(label=interval + 's', color=current_color, marker='o', linestyle='')

                    statistics_line = f'{cat_name}, {interval}, {formatted}\n'
                    tests_output.write(statistics_line)

            custom_legend.add_entry(label=f'Interval Mean, $p$ > {alpha_level}', color='black', marker='+', linestyle='')
            custom_legend.add_entry(label=f'Interval Mean, $p$ < {alpha_level}', color='black', marker='*', linestyle='')
            custom_legend.add_entry(label='Baseline Regression', color='gray', marker='None', linestyle='--')

            Stats.plot_line(regression_result, colors['baseline'])
            plt.ylim(-10, max_plot_range)
            plt.xlim(-1, max_day_range)

            plt.title(cat_name, fontsize=18)

            ax = plt.gca()

            if plot_index in [0, 2]: plt.ylabel('Water consumption (mL)', fontsize=16)
            if plot_index not in [0, 2]: ax.set_yticks([])
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

        plot_nr = AnalysisDrink.plot_nr(phase=phase, index=100)
        plt.subplot(nr_rows, 3, plot_nr)
        plt.axis('off')
        custom_legend.draw_legend('upper left')
        plt.tight_layout()

        output_file = f"{output_folder}phase_{phase}_{dependent_variable}.png"
        plt.savefig(output_file, dpi=300)

        output_file = f"{output_folder}phase_{phase}_{dependent_variable}.pdf"
        plt.savefig(output_file)

        plt.show()

    output_file = f"{output_folder}phase_{phase}_averages.xlsx"
    grps = data.groupby(['subject', 'interval'])
    mn = grps.session.agg(['mean', 'std'])
    mn.to_excel(output_file, index=True)

tests_output.close()
print(max_days_log)

# Save the piecewise_linear_activity results to a pickle file for later use
pickle_file = f"{output_folder}all_linear_regression_results.pck"
pickle_file_handle = open(pickle_file, 'wb')
pickle.dump(all_linear_regression_results, pickle_file_handle)
pickle_file_handle.close()
