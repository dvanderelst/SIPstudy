#  Data

This section explain the available data and how it is read in. 

- **`SIP_fitbit_data.csv`** 
	+ Contains the number of steps recorded.
	+ This file is read by the function `Read_Data` defined in `AnalysisStep.py`.

- **`SIP_data.csv`**
	+ Contains data on drinking behavior.
	+ This file is read by the function `Read_Data` defined in `AnalysisDrinking.py`. 

- **`SIP_observations_2-7-25_take2.csv`** 
	+ Contains information on location and activity. 
	+ This file is read by the function `Read_Data` defined in `AnalysisBehavior.py`.

# Step counts: `SCRIPT_process_steps.py`

This script analyzes and visualizes step count data for multiple subjects (cats) across experimental intervals.

## Main Steps

- Loads and preprocesses step data, filtering by subject and valid days.
- Groups and sums steps by day, interval, and intervention status.
- Runs regression analysis on baseline (pre-intervention) data for each subject.
- Compares intervention intervals to baseline using Kolmogorov-Smirnov statistical tests.
- Plots step counts and regression lines for each subject, highlighting significant differences.
- Generates and saves summary statistics and figures (`steps.png`, `steps.pdf`).
- Stores regression results in a pickle file for later use.

## Outputs

- Statistical test results (`steps_output/statistics_steps.txt`)
- Figures (`steps_output/steps.png`, `steps_output/steps.pdf`)
- Regression results (`steps_output/regression.pck`)

# Activity analysis: `SCRIPT_process_activity.py`

This script analyzes and visualizes activity data (from direct behavioral observations) for multiple subjects across feeding intervals.

## Main Steps

- Loads and preprocesses observational data using `AnalysisBehavior.read_data()`, excluding irrelevant behaviors and standardizing categories.
- Derives timing measures (`TimeSinceFeeding`, `TimeToFeeding`) and flags for whether animals were active or at the feeder.
- Splits data into baseline (no intervention) and intervention periods.
- Groups intervention data by feeder interval and time since feeding to compute average activity proportions.
- Runs piecewise logistic regression (`piecewise_linear_activity`) for each feeder interval (60s, 120s, 180s, 240s, 300s) to compare early vs. late phases of each interval.
- Extracts and formats p-values and slopes from the regressions, displaying them on the plots.
- Plots activity levels over time for each feeder interval, showing differences between intervention and baseline activity.
- Generates and saves summary figures (`activity.png`, `activity.pdf`).
- Stores regression results for all intervals in a pickle file for later use.

## Outputs

- Figures (`behavior_output/activity.png`, `behavior_output/activity.pdf`)
- Regression results (`behavior_output/piecewise_linear_activity_results.pck`)


# Drinking behavior: `SCRIPT_process_drinking.py`

This script analyzes water consumption data for multiple subjects (cats) across experimental intervals and phases.

## Main Steps

- Loads and preprocesses drinking data with `AnalysisDrink.read_data(phase)`, filtering by experimental phase and subject-specific cutoff dates.
- Iterates over both **Phase 1** (baseline-to-intervention transition) and **Phase 2** (post-cutoff intervention).
- For each phase and dependent variable (`session`, `overnight`, `total` consumption):
  - Fits a regression model on baseline (pre-intervention) data for each subject.
  - Compares intervention intervals against baseline predictions using Kolmogorov–Smirnov statistical tests.
  - Plots daily drinking measures by interval, overlaying regression lines and highlighting significant deviations.
  - Records summary statistics to a text file.
- Aggregates drinking session statistics (mean, standard deviation) and exports them to Excel files.
- Saves regression results for later reuse.

## Outputs

- Statistical test results (`drinking_output/statistics.txt`)
- Figures for each phase and dependent variable (`drinking_output/phase_[1|2]_[session|overnight|total].png` / `.pdf`)
- Summary averages by subject and interval (`drinking_output/phase_[1|2]_averages.xlsx`)
- Regression results (`drinking_output/all_linear_regression_results.pck`)

# Location analysis: `SCRIPT_process_location.py`

This script analyzes observational data on cats’ time spent at the feeder across different feeding intervals.

## Main Steps

- Loads and preprocesses location/activity observations using `AnalysisBehavior.read_data()`, converting raw codes into interpretable categories (e.g., feeder, fence, litter box).
- Splits data into baseline (no intervention) and intervention conditions.
- Groups intervention data by feeder interval and time since feeding to compute the proportion of time subjects spent at the feeder.
- Fits logistic regression models to test whether feeder interval predicts time at feeder (overall and relative to baseline).
- Runs piecewise logistic regression (`piecewise_linear_location`) for each feeder interval (60s, 120s, 180s, 240s, 300s), splitting early vs. late phases of each interval.
- Extracts p-values and slopes from models and overlays them on plots for interpretation.
- Plots time-at-feeder curves for each interval against baseline, displaying regression significance and formatted statistics.
- Generates additional exploratory subject-specific line plots using seaborn.
- Saves regression results for later reuse.

## Outputs

- Figures (`behavior_output/location.png`, `behavior_output/location.pdf`)
- Regression results (`behavior_output/piecewise_linear_location_results.pck`)


# Compiling the statistics

The script `SCRIPT_compile_stat_results.py` reads the output generated by each of the scripts dicussed above and generates a PDF file combining all stastistical results. This output is provided as supplmentary material to the paper.


