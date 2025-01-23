
from Library import StepAnalysis
from Library import Legend
from matplotlib import pyplot as plt
from Library import Settings
import matplotlib

output_folder = 'steps_output/'

matplotlib.rcParams['font.family'] = 'serif'
data = StepAnalysis.read_data()
data = data.query('steps > 0')
#%%
colors = Settings.colors

intervention_data = data.query('Intervention == True')
baseline_data = data.query('Intervention == False')

figure_size = (12, 8)
plt.figure(figsize=figure_size)

# Calculate total steps per Subject, Per Date
grp = data.groupby(['Subject', 'interval', 'date'], observed=False)
# Use agg to Create a column that is the sum of steps per group
# and one that is max of daily_tots per group
grp = grp.agg({'steps': ['sum', 'count'], 'daily_tots': 'max'})
grp = grp.reset_index()
# Save the data to an Excel file in the output folder
grp.to_excel(f"{output_folder}check_steps.xlsx")


for panel in [1, 2, 4, 5]:
    if panel == 1: cat = 'Bernie'
    if panel == 2: cat = 'Citrine'
    if panel == 4: cat = 'Elia'
    if panel == 5: cat = 'Minerva'

    custom_legend = Legend.CustomLegend()

    plt.subplot(2, 3, panel)

    # Get intervention data for the specific cat
    selected_intervention = intervention_data.query('Subject == @cat')
    grp = selected_intervention.groupby(['days_since_first', 'interval'], observed=False)
    grp = grp['steps'].sum()
    intervention_steps = grp.reset_index()
    intervention_steps['steps'] = intervention_steps['steps']

    intervention60 = intervention_steps.query('interval == 60')
    intervention120 = intervention_steps.query('interval == 120')
    intervention180 = intervention_steps.query('interval == 180')
    intervention240 = intervention_steps.query('interval == 240')
    intervention300 = intervention_steps.query('interval == 300')

    # Get baseline data for the specific cat
    selected_baseline = baseline_data.query('Subject == @cat')
    grp = selected_baseline.groupby(['days_since_first'], observed=False)
    grp = grp['steps'].sum()
    baseline_steps = grp.reset_index()
    baseline_steps['steps'] = baseline_steps['steps']

    # Plot the intervention data
    transparency = 0.25
    size = 50

    plt.scatter(intervention60['days_since_first'], intervention60['steps'], color=colors['60'], label='60s', s=size, alpha=transparency)
    plt.scatter(intervention120['days_since_first'], intervention120['steps'], color=colors['120'], label='120s', s=size, alpha=transparency)
    plt.scatter(intervention180['days_since_first'], intervention180['steps'], color=colors['180'], label='180s', s=size, alpha=transparency)
    plt.scatter(intervention240['days_since_first'], intervention240['steps'], color=colors['240'], label='240s', s=size, alpha=transparency)
    plt.scatter(intervention300['days_since_first'], intervention300['steps'], color=colors['300'], label='300s', s=size, alpha=transparency)

    custom_legend.add_entry(label='60s', color= colors['60'], marker='o', linestyle='')
    custom_legend.add_entry(label='120s', color= colors['120'], marker='o', linestyle='')
    custom_legend.add_entry(label='180s', color= colors['180'], marker='o', linestyle='')
    custom_legend.add_entry(label='240s', color= colors['240'], marker='o', linestyle='')
    custom_legend.add_entry(label='300s', color= colors['300'], marker='o', linestyle='')

    # Plot the baseline data
    transparency = 1
    size = 25

    plt.scatter(baseline_steps['days_since_first'], baseline_steps['steps'], color='grey', label='Baseline', s=size, alpha=transparency)
    custom_legend.add_entry(label='Baseline', color='grey', marker='o', linestyle='')

    # Markup of the plot
    plt.ylim(0,30000)
    plt.xlim(-1, 92)

    plt.xticks(fontsize=16)  # X-axis tick labels font size
    plt.yticks(fontsize=16)  # Y-axis tick labels font size

    ax = plt.gca()
    ax.set_facecolor('#F1F0EA')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    plt.xlabel('Days', fontsize=16)
    plt.ylabel('Steps', fontsize=16)
    plt.title(cat, fontsize=18)

    if panel == 1:
        plt.xticks([])
        plt.xlabel('')
    if panel == 2:
        plt.xticks([])
        plt.yticks([])
        plt.xlabel('')
        plt.ylabel('')
    if panel == 4:
        pass
    if panel == 5:
        plt.yticks([])
        plt.ylabel('')


plt.subplot(2, 3, 3)
plt.axis('off')
custom_legend.draw_legend('upper left')
plt.tight_layout()

output_file = f"{output_folder}steps.png"
plt.savefig(output_file, dpi=300)
plt.show()


# Tests
test1 = data.query('Subject == "Minerva" & interval in [60, 180]')
test1.to_excel(f"{output_folder}test1.xlsx")

test2 = data.query('interval==60 & Subject == "Bernie"')
test2.to_excel(f"{output_folder}test2.xlsx")