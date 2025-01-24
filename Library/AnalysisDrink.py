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


def read_phase(phase):
    data = pd.read_csv('data/SIP_data.csv', index_col=0)
    data = data.iloc[:, [0, 1, 2, 3, 4, 6, 7]]
    new_variables = ['interval', 'subject', 'date', 'weight', 'session', 'total', 'overnight']
    data.columns = new_variables
    data['interval'] = data['interval'].replace('NA (baseline or weekend)', 'baseline')
    data['date'] = pd.to_datetime(data['date'])  # Convert 'date' column to datetime
    earliest_date = data['date'].min()  # Find the earliest date
    data['days'] = (data['date'] - earliest_date).dt.days  # Calculate days since earliest date

    data.loc[data['session'] <= 0, 'session'] = np.nan
    data.loc[data['overnight'] <= 0, 'overnight'] = np.nan
    data.loc[data['total'] <= 0, 'total'] = np.nan

    data.loc[data['overnight'] > 300, 'total'] = np.nan
    data.loc[data['overnight'] > 300, 'overnight'] = np.nan

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


