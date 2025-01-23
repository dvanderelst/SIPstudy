import pandas as pd
import numpy as np

def read_data():
    data = pd.read_csv('data/SIP_fitbit_data.csv', index_col=0)
    data['Intervention'] = data['phase'].str.contains('Inter')
    data['TimeToFeeding'] = data['interval'] - data['rel_time']
    data['date'] = pd.to_datetime(data['date'])
    # Get the number of days since the first date for each subject
    # This allows plotting data on a global timeline
    data['days_since_first'] = data.groupby('Subject')['date'].transform(lambda x: (x - x.min()).dt.days)
    # for each Subject, Hour and Date, keep one row
    data = data.drop_duplicates(subset=['Subject', 'date', 'hour', 'interval'])
    return data


