import numpy as np
import pandas as pd

from scipy.interpolate import interp1d
from statsmodels.imputation import mice
from scipy.interpolate import interp1d

def na_interpolation(x, option = "linear", maxgap = np.inf, *args):
    data = x
    if len(data.shape) > 1 and data.shape[1] > 1:
        for i in range(data.shape[1]):
            if not np.any(np.isnan(data[:, i])):
                continue
            try:
                data[:, i] = na_interpolation(data[:, i], option, maxgap)
            except Exception as e:
                warning_msg = f"na_interpolation: No imputation performed for column {i} of the input dataset. Reason: {e}"
                print(warning_msg)
        return data
    else:
        missindx = np.isnan(data)
        if not np.any(missindx):
            return x
        if isinstance(data, pd.DataFrame):
            data = data.iloc[:, 0].values
        if np.sum(~missindx) < 2:
            raise ValueError("At least 2 non-NA data points required in the time series to apply na_interpolation.")
        if len(data.shape) > 1 and not data.shape[1] == 1:
            raise ValueError("Wrong input type for parameter x.")
        if len(data.shape) > 1:
            data = data[:, 0]
        if not np.issubdtype(data.dtype, np.number):
            raise ValueError("Input x is not numeric.")
        n = len(data)
        allindx = np.arange(1, n+1)
        indx = allindx[~missindx]
        data_vec = data.flatten()
        if option == "linear":
            f = interp1d(indx, data_vec[indx-1], kind="linear", fill_value="extrapolate")
        elif option == "spline":
            f = interp1d(indx, data_vec[indx-1], kind="cubic", fill_value="extrapolate")
        else:
            raise ValueError("Invalid option for parameter option.")
        gap = np.diff(np.where(missindx)[0])
        gap = np.insert(gap, 0, indx[0]-1)
        gap = np.append(gap, n-indx[-1])
        if np.max(gap) > maxgap:
            missindx[np.where(missindx)[0][np.argmax(gap)]] = False
            return na_interpolation(data, option, maxgap)
        data_vec[missindx] = f(np.where(missindx)[0]+1)
        data_vec.reshape(-1, 1)

        if option == "linear":
            if args.rule:
                interp = interp1d(indx, data_vec, kind=args.rule)(np.arange(n))
            else:
                interp = interp1d(indx, data_vec)(np.arange(n))
        elif option == "spline":
            interp = interp1d(indx, data_vec, kind="cubic")(np.arange(n))
        elif option == "stine":
            imp = mice.MICEData(np.column_stack((indx, data_vec)))
            imp.update_all()
            interp = imp.data[:, 1]
            if np.any(np.isnan(interp)):
                interp = np.nan_to_num(interp, nan=np.nan, copy=False)
        else:
            raise ValueError("Wrong parameter 'option' given. Value must be either 'linear', 'spline' or 'stine'.")
        data[missindx] = interp[missindx]
        if maxgap is not None and maxgap >= 0:
            rlencoding = np.diff(np.concatenate(([False], missindx, [False]))).nonzero()
            rlens = rlencoding[0][1:] - rlencoding[0][:-1]
            rstarts = rlencoding[0][:-1][np.cumsum(rlens <= maxgap) - 1]
            rends = rlencoding[0][1:][np.cumsum(rlens <= maxgap) - 1]
            for start, end in zip(rstarts, rends):
                data[start:end] = np.nan
        if data.ndim > 1:
            data[:, 0] = interp
            return data
        return data