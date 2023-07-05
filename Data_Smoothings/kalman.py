import itertools

import forecast as forecast
import numpy as np
from numpy import isnan
from statsmodels import stats
from statsmodels.tsa.statespace.kalman_filter import KalmanFilter
from statsmodels.tsa.statespace.structural import UnobservedComponents
import pandas as pd

from interpolate import na_interpolation


def na_kalman(x, model="StructTS", smooth=True, nit=-1, maxgap=np.inf, **kwargs):
    # Variable 'data' is used for all transformations to the time series
    # 'x' needs to stay unchanged to be able to return the same ts class in the end
    data = x.copy()

    # Mulivariate Input
    # The next 20 lines are just for checking and handling multivariate input.
    # ----------------------------------------------------------

    # Check if the input is multivariate
    if data.ndim > 1 and data.shape[1] > 1:
        # Go through columns and impute them by calling this function with univariate input
        for i in range(data.shape[1]):
            if not np.any(np.isnan(data[:, i])):
                continue
            # if imputing a column does not work - mostly because it is not numeric - the column is left unchanged
            try:
                data[:, i] = na_kalman(data[:, i], model, smooth, nit, maxgap, **kwargs)
            except Exception as e:
                print(f"na_kalman: No imputation performed for column {i} of the input dataset. Reason: {e}")
        return data

    # ----------------------------------------------------------
    # Univariate Input
    # All relveant imputation / pre- postprocessing  code is within this part
    # ----------------------------------------------------------
    else:
        missindx = np.isnan(data)

        ##
        ## 1. Input Check and Transformation
        ##

        # 1.1 Check if NAs are present
        if not np.any(np.isnan(data)):
            return x

        # 1.2 special handling data types
        if 'tbl' in str(type(data)):
            data = np.array(data[0])

        # 1.3 Check for algorithm specific minimum amount of non-NA values
        if np.count_nonzero(~np.isnan(data)) < 3:
            raise ValueError("At least 3 non-NA data points required in the time series to apply na_kalman.")

        # 1.4 Checks and corrections for wrong data dimension

        # Check if input dimensionality is not as expected
        if data.ndim != 1 and data.shape[1] != 1:
            raise ValueError("Wrong input type for parameter x.")

        # Altering multivariate objects with 1 column (which are essentially
        # univariate) to be dim = NULL
        if data.ndim != 1:
            data = data.iloc[:, 0]

        # 1.5 Check if input is numeric
        if not np.issubdtype(data.dtype, np.number):
            raise ValueError("Input x is not numeric.")

        # 1.6 Check if type of parameter smooth is correct
        if not isinstance(smooth, bool):
            raise ValueError("Parameter smooth must be of type logical ( TRUE / FALSE).")

        # 1.7 Transformation to numeric as 'int' can't be given to KalmanRun
        data.iloc[0:len(data)] = pd.to_numeric(data)

        # 1.8 Check for and mitigate all constant values in combination with StructTS
        # See https://github.com/SteffenMoritz/imputeTS/issues/26

        if isinstance(model, str) and model == "StructTS" and len(np.unique(data.values)) == 2:
            return na_interpolation(x)

        ##
        ## End Input Check and Transformation
        ##

        ##
        ## 2. Imputation Code
        ##

        # 2.1 Selection of state space model

        # State space representation of a arima model
        if model[1] == "auto.arima":
            mod = forecast.auto_arima(data, ...).model

        elif model[1] == "StructTS":
            # Fallback, in StructTS first value is not allowed to be NA, thus take first non-NA
            if np.isnan(data[1]):
                data[1] = data[np.argmin(np.isnan(data))]
            mod = stats.StructTS(data, ...).model0
        # User supplied model e.g. created with arima() or other state space models from other packages
        else:
            mod = model
            if len(mod) < 7:
                raise ValueError(
                    "Parameter model has either to be \"StructTS\"/\"auto.arima\" or a user supplied model in form of a list with at least components T, Z, h , V, a, P, Pn specified.")
          #  if mod.find('Z') == -1:
           #     raise ValueError(
            #        "Something is wrong with the user supplied model. Either choose \"auto.arima\" or \"StructTS\" or supply a state space model with at least components T, Z, h , V, a, P, Pn as specified under Details on help page for KalmanLike.")

        # 2.2 Selection if KalmanSmooth or KalmanRun
        if smooth:
            from statsmodels.tsa.statespace.kalman_filter import KalmanFilter
            from statsmodels.tsa.statespace import tools

            kal = KalmanFilter(mod, data, nit)
            kalman_smoothed = kal.smooth()
            erg = kalman_smoothed.states
        else:
            from statsmodels.tsa.statespace.kalman_filter import KalmanFilter
            from statsmodels.tsa.statespace import tools

            kal = KalmanFilter(mod, data, nit)
            kalman_run = kal.filter()
            erg = kalman_run.states

        # Check if everything is right with the model
        if erg.shape[1] != len(mod.Z):
            raise ValueError("Error with number of components $Z.")

        # 2.3 Getting Results

        # Out of all components in $states or$smooth only the ones
        # which have 1 or -1 in $Z are in the model
        # Therefore matrix multiplication is done
        karima = np.dot(erg[missindx, :], mod.Z)

        # Add imputations to the initial dataset
        data[missindx] = karima

        ##
        ## End Imputation Code
        ##

        ##
        ## 3. Post Processing
        ##

        # 3.1 Check for Maxgap option

        # If maxgap = Inf then do nothing and when maxgap is lower than 0
        if np.isfinite(maxgap) and maxgap >= 0:
            # Get logical vector of the time series via is.na() and then get the
            # run-length encoding of it. The run-length encoding describes how long
            # the runs of FALSE and TRUE are
            rlencoding = np.array([(k, np.isnan(g).all()) for k, g in itertools.groupby(x)])

            # Runs smaller than maxgap (which shall still be imputed) are set FALSE
            rlencoding[rlencoding[:, 0] <= maxgap, 1] = False

            # The original vector is being reconstructed by reverse.rls, only now the
            # longer runs are replaced now in the logical vector derived from is.na()
            # in the beginning all former NAs that are > maxgap are also FALSE
            en = np.concatenate([np.full(k, v) for k, v in rlencoding])

            # Set all positions in the imputed series with gaps > maxgap to NA
            # (info from en vector)
            data[en] = np.nan

            ##
            ## End Post Processing
            ##

            ##
            ## 4. Final Output Formatting
            ##

            # Give back the object originally supplied to the function
            # (necessary for multivariate input with only 1 column)
        if x.ndim > 1:
            x[:, 0] = data
            return x

        ##
        ## End Final Output Formatting
        ##
        return data
