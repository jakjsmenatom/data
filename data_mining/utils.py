from typing import Iterable, NamedTuple

import numpy as np
import pandas as pd


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

    def __init__(self) -> None:
        self.samples = []
        self.year_first = None
        self.value_first = None

    def read_csv(self, filename: str) -> None:
        df = pd.read_csv(filename)
        self.samples = [Sample(row.year, row.value) for _, row in df.iterrows()]
        self.year_first = self.samples[0].year
        self.value_first = self.samples[0].value

    def normalize(self) -> None:
        self.samples = [
            Sample(
                year=sample.year - self.year_first, value=sample.value / self.value_first,
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
