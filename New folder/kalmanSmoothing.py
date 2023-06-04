import pandas as pd
import numpy as np
from pykalman import KalmanFilter

df = pd.read_csv('dataset1.csv', header=0, parse_dates=[0], index_col=0)
df.index = pd.to_datetime(df.index, format='%d.%m.%Y')
observed_column = 'numbers'

frac = .90
for c in df.columns:
    idx = np.random.choice(a=df.index, size=int(len(df) * frac))
    df.loc[idx, c] = np.nan

observations = df[observed_column].values
kf = KalmanFilter(transition_matrices=[1],
                  observation_matrices=[1],
                  initial_state_mean=observations[0],
                  initial_state_covariance=1,
                  observation_covariance=1,
                  transition_covariance=0.01)


smoothed_state_means, smoothed_state_covariances = kf.smooth(observations)


print(smoothed_state_means)

