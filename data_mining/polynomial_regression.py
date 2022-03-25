#!.venv/bin/python

from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

from utils import Data, Sample, to_col_array  # noqa: WPS347

NAME = __file__.split('/')[-1].split('.')[-2]
PREDICTED_VALUES = 10
DEGREE = 2

if __name__ == '__main__':
    data = Data()
    data.read_csv(filename='jjnt_wb_hdp_swe.csv')
    data.normalize()

    reg = make_pipeline(PolynomialFeatures(DEGREE), LinearRegression())
    reg.fit(data.get_years_array(), data.get_values_array())

    # Get predictions
    data_preds = Data()
    for year in range(61, 61 + PREDICTED_VALUES):
        data_preds.samples.append(Sample(
            year=year,
            value=reg.predict(to_col_array([year]))[0][0],
        ))

    # Get predictions
    # preds_years = np.linspace(61, 61 + PREDICTED_VALUES, 10).reshape(-1, 1)
    # preds_values = reg.predict(data.get_years_array())

    # print(preds_years)
    # print(preds_values)

    # preds = {'year': [], 'value': []}
    # for year in range(61, 61 + PREDICTED_VALUES):
    #     value = reg.predict(year)
    #     preds['year'].append(year)
    #     preds['value'].append(value)

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
        y=data_preds.get_years_list(),
        color='green',
        label='Predicted data',
    )

    # ax.plot(years, fittedline, color='red', label='Reggression line', linewidth=2)

    ax.set_xlabel('Rok')
    ax.set_ylabel('Hodnota')
    ax.legend()

    fig.tight_layout()
    plt.savefig('{}.pdf'.format(NAME))
