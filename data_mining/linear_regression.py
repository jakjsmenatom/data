#!.venv/bin/python

from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

from utils import Data, Sample, to_col_array  # noqa: WPS347

NAME = __file__.split('/')[-1].split('.')[-2]
PREDICTED_VALUES = 10


if __name__ == '__main__':
    data = Data()
    data.read_csv(filename='jjnt_wb_hdp_swe.csv')
    data.normalize()

    # Apply linear regression
    reg = LinearRegression()
    reg.fit(data.get_years_array(), data.get_values_array())

    # Get fitted line
    slope = reg.coef_[0][0]
    intercept = reg.intercept_[0]
    fittedline = slope * data.get_years_array() + intercept

    # Get predictions
    data_preds = Data()
    for year in range(61, 61 + PREDICTED_VALUES):
        data_preds.samples.append(Sample(
            year=year,
            value=reg.predict(to_col_array([year]))[0][0],
        ))

    # Get MSE
    y_pred = []
    for year in range(0, data.get_years_list()[-1] + 1):
        value = reg.predict(to_col_array([year]))[0][0]
        y_pred.append([year, value])
    y_true = [[sample.year, sample.value] for sample in data.samples]
    mse = mean_absolute_error(y_true, y_pred)
    print('MSE = {}'.format(mse))

    # Get plot
    fig, ax = plt.subplots()

    ax.scatter(
        x=data.get_years_list(),
        y=data.get_values_list(),
        color='blue',
        label='Known data',
    )

    ax.scatter(
        x=data_preds.get_years_list(),
        y=data_preds.get_values_list(),
        color='green',
        label='Predicted data',
    )

    ax.plot(
        data.get_years_list(),
        fittedline,
        color='red',
        label='Reggression line',
        linewidth=2,
    )

    ax.set_xlabel('Rok')
    ax.set_ylabel('Hodnota')
    ax.legend()

    fig.tight_layout()
    plt.savefig('{}.pdf'.format(NAME))
