import pandas as pd
import sklearn.neighbors._base
import sys

sys.modules['sklearn.neighbors.base'] = sklearn.neighbors._base
from missingpy import MissForest
import numpy as np


df = pd.read_csv('dataset1.csv', header=0, parse_dates=[0], index_col=0)


missing_columns = ['numbers']
print(df.columns)

frac = .15
for c in df.columns:
    idx = np.random.choice(a=df.index, size=int(len(df) * frac))
    df.loc[idx, c] = np.nan

imputed_df = df.copy()
data_array = imputed_df.to_numpy()
data_array.reshape(-1, 1)

for column in missing_columns:

    X = df[[column]].values

    X.reshape(-1, 1)
    imputer = MissForest()

    imputer_fit = imputer.fit(data_array)
    X_imputed = imputer_fit.fit_transform(X)

    imputed_df[column] = X_imputed


print(imputed_df)
