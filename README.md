## The `read_data` Function

Each of the processing scripts begins by calling the `read_data` function from `data_processing.py` to load and preprocess the data. The `read_data` function loads and preprocesses step activity data from `data/SIP_fitbit_data.csv`. Its main steps are:

- Reads the CSV file into a pandas DataFrame.
- Adds an `Intervention` column indicating if the phase contains an intervention.
- Calculates `TimeToFeeding` as the difference between `interval` and `rel_time`.
- Converts the `date` column to datetime format.
- Renames the `Subject` column to `subject`.
- Removes duplicate rows for each subject, date, hour, and interval.
- Computes the number of days since the earliest date for each entry.
- Returns the cleaned DataFrame for further analysis.

## SCRIPT_process_steps.py

This script analyzes and visualizes step count data for multiple subjects (cats) across experimental intervals.

### Main Steps

- Loads and preprocesses step data, filtering by subject and valid days.
- Groups and sums steps by day, interval, and intervention status.
- Runs regression analysis on baseline (pre-intervention) data for each subject.
- Compares intervention intervals to baseline using Kolmogorov-Smirnov statistical tests.
- Plots step counts and regression lines for each subject, highlighting significant differences.
- Generates and saves summary statistics and figures (`steps.png`, `steps.pdf`).
- Stores regression results in a pickle file for later use.

### Outputs

- Statistical test results (`steps_output/statistics_steps.txt`)
- Figures (`steps_output/steps.png`, `steps_output/steps.pdf`)
- Regression results (`steps_output/regression.pck`)
