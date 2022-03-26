from typing import Iterable, NamedTuple

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error


def to_col_array(data: Iterable) -> np.array:
    """
    From array([1, 2, 3]) to array([[1], [2], [3]])
    """
    a = np.array(data)
    return a[::, None]


class Sample(NamedTuple):
    year: int
    value: float


class Data:

    def __init__(self, year_first: int = None, value_first: float = None) -> None:
        self.samples = []
        self.year_first = year_first
        self.value_first = value_first

    def read_csv(self, filename: str) -> None:
        df = pd.read_csv(filename)
        self.samples = [Sample(int(row.year), float(row.value)) for _, row in df.iterrows()]
        self.year_first = self.samples[0].year
        self.value_first = self.samples[0].value

    def normalize(self) -> None:
        self.samples = [
            Sample(
                year=sample.year - self.year_first, value=sample.value / self.value_first,
            ) for sample in self.samples
        ]

    def denormalize(self) -> None:
        self.samples = [
            Sample(
                year=sample.year + self.year_first, value=sample.value * self.value_first,
            ) for sample in self.samples
        ]

    def get_years_list(self) -> list[int]:
        return [sample.year for sample in self.samples]

    def get_values_list(self) -> list[float]:
        return [sample.value for sample in self.samples]

    def get_years_array(self) -> np.array:
        return to_col_array(self.get_years_list())

    def get_values_array(self) -> np.array:
        return to_col_array(self.get_values_list())

    def get_mse(self, model):
        y_pred = []

        for year in range(0, self.get_years_list()[-1] + 1):
            value = model.predict(to_col_array([year]))[0][0]
            y_pred.append([year, value])

        y_true = [[sample.year, sample.value] for sample in self.samples]
        return mean_absolute_error(y_true, y_pred)
