import re
import pandas as pd
import datetime
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

#write
# span('2008-01-02 00:00', '2011-12-31 23:00')
#or even shorter
# span('2008-01-02', '2011-12-31')
#instead of
# pd.date_range('2008-01-02 00:00', '2011-12-31 23:00', freq='H')

def span(start, end=None, freq='H'):
    if not end:
        end = start
    pattern = re.compile("^....-..-..$") #matches patterns like YYYY-MM-DD
    if pattern.match(start):
        start += " 00:00"
    if pattern.match(end):
        end += " 23:00"
    return pd.date_range(start=start, end=end, freq=freq)


def metrics_dict(y_true, y_pred, metric_strs):
    """Get a dict with evaluations of the requested metrics

    Args:
        y_true (array-like): actual data
        y_pred (array-like): predicted data
        metric_strs (list): list of strings identifying the metrics

    Returns:
        dict: dict with metric_strs as keys and the respective metric values
    """
    
    metric_funcs = {
        "mae": mean_absolute_error,
        "mse": mean_squared_error,
        "r2_score": r2_score,
    }
    return {
        name: func(y_true, y_pred)
        for (name, func) in metric_funcs.items()
        if name in metric_strs
    }
    
def datetime2index(dt):
    duration = dt - datetime.datetime(2008, 1, 2)
    index = duration.days*24 + duration.seconds//3600
    return index

def index2datetime(index):
    dt = datetime.datetime(2008, 1, 2) + datetime.timedelta(hours=index)
    return dt