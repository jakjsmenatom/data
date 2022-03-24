import numpy as np
import pandas as pd


def get_data(filename: str) -> tuple[list, list]:
    # Load the dataset to the Data Frame
    df = pd.read_csv(filename)

    # Get first values
    df_year_min = df['year'][0]
    df_value_min = df['value'][0]

    # Normalize
    df['year'] -= df_year_min
    df['value'] /= df_value_min

    # Convert pandas Series to the numpy Array
    array_years = np.array(list(df['year']))
    array_values = np.array(list(df['value']))

    # Convert row vector to column vector
    array_years = array_years[::, None]
    array_values = array_values[::, None]

    return array_years, array_values
