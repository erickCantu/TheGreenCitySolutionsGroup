import itertools
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

#dealing with seasons

def harmonic_approx(x, season_length, coef, intercept=0):
    sum = np.zeros(x.shape) + intercept

    for (i, (c, trig_fun)) in enumerate(zip(coef, itertools.cycle([np.sin, np.cos]))):
        d = i//2+1
        sum += c * trig_fun(x * d * 2*np.pi / season_length)
    
    return sum

def fit_tri(ydata, harmonic_degree, season_length=24*365, x=None, fit_intercept=False):

    if x is None:
        x = ydata.index #assuming that ydata is a Series

    harmonics = range(1, harmonic_degree+1)

    basis = []
    for multiplier in harmonics:
        basis.append(pd.Series( np.sin(x*multiplier*2*np.pi/season_length), name = f'beta_{multiplier}_sin'))
        basis.append(pd.Series( np.cos(x*multiplier*2*np.pi/season_length), name = f'beta_{multiplier}_cos'))

    trig_basis = pd.concat(basis, axis=1)

    lr = LinearRegression()
    model = lr.fit(trig_basis, ydata)
    if fit_intercept:
        intercept = model.intercept_
    else:
        intercept = 0
    
    approximation_result = harmonic_approx(x, season_length, model.coef_, intercept)

    return (model, approximation_result)