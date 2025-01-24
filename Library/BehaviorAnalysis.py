import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from Library import PredictionData



def logit_model(data, model_description):
    model = smf.logit(model_description, data=data)
    result = model.fit()
    summary = result.summary()
    return result, summary

def read_data():
    data = pd.read_csv('data/SIP_observations.csv', index_col=0)
    data = data.query('action_cat != "OutofView"')
    data = data.query('action_cat != "Pace"')
    data = data.copy()
    data['TimeToFeeding'] = data['Feeder_Interval'] - data['rel_time']
    data['Active'] = (data['action_cat'] == 'Active') * 1
    data['Feeder'] = data['Location'] == 'Feeder'
    data['Intervention'] = data['Phase'].str.contains('Inter')

    # Applying the transformations
    data["Location"] = data["Location"].astype(str)
    data["phase"] = np.where(data["Feeder_Interval"] > 0, "Intervention", "Baseline")
    data["Interaction"] = np.where(data["Interaction"] == "0", "Feeder", data["Interaction"].astype(str))
    data["Location"] = np.where(data["Location"] == "0", "Feeder", data["Location"])
    data["Location"] = np.where(data["Location"] == "9", "Fence", data["Location"])
    data["Location"] = np.where(data["Location"] == "20", "Litter Box", data["Location"])
    data["Location"] = np.where(data["Location"] == "8", "Shelf", data["Location"])
    data["Location"] = np.where(data["Location"] == "10", "Out of View", data["Location"])
    data["Activity"] = np.where(data["Activity"] == "10", "Out of View", data["Activity"])

    # Using a lambda function for loc_cat similar to case_when
    data["loc_cat"] = data["Location"].apply(lambda x: "Feeder_Area" if x in ["Feeder", "5", "6"] else
    "Out of View" if x == "Out of View" else "Non-Feeder")

    data['AtFeeder'] = (data['loc_cat'] == 'Feeder_Area') * 1

    data['date'] = pd.to_datetime(data['date'])

    return data

def piecewise_linear(intervention_data, split_time, normalized=False, full=False, use_actual=True):
    split_time = split_time * 1.0
    prediction_data = PredictionData.make_data(full=full)

    selected = intervention_data.copy()
    selected['TimeToFeedingNormalized'] = selected['TimeToFeeding'] / 15
    selected['Active'] = selected['Active'].astype('int')
    model_description = 'Active ~ C(Subject) + Feeder_Interval + TimeToFeeding'
    if normalized: model_description = 'Active ~ C(Subject) + Feeder_Interval + TimeToFeedingNormalized'

    intervals = selected['Feeder_Interval'].unique()
    if len(intervals)==1:
        model_description = 'Active ~ C(Subject) + TimeToFeeding'
        if normalized: model_description = 'Active ~ C(Subject) + TimeToFeedingNormalized'

    cats_in_data = intervention_data['Subject'].unique()
    prediction_data = prediction_data.query('Subject in @cats_in_data')
    prediction_data = prediction_data.query('Feeder_Interval in @intervals')
    if use_actual: prediction_data = intervention_data.copy()

    # PART 1
    first_part = selected.query('TimeToFeeding >= @split_time')
    model = smf.logit(model_description, data=first_part)
    result1 = model.fit()
    summary1 = result1.summary()

    prediction_data1 = prediction_data.query('TimeToFeeding >= @split_time')
    prediction_data1 = prediction_data1.copy()
    prediction_data1['Predicted'] = result1.predict(prediction_data1)
    prediction1 = prediction_data1.groupby('TimeToFeeding')['Predicted'].mean()
    prediction1 = prediction1.reset_index()

    # PART 2
    second_part = selected.query('TimeToFeeding < @split_time')
    model = smf.logit(model_description, data=second_part)
    result2 = model.fit()
    summary2 = result2.summary()

    prediction_data2 = prediction_data.query('TimeToFeeding < @split_time')
    prediction_data2 = prediction_data2.copy()
    prediction_data2['Predicted'] = result2.predict(prediction_data2)
    prediction2 = prediction_data2.groupby('TimeToFeeding')['Predicted'].mean()
    prediction2 = prediction2.reset_index()

    pvalue1 = result1.pvalues['TimeToFeeding']
    pvalue2 = result2.pvalues['TimeToFeeding']

    results = {}
    results['result1'] = result1
    results['result2'] = result2
    results['prediction1'] = prediction1
    results['prediction2'] = prediction2
    results['summary1'] = summary1
    results['summary2'] = summary2
    results['pvalue1'] = pvalue1
    results['pvalue2'] = pvalue2
    return results



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