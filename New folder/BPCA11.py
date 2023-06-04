import numpy as np
import pandas as pd
from bpca import BPCA
from pca_all_impute import PCAImputer


def csv(file_path):

    df = pd.read_csv(file_path, header=0, parse_dates=[0], index_col=0)

    df.index = pd.to_datetime(df.index, format='%d.%m.%Y')
    data_missing1 = df.copy()
    frac = .99
    idx = np.random.choice(a=df.index, size=int(len(df) * frac))
    for c in df.columns:

        df.loc[idx, c] = np.nan
    print(df)
    data_missing1[np.where(idx)] = np.nan

    #imputed_df = df.copy()
    #data_array = imputed_df.to_numpy()
    missing_columns = ['numbers']
    #data_missing1 = df.copy()

    print(data_missing1)
    for column in missing_columns:
        cov = np.diag(np.array(df[[column]].values))
        #imputer = BPCA()
        #imputed_df[column] = imputer.fit(cov, iters=10, verbose=True, trace_loglikelihood=True)
        bpca_imputer1 = PCAImputer('bpca')
        data_bpca_imputed1, missing_columns = bpca_imputer1.fit_transform(data_missing1, verbose=True, trace_mse=True,
                                                                    cdata=df[[column]].values, n_iteration=300)
       # print(data_bpca_imputed1)


filename = "dataset1.csv"
csv(filename)
