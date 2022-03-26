#!.venv/bin/python

from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

from utils import Data, Sample, to_col_array  # noqa: WPS347

NAME = __file__.split('/')[-1].split('.')[-2]
PREDICTED_VALUES = 10
MAX_DEGREE = 3


def execute(degree: int) -> None:
    data = Data()
    data.read_csv(filename='jjnt_wb_hdp_swe.csv')
    data.normalize()

    reg = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    reg.fit(data.get_years_array(), data.get_values_array())

    # Get MSE
    y_pred = []
    for year in range(0, data.get_years_list()[-1] + 1):
        value = reg.predict(to_col_array([year]))[0][0]
        y_pred.append([year, value])
    y_true = [[sample.year, sample.value] for sample in data.samples]
    mse = mean_absolute_error(y_true, y_pred)
    print('Degree = {}'.format(degree))
    print('MSE = {}'.format(mse))

    # Get predictions
    data_preds = Data()
    for year in range(61, 61 + PREDICTED_VALUES):
        data_preds.samples.append(Sample(
            year=year,
            value=reg.predict(to_col_array([year]))[0][0],
        ))

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
        data.get_years_array(),
        reg.predict(data.get_years_array()),
        color='red',
        label='Reggression curve (degree {})'.format(degree),
        linewidth=2,
    )

    ax.set_xlabel('Rok')
    ax.set_ylabel('Hodnota')
    ax.legend()

    fig.tight_layout()
    plt.savefig('{}_{}.pdf'.format(NAME, degree))


if __name__ == '__main__':
    for degree in range(1, MAX_DEGREE + 1):
        execute(degree)
