import inline as inline

import rpy2.robjects as robjects
# import R packages
from rpy2.robjects.packages import importr
imputeTS = importr('imputeTS') 

kalman_StructTs = robjects.r['na.kalman']
kalman_auto_arima = robjects.r['na.kalman']

# for other imputation methods
import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
#%matplotlib inline
df = pd.read_csv('dataset1.csv', header=0, parse_dates=[0], index_col=0)

missing_minutes = list(df[df['numbers'].isnull()].index)


def method_plot(df, cols):
    fig, ax = plt.subplots()
    if isinstance(cols, str):
        df[cols].plot(style='b--', ax=ax)
    else:
        for c in cols:
            df[c].plot(style='b--', ax=ax)
    df['numbers'].plot(style='bo', ax=ax)

this_value = np.ndarray.tolist(df['numbers'].values)
this_value = robjects.FloatVector(this_value)

df['dataset1_kalman'] = kalman_StructTs(this_value, model = "StructTS")
method_plot(df, 'dataset1_kalman')
