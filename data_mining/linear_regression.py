#!.venv/bin/python

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression

NAME = __file__.split('/')[-1].split('.')[-2]
PREDICTED_VALUES = 10


def df_series_to_np_array(series: pd.core.series.Series) -> np.ndarray:
    np_array = np.array(list(series))  # convert series to the numpy array
    return np_array[::, None]  # convert row vector to column vector


if __name__ == '__main__':
    # Load the dataset to the Data Frame
    df = pd.read_csv('jjnt_wb_hdp_swe.csv')

    # Store first values
    DF_YEAR_MIN = df['year'][0]
    DF_VALUE_MIN = df['value'][0]

    # Normalization
    df['year'] -= DF_YEAR_MIN
    df['value'] /= DF_VALUE_MIN

    X = df_series_to_np_array(df['year'])
    Y = df_series_to_np_array(df['value'])

    # Apply linear regression
    reg = LinearRegression().fit(X, Y)  # start regression (X and y are both column vectors)

    # Get fitted line
    slope = reg.coef_[0][0]
    intercept = reg.intercept_[0]
    fittedline = slope * X + intercept

    # Get predictions
    preds = {'year': [], 'value': []}
    for year in range(61, 61 + PREDICTED_VALUES):
        value = reg.predict(np.array([year])[::, None])[0][0]
        preds['year'].append(year)
        preds['value'].append(value)

    # Get plot
    _, ax = plt.subplots()

    chart_1 = ax.scatter(x=list(df.year), y=list(df.value), color='blue', label='Known data')
    chart_2 = ax.scatter(preds['year'], preds['value'], color='green', label='Predicted data')
    chart_3 = ax.plot(X, fittedline, color='red', label='Reggression line', linewidth=2)

    ax.set_xlabel('Rok')
    ax.set_ylabel('Hodnota')
    ax.legend()

    plt.savefig('{}.pdf'.format(NAME))
