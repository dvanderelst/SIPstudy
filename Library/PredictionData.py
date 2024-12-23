import pandas as pd

def make_data(full=True):
    cats = 'Bernie', 'Citrine', 'Minerva', 'Elia'
    intervals = [60, 120, 180, 240, 300]
    Subject = []
    Feeder_Interval = []
    TimeToFeeding = []
    for cat in cats:
        for interval in intervals:
            time_to_feedings = list(range(0, interval + 15, 15))
            if full: time_to_feedings = list(range(0, 300 + 15, 15))
            for time_to_feeding in time_to_feedings:
                Subject.append(cat)
                Feeder_Interval.append(interval)
                TimeToFeeding.append(time_to_feeding)

    data = pd.DataFrame({'Subject': Subject, 'Feeder_Interval': Feeder_Interval, 'TimeToFeeding': TimeToFeeding})
    return data