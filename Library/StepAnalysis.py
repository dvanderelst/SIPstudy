import pandas as pd


def read_data():
    data = pd.read_csv('data/SIP_fitbit_data.csv', index_col=0)
    data['Intervention'] = data['phase'].str.contains('Inter')
    data['TimeToFeeding'] = data['interval'] - data['rel_time']
    data['date'] = pd.to_datetime(data['date'])
    # Get the number of days since the first date for each subject
    # Rename "Subject" to "subject"
    data = data.rename(columns={'Subject': 'subject'})
    # for each Subject, Hour and Date, keep one row
    data = data.drop_duplicates(subset=['subject', 'date', 'hour', 'interval'])
    earliest_date = data['date'].min()  # Find the earliest date
    data['days'] = (data['date'] - earliest_date).dt.days  # Calculate days since earliest date
    return data


