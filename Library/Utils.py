import pandas as pd
import numpy as np

def plot_nr(phase, index):
    if phase == 1:
        if index == 0: return 1
        if index == 1: return 2
        if index == 2: return 4
        if index == 3: return 5
        if index > 3: return 3

    if phase == 2:
        if index == 0: return 1
        if index == 1: return 2
        if index > 1: return 3


def format_ktest_result_apa(statistic, pvalue, alpha=0.05):
    if statistic == 'NaN': return f"k = NaN, p = NaN"
    if pvalue < alpha:
        formatted_pvalue = "p < " + str(alpha)
    else:
        formatted_pvalue = f"p = {pvalue:.2f}"
    formatted_output = f"k = {statistic:.2f}, {formatted_pvalue}"
    return formatted_output

def pvalue_to_marker(p, levels=None, markers=None):
    if levels is None:
        levels = [0.001, 0.01, 0.05, 0.1]
    if markers is None:
        markers = ["***", "**", "*", "."]
    if len(levels) != len(markers):
        raise ValueError("Levels and markers must have the same length.")
    for level, marker in zip(levels, markers):
        if p < level:
            return marker
    return "n.s."


def format_pvalue(p, levels=None, subscript = ''):
    if levels is None:
        levels = [0.001, 0.01, 0.05, 0.1]
    levels = sorted(levels)
    for level in levels:
        if p < level:
            return f"$p_{subscript} < {level}$"
    return f"$p_{subscript} = {p:.2f}$"

def format_ttest_result_apa(ttest_result, alpha=0.05):
    statistic = ttest_result.statistic
    pvalue = ttest_result.pvalue
    df = ttest_result.df
    formatted_pvalue = format_pvalue(pvalue, [alpha])
    formatted_output = f"t({df:.0f}) = {statistic:.2f}, {formatted_pvalue}"
    return formatted_output

def read_phase(phase):
    data = pd.read_csv('data/SIP_data.csv', index_col=0)
    data = data.iloc[:, [0, 1, 2, 3, 4, 6, 7]]
    new_variables = ['interval', 'subject', 'date', 'weight', 'session', 'total', 'overnight']
    data.columns = new_variables
    data['interval'] = data['interval'].replace('NA (baseline or weekend)', 'baseline')
    data['date'] = pd.to_datetime(data['date'])
    data['date'] = pd.to_datetime(data['date'])  # Convert 'date' column to datetime
    earliest_date = data['date'].min()  # Find the earliest date
    data['days'] = (data['date'] - earliest_date).dt.days  # Calculate days since earliest date

    # Original DataFrame
    original_data = pd.DataFrame(data)
    #data = data.dropna()
    #data = add_block_number(data)
    #data = data.query('session > 0') #remove negative amount of drinking
    #data = data.query('overnight > 0')
    #data = data.query('total > 0')

    data.loc[data['session'] <= 0, 'session'] = np.nan
    data.loc[data['overnight'] <= 0, 'overnight'] = np.nan
    data.loc[data['total'] <= 0, 'total'] = np.nan

    data.loc[data['overnight'] > 300, 'total'] = np.nan
    data.loc[data['overnight'] > 300, 'overnight'] = np.nan

    # Print removed rows
    #removed_data = original_data[~original_data.index.isin(data.index)]
    #print("Removed rows:")
    #print(removed_data)

    if phase == 1:
        cutoff_date = pd.to_datetime('7-3-23', format='%m-%d-%y')
        data = data.loc[(data['subject'] != 'Citrine') | (data['date'] <= cutoff_date)]
        cutoff_date = pd.to_datetime('8-14-23', format='%m-%d-%y')
        data = data.loc[(data['subject'] != 'Elia') | (data['date'] <= cutoff_date)]

    if phase == 2:
        cutoff_date = pd.to_datetime('7-2-23', format='%m-%d-%y')
        data1 = data.loc[(data['subject'] == 'Citrine') & (data['date'] > cutoff_date)]
        cutoff_date = pd.to_datetime('8-13-23', format='%m-%d-%y')
        data2 = data.loc[(data['subject'] == 'Elia') & (data['date'] > cutoff_date)]
        data = pd.concat([data1, data2])

    return data

def add_block_number(df, max_gap_days=5):
    subject_column = 'subject'
    condition_columns = ['interval']
    day_column = 'days'

    #df_sorted = df.sort_values(by=[subject_column, *condition_columns, day_column])
    df_sorted = df.sort_values(by=[subject_column, day_column])

    sessions = []
    session_count = 0
    last_subject = None
    last_conditions = None
    last_day = None

    for index, row in df_sorted.iterrows():
        if row[subject_column] != last_subject:
            session_count = 0
        elif row[condition_columns].tolist() != last_conditions or (row[day_column] - last_day) > max_gap_days:
            session_count += 1
        sessions.append(session_count)
        last_subject = row[subject_column]
        last_conditions = row[condition_columns].tolist()
        last_day = row[day_column]

    df_with_block = df_sorted.copy()
    df_with_block['block'] = sessions

    return df_with_block


# def average_of_consecutive_sets(days, threshold=5):
#     numbers = days.values
#     averages = []
#     current_group = []
#     current_sum = 0
#     count = 0
#
#     for i, num in enumerate(numbers):
#         if not current_group or abs(num - current_group[-1]) <= threshold:
#             current_group.append(num)
#             current_sum += num
#             count += 1
#         else:
#             averages.append(current_sum / count)
#             current_group = [num]
#             current_sum = num
#             count = 1
#
#     if current_group:  # Process the last group
#         averages.append(current_sum / count)
#
#     return averages