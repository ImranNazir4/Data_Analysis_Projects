import pandas as pd
import numpy as np
from impyute.imputation.cs import EM


df = pd.read_csv('dataset1.csv')


missing_columns = ['numbers']

frac = .15
for c in df.columns:
    idx = np.random.choice(a=df.index, size=int(len(df) * frac))
    df.loc[idx, c] = np.nan

imputed_df = df.copy()


for column in missing_columns:

    X = df[[column]].values

    imputed_X = EM().fit_transform(X)

    imputed_df[column] = imputed_X


print(imputed_df)
