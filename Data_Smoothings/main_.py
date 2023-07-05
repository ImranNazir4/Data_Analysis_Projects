import numpy as np
import pandas as pd

from kalman import na_kalman

df = pd.read_csv('Dataset1.csv', header=0, parse_dates=[0], index_col=0)

missing_columns = ['numbers']
print(df.columns)

frac = .15
for c in df.columns:
    idx = np.random.choice(a=df.index, size=int(len(df) * frac))
    df.loc[idx, c] = np.nan

na_kalman((df), model="StructTS", smooth=True)
