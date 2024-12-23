import numpy as np

def piecewise_linear(intervention_data, split_time, normalized=False):
    selected = intervention_data.copy()
    selected['TimeToFeedingNormalized'] = selected['TimeToFeeding'] / 15
    selected['Active'] = selected['Active'].astype('int')

    # -- Logistic Regression -- max time to split_time
    first_part = selected.query('TimeToFeeding >= @split_time')
    model = smf.logit("Active ~ C(Subject) + Feeder_Interval + TimeToFeeding", data=first_part)
    result_part1 = model.fit()
    print('# PART 1')
    print(result_part1.summary())

    prediction_data1 = prediction_data.query('TimeToFeeding >= @split_time')
    prediction_data1['Predicted'] = result_part1.predict(prediction_data1)
    prediction1 = prediction_data1.groupby('TimeToFeeding')['Predicted'].mean()
    prediction1 = prediction1.reset_index()

def compute_transition_matrix(data):
    states = data['Active']
    states = states.values * 1
    states = states.astype('int')

    cats = data['Subject']
    cats = cats.values

    intervals = data['Feeder_Interval']
    intervals = intervals.values

    # Initialize the transition count matrix for two states (0 and 1)
    transition_counts = np.zeros((2, 2))
    count = np.size(states)
    for index in range(1, count):
        # Get the current state and the previous state
        previous_cat = cats[index - 1]
        current_cat = cats[index]
        same_cat = previous_cat == current_cat

        previous_interval = intervals[index - 1]
        current_interval = intervals[index]
        same_interval = previous_interval == current_interval

        current_state = states[index]
        previous_state = states[index - 1]

        if same_cat and same_interval: transition_counts[previous_state, current_state] += 1
    return transition_counts / np.sum(transition_counts, axis=1)[:, None]