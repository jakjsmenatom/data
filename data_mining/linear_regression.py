#!.venv/bin/python

import numpy as np
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression

from utils import get_data

NAME = __file__.split('/')[-1].split('.')[-2]
PREDICTED_VALUES = 10

if __name__ == '__main__':
    years, values = get_data(filename='jjnt_wb_hdp_swe.csv')

    # Apply linear regression
    reg = LinearRegression().fit(years, values)  # start regression (X and y are both column vectors)

    # Get fitted line
    slope = reg.coef_[0][0]
    intercept = reg.intercept_[0]
    fittedline = slope * years + intercept

    # Get predictions
    preds = {'year': [], 'value': []}
    for year in range(61, 61 + PREDICTED_VALUES):
        value = reg.predict(np.array([year])[::, None])[0][0]
        preds['year'].append(year)
        preds['value'].append(value)

    # Get plot
    fig, ax = plt.subplots()

    ax.scatter(x=list(years), y=list(values), color='blue', label='Known data')
    ax.scatter(preds['year'], preds['value'], color='green', label='Predicted data')
    ax.plot(years, fittedline, color='red', label='Reggression line', linewidth=2)

    ax.set_xlabel('Rok')
    ax.set_ylabel('Hodnota')
    ax.legend()

    fig.tight_layout()
    plt.savefig('{}.pdf'.format(NAME))
