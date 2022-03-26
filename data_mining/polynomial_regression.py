#!.venv/bin/python

from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

from utils import Data, Sample, to_col_array  # noqa: WPS347

NAME = __file__.split('/')[-1].split('.')[-2]
NUM_OF_PRED = 10
MAX_DEGREE = 3
FILENAMES = [
    'wb__celkova_populace__cze',
    'wb__hdp_na_obyvatele__swe',
    'imf__statni_dluh_centralni_vlady_procento_hdp__usa',
]


def execute(degree: int, filename: str) -> None:
    data = Data()
    data.read_csv('data/{}.csv'.format(filename))
    data.normalize()

    # Create regression model and fit it to data
    reg = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    reg.fit(data.get_years_array(), data.get_values_array())

    # Get MSE
    mse = data.get_mse(reg)
    print('Degree = {}'.format(degree))
    print('MSE = {}'.format(mse))

    # Get predictions
    data_preds = Data(year_first=data.year_first, value_first=data.value_first)
    for year in range(61, 61 + NUM_OF_PRED):
        data_preds.samples.append(Sample(
            year=year,
            value=reg.predict(to_col_array([year]))[0][0],
        ))

    plot_y = reg.predict(data.get_years_array()) * data.value_first

    # Denormalize data for draw charts
    data.denormalize()
    data_preds.denormalize()

    fig, ax = plt.subplots()

    ax.plot(
        data.get_years_array(),
        plot_y,
        color='red',
        label='Reggression curve (degree {})'.format(degree),
        linewidth=2,
    )

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

    ax.set_xlabel('Rok')
    ax.set_ylabel('Hodnota')
    ax.legend()

    fig.tight_layout()
    plt.savefig('img/{}_{}_{}.png'.format(filename, NAME, degree))


if __name__ == '__main__':
    for filename in FILENAMES:
        for degree in range(1, MAX_DEGREE + 1):
            execute(degree, filename)
